---
title: "Problem 3. The BSW Conjecture"
subtitle: "NSUCRYPTO 2026, Second round — solution"
lang: en
---

## Summary of what is proved

The problem asks to prove Conjecture 1 for all $q$, for an infinite class of $q$, or for finitely many $q$. The case $q\equiv 1 \;(\mathrm{mod}\;4)$ is the theorem of Blokhuis, Seress and Wilbrink (BSW). Everything below concerns the open case $q\equiv 3 \;(\mathrm{mod}\;4)$.

1. **Conjecture 1 holds for all 61 prime powers $q\equiv 3 \;(\mathrm{mod}\;4)$ with $31<q<700$** (computer-assisted; the algorithm is proved correct in Section 5 and was checked by a second, unrelated program). Together with BSW this gives: *Conjecture 1 holds for every odd prime power $31<q<700$.*

2. **Theorem A** (every $q\equiv 3 \;(\mathrm{mod}\;4)$, no lower bound). The hypotheses of Conjecture 1 say exactly that $\psi$ preserves a certain "orientation" of all triples of points that contain a pair $\{x,\psi x\}$. The conclusion $\psi(x)=n/x$ holds **if and only if** $\psi$ preserves the orientation of *all* triples, and this is the case **if and only if no three pairs form a "negative triangle"**, where the sign of a triangle has the closed form $\chi((1-\lambda_1)(1-\lambda_2)(1-\lambda_3))$ in terms of the three pairwise cross-ratios. So the conjecture is equivalent to a purely combinatorial statement about triangles.

3. **Theorem B** (stability, every odd $q$). If $\psi(x)=n/x$ holds for more than $\tfrac{q+2\sqrt q-7}{2}$ elements $x$, then it holds for all $x$.

4. **Theorem C** (spreading, every odd $q$). A map $\psi$ that satisfies the hypotheses but is *not* of the form $n/x$ agrees with any map $x\mapsto n'/x$ on at most $7\sqrt q+12$ elements $x$. A counterexample would have to be "spread out" with respect to every candidate $n'$.

5. **The bound $q>31$ cannot be lowered.** For $q=7,11,19,23,27,31$ there are maps $\psi$ satisfying all hypotheses that are not of the form $n/x$. Their existence was already stated by BSW ($q=7,11$ go back to Korchmáros, 1981); here they are listed explicitly, and the $q=7,11,31$ ones are explained as "antipodal maps" of the rotation groups of the cube and the icosahedron.

6. Two natural proof strategies for the general case are shown to be impossible (Section 7): no clique-bound (Hoffman / Delsarte / Lovász theta) certificate can be tight, and for $q>11$ the involutions attached to the chords of a counterexample generate the whole group $PGL(2,q)$ (Theorem E, a Dickson-type argument). Exact identities satisfied by every good matching (every three chords give a genus-two curve with exactly $q+1$ points) are proved in Proposition 4.2.

The conjecture for all $q$, or for an infinite class, remains open. All programs, raw outputs and the counterexamples are supplied with this report (Appendix).

---

## 1. Notation and a reformulation as a matching problem

Throughout, $q$ is an odd prime power, $F=GF(q)$, and $\chi$ is the quadratic character of $F$ ($\chi(0)=0$, $\chi(a)=1$ for non-zero squares, $\chi(a)=-1$ for non-squares). Recall $\chi(ab)=\chi(a)\chi(b)$ and $\chi(-1)=-1$ exactly when $q\equiv 3 \;(\mathrm{mod}\;4)$.

We work on the projective line $PG(1,q)=F\cup\{\infty\}$, with the representatives $x\mapsto(x,1)$ and $\infty\mapsto(1,0)$, and we write
$$[u,v]=\det(\mathrm{rep}(u),\mathrm{rep}(v)),\qquad\text{so that }[x,y]=x-y,\quad[\infty,y]=1,\quad[x,\infty]=-1 .$$
The *cross-ratio* of four distinct points is $(a,b;c,d)=\dfrac{[a,c]\,[b,d]}{[a,d]\,[b,c]}$. It does not depend on the representatives and is invariant under the group $PGL(2,q)$ of Möbius maps $z\mapsto\frac{\alpha z+\beta}{\gamma z+\delta}$.

**Definition.** Two disjoint pairs (we call them *chords*) $\{a,b\}$ and $\{c,d\}$ **cross** if $\chi((a,b;c,d))=-1.$

This is well defined since $(b,a;c,d)=(a,b;c,d)^{-1}$, it is symmetric in the two chords, and it is $PGL(2,q)$-invariant. For finite points,
$$\chi((a,b;c,d))=\chi((a-c)(a-d)(b-c)(b-d)),$$
because the cross-ratio differs from this product by the square $((a-d)(b-c))^2$. If one point is $\infty$, simply omit the two factors containing it.

**Lemma 1.1 (dictionary).** A map $\psi$ satisfies the hypotheses of Conjecture 1 if and only if
$$M_\psi=\big\{\{0,\infty\}\big\}\cup\big\{\{x,\psi x\}:x\in F^*\big\}$$
is a perfect matching of $PG(1,q)$ (a partition into $\tfrac{q+1}{2}$ chords) in which **every two chords cross**. Moreover $\psi(x)=n/x$ for all $x$ if and only if $M_\psi$ is the set of orbits of the Möbius involution $z\mapsto n/z$.

