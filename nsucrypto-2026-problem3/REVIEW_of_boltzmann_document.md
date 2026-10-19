# Review of *BSW conjecture: Boltzmann program results* (16 pp.) and `bsw_boltzmann_code.zip`

## What it claims, and what checks out

* **Computation: Conjecture 1 for all prime powers q ≡ 3 (mod 4) with 31 < q ≤ 2 251** (163 values in the log, 103 ≤ q ≤ 2 251; the smaller values are stated to come from the Python enumerator). Its search is a different algorithm from both of ours: no symmetry breaking, but a *sign-class balance* pruning (every unmatched point carries the vector of signs with respect to the chosen chords; partner classes must have equal size). The pruning is sound (the argument on p. 6 is correct, including the hash-collision remark), and it is dramatically effective: ~q^2.5 nodes instead of ~q^8. We adopted it in `verify_bsw.c` (option `-nobalance` turns it off): identical solution counts for every q tested, and q = 691 drops from 630 s to 6 s. Its log agrees with our 61 values 31 < q < 700 in every case; our own extended run (Section 5 of the report) then re-checks its range with unrelated code.
* **Theorem B (odd-product identities)** is correct and nice: for any odd number of chords of a good matching, Σ_y Π s_{p_i}(y) = 0; for three finite chords this says the genus-2 curve w² = sextic has exactly q + 1 points. The three-line proof is right. Verified numerically on the canonical matchings and the q = 31 counterexample (600 random odd products, 0 violations; all 455 / 1 330 / 3 654 genus-2 triples have q + 1 points). We added it to our report as Proposition 4.2.
* **Proposition C (parity law)** and the two-graph θ are the same facts as our Section 3 ("exotic quadruples"). **Theorem A** there is our Theorem A, in a seven-fold list of equivalent forms; (2 ⇒ 1) is the same Carlitz–McConnel step.
* **Proposition F (Dickson reduction)** is a genuine theorem and strengthens our earlier computational remark (§8.3 of SOLUTION.md) to a proof. We re-proved it as Theorem E of the report. Two points in its proof need repair:
  1. *Dihedral case.* "Every ι_p commutes with the involution of T" assumes the rotation subgroup has even order. If the rotation subgroup has odd order it contains no involution. The correct argument: H ≤ N(T), and every hyperbolic reflection in N(T) has an antipodal pair {w, −w} of the norm-one circle as its fixed points, so all chords are orbits of z ↦ −z. This closes the gap for every order.
  2. *S₄ case.* "m ≤ 6 and q = 11" should read "m ≤ 6, so q ≤ 11"; q = 7 is excluded by the computation (|H| = |PGL(2,7)| for the q = 7 class), not by the argument. The statement is correct as given, the proof needs that remark.
  The claim "two chords cross exactly when ι_pι_r is elliptic" (used but not proved there) is correct: with p = {0,∞}, r = {c,d} the fixed points of ι_pι_r are the roots of z² = cd. Verified numerically for q = 31, 43, 59 (3 000 random chord pairs each, 0 mismatches).
* **Lemma D (Weil stability)** is correct but weaker than our Theorem B: its threshold (q + 3√q)/2 + 2 against our (q + 2√q − 7)/2; the difference is that it uses a quartic (bound 3√q) where the elliptic-curve count of our Lemma 4.1 gives 2√q.
* **Proposition G (concurrency bound)** n_Q ≤ (q−1)/2^{t+1} + t√q + 3/2, i.e. O(√q log q), is correct as far as we can see. Our Theorem C gives 3.5√q + 6, which is stronger for q > 128 (no logarithm); Proposition G is stronger for small q. The "agreement with any Möbius map" remark is a nice extension we do not have.
* **Section 4 (energy–distance landscape).** The finite data (E ≥ c·d is useless, c_q → 0) are a reasonable negative result; nothing to object to.
* **Route 4 ("Gram-matrix route … LP bounds in the association scheme … none was run")**: our `theta_test.py` answers this: no PGL-invariant clique-bound certificate can be tight for q = 43, 47, 59, 67 (SOLUTION.md §8.2), so this route is closed.
* **Table of exceptional classes (p. 4–5)** agrees with our structure computations (stabilisers S₄, A₅, S₄; D₄; D₆, D₄; D₄×C₃; A₅) and with the other manuscript's Table 2.

## Issues

| # | where | severity | comment |
|---|---|---|---|
| 1 | Prop. F, dihedral case | gap in proof | see above; fixable. |
| 2 | Prop. F, S₄ case | gap in proof | q = 7 needs the computation; say so. |
| 3 | p. 1, "Van de Voorde (2012) records that … checked for q < 131" | attribution | the other manuscript attributes the q ≤ 131 search to Brouwer via BSW §3; neither could be verified from the sources available here. Cite the primary source. |
| 4 | Lemma D | not an error | strictly weaker than the available bound; cite or improve. |
| 5 | Section 3, "two independent implementations agree on every count for all 20 odd prime powers q ≤ 83" | scope | the C enumerator alone covers q ≥ 103; for 103 ≤ q ≤ 2 251 there is one implementation. Our run supplies the second. |
| 6 | code: `enum_c.c` allocates and frees four tables at every node | efficiency only | harmless. |
| 7 | prose | style | "Boltzmann program", "energy", "partition function" are the author's framework and add nothing to the mathematics; for an Olympiad submission state the results without the metaphor. |

## What we took over into our submission

1. The balance pruning (with attribution in the code comment and in Section 5.2 of the report), and the resulting extension of the verified range.
2. Proposition 4.2 (odd-product identities / genus-2 curves with q + 1 points).
3. Theorem E (chords of a counterexample generate PGL(2,q)), with the corrected proof.
