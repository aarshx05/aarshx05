/*
 * verify_bsw.c -- exhaustive computer check of the BSW conjecture
 * (NSUCRYPTO 2026, round 2, Problem 3) for one odd prime power q.
 *
 * Model (see SOLUTION.md, Section 1):
 *   The points of PG(1,q) are 0..q-1 (field elements) and q (= infinity).
 *   Two disjoint pairs {a,b},{c,d} "cross" iff chi((a-c)(a-d)(b-c)(b-d)) = -1,
 *   where factors involving infinity are omitted. This is chi of the cross
 *   ratio (a,b;c,d).
 *   A map psi as in Conjecture 1 is the same thing as a perfect matching M of
 *   PG(1,q) that contains {0,inf} and in which every two pairs cross.
 *   psi is "canonical" iff psi(x) = n/x, i.e. M is the orbit set of an elliptic
 *   involution of PGL(2,q).
 *
 * Normalisation (Lemma 6.1 in SOLUTION.md):
 *   Every pair of crossing chords is PGL(2,q)-equivalent to ({0,inf},{1,n})
 *   with n a non-square. The class of the cross ratio up to l ~ 1/l is a
 *   complete invariant. For a matching M let n*(M) be the smallest class
 *   representative min(l,1/l) (field elements ordered by their integer code)
 *   over all pairs of chords of M. Every M is equivalent to an M' that contains
 *   {0,inf} and {1,n*} and in which every pair of chords has class >= n*.
 *   So it suffices to list, for every non-square n with n <= 1/n, all
 *   matchings that contain {0,inf} and {1,n} and whose pairwise classes are all
 *   >= n. ("-all" mode turns this symmetry breaking off and loops over every
 *   non-square n.)
 *
 * Search: plain backtracking over perfect matchings with forward checking.
 *   cand[w] = set of still-uncovered z such that {w,z} crosses every chosen
 *   pair. For the first D chosen pairs (D = 3 by default, "-eager=D") cand[w]
 *   is also filtered by the class condition. For later pairs the class
 *   condition is checked when a pair is chosen (class_ok). We branch on the
 *   uncovered point with the fewest candidates. Every filter only removes
 *   partners that are incompatible with a pair already chosen, so the search
 *   is exhaustive. D only affects speed, not the result.
 *
 * Sign-class balance pruning (see the comment at the declaration of hash_frames)
 * cuts the search from about q^8 to about q^2.5 nodes; "-nobalance" turns it off.
 *
 * Every complete matching found is re-checked against the definition by brute
 * force before it is counted.
 *
 * Build: gcc -O3 -march=native -o verify_bsw verify_bsw.c
 * Usage: ./verify_bsw q [-all] [-print] [-eager=D]
 * Output: one summary line, for example
 *   q=43 ... canonical=1 noncanonical=0 RESULT: conjecture holds for q=43
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int q, p, k, N, W;
static int *lg, *ex;
static signed char *V;  /* V[x*N+y] = chi(x-y), with V = 1 whenever x or y is infinity */
static uint64_t *R;     /* R[z] = bitset {w : V[w][z] = +1} */
static int *crep;       /* crep[l] = min(l, 1/l) as integer codes */

/* ---------------- finite field GF(p^k), elements coded base p ---------------- */
static int fadd_sub(int a, int b, int sgn) {
    int r = 0, m = 1;
    for (int i = 0; i < k; i++) {
        int da = a % p, db = b % p;
        a /= p; b /= p;
        r += (((da + sgn * db) % p + p) % p) * m;
        m *= p;
    }
    return r;
}
static int fsub(int a, int b) { return fadd_sub(a, b, -1); }
static int fmul(int a, int b) { if (!a || !b) return 0; return ex[(lg[a] + lg[b]) % (q - 1)]; }
static int finv(int a) { return ex[(q - 1 - lg[a]) % (q - 1)]; }
static int chi(int a) { if (!a) return 0; return (lg[a] % 2 == 0) ? 1 : -1; }

