"""
Independent brute-force cross-check of verify_bsw.c for small prime q.

It counts every map psi of GF(q)* that satisfies the hypotheses of
Conjecture 1 *literally as stated*:
  * psi is an involution of GF(q)*,
  * psi pairs every square with a non-square,
  * chi((x-y)(x-psi y)(psi x-y)(psi x-psi y)) = -1 whenever y not in {x, psi x}.
It also counts how many of them have the form psi(x) = n/x.

No projective geometry, symmetry breaking or bitsets are used. The program
assigns psi(s) for the squares s one at a time and tests the condition against
the pairs already chosen.

Usage: python3 bruteforce_check.py 7 11 19 23 31
"""
import sys


def count(q):
    squares = sorted({x * x % q for x in range(1, q)})
    nonsq = [x for x in range(1, q) if x not in set(squares)]
    sqset = set(squares)

    def chi(a):
        a %= q
        return 0 if a == 0 else (1 if a in sqset else -1)

    def ok(x, px, y, py):
        return chi((x - y) * (x - py) * (px - y) * (px - py)) == -1

    pairs = []
    used = set()
    found = [0, 0]  # total, canonical

    def rec(i):
        if i == len(squares):
            psi = {}
            for a, b in pairs:
                psi[a] = b
                psi[b] = a
            found[0] += 1
            n = psi[1]
            if all(psi[x] == n * pow(x, q - 2, q) % q for x in range(1, q)):
                found[1] += 1
            return
        x = squares[i]
        for px in nonsq:
            if px in used:
                continue
            if all(ok(x, px, y, py) for (y, py) in pairs):
                pairs.append((x, px))
                used.add(px)
                rec(i + 1)
                used.discard(px)
                pairs.pop()

    rec(0)
    return found


for arg in sys.argv[1:]:
    q = int(arg)
    tot, can = count(q)
    print(f"q={q}: valid psi = {tot}, of the form n/x = {can}, others = {tot - can}")