*Proof.* $\psi$ has no fixed point, because it changes the quadratic character. The chord $\{0,\infty\}$ crosses $\{x,\psi x\}$ iff $\chi((0-x)(0-\psi x))=\chi(x\psi x)=-1$, i.e. iff $x$ and $\psi x$ have opposite characters — this is "$\psi$ pairs squares with non-squares". Two chords $\{x,\psi x\},\{y,\psi y\}$ with $y\notin\{x,\psi x\}$ cross iff the displayed condition of Conjecture 1 holds. $\square$

We call such a matching a **good matching**, and we call it **canonical** if it is the orbit set of some Möbius involution without fixed points (an *elliptic* involution; in suitable coordinates every such involution is $z\mapsto n/z$ with $n$ a non-square). Conjecture 1 for a given $q$ says: *every good matching is canonical.*

**Lemma 1.2.** For every non-square $n$ the map $\psi(x)=n/x$ satisfies the hypotheses.

*Proof.* $x\cdot\psi(x)=n$ is a non-square. For $y\notin\{x,n/x\}$,
$$(x-y)(x-\frac ny)(\frac nx-y)(\frac nx-\frac ny)=\frac{n\,(x-y)^2\,(xy-n)^2}{x^2y^2},$$
whose character is $\chi(n)=-1$. $\square$

*Geometric meaning.* Identify $PG(1,q)$ with the conic $C$ of the problem statement; a chord is a secant line. Two chords cross exactly when the two secants meet in an interior point. So a good matching is a set of $\frac{q+1}{2}$ secants, any two of which meet in an interior point, and "canonical" means they all pass through one interior point. Taking poles turns this into Conjecture 2.

---

## 2. Orientation of triples when $q\equiv 3 \;(\mathrm{mod}\;4)$

From here to the end of Section 3 assume $q\equiv 3\;(\mathrm{mod}\;4)$, so $\chi(-1)=-1$.

For three distinct points $u,v,w$ define the **orientation**
$$o(u,v,w)=\chi([u,v]\,[v,w]\,[w,u])\in\{\pm1\}.$$
Each point occurs twice, so $o$ does not depend on the representatives. For a Möbius map $g$ with matrix of determinant $\det g$ one has $[gu,gv]=\det g\cdot[u,v]\cdot(\text{a square})$, hence
$$o(gu,gv,gw)=\chi(\det g)\,o(u,v,w).$$
So the maps with square determinant (the group $PSL(2,q)$) **preserve** $o$, the others reverse it. Because $\chi(-1)=-1$, swapping two arguments changes the sign of $o$, and cyclically rotating the arguments does not. This is a finite-field version of the cyclic order of points on a circle.

**Lemma 2.1 (crossing = opposite sides).** Chords $\{a,b\}$ and $\{c,d\}$ cross if and only if $o(a,c,b)=-o(a,d,b)$. In words: $c$ and $d$ lie on different "sides" of the chord $ab$, exactly as for chords of a circle.

*Proof.* $o(a,c,b)\,o(a,d,b)=\chi([a,c][c,b][a,d][d,b])$ (the factor $[b,a]^2$ dropped). Using $[c,b]=-[b,c]$ and $[d,b]=-[b,d]$ this is $\chi([a,c][b,c][a,d][b,d])=\chi((a,b;c,d))$, as the cross-ratio differs from this product by a square. $\square$

**Lemma 2.2 (four points).** For any four distinct points,
$$o(u_2,u_3,u_4)\,o(u_1,u_3,u_4)\,o(u_1,u_2,u_4)\,o(u_1,u_2,u_3)=1 .$$

*Proof.* Write $d(u,v)=\chi([u,v])$, so $d(v,u)=-d(u,v)$ and $o(u,v,w)=d(u,v)d(v,w)d(w,u)$. In the product every edge of the complete graph on $u_1,\dots,u_4$ occurs twice; four of the six edges occur twice in the same direction, the edges $u_1u_3$ and $u_2u_4$ once in each direction, contributing $(-1)^2=1.$ $\square$

---

## 3. Theorem A: canonical if and only if there is no negative triangle

Let $\psi$ be any fixed-point-free involution of $PG(1,q)$ and put
$$E(u,v,w)=o(u,v,w)\;o(\psi u,\psi v,\psi w).$$

**Lemma 3.1.** $M_\psi$ is good if and only if $E(a,c,\psi a)=1$ for every $a$ and every $c\notin\{a,\psi a\}$.

In words: *the hypotheses of Conjecture 1 say exactly that $\psi$ preserves the orientation of every triple that contains one of its own chords.*

*Proof.* Let $b=\psi a$, $d=\psi c$. Then $o(\psi a,\psi c,\psi b)=o(b,d,a)=o(a,b,d)=-o(a,d,b)$, so $E(a,c,b)=-o(a,c,b)\,o(a,d,b)=-\chi((a,b;c,d))$ by Lemma 2.1. $\square$