/* multiply element (base-p digits) by the generator x modulo the monic poly with low coeffs c[] */
static int mulx(int cur, const int *c, int *dig) {
    for (int j = 0; j <= k; j++) dig[j] = 0;
    int tmp = cur;
    for (int j = 0; j < k; j++) { dig[j + 1] = tmp % p; tmp /= p; }
    int top = dig[k];
    for (int j = 0; j < k; j++) dig[j] = ((dig[j] - top * c[j]) % p + p) % p;
    int nv = 0, m = 1;
    for (int j = 0; j < k; j++) { nv += dig[j] * m; m *= p; }
    return nv;
}
static int build_field(void) {
    int t = q; p = 0;
    for (int d = 2; d <= t; d++) if (t % d == 0) { p = d; break; }
    if (p == 0 || p == 2) return 0;
    k = 0; t = q; while (t % p == 0) { t /= p; k++; }
    if (t != 1) return 0;
    lg = malloc(sizeof(int) * q); ex = malloc(sizeof(int) * q);
    int *c = malloc(sizeof(int) * (k + 1)), *dig = malloc(sizeof(int) * (k + 2));
    /* search a primitive monic polynomial of degree k (for k = 1: x - g, g a primitive root) */
    for (int code = 0; code < q; code++) {
        int tt = code;
        for (int i = 0; i < k; i++) { c[i] = tt % p; tt /= p; }
        if (c[0] == 0) continue;
        int cur = 1, ord = 0;
        do { cur = mulx(cur, c, dig); ord++; } while (cur != 1 && ord <= q);
        if (ord != q - 1) continue;
        cur = 1;
        for (int i = 0; i < q - 1; i++) { ex[i] = cur; lg[cur] = i; cur = mulx(cur, c, dig); }
        free(c); free(dig);
        return 1;
    }
    return 0;
}

/* ---------------- projective helpers ---------------- */
/* det of representatives (x,1) for finite x and (1,0) for infinity */
static int pdet(int x, int y) {
    if (x == q) return 1;
    if (y == q) return fsub(0, 1);
    return fsub(x, y);
}
static int crossratio(int a, int b, int c, int d) { /* (a,b;c,d) */
    return fmul(fmul(pdet(a, c), pdet(b, d)), finv(fmul(pdet(a, d), pdet(b, c))));
}
static int crosses(int a, int b, int c, int d) {
    return V[(size_t)a * N + c] * V[(size_t)a * N + d] * V[(size_t)b * N + c] * V[(size_t)b * N + d] == -1;
}

/* ---------------- search ---------------- */
#define BIT(bs, i) ((bs)[(i) >> 6] >> ((i) & 63) & 1ULL)
#define SETB(bs, i) ((bs)[(i) >> 6] |= 1ULL << ((i) & 63))

static uint64_t **cand_frames, **cov_frames;
static int nframes;
static int *partner;
static int pa[1 << 16], pb[1 << 16], npairs;
static int curn, symbreak = 1, printsol = 0, eager_depth = 3;
static long long nsol, ncanon, nnoncanon, nodes, verify_fail;
static uint64_t lastmask;
static unsigned char *goodlog; /* goodlog[e] = 1 iff crep(g^e) >= curn (g the primitive element) */
/* Sign-class balance pruning. Every uncovered point w carries the vector of signs
   V[w][u]V[w][v] over the chosen pairs {u,v}; the partner of w must carry the opposite
   vector, so psi maps each sign class onto its complementary class and the two classes
   have equal size. We keep a 64-bit hash of the vector per point (XOR of a random word
   per pair whose sign is +1); the complementary class has hash h ^ rall, where rall is the
   XOR of all words used. Hash collisions can only merge classes, which weakens the test
   but never makes it reject a good matching, so the pruning is sound. */
