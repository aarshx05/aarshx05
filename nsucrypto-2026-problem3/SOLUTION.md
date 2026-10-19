# NSUCRYPTO 2026, Round 2, Problem 3: «The BSW Conjecture»

The problem asks for a proof of Conjecture 1 for all $q$, or for an infinite class of $q$, or for finitely many $q$. The case $q\equiv 1 \pmod 4$ is already known (Blokhuis–Seress–Wilbrink). Everything below concerns the open case $q\equiv 3 \pmod 4$.

## Results at a glance

| # | Result | Type |
|---|--------|------|
| **1** | **Conjecture 1 holds for all 61 prime powers $q\equiv 3 \pmod 4$ with $31<q<700$** (the list is in §6). Together with BSW, this proves the conjecture for **every odd prime power $31<q<700$**. | computer-assisted proof; the algorithm's correctness is proved in §6 |
| **2** | The condition $q>31$ is **sharp**. There are counterexamples for $q=7,11,19,23,27,31$ (their existence was already stated in the BSW abstract, and $q=7,11$ go back to Korchmáros 1981; what is new here is the explicit list, the stabilisers, and the polyhedral description). None exist for small $q\equiv1 \pmod 4$ (checked for all 37 prime powers $5\le q\le 293$). The $q=31$ counterexample is an "icosahedral" involution coming from a subgroup $A_5\le PSL(2,31)$. | explicit examples (§7) |
| **3** | **Theorem A** (exact reformulation, every $q\equiv3 \pmod 4$). Every crossing involution $\psi$ carries a well-defined sign $\pm1$ on each triple of its pairs. $\psi$ is canonical ($\psi(x)=n/x$) **iff no triple is negative**. The sign has the closed form $\chi\big((1-\lambda_1)(1-\lambda_2)(1-\lambda_3)\big)$, where $\lambda_i$ are the three pairwise cross-ratios. The proof uses Carlitz's theorem on permutations. | theorem (§3) |
| **4** | **Theorem B** (stability, every odd $q$). If $\psi(x)=n/x$ holds for more than $\frac{q+2\sqrt q-7}{2}$ elements $x\in GF(q)^*$, then it holds for all $x$. More generally, a crossing involution that shares more than $\frac{q-3+2\sqrt q}{4}$ pairs with an elliptic involution $\iota$ equals $\iota$. | theorem (§4) |
| **5** | **Theorem C** (spreading, every odd $q$). A non-canonical $\psi$ shares at most $3.5\sqrt q+6$ pairs with **any** elliptic involution. In the language of Conjecture 2: every passant contains at most $3.5\sqrt q+6$ points of a non-collinear complete exterior set. | theorem (§5) |

Theorems A–C reduce the open case to one specific configuration. A counterexample for large $q$ would have to be "spread out" (every line meets it in $O(\sqrt q)$ points), and every one of its points would have to lie in a "negative triangle". §8 explains why this is the remaining difficulty.

---

## 1. Notation and the matching formulation

Throughout, $q$ is an odd prime power, $F=GF(q)$, and $\chi$ is the quadratic character ($\chi(0)=0$). We write $PG(1,q)=F\cup\{\infty\}$. We use the representatives $x\mapsto (x,1)$ and $\infty\mapsto(1,0)$, and set
$$[u,v]=\det(\text{rep}(u),\text{rep}(v)),\qquad\text{so } [x,y]=x-y,\quad [\infty,y]=1,\quad [x,\infty]=-1 .$$
The cross-ratio $(a,b;c,d)=\dfrac{[a,c][b,d]}{[a,d][b,c]}$ does not depend on the chosen representatives and is invariant under $PGL(2,q)$.

**Definition.** Two disjoint unordered pairs $\{a,b\},\{c,d\}\subset PG(1,q)$ **cross** if $\chi\big((a,b;c,d)\big)=-1$.

This relation is well defined because $(b,a;c,d)=(a,b;c,d)^{-1}$. It is symmetric and $PGL(2,q)$-invariant. For finite points,
$$\chi\big((a,b;c,d)\big)=\chi\big((a-c)(a-d)(b-c)(b-d)\big),$$
since the cross-ratio differs from this product by the square $((a-d)(b-c))^2$. If $b=\infty$, the factors containing $b$ are simply omitted.

**Lemma 1.1 (dictionary).** A map $\psi$ satisfies the hypotheses of Conjecture 1 iff
$$M_\psi=\big\{\{0,\infty\}\big\}\cup\big\{\{x,\psi x\}: x\in F^*\big\}$$
is a perfect matching of $PG(1,q)$ in which **every two pairs cross**. Moreover, $\psi(x)=n/x$ iff $M_\psi$ is the set of orbits of the Möbius involution $z\mapsto n/z$.

*Proof.* $\psi$ has no fixed points because it changes the quadratic character. The pair $\{0,\infty\}$ crosses $\{x,\psi x\}$ iff $\chi((0-x)(0-\psi x))=\chi(x\psi x)=-1$, which says exactly that $\psi$ pairs squares with non-squares. Two finite pairs cross iff the displayed condition of Conjecture 1 holds. $\square$

We call such a $\psi$ (equivalently, such a matching $M$) a **crossing involution**. It is **canonical** if $M$ is the orbit set of an elliptic involution $\iota\in PGL(2,q)$. In Conjecture 2 language, $M$ corresponds to the set $S$ of poles of its chords: $S$ is a complete exterior set, and "canonical" means "collinear".