**Lemma 3.2.** Let $M_\psi$ be good. If $a,c,e$ lie in three different chords then $E(a,c,e)=E(\psi a,c,e)$. Consequently, for three distinct chords $\pi,\rho,\sigma$ of $M_\psi$ the value
$$\widehat E(\pi,\rho,\sigma)=E(a,c,e)\qquad(a\in\pi,\ c\in\rho,\ e\in\sigma)$$
is well defined, symmetric, and invariant under $PGL(2,q)$; and $\widehat E$ satisfies the identity of Lemma 2.2 on any four chords.

*Proof.* $E$ satisfies the identity of Lemma 2.2 because both $o$ and $o\circ\psi$ do, and $E$ is symmetric because a transposition flips both factors. Apply the identity to the four points $a,\psi a,c,e$ and use $E(a,\psi a,c)=E(a,\psi a,e)=1$ (Lemma 3.1). Under a Möbius map the factor $\chi(\det g)$ appears twice. $\square$

We call a triple of chords **negative** if $\widehat E=-1$.

**Proposition 3.3 (closed form).** Let $\pi,\rho,\sigma$ be pairwise crossing chords and $\lambda_1,\lambda_2,\lambda_3$ the cross-ratios of the three pairs of chords (as in the Definition of Section 1). Then
$$\widehat E(\pi,\rho,\sigma)=\chi((1-\lambda_1)(1-\lambda_2)(1-\lambda_3)).$$
Each factor $\chi(1-\lambda)$ is independent of the order of the points, since $\chi(1-\lambda^{-1})=\chi(\lambda-1)\chi(\lambda)=\chi(1-\lambda)$ when $\chi(\lambda)=-1$.

*Proof.* Both sides are $PGL(2,q)$-invariant and $PGL(2,q)$ is 3-transitive, so we may assume $\pi=\{0,\infty\}$, $\rho=\{1,n\}$, $\sigma=\{x,y\}$. Then
$$\widehat E=o(0,1,x)\,o(\infty,n,y)=\chi(x(x-1))\,\chi(y-n).$$
The cross-ratios are $\lambda_1=1/n$, $\lambda_2=x/y$, $\lambda_3=\dfrac{(1-x)(n-y)}{(1-y)(n-x)}$, and a direct computation gives
$$(1-\lambda_1)(1-\lambda_2)(1-\lambda_3)=-\frac{(n-1)^2(x-y)^2}{n\,y\,(1-y)(n-x)},$$
whose character is $\chi(y(1-y)(n-x))$ (recall $\chi(-n)=1$). Multiplying by $\chi(x(x-1)(y-n))$ gives $\chi(xy)\cdot\chi((1-x)(1-y)(n-x)(n-y))=(-1)(-1)=1$ by the crossing conditions for $(\pi,\sigma)$ and $(\rho,\sigma)$. $\square$

**Theorem A.** Let $q\equiv 3\;(\mathrm{mod}\;4)$ (any size) and let $\psi$ satisfy the hypotheses of Conjecture 1. The following are equivalent.

1. $\psi(x)=n/x$ for some non-square $n$.
2. $M_\psi$ has no negative triangle: $\chi((1-\lambda_1)(1-\lambda_2)(1-\lambda_3))=1$ for every three chords.
3. $\psi$ preserves the orientation $o$ of **every** triple of points of $PG(1,q)$.

*Proof.* (1 ⇒ 3): $z\mapsto n/z$ has matrix $\begin{pmatrix}0&n\\1&0\end{pmatrix}$ of determinant $-n$, a square because $\chi(-1)=\chi(n)=-1$. So $\psi\in PSL(2,q)$ preserves $o$.

(3 ⇔ 2): triples meeting some chord twice have $E=1$ by Lemma 3.1; all other triples give $\widehat E$.

(3 ⇒ 1): Let $g$ be any permutation of $PG(1,q)$ preserving $o$. Since $PSL(2,q)$ is 2-transitive, composing with a suitable $h\in PSL(2,q)$ we get $f=h\circ g$ fixing $\infty$ and $0$. As $o(\infty,x,y)=\chi(y-x)$, $f$ satisfies $\chi(f(y)-f(x))=\chi(y-x)$ for all $x\ne y$ in $F$, i.e. every "slope" $\frac{f(y)-f(x)}{y-x}$ is a non-zero square. By **Carlitz's theorem** (L. Carlitz, Proc. AMS 11 (1960); extended to all odd $q$ by McConnel, Acta Arith. 8 (1963)), such an $f$ is of the form $f(x)=\alpha+\beta x^{p^j}$. Hence $g$ is a Möbius map composed with a field automorphism.

Now $q=p^k$ with $k$ odd (since $q\equiv 3\;(\mathrm{mod}\;4)$), so the group of field automorphisms has odd order $k$, and an involution $g$ in the semidirect product must lie in $PGL(2,q)$ — in fact in $PSL(2,q)$, as it preserves $o$. A Möbius map exchanging $0$ and $\infty$ is $z\mapsto n/z$, and $n=\psi(1)$ is a non-square. $\square$