static uint64_t **hash_frames, *rall_frames, *randw;
typedef struct { uint64_t key; int flag; } KF;
static KF *kf;                 /* scratch for the balance test */
static int balance = 1;
static long long nbalance_rej;
static int *la;                /* scratch: la[w] = log of [w,u]/[w,v] for the pair being added */

static void ensure_frame(int d) {
    while (nframes <= d) {
        cand_frames[nframes] = malloc(sizeof(uint64_t) * (size_t)N * W);
        cov_frames[nframes] = malloc(sizeof(uint64_t) * (size_t)W);
        hash_frames[nframes] = malloc(sizeof(uint64_t) * (size_t)N);
        if (!cand_frames[nframes] || !cov_frames[nframes] || !hash_frames[nframes]) { fprintf(stderr, "out of memory\n"); exit(2); }
        nframes++;
    }
}

/* add pair (u,v) to the state of depth d, producing depth d+1; returns 0 if some uncovered point is left without a candidate */
static int add_pair(int d, int u, int v) {
    ensure_frame(d + 1);
    uint64_t *cand = cand_frames[d], *ncand = cand_frames[d + 1];
    uint64_t *cov = cov_frames[d], *ncov = cov_frames[d + 1];
    memcpy(ncov, cov, sizeof(uint64_t) * W);
    SETB(ncov, u); SETB(ncov, v);
    {   /* sign-class hashes of the next frame */
        const uint64_t *h = hash_frames[d]; uint64_t *nh = hash_frames[d + 1], rw = randw[d];
        for (int w = 0; w < N; w++) nh[w] = (V[(size_t)w * N + u] * V[(size_t)w * N + v] > 0) ? (h[w] ^ rw) : h[w];
        rall_frames[d + 1] = rall_frames[d] ^ rw;
    }
    uint64_t bplus[W], bminus[W];
    for (int i = 0; i < W; i++) {
        uint64_t x = R[(size_t)u * W + i] ^ R[(size_t)v * W + i];  /* V[z][u] != V[z][v] */
        bminus[i] = x & ~ncov[i];
        bplus[i] = ~x & ~ncov[i];
    }
    bplus[W - 1] &= lastmask; bminus[W - 1] &= lastmask;
    for (int w = 0; w < N; w++) {
        if (BIT(ncov, w)) continue;
        int s = V[(size_t)w * N + u] * V[(size_t)w * N + v];
        const uint64_t *src = cand + (size_t)w * W, *msk = (s > 0) ? bminus : bplus;
        uint64_t *dst = ncand + (size_t)w * W, any = 0;
        for (int i = 0; i < W; i++) { dst[i] = src[i] & msk[i]; any |= dst[i]; }
        if (!any) return 0;
    }
    if (symbreak && d < eager_depth) {
        /* Eager class filter: drop z from cand[w] if the cross ratio (w,z;u,v) has class rep < curn.
           (w,z;u,v) = A_w / A_z with A_w = [w,u]/[w,v], so its log is la[w] - la[z]. */
        for (int w = 0; w < N; w++) {
            if (BIT(ncov, w)) continue;
            la[w] = (lg[pdet(w, u)] - lg[pdet(w, v)] + (q - 1)) % (q - 1);
        }
        for (int w = 0; w < N; w++) {
            if (BIT(ncov, w)) continue;
            uint64_t *dst = ncand + (size_t)w * W, any = 0;
            for (int i = 0; i < W; i++) {
                uint64_t b = dst[i];
                while (b) {
                    int j = __builtin_ctzll(b); b &= b - 1;
                    int z = i * 64 + j;
                    int e = la[w] - la[z]; if (e < 0) e += q - 1;
                    if (!goodlog[e]) dst[i] &= ~(1ULL << j);
                }
                any |= dst[i];
            }
            if (!any) return 0;
        }
    }
    partner[u] = v; partner[v] = u;
    return 1;
}

static int class_ok(int u, int v) {
    if (!symbreak) return 1;
    for (int i = 0; i < npairs; i++)
        if (crep[crossratio(u, v, pa[i], pb[i])] < curn) return 0;
    return 1;
}