**Lemma 1.2 (canonical maps work).** For a non-square $n$, the map $\psi(x)=n/x$ satisfies the hypotheses.

*Proof.* $x\cdot\psi(x)=n$ is a non-square. For $y\notin\{x,n/x\}$,
$$(x-y)\Big(x-\frac ny\Big)\Big(\frac nx-y\Big)\Big(\frac nx-\frac ny\Big)=\frac{n\,(x-y)^2(xy-n)^2}{x^2y^2},$$
whose character is $\chi(n)=-1$. $\square$

---

## 2. Orientation on $PG(1,q)$ when $q\equiv 3 \pmod 4$

From now until the end of §3, assume $q\equiv3 \pmod 4$, so that $\chi(-1)=-1$.

For distinct $u,v,w\in PG(1,q)$ define the **orientation**
$$o(u,v,w)=\chi\big([u,v]\,[v,w]\,[w,u]\big)\in\{\pm1\}.$$
Each point appears twice, so $o$ is independent of the representatives. For $g\in GL(2,q)$ we have $[gu,gv]=\det g\,[u,v]$, hence
$$o(gu,gv,gw)=\chi(\det g)\,o(u,v,w).$$
So **$PSL(2,q)$ preserves $o$**, and the other coset of $PGL(2,q)$ reverses it. Because $\chi(-1)=-1$, $o$ is alternating: a transposition of two arguments changes its sign, and a cyclic shift does not. This mirrors the cyclic order of the real projective line.

**Lemma 2.1.** The pairs $\{a,b\}$ and $\{c,d\}$ cross iff $o(a,c,b)=-o(a,d,b)$. In words: $c$ and $d$ lie "on different sides" of the chord $ab$, exactly as for chords of a circle.

*Proof.*
$$o(a,c,b)\,o(a,d,b)=\chi([a,c][c,b][a,d][d,b])=\chi([a,c][b,c][a,d][b,d])=\chi\big((a,b;c,d)\big).$$
In the first step the factor $[b,a]^2$ is dropped. The second step uses $[c,b]=-[b,c]$ and $[d,b]=-[b,d]$. The last step holds because $(a,b;c,d)$ differs from $[a,c][b,d][a,d][b,c]$ by a square. $\square$

**Lemma 2.2 (cocycle).** For any four distinct points,
$$o(u_2,u_3,u_4)\,o(u_1,u_3,u_4)\,o(u_1,u_2,u_4)\,o(u_1,u_2,u_3)=1.$$

*Proof.* Write $d(u,v)=\chi([u,v])$, so that $d(v,u)=-d(u,v)$ and $o(u,v,w)=d(u,v)d(v,w)d(w,u)$. In the product, four of the six edges occur twice with the same orientation. The edges $\{2,4\}$ and $\{1,3\}$ occur once in each orientation, contributing $(-1)^2=1$. $\square$

---

## 3. Theorem A: canonical iff no negative triangle

Let $\psi$ be any fixed-point-free involution of $PG(1,q)$, and define
$$E(u,v,w)=o(u,v,w)\;o(\psi u,\psi v,\psi w).$$

**Lemma 3.1.** $M_\psi$ is crossing iff $E(a,c,\psi a)=1$ for every $a$ and every $c\notin\{a,\psi a\}$.

So the hypothesis of the conjecture says exactly this: **$\psi$ preserves the orientation of every triple that contains one of its own pairs.**

*Proof.* Put $b=\psi a$ and $d=\psi c$. Then $o(\psi a,\psi c,\psi b)=o(b,d,a)=o(a,b,d)=-o(a,d,b)$. So $E(a,c,b)=-o(a,c,b)\,o(a,d,b)=-\chi((a,b;c,d))$ by Lemma 2.1. $\square$

**Lemma 3.2.** Let $M_\psi$ be crossing. Then $E(a,c,e)=E(\psi a,c,e)$ whenever $a,c,e$ lie in three different pairs. Consequently, for three distinct pairs $\pi,\rho,\sigma\in M_\psi$, the value
$$\widehat E(\pi,\rho,\sigma)=E(a,c,e)\qquad(a\in\pi,\ c\in\rho,\ e\in\sigma)$$
is well defined and symmetric. It is $PGL(2,q)$-invariant, and it satisfies the cocycle identity on any four pairs, so it is a *two-graph* on $M_\psi$.

*Proof.* $E$ inherits the identity of Lemma 2.2 from $o$ and $o\circ\psi$, and it is symmetric because a transposition flips both factors. Apply the identity to $\{a,\psi a,c,e\}$ and use $E(a,\psi a,c)=E(a,\psi a,e)=1$ from Lemma 3.1. $PGL$-invariance: $\chi(\det g)$ appears twice. $\square$

**Proposition 3.3 (closed form).** For three pairwise crossing pairs, let $\lambda_1,\lambda_2,\lambda_3$ be the cross-ratios of the three pairs of pairs. Then
$$\boxed{\ \widehat E(\pi,\rho,\sigma)=\chi\big((1-\lambda_1)(1-\lambda_2)(1-\lambda_3)\big)\ }$$
Each factor $\chi(1-\lambda)$ is independent of the order of the points, because $\chi(1-\lambda^{-1})=\chi(\lambda-1)\chi(\lambda)=\chi(1-\lambda)$ when $\chi(\lambda)=-1$.