**Remarks.** (a) The equivalence (1)⇔(3) is the "Carlitz" reduction, the same route BSW take for $q\equiv 1\;(\mathrm{mod}\;4)$; the triangle criterion (2) and its closed form are new. (b) *Combinatorial version.* For four distinct points $a,b,c,d$ the three ways to pair them have cross-ratios $\lambda$, $1-\lambda$, $1-\lambda^{-1}$ (up to inversion), whose product $-(1-\lambda)^2$ is a non-square; so an *odd* number of the three pairings cross — either exactly one (as on a real circle) or all three (*exotic* quadruple, impossible over the reals). For two crossing chords, $\chi(1-\lambda)=-1$ exactly when their four points form an exotic quadruple. So Theorem A says: *$\psi$ is canonical iff the "exotic graph" on its chords is complete bipartite (or empty).* (c) In a non-canonical good matching *every* chord lies in a negative triangle: if $\pi_0$ lay in none, Lemma 2.2 for chords would give $\widehat E(\rho,\sigma,\tau)=\widehat E(\pi_0,\rho,\sigma)\widehat E(\pi_0,\rho,\tau)\widehat E(\pi_0,\sigma,\tau)=1$ for all triples.

---

## 4. Theorems B and C: stability and spreading (every odd $q$)

We use Weil's bound in the form: *if $h\in F[t]$ is not a constant times a square and has $d$ distinct roots, then $|\sum_{t\in F}\chi(h(t))|\le(d-1)\sqrt q$.*

**Lemma 4.1.** Let $\iota$ be an elliptic involution and $\sigma$ a chord that is not an orbit of $\iota$. Then $\sigma$ crosses at most $\dfrac{q-3+2\sqrt q}{4}$ of the $\frac{q+1}{2}$ orbits of $\iota$.

*Proof.* All elliptic involutions are conjugate, so let $\iota(z)=n/z$, $n$ a non-square. Let $K=F(\sqrt n)$ and identify $z\in F$ with the line $F\cdot(z+\sqrt n)\subset K$ and $\infty$ with $F\cdot 1$. Multiplication by elements of $K^*$ induces a cyclic subgroup of $PGL(2,q)$ of order $q+1$ acting regularly on $PG(1,q)$; multiplication by $\sqrt n$ is exactly $\iota$, so this group commutes with $\iota$. Applying a suitable element we may assume $\sigma=\{c,d\}\subset F^*$.

The orbits of $\iota$ are $\{0,\infty\}$ and the chords $\{a,n/a\}$, $a\in F^*$; the latter correspond bijectively to $T=\{t:\chi(t^2-4n)=1\}$ via $t=a+n/a$. From $(c-a)(ac-n)=-ac\,(t-t_c)$ with $t_c=c+n/c$ one gets: $\sigma$ crosses $\{a,n/a\}$ iff $\chi(cd)\,\chi((t-t_c)(t-t_d))=-1$, and $\sigma$ crosses $\{0,\infty\}$ iff $\chi(cd)=-1$. Writing $e=\chi(cd)$, $\mathcal E=\sum_{t\in F}\chi((t^2-4n)(t-t_c)(t-t_d))$ and counting with $\mathbf 1_T(t)=\frac{1+\chi(t^2-4n)}{2}$, the number of orbits crossed by $\sigma$ is exactly
$$N(\sigma)=\frac{q-3}{4}-\frac{e\,(1+\mathcal E)}{4}.$$
The quartic $(t^2-4n)(t-t_c)(t-t_d)$ is square-free with square leading coefficient, so $-1-\mathcal E$ is the trace of Frobenius of an elliptic curve and Hasse's bound gives $|1+\mathcal E|\le 2\sqrt q$. $\square$

(The exact formula and the bound were checked for every chord and all $43\le q\le 131$; the bound is attained up to rounding, e.g. $13$ for $q=43$ against $13.28$.)

**Theorem B (stability).** Let $M$ be a good matching and $\iota$ an elliptic involution. If $M$ contains more than $\frac{q-3+2\sqrt q}{4}$ orbits of $\iota$, then $M$ is the orbit set of $\iota$. In particular: *if $\psi(x)=n/x$ for more than $\frac{q+2\sqrt q-7}{2}$ elements $x\in F^*$, then $\psi(x)=n/x$ for all $x$.*

*Proof.* A chord of $M$ that is not an orbit of $\iota$ would have to cross all the orbits of $\iota$ lying in $M$, contradicting Lemma 4.1. $\square$

**Theorem C (spreading).** Let $M$ be a good matching that is not canonical and $\iota$ any elliptic involution. Then $M$ contains at most $3.5\sqrt q+6$ orbits of $\iota$. (Equivalently: a non-canonical $\psi$ agrees with $x\mapsto n'/x$ on at most $7\sqrt q+12$ elements, for every non-square $n'$.)