static int verify_solution(void) {
    /* brute-force check of the definition: perfect matching, contains {0,inf}, all pairs cross */
    if (partner[0] != q || partner[q] != 0) return 0;
    for (int x = 0; x <= q; x++) if (partner[x] == x || partner[partner[x]] != x) return 0;
    for (int a = 0; a <= q; a++) for (int c = 0; c <= q; c++) {
        int b = partner[a], d = partner[c];
        if (a < b && c < d && a != c && !crosses(a, b, c, d)) return 0;
    }
    return 1;
}
static int is_canonical(void) {
    for (int x = 1; x < q; x++) if (partner[x] != fmul(curn, finv(x))) return 0;
    return 1;
}
static void print_solution(void) {
    printf("  solution (n=%d):", curn);
    for (int x = 0; x <= q; x++) if (x < partner[x]) {
        if (partner[x] == q) printf(" {%d,inf}", x); else printf(" {%d,%d}", x, partner[x]);
    }
    printf("\n");
}

static int cmp_kf(const void *A, const void *B) {
    const KF *a = A, *b = B;
    if (a->key != b->key) return a->key < b->key ? -1 : 1;
    return a->flag - b->flag;
}
/* returns 0 iff some sign class and its complementary class have different sizes */
static int balanced(int d) {
    const uint64_t *h = hash_frames[d], *cov = cov_frames[d]; uint64_t rall = rall_frames[d];
    int n = 0;
    for (int w = 0; w < N; w++) {
        if (BIT(cov, w)) continue;
        uint64_t a = h[w], b = a ^ rall;
        kf[n].key = a < b ? a : b; kf[n].flag = a < b ? 0 : 1; n++;
    }
    qsort(kf, n, sizeof(KF), cmp_kf);
    for (int i = 0; i < n; ) {
        int j = i, c0 = 0, c1 = 0;
        while (j < n && kf[j].key == kf[i].key) { if (kf[j].flag) c1++; else c0++; j++; }
        if (c0 != c1) return 0;
        i = j;
    }
    return 1;
}