*Proof.* Both sides are $PGL(2,q)$-invariant and $PGL(2,q)$ is 3-transitive, so we may take $\pi=\{0,\infty\}$, $\rho=\{1,n\}$, $\sigma=\{x,y\}$. Then
$$\widehat E=o(0,1,x)\,o(\infty,n,y)=\chi(x(x-1))\cdot\chi(y-n).$$
The cross-ratios are $\lambda_1=1/n$, $\lambda_2=x/y$ and $\lambda_3=\frac{(1-x)(n-y)}{(1-y)(n-x)}$. A direct computation gives
$$(1-\lambda_1)(1-\lambda_2)(1-\lambda_3)=-\frac{(n-1)^2(x-y)^2}{n\,y(1-y)(n-x)}.$$
Its character is $\chi(y(1-y)(n-x))$. Multiplying this by $\chi(x(x-1)(y-n))$ gives
$$\chi(xy)\cdot\chi\big((1-x)(1-y)(n-x)(n-y)\big)=(-1)(-1)=1,$$
by the crossing conditions for $(\pi,\sigma)$ and $(\rho,\sigma)$. $\square$

(This formula was also checked numerically on tens of thousands of random triples for $q=7,\dots,67$.)

**Theorem A.** Let $q\equiv3 \pmod 4$, with no lower bound on $q$, and let $\psi$ satisfy the hypotheses of Conjecture 1. (The equivalence (1)⇔(3) is the "twisted Carlitz" reformulation; the same reduction to Carlitz's theorem is the route BSW take for $q\equiv1 \pmod 4$. The triangle criterion (2) and its closed form are the new content.) The following are equivalent:

1. $\psi(x)=n/x$ for some non-square $n$.
2. $\widehat E\equiv 1$. That is, for every three pairs of $M_\psi$, $\chi\big((1-\lambda_1)(1-\lambda_2)(1-\lambda_3)\big)=1$.
3. $\psi$ preserves the orientation $o$ of *every* triple of points.

*Proof.*

(1⇒3): $z\mapsto n/z$ has matrix $\begin{pmatrix}0&n\\1&0\end{pmatrix}$ with determinant $-n$, which is a square since $\chi(-1)=\chi(n)=-1$. So $\psi\in PSL(2,q)$ preserves $o$.

(3⇔2): Triples that meet a pair of $M_\psi$ twice have $E=1$ by Lemma 3.1. All other triples give $\widehat E$.

(3⇒1): Let $g$ be any permutation of $PG(1,q)$ preserving $o$. $PSL(2,q)$ is 2-transitive on $PG(1,q)$, so some $h\in PSL(2,q)$ makes $f=h\circ g$ fix $\infty$ and $0$. Since $o(\infty,x,y)=\chi(y-x)$, the map $f$ satisfies $\chi(f(y)-f(x))=\chi(y-x)$. So $\frac{f(y)-f(x)}{y-x}$ is a non-zero square for all $x\ne y$. By **Carlitz's theorem** (L. Carlitz, *A theorem on permutations in a finite field*, Proc. AMS 11 (1960); generalised by McConnel, 1963), $f(x)=ax^{p^j}$. Hence $g\in P\Sigma L(2,q)$.

Now $q=p^k$ with $k$ odd, because $q\equiv3 \pmod 4$. So $P\Sigma L(2,q)/PSL(2,q)\cong C_k$ has odd order, and the involution $\psi$ lies in $PSL(2,q)$. A Möbius map exchanging $0$ and $\infty$ is $z\mapsto n/z$, and $n=\psi(1)$ is a non-square. $\square$

**A purely combinatorial version.** For four distinct points $a,b,c,d$, the cross-ratios of the three pairings $ab|cd$, $ac|bd$, $ad|bc$ are $\lambda$, $1-\lambda$ and $1-\lambda^{-1}$ (up to inversion). Their product is $-(1-\lambda)^2$, which is a non-square. So an **odd** number of the three pairings cross: either exactly one (an *ordinary* quadruple, as on a real circle) or all three (an *exotic* quadruple, impossible over $\mathbb R$). For two crossing pairs $P,Q$,
$$\chi(1-\lambda(P,Q))=-1\iff P\cup Q\text{ is exotic}.$$
Hence $\widehat E$ is the two-graph of the "exotic graph" $X_\psi$ on $M_\psi$. **Theorem A says: $\psi$ is canonical iff $X_\psi$ is complete bipartite (possibly empty).**

**Corollaries.**

* **Conjecture 1 for a given $q\equiv 3 \pmod 4$ ⇔ no complete exterior set contains a negative triangle.** A negative triangle is three points whose pairwise cross-ratios satisfy $\chi(\prod(1-\lambda_i))=-1$.
* In a non-canonical $\psi$, **every pair lies in a negative triangle.** Suppose some $\pi_0$ lies in none. Then by the cocycle identity, $\widehat E(\rho,\sigma,\tau)=\widehat E(\pi_0,\rho,\sigma)\widehat E(\pi_0,\rho,\tau)\widehat E(\pi_0,\sigma,\tau)=1$ for all $\rho,\sigma,\tau$.
* **Spectral form.** Let $C$ be the Paley skew conference matrix on $PG(1,q)$, $C_{uv}=\chi([u,v])$, and let $P$ be the permutation matrix of $\psi$. Then $K=C\circ(PCP^{\mathsf T})$ (entrywise product) has entries $K_{uv}=\chi\big((\psi u-\psi v)(u-v)\big)$. $\psi$ is canonical iff $K+I$ has rank 1, iff $\lambda_{\max}(K)=q$.

The small counterexamples of §7 all contain negative triangles. Through every point of each of them there is one, as the corollary requires.

---

## 4. Theorem B: stability (every odd $q$)

**Lemma 4.1.** Let $\iota$ be an elliptic involution and $\sigma$ a pair that is not an $\iota$-pair. Then $\sigma$ crosses at most $\dfrac{q-3+2\sqrt q}{4}$ of the $\frac{q+1}{2}$ pairs of $\iota$.

*Proof.* All elliptic involutions are conjugate, so let $\iota(z)=n/z$ with $n$ a non-square.

Let $K=F(\sqrt n)$ and identify $z\in PG(1,q)$ with the line $F\cdot(z+\sqrt n)\subset K$, and $\infty$ with $F\cdot1$. Multiplication by $\alpha\in K^*$ then induces a cyclic group $K^*/F^*\le PGL(2,q)$ of order $q+1$ that acts regularly on $PG(1,q)$. Multiplication by $\sqrt n$ is exactly $z\mapsto n/z$, so this group centralises $\iota$. Conjugating by a suitable element of the group, we may assume $\sigma=\{c,d\}\subset F^*$.

The $\iota$-pairs are $\{0,\infty\}$ and the pairs $\{a,n/a\}$, $a\in F^*$. The latter are in bijection with $T=\{t: \chi(t^2-4n)=1\}$ via $t=a+n/a$. A short computation gives
$$(c-a)(ac-n)=-ac\,(t-t_c),\qquad t_c=c+n/c,$$
so $\sigma$ crosses $\{a,n/a\}$ iff $\chi(cd)\,\chi\big((t-t_c)(t-t_d)\big)=-1$. It crosses $\{0,\infty\}$ iff $\chi(cd)=-1$.

Write $e=\chi(cd)$ and $\mathcal E=\sum_{t\in F}\chi\big((t^2-4n)(t-t_c)(t-t_d)\big)$, and count with $\mathbf 1_T(t)=\frac{1+\chi(t^2-4n)}2$. The number of $\iota$-pairs crossed by $\sigma$ is exactly
$$N(\sigma)=\frac{q-3}{4}-\frac{e\,(1+\mathcal E)}{4}.$$
The quartic $(t^2-4n)(t-t_c)(t-t_d)$ is square-free with a square leading coefficient. So $-1-\mathcal E$ is the trace of Frobenius of an elliptic curve, and Hasse's bound gives $|1+\mathcal E|\le2\sqrt q$. $\square$

(The exact formula and the bound were checked for every chord, for all $43\le q\le131$. The bound is attained up to rounding.)

**Theorem B.** Let $M$ be a crossing perfect matching and $\iota$ an elliptic involution with $|M\cap\iota|>\frac{q-3+2\sqrt q}{4}$. Then $M=\iota$.

*Proof.* A pair $\sigma\in M\setminus\iota$ would have to cross all pairs of $M\cap\iota$, contradicting Lemma 4.1. $\square$

**Corollary.** *If $\psi(x)=n/x$ for more than $\frac{q+2\sqrt q-7}{2}$ elements $x\in GF(q)^*$, then $\psi(x)=n/x$ for all $x$.* Agreement on just over half of the field forces agreement everywhere.

---

## 5. Theorem C: counterexamples are spread out (every odd $q$)

**Theorem C.** Let $M$ be a non-canonical crossing perfect matching and $\iota$ any elliptic involution. Then
$$|M\cap\iota|\ \le\ 1+3.5\sqrt q+\frac{4q}{q-2\sqrt q+5}\ \le\ 3.5\sqrt q+6 .$$

*Proof.* Let $a=|M\cap\iota|\ge1$. Using the cyclic group from Lemma 4.1, which acts transitively on $\iota$-pairs, we may assume $\iota(z)=n/z$ and $\{0,\infty\}\in M\cap\iota$. Set
$$A=\textstyle\bigcup(M\cap\iota)\setminus\{0,\infty\},\qquad B=PG(1,q)\setminus\bigcup(M\cap\iota)\subset F^*,$$
so $|A|=2a-2$ and $|B|=q+1-2a>0$. For $v\in B$ put
$$F_v(u)=(u-v)(u-\psi v)(n-uv)(n-u\psi v).$$

* For $u\in A$ and $v\in B$, the crossing of $\{u,n/u\}$ with $\{v,\psi v\}$ means $\chi(F_v(u))=-1$.
* $F_v$ has the four distinct roots $v,\ \psi v,\ n/v,\ n/\psi v$. Indeed, $v\psi v=n$ would put $\{v,\psi v\}$ in $M\cap\iota$, and $v^2\ne n$.
* $F_vF_{v'}$ is a constant times a square only if $F_v$ and $F_{v'}$ have the same roots. For fixed $v$, this happens for at most 4 values of $v'$.

Let $\Phi(u)=\sum_{v\in B}\chi(F_v(u))$, so $\Phi\equiv-|B|$ on $A$. Using Weil's bound $|\sum\chi(f)|\le(\deg f-1)\sqrt q$ for $f$ not a constant times a square,
$$(2a-2)|B|^2\le\sum_{u\in F}\Phi(u)^2=\sum_{v,v'\in B}\sum_{u\in F}\chi(F_vF_{v'})\le 4q|B|+7\sqrt q\,|B|^2 .$$
By Theorem B, $|B|\ge\frac{q-2\sqrt q+5}{2}$, which gives the bound. Finally, $\frac{4q}{q-2\sqrt q+5}\le5$ is equivalent to $(\sqrt q-5)^2\ge0$. $\square$

