# Review of the manuscript *Complete exterior sets of conics for q ≡ 3 (mod 4): an exact matching reformulation, a stability lemma, and a computer verification for 31 < q ≤ 431* (21 pp.) and its code bundle

Two independent reviews were done: a first-hand read of the manuscript, logs and code, and a separate line-by-line referee pass by a second model (Opus) that re-ran every program on its own field tables. The findings agree.

## Verdict

**Mathematically sound; computation reproduced and independently confirmed. Minor revision.** No fatal or significant error was found in Sections 2–8. All 38 values 31 < q ≤ 431 are confirmed by an unrelated program (`verify_bsw.c`, different field construction, different symmetry breaking, brute-force re-check of every solution), which also extends the result to all 61 prime powers q ≡ 3 (mod 4) with 31 < q < 700. The counterexample counts of Table 2 (5, 12, 54, 121, 104, 31) match our raw counts exactly.

## Issues to fix (none affects the results)

| # | where | severity | issue / fix |
|---|---|---|---|
| 1 | p. 9, text after Prop. 6.1 | minor, factual slip | "Part (d) is used only by `--reduce` … for the primes q = 419, 431, where a^p = a." For primes the Frobenius is trivial; the reduction that does the work for 419, 431 is (c), a ~ 1/a. Table 1's caption and Thm 6.3 already say (c); make the text agree. The reduction itself is valid: (q+1)/4 classes (a = −1 is self-paired), giving the 105 and 108 branches of Table 1. |
| 2 | Prop. 8.2 and following text | minor, gap in exposition | "the identity yields no contradiction" omits the parity step. State that the LHS is even and that for q ≡ 3 (mod 4) the RHS is (3q−25)/2 + c₃(X) with (3q−25)/2 even, so a contradiction would need c₃ odd; the brute-force check (c₃ ∈ {0,2,4}, and ∈ {2,4} when (a−c)(b−d) is a non-square) is confirmed. |
| 3 | Remark 4.6 | minor | The regular group T of maps t ↦ (at+nb)/(bt+a) is used before it is proved (Lemma 5.2, Step 1). Add a forward reference. |
| 4 | Prop. 8.1(b) | minor | Carlitz's theorem is applied for general q = p^e; cite a version valid for all odd q (McConnel 1963; Bruen–Levinger 1973; or [10, Result 1.1]) and state the normalised form F(x) = a + b·x^{p^k}. The deduction (e \| 2k with e odd ⇒ e \| k; χ(n/b) = −1) is correct. |
| 5 | Remark 5.4 / §8 | under-claim | For q = 19 the counterexample has k_max = 6 against the bound (q−3+2√q)/4 = 6.18. Corollary 5.3 is essentially tight against a genuine counterexample, not just "numerically nearly sharp". Worth saying. |
| 6 | Remark 7.2 | cosmetic | "q+1 ≤ 2(\|H\|−1)" is valid but crude (a cyclic subgroup fixes one pair). Fine as is. |
| 7 | Ref. [2] | bibliography | Van de Voorde: add volume/year for Discrete Mathematics. |
| 8 | bundle, `results/gen_tables_report.txt` | bundle hygiene | The report ends with `final problems: ['naive comparison incomplete: [131]']`. The paper correctly claims the naive check only up to 127; either run q = 131 or remove the expectation from the script. |
| 9 | §6.3, "15–20 CPU-minutes" | cosmetic | q = 383, implementation 1, took 1240 s ≈ 20.7 min. |

## Novelty and literature