*Proof.* Let $a\ge 1$ be the number of common chords. As in Lemma 4.1 assume $\iota(z)=n/z$ and $\{0,\infty\}\in M$. Let $A$ be the set of points of the common chords other than $0,\infty$ ($|A|=2a-2$) and $B$ the set of points of the remaining chords ($|B|=q+1-2a>0$, $B\subset F^*$). For $v\in B$ put
$$F_v(u)=(u-v)(u-\psi v)(n-uv)(n-u\,\psi v).$$
For $u\in A$, $v\in B$ the crossing of $\{u,n/u\}$ with $\{v,\psi v\}$ says $\chi(F_v(u))=-1$. $F_v$ has the four distinct roots $v,\psi v,n/v,n/\psi v$ (note $v\psi v\ne n$ because $\{v,\psi v\}$ is not an orbit of $\iota$, and $v^2\ne n$). Two polynomials $F_v,F_{v'}$ have the same root set for at most $4$ values $v'$ per $v$, and otherwise $F_vF_{v'}$ is not a constant times a square. Let $\Phi(u)=\sum_{v\in B}\chi(F_v(u))$; then $\Phi\equiv-|B|$ on $A$, and by Weil's bound
$$(2a-2)|B|^2\le\sum_{u\in F}\Phi(u)^2=\sum_{v,v'\in B}\sum_{u\in F}\chi(F_vF_{v'})\le 4q|B|+7\sqrt q\,|B|^2 .$$
By Theorem B, $|B|\ge\frac{q-2\sqrt q+5}{2}$, which gives $a\le 1+3.5\sqrt q+\frac{4q}{q-2\sqrt q+5}\le 3.5\sqrt q+6$, the last step being $(\sqrt q-5)^2\ge 0$. $\square$

In the language of Conjecture 2: *if a set $S$ as in Conjecture 2 is not contained in a passant, then every passant contains at most $3.5\sqrt q+6$ points of $S$.*

**Proposition 4.2 (exact identities).** Let $M$ be a good matching, $q$ any odd prime power. For a chord $p=\{a,b\}$ put $s_p(y)=\chi([y,a]\,[y,b])$ for $y\notin p$ (for finite points this is $\chi((y-a)(y-b))$, the factor of $\infty$ omitted, and $s_p(\infty)=1$) and $s_p(y)=0$ for $y\in p$. Then for any **odd** number of chords $p_1,\dots,p_{2j+1}$ of $M$,
$$\sum_{y\in PG(1,q)}\ s_{p_1}(y)\,s_{p_2}(y)\cdots s_{p_{2j+1}}(y)=0 .$$
In particular, for any three chords of $M$ with six finite endpoints $a_1,\dots,a_6$, the curve $w^2=(y-a_1)(y-a_2)\cdots(y-a_6)$ has **exactly $q+1$ points** over $GF(q)$ (two of them at infinity).

*Proof.* For $y\notin p$ we have $y,\psi y\notin p$ and $\chi\big((a,b;y,\psi y)\big)=\chi([a,y][b,\psi y][a,\psi y][b,y])=s_p(y)\,s_p(\psi y)$, so the crossing of $p$ with $\{y,\psi y\}$ says $s_p(\psi y)=-s_p(y)$. A product of an odd number of such functions therefore changes sign under $\psi$ on the complement of $p_1\cup\dots\cup p_{2j+1}$, and vanishes on that union. The complement is a union of chords $\{y,\psi y\}$ of $M$, and the two terms of each chord cancel. For the curve: the sum over $y\in F$ of $\chi(f(y))$, $f$ the sextic, equals $-s(\infty)=-1$, so the number of affine points is $\sum_{y\in F}(1+\chi(f(y)))=q-1$; the leading coefficient $1$ is a square, which gives two more points at infinity. $\square$

These identities hold for the canonical matching and for the counterexamples alike (checked on all of them), so they do not decide the conjecture; but they are exact constraints of "Weil strength" on every triple of chords, and they explain why the search of Section 5 is so fast: a partial matching whose sign classes are unbalanced can never be completed.

---

## 5. Proof for all $q\equiv 3 \;(\mathrm{mod}\;4)$ with $31<q<700$

### 5.1 Reduction to a finite search

For crossing chords $\pi,\rho$ the class $\{\lambda,\lambda^{-1}\}$ of their cross-ratio is a complete $PGL(2,q)$-invariant of the unordered pair $\{\pi,\rho\}$ (because $PGL(2,q)$ is sharply 3-transitive). Order the elements of $F$ by their integer codes and put $\mathrm{rep}(\lambda)=\min(\lambda,\lambda^{-1})$.

**Lemma 5.1.** If a non-canonical good matching exists, then there is one, $M'$, such that $M'$ contains $\{0,\infty\}$ and $\{1,n\}$ for a non-square $n$ with $n\le n^{-1}$, and every two chords of $M'$ have $\mathrm{rep}\ge n$.

*Proof.* Take a non-canonical good $M$ and two of its chords $\{a,b\},\{c,d\}$ with the smallest value $n^*$ of $\mathrm{rep}$. Some $g\in PGL(2,q)$ maps $a,b,c$ to $0,\infty,1$ (or to $\infty,0,1$); then $g(d)$ equals $\lambda^{\pm1}$ and we choose the option equal to $n^*$. Cross-ratio classes and being canonical are $PGL$-invariant. $\square$

### 5.2 The algorithm (`verify_bsw.c`)

For each non-square $n\le n^{-1}$ the program lists **all** perfect matchings $M\supseteq\{\{0,\infty\},\{1,n\}\}$ in which every two chords cross and every two chords have $\mathrm{rep}\ge n$, by depth-first search:

* for every uncovered point $w$ it keeps the set of uncovered $z$ such that $\{w,z\}$ crosses every chosen chord (and, for the first three chords, also satisfies the class condition);
* it branches on the uncovered point with the fewest candidates, over **all** its candidates;
* a branch is abandoned only when some uncovered point has no candidate left, when a candidate violates the class condition, or when the *sign classes are unbalanced*: every uncovered point $w$ carries the vector of signs $s_{p}(w)$ over the chosen chords $p$; the partner of $w$ must carry the opposite vector (Proposition 4.2), so in any completion $\psi$ maps each class of equal vectors onto the class of opposite vectors, and the two classes must have the same size. (The program keeps a 64-bit hash of the vector; a hash collision can only merge classes, which weakens the test but never rejects a good matching.)

Every rule only discards matchings that violate the constraints, so the enumeration is exhaustive. The balance test is what makes the search feasible for large $q$: without it the number of search nodes grows like $q^8$, with it like $q^{2.5}$ (for $q=691$: 65 million nodes and 630 s against 53 thousand nodes and 6 s). Every complete matching found is re-checked against the definition by brute force and then tested for being canonical. **Conjecture 1 holds for $q$ exactly when, for every $n$, the only matching found is the canonical one** (Lemmas 1.1 and 5.1).

### 5.3 Validation

* *Sanity invariant.* The canonical matching must be found exactly once per $q$, in the class $n^*$ of its own smallest cross-ratio. This held for every $q$ tested.
* *Independent program.* `bruteforce_check.py` uses only the literal statement of Conjecture 1 (no geometry, no symmetry breaking, no bitsets) and counts all valid $\psi$. Its counts agree with the C program run without symmetry breaking (`-all`) for every $q$ tested:

  | $q$ | 7 | 11 | 19 | 23 | 31 | 43 | 47 | 59 | 67 | 71 | 79 | 83 | 103 | 107 | 127 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | valid $\psi$ | 5 | 12 | 54 | 121 | 31 | 21 | 23 | 29 | 33 | 35 | 39 | 41 | 51 | 53 | 63 |
  | of the form $n/x$ | 3 | 5 | 9 | 11 | 15 | 21 | 23 | 29 | 33 | 35 | 39 | 41 | 51 | 53 | 63 |

  So all ten values $43\le q\le 127$ are proved twice by unrelated code. (The number of maps $n/x$ is $\frac{q-1}{2}$, one per non-square.)
* *Consistency with known results.* For $q\equiv 1\;(\mathrm{mod}\;4)$ the program finds no counterexample for any of the 37 prime powers $5\le q\le 293$ (as BSW's theorem predicts), and for $q\equiv 3\;(\mathrm{mod}\;4)$, $7\le q\le 31$, it finds exactly the counterexamples of Section 6.
* *Field arithmetic.* For $q=p^k$, $k>1$, the program constructs $GF(q)$ from a primitive polynomial it finds by search and uses log/exponent tables; the values $q=243=3^5$ and $q=343=7^3$ are included.

### 5.4 Result

**Theorem D (computer-assisted).** Conjecture 1 holds for each of the 61 prime powers $q\equiv 3\;(\mathrm{mod}\;4)$ with $31<q<700$:

43, 47, 59, 67, 71, 79, 83, 103, 107, 127, 131, 139, 151, 163, 167, 179, 191, 199, 211, 223, 227, 239, **243**, 251, 263, 271, 283, 307, 311, 331, **343**, 347, 359, 367, 379, 383, 419, 431, 439, 443, 463, 467, 479, 487, 491, 499, 503, 523, 547, 563, 571, 587, 599, 607, 619, 631, 643, 647, 659, 683, 691.

For every one of them the program reports `canonical=1 noncanonical=0 verify_fail=0` (file `results_q3mod4_32_700.txt`). Some rows:

| $q$ | field | classes $n$ searched | search nodes | time (s) |
|---:|---|---:|---:|---:|
| 43 | $GF(43)$ | 11 | 62 | 0.00 |
| 103 | $GF(103)$ | 26 | 709 | 0.00 |
| 243 | $GF(3^5)$ | 61 | 66 325 | 0.33 |
| 343 | $GF(7^3)$ | 86 | 595 172 | 2.69 |
| 503 | $GF(503)$ | 126 | 5 922 226 | 29 |
| 599 | $GF(599)$ | 150 | 20 351 591 | 161 |
| 691 | $GF(691)$ | 173 | 65 243 036 | 630 |

(The node counts and times in this table are those of the original run, without the balance test of Section 5.2; the whole range took about 65 CPU-minutes. With the balance test the same program needs 53 thousand nodes and 6 s for $q=691$, and the whole range takes a few minutes.)

**Corollary.** Together with the theorem of Blokhuis–Seress–Wilbrink for $q\equiv 1\;(\mathrm{mod}\;4)$, *Conjecture 1 holds for every odd prime power $q$ with $31<q<700$.*

*Independent confirmation.* The 38 values $31<q\le 431$ were also checked by a separately written program (two implementations of a different search, with a naive third program up to $q=127$), and a third, again separately written program using the balance pruning reports the conjecture for every prime power $q\equiv 3\pmod 4$ with $103\le q\le 2251$; the solution counts of all three programs agree on every common value. With the balance pruning now built into `verify_bsw.c`, the cost grows only like $q^{2.5}$ nodes, so the range can be pushed further at will (`run_all.sh 700 3000`).

---

## 6. The bound $q>31$ cannot be improved

For every prime power $q\equiv 3\;(\mathrm{mod}\;4)$ with $7\le q\le 31$ there is a non-canonical good matching (for $q=3$ there is none). The *existence* of these examples is stated in the BSW abstract, and $q=7,11$ were found by Korchmáros (J. Combin. Theory A 31, 1981); the explicit lists, stabilisers and the polyhedral description are our computation. Written as the chords of $M_\psi$ (verified against the statement of Conjecture 1 by `check_examples.py`):

* $q=7$: {0,∞}, {1,3}, {2,6}, {4,5}. Its stabiliser in $PGL(2,7)$ is $S_4$ (the rotation group of the cube acting on 8 points) and $\psi(x)$ is the second fixed point of the stabiliser of $x$: an "antipodal map".
* $q=11$: {0,∞}, {1,2}, {3,6}, {4,8}, {5,10}, {7,9} — here $\psi(x)=2x$ on squares and $x/2$ on non-squares; the antipodal map of the icosahedron ($A_5\le PSL(2,11)$).
* $q=19$: {0,∞}, {1,2}, {3,4}, {5,8}, {6,13}, {7,10}, {9,15}, {11,18}, {12,16}, {14,17} (stabiliser of order 8).
* $q=23$: {0,∞}, {1,5}, {2,7}, {3,22}, {4,20}, {6,15}, {8,14}, {9,10}, {11,16}, {12,19}, {13,21}, {17,18} (stabiliser of order 12).
* $q=27$: in $GF(27)=GF(3)[\theta]$, elements coded as $c_0+3c_1+9c_2$ for $c_0+c_1\theta+c_2\theta^2$ with the primitive polynomial used by the program: {0,∞}, {1,2}, {3,13}, {4,9}, {5,16}, {6,26}, {7,23}, {8,18}, {10,12}, {11,17}, {14,15}, {19,22}, {20,24}, {21,25}. It commutes with the Frobenius $z\mapsto z^3$ and restricts to the canonical map $z\mapsto -1/z$ on $PG(1,3)$.
* $q=31$: {0,∞}, {1,3}, {2,30}, {4,24}, {5,15}, {6,19}, {7,11}, {8,29}, {9,21}, {10,26}, {12,14}, {13,25}, {16,23}, {17,28}, {18,22}, {20,27}. Its stabiliser is $A_5$ with orbits of sizes $12+20$: the vertices of an icosahedron and of a dodecahedron, and $\psi$ is the antipodal map. 320 of its 560 triangles are negative.

The polyhedral mechanism is bounded: $A_5$ has at most $12+20+30=62$ points with non-trivial stabiliser and $S_4$ at most 26, so antipodal maps of polyhedral groups cannot cover $q+1$ points once $q>61$. The remaining examples ($q=19,23,27$) have small symmetry and look like isolated coincidences. This is consistent with Theorem D.

---

## 7. What remains, and two approaches that cannot work

Theorems A–C show that a counterexample for large $q$ would have to contain negative triangles through every chord (Theorem A) and be spread out with respect to every elliptic involution (Theorem C). We also record two negative results, so that nobody repeats these attempts.

**No clique-bound certificate.** On the graph whose vertices are all chords, adjacent when they cross, a good matching is a clique of size $\frac{q+1}{2}$. The method of BSW for $q\equiv 1\;(\mathrm{mod}\;4)$ is of Hoffman/Delsarte type, and its natural generalisation is a Lovász-theta certificate: a $PGL(2,q)$-invariant matrix $Z$ with $\lambda_{\max}(Z)=\frac{q+1}{2}$. Such a $Z$ would force every maximum clique to satisfy strong regularity conditions. Averaging over $PGL(2,q)$, $Z$ may be assumed constant on the cross-ratio classes, and then tightness for the canonical clique is a linear system with one unknown per non-crossing class. `theta_test.py` computes it: for $q=43,47,59,67$ the system has full column rank, so the only solution is $Z=J$, which is not a certificate. **Hence no clique-bound proof exists for $q\equiv 3\;(\mathrm{mod}\;4)$.** The reason is visible in Lemma 4.1: the number of canonical chords crossed by an outside chord is governed by an elliptic-curve point count and is far from constant.

**Theorem E (the chords generate the whole group).** Let $q\equiv 3\pmod 4$, $q>11$, and let $M$ be a good matching. For a chord $p=\{a,b\}$ let $\iota_p$ be the Möbius involution fixing $a$ and $b$ (in coordinates $a=0$, $b=\infty$ it is $z\mapsto -z$). If $M$ is not canonical, then the involutions $\iota_p$, $p\in M$, generate all of $PGL(2,q)$.

*Proof.* Two facts first. (i) $\iota_p\notin PSL(2,q)$: its matrix $\mathrm{diag}(1,-1)$ has determinant $-1$, a non-square. (ii) If chords $p,r$ cross then $\iota_p\iota_r$ has no fixed point ("elliptic"): with $p=\{0,\infty\}$, $r=\{c,d\}$ one computes $\iota_r(z)=\frac{(c+d)z-2cd}{2z-(c+d)}$ and the fixed points of $\iota_p\iota_r$ are the solutions of $z^2=cd$, which exist iff $\chi(cd)=1$, i.e. iff $p,r$ do **not** cross (Lemma 1.1).

Let $H=\langle\iota_p:p\in M\rangle$ and run through Dickson's list of the subgroups of $PGL(2,q)$ (cyclic; dihedral; subgroups fixing a point; $A_4$, $S_4$, $A_5$; $PSL(2,q_0)$ and $PGL(2,q_0)$ for subfields $GF(q_0)\subseteq GF(q)$; see e.g. Cameron–Omidi–Tayfeh-Rezaie, *3-designs from PGL(2,q)*, Electron. J. Combin. 13 (2006), Thm. 2).
*Cyclic:* contains one involution, but $H$ contains $m\ge 2$. *Fixing a point:* $\iota_p$ fixes only the two points of $p$, and distinct chords are disjoint. *$A_4$, $A_5$, and $S_4\le PSL(2,q)$:* these lie in $PSL(2,q)$, contradicting (i). *$S_4\not\le PSL(2,q)$:* then $S_4\cap PSL(2,q)=A_4$ and the involutions outside $A_4$ are the six transpositions, so $m\le 6$, $q\le 11$. *Subfield groups:* an element of $PGL(2,q_0)$ with two fixed points in $PG(1,q)$ has them in $PG(1,q_0)$ (they are roots of a quadratic over $GF(q_0)$, and $q=q_0^r$ with $r$ odd), so all chords of $M$ would lie in a subline with $q_0+1<q+1$ points. *Dihedral:* the product of two reflections $\iota_p\iota_r$ is a rotation and is elliptic by (ii), so the rotation subgroup lies in a cyclic group $T$ of order $q+1$ (a "non-split torus") and $H\le N(T)$. In the model of Lemma 4.1 ($PG(1,q)=$ the norm-one circle $U\subset GF(q^2)$, $T=$ the rotations $z\mapsto\zeta z$), the elements of $N(T)\setminus T$ are the maps $z\mapsto\zeta/z$, whose fixed points are the solutions of $z^2=\zeta$ in $U$: a pair $\{w,-w\}$. So every $\iota_p$ has an *antipodal* pair as its fixed points, i.e. every chord of $M$ is an orbit of the fixed-point-free involution $z\mapsto -z$, and $M$ is canonical. $\square$

So for $q>11$ a counterexample cannot be "small" in the group: its chords generate the whole group $PGL(2,q)$, and nothing can be extracted from the subgroup structure. (For the counterexamples at $q=7$ and $11$ the group generated is $S_4$, and the matching is invariant under it; for the other counterexamples the computation confirms $H=PGL(2,q)$.)

**Spectral form.** With $K_{uv}=\chi([u,v][\psi u,\psi v])$, Theorem A says that $\psi$ is canonical iff $\lambda_{\max}(K)=q$. For the counterexamples $\lambda_{\max}(K)\le 11$: they behave like random $\pm1$ matrices, while the canonical one is rank-one plus identity. So a proof must establish a sharp dichotomy; there is no "almost canonical" regime to perturb from (Theorem B says the same).

---

## Appendix: files supplied with this report

| file | purpose |
|---|---|
| `verify_bsw.c` | the search of Section 5 (`gcc -O3 -march=native -o verify_bsw verify_bsw.c`; `./verify_bsw q [-all] [-print]`) |
| `run_all.sh` | runs it for every prime power $q\equiv 3\;(\mathrm{mod}\;4)$ in a range |
| `results_q3mod4_32_700.txt` | output for all 61 values $31<q<700$ (Theorem D) |
| `results_q1mod4_5_293.txt` | consistency run for $q\equiv 1\;(\mathrm{mod}\;4)$ |
| `bruteforce_check.py` | independent brute-force count of all valid $\psi$ for small prime $q$ |
| `check_examples.py` | verifies the counterexamples of Section 6 against the statement |
| `theta_test.py`, `structure_probe.py` | the computations of Section 7 |

To reproduce everything: `./run_all.sh 32 700`, `python3 bruteforce_check.py 7 11 19 23 31 43 47 59`, `python3 check_examples.py`.

*Use of generative AI.* The arguments, programs and computations in this report were produced with the assistance of an AI system (Claude, Anthropic), as permitted by the rules; all proofs are given in full and all computations can be reproduced from the supplied code.