In Conjecture 2 language: **if a complete exterior set is not collinear, every passant contains at most $3.5\sqrt q+6$ of its points.** For $q\gtrsim250$ this is far below the $\frac{q+1}{2}$ points of the canonical example.

**Proposition 4.2 (exact identities, every odd $q$).** Let $M$ be a good matching. For a chord $p=\{a,b\}$ put $s_p(y)=\chi([y,a][y,b])$ for $y\notin p$ and $s_p(y)=0$ for $y\in p$ (so $s_p(\infty)=1$ for finite $p$). For any odd number of chords $p_1,\dots,p_{2j+1}$ of $M$,
$$\sum_{y\in PG(1,q)} s_{p_1}(y)\cdots s_{p_{2j+1}}(y)=0 .$$
In particular, for three chords of $M$ with finite endpoints $a_1,\dots,a_6$ the genus-two curve $w^2=\prod(y-a_i)$ has exactly $q+1$ rational points.

*Proof.* $\chi((a,b;y,\psi y))=s_p(y)s_p(\psi y)$ for $y\notin p$, so crossing says $s_p(\psi y)=-s_p(y)$. An odd product is therefore $\psi$-odd off $\bigcup p_i$ and zero on it; the complement is a union of chords of $M$, on each of which the two terms cancel. For the curve, $\sum_{y\in F}\chi(f(y))=-s(\infty)=-1$ gives $q-1$ affine points, plus two at infinity. $\square$

