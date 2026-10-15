#!/usr/bin/env python3
"""The dimensionless restatement: parse the census lines of the arms and report, per population,
the fired impulse's size |dv|/|v| as log2 buckets (bucket b is 2^(b-48) of the body's speed),
the word-unit dv buckets, and the fire rates. Then the derived arithmetic for the dossier:
grid kicks per orbit and the impulse at the behaviour floor, dimensionless and in word units.

Usage: dim.py <n1e4_coast_base.txt> [more arms]
"""
import re
import sys

NAMES = ["planet/child", "planet/root", "moon/child", "moon/root", "ship/child", "ship/root", "player/child", "player/root"]

PAT = re.compile(
    r"(\S+) kicks=(\d+) fired=(\d+) fire_rate=(\S+) dv_log2=\[([^\]]*)\] dim_log2=\[([^\]]*)\]"
)


def buckets(vec):
    return [int(x) for x in vec.split(",")]


def spread(bs, lo=None):
    """(median, p01, p99, n) of the bucketed distribution, as exponents of 2 (bucket b = 2^(b-48))."""
    tot = sum(bs)
    if tot == 0:
        return None
    def at(p):
        acc, target = 0, round(tot * p)
        for b, c in enumerate(bs):
            acc += c
            if acc >= target:
                return b - 48
        return len(bs) - 1 - 48
    lo = next((b for b, c in enumerate(bs) if c), len(bs) - 1)
    hi = next((b for b in range(len(bs) - 1, -1, -1) if bs[b]), 0)
    return at(0.5), at(0.01), at(0.99), lo - 48, hi - 48, tot


for path in sys.argv[1:]:
    print(path.split("/")[-1])
    for line in open(path):
        if not line.startswith("census:"):
            continue
        for m in PAT.finditer(line):
            name, k, f, rate, dv, dim = m.groups()
            dv, dim = buckets(dv), buckets(dim)
            sp = spread(dim)
            if sp is None:
                continue
            med, p01, p99, lo, hi, n = sp
            dv_hi = max(b for b, c in enumerate(dv) if c)
            print(
                "  %-13s kicks=%s fired=%s rate=%s dv>=2^%d |dv|/|v|: median 2^%d, p01 2^%d, p99 2^%d, range 2^%d..2^%d (n=%d)"
                % (name, k, f, rate, dv_hi, med, p01, p99, lo, hi, n)
            )

# The derived arithmetic, printed once (constants measured elsewhere in the record):
I = 28141.5      # s, the belt's median fire interval (this run's baseline arm regenerates it)
P_ORBIT = 1.246e8  # s, a 2.5 AU orbit (the belt's midpoint; scenario: 2-3 AU)
grid_per_orbit = P_ORBIT / I
print("derived: grid kicks/orbit = %.0f (I=%.1f s, P=%.3e s)" % (grid_per_orbit, I, P_ORBIT))
for floor in (2, 8):
    coarsen = grid_per_orbit / floor
    print(
        "  at the behaviour floor (%d kicks/orbit): %.0fx coarser; a floor kick carries ~2^%.1f word units if dv grows with ds (measured >= 2^7 at the grid)"
        % (floor, coarsen, 7 + __import__("math").log2(coarsen))
    )