* The literature claims check out as far as they can be checked without the BSW paper itself: the BSW abstract does state that for q ≡ 3 (mod 4) other examples exist "at least for q = 7, 11, …, 31" ([Springer](https://link.springer.com/article/10.1007/BF01204717), [TU/e portal](https://research.tue.nl/en/publications/characterization-of-complete-exterior-sets-of-conics/)); Van de Voorde ([arXiv:1201.0484](https://arxiv.org/abs/1201.0484)) confirms the BSW conjecture for q > 31 and that q = 7, 11 are the only cases known to give sets without tangents. Brouwer's search up to q = 131, the "no idea how to prove" remark and the classification counts are cited to [1, §3] and could not be verified from secondary sources.
* **Theorem A** is a clean restatement of the involution ⇔ exterior-set equivalence that BSW already use (and that the NSUCRYPTO statement quotes). Present it as such; the matching language (M) is a convenient repackaging, not a new result. Proposition 8.1 (the "twisted Carlitz" form, D ≡ 1 ⇔ canonical) is the same reduction we make in our Theorem A, (1)⇔(3).
* **Theorem B** (Weil-bound stability) appears to be new but modest. It should be compared with Van de Voorde's one-point extension result (for q ≡ 3 mod 4 a point extending the exterior points of a passant must lie on that passant), which is the k = (q+1)/2 case of the same phenomenon.
* "Two separately written implementations" is honestly qualified in §6.3 (same algorithm, same branching rule, same tables); the abstract should say "two implementations of the same algorithm". Genuine independence is provided by `ref_search.py` (q ≤ 127) and now by our `verify_bsw.c` (all q < 700).
* Missing from the manuscript, available in our SOLUTION.md and worth adding: the triangle criterion (canonical ⇔ no negative triangle, with the closed form χ((1−λ₁)(1−λ₂)(1−λ₃))), the spreading theorem (a counterexample shares ≤ 3.5√q + 6 chords with any pencil), and the two negative results (no theta/Delsarte clique certificate can be tight; the crossing involutions of the generic counterexamples generate all of PSL(2,q)).

## What was verified to be correct

Lemmas 2.1–2.5 (signs, ∞ conventions, cross-ratio factorisation); Lemma 4.2 (resultant identity, checked symbolically on 1000 random cases and for x' = ∞); Lemma 4.3(a)–(e) (numerically for all interior points, q ≤ 43); Theorem 4.4, Prop. 4.5; Remark 3.2 (Hoffman bound = q, clique–coclique bound = (q+1)/2); Remark 4.6 ((q+1)/4 harmonic pairs per pencil, q = 7…43); Lemma 5.2 in every step (group T, reduction to f = {y,∞}, R(e_x,f) = (x−y)(n−xy)/x, three distinct roots, the factor 2, the final inequality; max N(f) = 13, 17, 30 for q = 43, 59, 103 as stated); Corollary 5.3; Prop. 6.1(a)–(d); Lemma 6.2 (enumeration complete; no pruning beyond "a point with no admissible partner"); Section 7 (every representative recomputed, including q = 27: good, with |H|, element-order profile, k_max and harmonic count matching Table 2; orbit sizes sum to "exc."; Example 7.1); Section 8 identities (Σ C(k_I,2), Σ k_I, Prop. 8.1(a), Gram reformulation, Prop. 8.2 with α = 1, β = −1/2, γ = 1/2; identity holds on all 16 524 chord pairs of the q ≤ 31 counterexamples, 9 388 violating D = 1).

Computation: `goodmatch.c` and `goodmatch2.c` compile with `-Wall`; run on q = 3, 7, 11, 19, 23, 27, 31, 43, 47, 59, 83, 103, 127, 131, 211, 243 with freshly built tables certified by `verify_tables.c`; solution and node counts equal Table 1 / Table 2 / the logs exactly. The resumed logs for 419 and 431 contain exactly the 105 and 108 representatives, each once, with node totals equal to the other implementation's. Listed sources are byte-identical to `paper/code/` and all SHA-256 checksums match Appendix A.3. ∞ handling, bitset masking, and the `--reduce` orbit closure are correct.

Independent verifier agreement: `verify_bsw -all` gives 5, 12, 54, 121, 104, 31 for q ≤ 31 and (q−1)/2 for 43–131, 211, 243, 209 for q = 419 and 215 for q = 431 (all canonical, 0 verify failures); symmetry-broken mode gives exactly one solution, the pencil, for all 38 values.