The identities hold for canonical and non-canonical matchings alike (checked on all counterexamples); they are the reason the balance pruning of §6.2 is so effective.

---

## 6. Proof for finitely many $q$: all $q\equiv3 \pmod 4$ with $31<q<700$

### 6.1 Reduction to a finite search with symmetry breaking

For crossing pairs $\pi,\rho$, the class $[\lambda]=\{\lambda,\lambda^{-1}\}$ of their cross-ratio is a complete $PGL(2,q)$-invariant of the unordered pair $\{\pi,\rho\}$. This holds because $PGL(2,q)$ is sharply 3-transitive. Order $F$ by the integer codes of its elements, and let $\mathrm{rep}(\lambda)=\min(\lambda,\lambda^{-1})$.

**Lemma 6.1.** Suppose a non-canonical crossing perfect matching exists. Then there is one, $M'$, with these properties:

* $M'$ contains $\{0,\infty\}$ and $\{1,n\}$, where $n$ is a non-square with $n\le n^{-1}$.
* Every two pairs of $M'$ have $\mathrm{rep}\ge n$.

*Proof.* Take a non-canonical $M$ and two of its pairs $\{a,b\},\{c,d\}$ with the smallest value $n^*$ of $\mathrm{rep}$. Some $g\in PGL(2,q)$ maps $a,b,c$ to $0,\infty,1$, or to $\infty,0,1$. Then $g(d)$ is $\lambda^{-1}$ or $\lambda$ respectively, and we choose the option giving $n^*$. Cross-ratio classes and canonicity are both $PGL$-invariant. $\square$

### 6.2 The algorithm ([`verify_bsw.c`](verify_bsw.c))

For each such $n$ the program enumerates **all** perfect matchings $M\supseteq\{\{0,\infty\},\{1,n\}\}$ in which every two pairs cross and every two pairs have $\mathrm{rep}\ge n$. It is a depth-first search:

* It keeps, for every uncovered point $w$, the bitset of all uncovered $z$ such that $\{w,z\}$ crosses every chosen pair. Crossing factorises as $\chi$ of a product of four differences, so each update is a few word operations per point.
* For the first three chosen pairs, these candidate sets are also filtered by the class condition. This uses $(w,z;u,v)=A_w/A_z$ with $A_w=[w,u]/[w,v]$, so one table lookup per candidate suffices. For deeper pairs the class condition is checked when a pair is chosen.
* It branches on the uncovered point with the fewest candidates, over **all** of its candidates.
* A branch is pruned only when a candidate violates the class condition, when some uncovered point has no candidate left, or when the **sign classes are unbalanced**: each uncovered point $w$ carries the vector of signs $s_p(w)=\chi([w,a][w,b])$ over the chosen chords $p=\{a,b\}$; its partner must carry the opposite vector (Proposition 4.2), so $\psi$ maps every class of equal vectors onto the class of opposite vectors and the two classes have equal size. The program stores a 64-bit hash of the vector; a collision can only merge classes, which weakens the test but never rejects a good matching. This pruning (taken from the "Boltzmann program" document, see `REVIEW_of_boltzmann_document.md`) reduces the search from about $q^8$ to about $q^{2.5}$ nodes.