static void search(int d) {
    nodes++;
    uint64_t *cand = cand_frames[d], *cov = cov_frames[d];
    if (balance && !balanced(d)) { nbalance_rej++; return; }
    int best = -1, bestc = 1 << 30;
    for (int w = 0; w < N; w++) {
        if (BIT(cov, w)) continue;
        int c = 0;
        for (int i = 0; i < W; i++) c += __builtin_popcountll(cand[(size_t)w * W + i]);
        if (c < bestc) { bestc = c; best = w; if (c <= 1) break; }
    }
    if (best < 0) {
        if (!verify_solution()) { verify_fail++; return; }
        nsol++;
        if (is_canonical()) ncanon++;
        else { nnoncanon++; if (printsol) print_solution(); }
        return;
    }
    if (bestc == 0) return;
    uint64_t cu[W];
    memcpy(cu, cand + (size_t)best * W, sizeof(uint64_t) * W);
    for (int i = 0; i < W; i++) {
        uint64_t b = cu[i];
        while (b) {
            int j = __builtin_ctzll(b); b &= b - 1;
            int v = i * 64 + j;
            if (!class_ok(best, v)) continue;
            if (add_pair(d, best, v)) {
                pa[npairs] = best; pb[npairs] = v; npairs++;
                search(d + 1);
                npairs--;
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s q [-all] [-print] [-eager=D] [-nobalance]\n", argv[0]); return 1; }
    q = atoi(argv[1]);
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "-all")) symbreak = 0;
        if (!strcmp(argv[i], "-print")) printsol = 1;
        if (!strncmp(argv[i], "-eager=", 7)) eager_depth = atoi(argv[i] + 7);
        if (!strcmp(argv[i], "-nobalance")) balance = 0;
    }
    if (!build_field()) { fprintf(stderr, "q must be an odd prime power\n"); return 1; }
    clock_t t0 = clock();
    N = q + 1; W = (N + 63) / 64;
    lastmask = (N % 64) ? (~0ULL >> (64 - N % 64)) : ~0ULL;
    V = malloc((size_t)N * N);
    for (int x = 0; x < N; x++) for (int y = 0; y < N; y++)
        V[(size_t)x * N + y] = (x == y) ? 0 : (x == q || y == q) ? 1 : chi(fsub(x, y));
    R = calloc((size_t)N * W, sizeof(uint64_t));
    for (int z = 0; z < N; z++) for (int w = 0; w < N; w++) if (V[(size_t)w * N + z] == 1) SETB(R + (size_t)z * W, w);
    crep = malloc(sizeof(int) * q);
    crep[0] = 0;
    for (int l = 1; l < q; l++) { int li = finv(l); crep[l] = l < li ? l : li; }
    cand_frames = calloc(N / 2 + 4, sizeof(uint64_t *));
    cov_frames = calloc(N / 2 + 4, sizeof(uint64_t *));
    hash_frames = calloc(N / 2 + 4, sizeof(uint64_t *));
    rall_frames = calloc(N / 2 + 4, sizeof(uint64_t));
    randw = malloc(sizeof(uint64_t) * (N / 2 + 4));
    { uint64_t st = 0x9E3779B97F4A7C15ULL ^ (uint64_t)q;   /* splitmix64 */
      for (int i = 0; i < N / 2 + 4; i++) { uint64_t z = (st += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; randw[i] = z ^ (z >> 31); } }
    kf = malloc(sizeof(KF) * N);
    partner = malloc(sizeof(int) * N);
    goodlog = malloc(q);
    la = malloc(sizeof(int) * N);
    ensure_frame(0);

    long long tsol = 0, tcan = 0, tnon = 0, tnodes = 0, tfail = 0;
    int nclasses = 0;
    for (int n = 1; n < q; n++) {
        if (chi(n) != -1) continue;
        if (symbreak && finv(n) < n) continue;   /* n ~ 1/n */
        nclasses++;
        curn = n;
        for (int e = 0; e < q - 1; e++) goodlog[e] = crep[ex[e]] >= curn;
        memset(cov_frames[0], 0, sizeof(uint64_t) * W);
        memset(hash_frames[0], 0, sizeof(uint64_t) * N); rall_frames[0] = 0;
        for (int w = 0; w < N; w++) {
            uint64_t *c = cand_frames[0] + (size_t)w * W;
            memset(c, 0, sizeof(uint64_t) * W);
            for (int z = 0; z < N; z++) if (z != w) SETB(c, z);
        }
        nsol = ncanon = nnoncanon = nodes = verify_fail = 0;
        npairs = 0;
        if (add_pair(0, 0, q)) {
            pa[npairs] = 0; pb[npairs] = q; npairs++;
            if (add_pair(1, 1, n)) {
                pa[npairs] = 1; pb[npairs] = n; npairs++;
                search(2);
            }
        }
        tsol += nsol; tcan += ncanon; tnon += nnoncanon; tnodes += nodes; tfail += verify_fail;
    }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("q=%d p=%d k=%d q%%4=%d mode=%s classes=%d nodes=%lld solutions=%lld canonical=%lld noncanonical=%lld verify_fail=%lld time=%.2fs ",
           q, p, k, q % 4, symbreak ? "symbreak" : "all", nclasses, tnodes, tsol, tcan, tnon, tfail, secs);
    if (tfail) printf("RESULT: INTERNAL ERROR\n");
    else if (symbreak && tcan != 1) printf("RESULT: SANITY CHECK FAILED (canonical found %lld times, expected 1)\n", tcan);
    else if (tnon == 0) printf("RESULT: conjecture holds for q=%d\n", q);
    else printf("RESULT: counterexamples exist for q=%d\n", q);
    return 0;
}
