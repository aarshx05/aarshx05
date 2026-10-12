"""
Check the explicit small-q counterexamples listed in SOLUTION.md, section 7.

For each example the script checks the hypotheses of Conjecture 1 directly:
psi is an involution of GF(q)*, it pairs squares with non-squares, and
chi((x-y)(x-psi y)(psi x-y)(psi x-psi y)) = -1 for all y not in {x, psi x}.
It then checks that psi is NOT of the form x -> n/x.
"""

EXAMPLES = {
    7: [(1, 3), (2, 6), (4, 5)],
    11: [(1, 2), (3, 6), (4, 8), (5, 10), (7, 9)],
    19: [(1, 2), (3, 4), (5, 8), (6, 13), (7, 10), (9, 15), (11, 18), (12, 16), (14, 17)],
    23: [(1, 5), (2, 7), (3, 22), (4, 20), (6, 15), (8, 14), (9, 10), (11, 16), (12, 19),
         (13, 21), (17, 18)],
    31: [(1, 3), (2, 30), (4, 24), (5, 15), (6, 19), (7, 11), (8, 29), (9, 21), (10, 26),
         (12, 14), (13, 25), (16, 23), (17, 28), (18, 22), (20, 27)],
}

for q, pairs in EXAMPLES.items():
    sq = {x * x % q for x in range(1, q)}

    def chi(a):
        a %= q
        return 0 if a == 0 else (1 if a in sq else -1)

    psi = {}
    for a, b in pairs:
        psi[a] = b
        psi[b] = a
    assert sorted(psi) == list(range(1, q)), "psi must be an involution of GF(q)*"
    assert all(chi(x) == -chi(psi[x]) for x in psi), "squares must be paired with non-squares"
    ok = all(
        chi((x - y) * (x - psi[y]) * (psi[x] - y) * (psi[x] - psi[y])) == -1
        for x in psi for y in psi if y not in (x, psi[x])
    )
    n = psi[1]
    canonical = all(psi[x] == n * pow(x, q - 2, q) % q for x in psi)
    print(f"q={q}: hypotheses of Conjecture 1 hold: {ok}; psi is of the form n/x: {canonical}")
    assert ok and not canonical
print("all examples are genuine counterexamples")