Both pruning rules only discard matchings that cannot satisfy the constraints, so the enumeration is exhaustive. Every complete matching found is re-checked against the definition by brute force, and then tested for canonicity.

### 6.3 Validation

* **Sanity invariant.** The canonical matching must be found **exactly once** per $q$, in the class $n^*$ of its own smallest cross-ratio. This held for every $q$ tested.
* **Independent brute force.** [`bruteforce_check.py`](bruteforce_check.py) is a separate program that uses only the literal statement of Conjecture 1: no projective geometry, symmetry breaking or bitsets. It counts all valid $\psi$. Its counts agree with `verify_bsw -all` for every $q$ tested:

  | $q$ | 7 | 11 | 19 | 23 | 31 | 43 | 47 | 59 | 67 | 71 | 79 | 83 | 103 | 107 | 127 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | valid $\psi$ | 5 | 12 | 54 | 121 | 31 | 21 | 23 | 29 | 33 | 35 | 39 | 41 | 51 | 53 | 63 |
  | canonical ($=\frac{q-1}2$) | 3 | 5 | 9 | 11 | 15 | 21 | 23 | 29 | 33 | 35 | 39 | 41 | 51 | 53 | 63 |

  So all ten values $q\equiv3 \pmod 4$ with $43\le q\le127$ are proved twice, by unrelated code.
* **Consistency.** For $q\equiv 1 \pmod 4$, the program finds no counterexample for any of the 37 prime powers $5\le q\le 293$, which agrees with BSW. For $q\equiv 3 \pmod 4$ with $7\le q\le 31$, it finds the counterexamples of §7.

### 6.4 Result

**Theorem D (computer-assisted).** Conjecture 1 holds for each of the following 61 prime powers $q\equiv 3 \pmod 4$. They are all such prime powers with $31<q<700$; the prime powers $243=3^5$ and $343=7^3$ are in bold.

43, 47, 59, 67, 71, 79, 83, 103, 107, 127, 131, 139, 151, 163, 167, 179, 191, 199, 211, 223, 227, 239, $\mathbf{243}$, 251, 263, 271, 283, 307, 311, 331, $\mathbf{343}$, 347, 359, 367, 379, 383, 419, 431, 439, 443, 463, 467, 479, 487, 491, 499, 503, 523, 547, 563, 571, 587, 599, 607, 619, 631, 643, 647, 659, 683, 691.

For every one of them the program reports `canonical=1 noncanonical=0 verify_fail=0` (full output in [`results_q3mod4_32_700.txt`](results_q3mod4_32_700.txt)). A few representative rows:

| $q$ | field | classes $n$ searched | search nodes | time |
|---:|---|---:|---:|---:|
| 43 | $GF(43)$ | 11 | 62 | 0.00s |
| 103 | $GF(103)$ | 26 | 709 | 0.00s |
| 243 | $GF(3^5)$ | 61 | 66,325 | 0.33s |
| 343 | $GF(7^3)$ | 86 | 595,172 | 2.69s |
| 503 | $GF(503)$ | 126 | 5,922,226 | 29.47s |
| 599 | $GF(599)$ | 150 | 20,351,591 | 160.92s |
| 643 | $GF(643)$ | 161 | 36,928,480 | 337.49s |
| 691 | $GF(691)$ | 173 | 65,243,036 | 630.04s |

The whole range took about 65 CPU-minutes in total, run in parallel on 4 cores. The running time grows roughly like $q^{8}$ to $q^{9}$, so extending the same program to all $q<1000$ would take roughly two CPU-days. `run_all.sh 700 1000` does exactly that.

Combined with the Blokhuis–Seress–Wilbrink theorem ($q\equiv1 \pmod 4$, $q>31$), **Conjecture 1 holds for every odd prime power $31<q<700$.**

To reproduce:

```
gcc -O3 -march=native -o verify_bsw verify_bsw.c
./verify_bsw 43            # one q
./run_all.sh 32 700        # every prime power q = 3 mod 4 in the range
python3 bruteforce_check.py 7 11 19 23 31 43 47
```

---

## 7. Small $q$: the bound $q>31$ is sharp

*Attribution.* The abstract of Blokhuis–Seress–Wilbrink already states that for $q\equiv3 \pmod 4$ other examples exist "at least for $q=7,11,\dots,31$", and the $q=7,11$ examples appear in G. Korchmáros, *Example of a chain of circles on an elliptic quadric of PG(3,q), q=7,11*, J. Combin. Theory Ser. A 31 (1981). So the sharpness of $q>31$ is not new; the explicit lists, stabilisers and the polyhedral description below are our own computation.

For **every** prime power $q\equiv3 \pmod 4$ with $7\le q\le31$ there is a non-canonical $\psi$. For $q=3$ there is none. Examples, written as the pairs of $M_\psi$ (the prime ones are verified directly against the statement of Conjecture 1 by `check_examples.py`):

* $q=7$: $\{0,\infty\},\{1,3\},\{2,6\},\{4,5\}$.
  This is the antipodal map of the cube: an $S_4\le PGL(2,7)$ acts on the 8 points, and $\psi(x)$ is the second fixed point of the stabiliser of $x$.
