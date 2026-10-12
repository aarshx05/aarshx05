#!/bin/sh
# Run verify_bsw for every prime power q = 3 (mod 4) with LO <= q <= HI, using all CPU cores.
# Usage: ./run_all.sh 32 1000 > results.txt
LO=${1:-32}; HI=${2:-1000}
[ -x ./verify_bsw ] || gcc -O3 -march=native -o verify_bsw verify_bsw.c || exit 1
python3 - "$LO" "$HI" <<'PY' | xargs -P "$(nproc)" -I{} ./verify_bsw {} | sort -t= -k2 -n
import sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
def prime_power(n):
    d = next(d for d in range(2, n + 1) if n % d == 0)
    while n % d == 0:
        n //= d
    return n == 1
qs = [q for q in range(max(lo, 3), hi + 1) if q % 4 == 3 and prime_power(q)]
print("\n".join(map(str, sorted(qs, reverse=True))))
PY
