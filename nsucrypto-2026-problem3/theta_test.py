"""
Shows that no Lovasz-theta / weighted-Hoffman (Delsarte) clique bound can be tight for this problem.

Crossing graph: vertices = chords of PG(1,q), adjacent iff they cross. An all-crossing matching is a
clique of size m = (q+1)/2. A theta-type certificate for "max clique = m" is a PGL(2,q)-invariant
matrix Z = J + sum_c z_c A_c over the NON-crossing orbital classes c (chords sharing a point, and
square cross-ratio classes) with lambda_max(Z) = m. Tightness forces Z 1_S = m 1_S for the canonical
clique S, i.e. for every chord outside S the weighted count of non-crossing S-chords is zero.
This script shows that linear system has only the zero solution, so no such certificate exists.
"""
import sys
import numpy as np

for q in map(int, sys.argv[1:] or ["43", "47", "59", "67"]):
    INF = q
    sq = {x * x % q for x in range(1, q)}
    chi = lambda a: 0 if a % q == 0 else (1 if a % q in sq else -1)
    inv = lambda x: pow(x, q - 2, q)
    pc = lambda x: (1, 0) if x == INF else (x, 1)
    det = lambda A, B: (A[0] * B[1] - A[1] * B[0]) % q
    cr = lambda a, b, c, d: det(pc(a), pc(c)) * det(pc(b), pc(d)) * inv(det(pc(a), pc(d)) * det(pc(b), pc(c))) % q
    n = next(x for x in range(2, q) if chi(x) == -1)
    S = [(0, INF)] + [(a, n * inv(a) % q) for a in range(1, q) if a < n * inv(a) % q]
    classes = sorted({min(l, inv(l)) for l in range(2, q) if chi(l) == 1})
    cidx = {c: i + 1 for i, c in enumerate(classes)}
    rows = []
    for c in range(q + 1):
        for d in range(c + 1, q + 1):
            if (c, d) in S:
                continue
            v = np.zeros(len(classes) + 1)
            for (a, b) in S:
                if len({a, b, c, d}) < 4:
                    v[0] += 1
                    continue
                l = cr(a, b, c, d)
                if chi(l) == 1:
                    v[cidx[min(l, inv(l))]] += 1
            rows.append(v)
    A = np.array(rows)
    s = np.linalg.svd(A, compute_uv=False)
    rank = int(np.sum(s > 1e-8))
    print(f"q={q}: unknowns={A.shape[1]} rank={rank} -> nullity={A.shape[1]-rank} (0 means: no tight certificate)")