* $q=11$: $\{0,\infty\},\{1,2\},\{3,6\},\{4,8\},\{5,10\},\{7,9\}$.
  Here $\psi(x)=2x$ on squares and $x/2$ on non-squares. It is the antipodal map of the icosahedron ($A_5\le PSL(2,11)$, orbit of size 12).
* $q=19$: $\{0,\infty\},\{1,2\},\{3,4\},\{5,8\},\{6,13\},\{7,10\},\{9,15\},\{11,18\},\{12,16\},\{14,17\}$. Its stabiliser has order 8.
* $q=23$: $\{0,\infty\},\{1,5\},\{2,7\},\{3,22\},\{4,20\},\{6,15\},\{8,14\},\{9,10\},\{11,16\},\{12,19\},\{13,21\},\{17,18\}$. Its stabiliser has order 12.
* $q=27$: exists (computed in $GF(27)$; see `verify_bsw 27 -print`).
* $q=31$: $\{0,\infty\},\{1,3\},\{2,30\},\{4,24\},\{5,15\},\{6,19\},\{7,11\},\{8,29\},\{9,21\},\{10,26\},\{12,14\},\{13,25\},\{16,23\},\{17,28\},\{18,22\},\{20,27\}$.
  Its stabiliser in $PGL(2,31)$ is $A_5$, with orbits of sizes $12+20=32$: the vertices of an icosahedron and of a dodecahedron. $\psi$ is the antipodal map: $\psi(x)$ is the second fixed point of $\mathrm{Stab}_{A_5}(x)$. 320 of its 560 triangles are negative.

The examples at $q=7,11,31$ come from the exceptional rotation groups $S_4$ and $A_5$: $\psi(x)$ is the second fixed point of $\mathrm{Stab}_G(x)$, an "antipodal map" whose pairs happen to satisfy all the character conditions. These groups have bounded order. $A_5$ has at most $12+20+30=62$ points with non-trivial stabiliser, and $S_4$ at most $6+8+12=26$. So this mechanism cannot cover all $q+1$ points once $q>61$. For the normaliser of a non-split torus, a dihedral group, the same construction gives exactly the canonical matching $z\mapsto -z$ on the norm-1 circle. For the split torus it gives the pairs of $z\mapsto -z$, which do not cross. The examples at $q=19,23$ have smaller symmetry groups, of orders 8 and 12, and look like isolated coincidences. All of this is consistent with the absence of counterexamples for $31<q<700$.

---

## 8. Approaches to the general case that cannot work, and why

This section records attempts at the general case that were tested and ruled out, so that nobody repeats them. Two of them are proper negative results.

### 8.1 A rep-free form of Theorem A

For chords $\pi=\{a,\psi a\}$, $\rho=\{c,\psi c\}$ put
$$E_{\pi\rho}=\chi\big((a,c;\psi a,\psi c)\big)=\chi\big([a,\psi a][c,\psi c][a,\psi c][c,\psi a]\big).$$
This is independent of which endpoint represents each chord (swapping $a\leftrightarrow\psi a$ flips two of the four brackets), and $E_{\pi\rho}=\chi(1-\lambda(\pi,\rho))$ is the exotic sign of §3. Theorem A reads: **$\psi$ is canonical iff $E=\varepsilon\varepsilon^{\mathsf T}-I$ for some $\varepsilon\in\{\pm1\}^{M}$.** For $\psi(z)=n/z$ one has $E_{\pi\rho}=\varepsilon(a)\varepsilon(c)$ with $\varepsilon(a)=\chi(a^2-n)$.

With $T$ the number of positive triangles minus negative ones (so $T=\binom m3$ iff canonical) and $K$ the matrix of §3,
$$\operatorname{tr}K^3=3(q^2-1)+48\,T,\qquad \lambda_{\max}(K)=2\lambda_{\max}(E+I)-1 .$$
(The first identity: ordered point-triples that meet some chord twice all contribute $+1$ by Lemma 3.1; there are $3(q^2-1)$ of them. The second: $K+I=D\big((E+I)\otimes J_2\big)D$ for a diagonal $\pm1$ matrix $D$.) So the conjecture is the statement $\lambda_{\max}(K)=q$, and a proof must get at $\operatorname{tr}K^3$ or $\lambda_{\max}(K)$ from the hypothesis.

### 8.2 Negative result: no clique-bound certificate exists

Let $\Gamma$ be the graph on all $q(q+1)/2$ chords, adjacent when they cross. An all-crossing matching is a clique of size $m=(q+1)/2$. The Blokhuis–Seress–Wilbrink style of argument for $q\equiv1 \pmod 4$ is a bound of Hoffman/Delsarte type, and its natural generalisation is the Lovász theta bound: a $PGL(2,q)$-invariant matrix $Z=J+\sum_c z_cA_c$ (sum over the non-crossing orbital classes $c$) with $\lambda_{\max}(Z)=m$. If such a $Z$ existed, every clique of size $m$ would satisfy $Z\mathbf 1_S=m\mathbf 1_S$, which gives strong regularity conditions that could be exploited. Averaging over $PGL(2,q)$ shows that one may assume $Z$ class-constant, so the condition for the canonical clique $S$ is a linear system in the $(q-1)/4+1$ unknowns $z_c$, one equation per chord outside $S$.

[`theta_test.py`](theta_test.py) computes this system. **For $q=43,47,59,67$ it has full column rank, so the only solution is $z=0$, which is not a certificate.** Hence $\vartheta(\bar\Gamma)>m$ for these $q$ and the clique-bound route is closed for $q\equiv3 \pmod 4$. The reason is Lemma 4.1: the number of canonical chords crossed by an outside chord is governed by an elliptic-curve point count and is far from constant, and no reweighting of the cross-ratio classes evens it out.

### 8.3 Theorem E: the chords of a counterexample generate $PGL(2,q)$

For a chord $p=\{a,b\}$ let $\iota_p$ be the involution of $PG(1,q)$ fixing $a$ and $b$ ($z\mapsto -z$ when $p=\{0,\infty\}$). Two facts: (i) $\iota_p\notin PSL(2,q)$, since $\det\mathrm{diag}(1,-1)=-1$ is a non-square; (ii) for $p=\{0,\infty\}$, $r=\{c,d\}$ one has $\iota_r(z)=\frac{(c+d)z-2cd}{2z-(c+d)}$ and the fixed points of $\iota_p\iota_r$ solve $z^2=cd$, so $\iota_p\iota_r$ is fixed-point-free ("elliptic") iff $p$ and $r$ cross.

**Theorem E.** Let $q\equiv 3 \pmod 4$, $q>11$, and let $M$ be a non-canonical good matching. Then $\langle\iota_p:p\in M\rangle=PGL(2,q)$.

*Proof.* Let $H$ be the group generated and use Dickson's list of subgroups of $PGL(2,q)$ (cyclic, dihedral, subgroups of a point stabiliser, $A_4,S_4,A_5$, $PSL(2,q_0)$, $PGL(2,q_0)$; e.g. Cameron–Omidi–Tayfeh-Rezaie, Electron. J. Combin. 13 (2006), Thm. 2). Cyclic: one involution only. Point stabiliser: distinct chords are disjoint. $A_4,A_5,S_4\le PSL$: contradicts (i). $S_4\not\le PSL$: its involutions outside $A_4$ are six transpositions, so $m\le6$ and $q\le 11$. Subfield groups: an element of $PGL(2,q_0)$ with two fixed points in $PG(1,q)$ has them in $PG(1,q_0)$ ($q=q_0^r$, $r$ odd), so $M$ would lie in a subline. Dihedral: $\iota_p\iota_r$ is an elliptic rotation by (ii), so the rotation subgroup lies in a non-split torus $T$ and $H\le N(T)$; in the circle model of Lemma 4.1 the reflections of $N(T)$ are $z\mapsto\zeta/z$ with fixed points $\{w,-w\}$, so every chord of $M$ is an orbit of $z\mapsto -z$ and $M$ is canonical. $\square$

This upgrades the earlier computational observation (`structure_probe.py`: for $q=19,23,31$ the involutions generate the whole group) to a theorem, and shows that Dickson's classification gives no shortcut. The statement and the idea are from the "Boltzmann program" document; the dihedral case there needs the antipodal-pair argument above, and $q=7$ is excluded by computation ($|H|=|PGL(2,7)|$ for the $q=7$ class).

### 8.4 Spectral gap of the counterexamples

For the same five counterexamples, $\lambda_{\max}(K)=3,3,11,9.93,9.93$, against $\lambda_{\max}(K)=q$ for the canonical solution. The non-canonical $E$ behaves like a random $\pm1$ matrix ($\lambda_{\max}\approx2\sqrt m$), while the canonical one has rank one. A proof will therefore have to show a dichotomy, not a perturbation statement: there is no "almost canonical" regime to exploit (Theorem B already says agreement on just over half the points forces full agreement).

### 8.5 Subfields

The $q=27$ counterexample is invariant under the Frobenius $z\mapsto z^3$ and restricts to the canonical solution $z\mapsto-1/z$ on $PG(1,3)$. In general, if $\psi$ commutes with Frobenius then $\psi|_{PG(1,p)}$ is again all-crossing (for $x\in GF(p)$, $\chi_q(x)=\chi_p(x)^k=\chi_p(x)$ as $k$ is odd), hence canonical once $p\ge43$. But this says nothing about $\psi$ off the subfield, and the prime-field counterexamples show that a subfield argument cannot be the whole story.

### 8.6 What a proof must do

Theorems A–C show that a counterexample for large $q$ has very specific features:

Theorems A–C show that a counterexample for large $q$ has very specific features:

* By Theorem A, it contains negative triangles, and every pair lies in one.
* By Theorem C, it is spread out: every elliptic involution shares $O(\sqrt q)$ pairs with it.
* It survives all $\binom{(q+1)/2}{2}$ crossing conditions.

Weil-type estimates cannot rule out spread-out configurations by themselves. They control sums over *structured* sets, and Theorems B and C use exactly the structure that a single involution provides. Excluding spread-out examples seems to need a global argument, for instance a polynomial (Rédei-type) argument. A natural target is the triviality of the two-graph $\widehat E$ of Theorem A. Over the reals, the analogue of $\widehat E\equiv1$ follows from the betweenness axioms of the circle. Over $GF(q)$ it must come from arithmetic, and the counterexamples up to $q=31$ show that arithmetic only wins once $q$ is large enough.
