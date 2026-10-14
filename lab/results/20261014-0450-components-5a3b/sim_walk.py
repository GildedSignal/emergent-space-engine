#!/usr/bin/env python3
"""Simulate OrbitShape::bound's ladder in float and match the dumped knot psis (p=8, e=0.1)."""
import math

# EDGE table (Q62) from tables.rs
EDGE = [4611686018427387904, 4416165660797809419, 4228934724888366668, 4049641766413219908,
        3877950241171266237, 3713537873331429433, 3556096050500581047, 3405329244438597040,
        3260954456333195553, 3122700685593301682, 2990308421163830843, 2863529154407056491,
        2742124912636209756, 2625867812425724110, 2514539631859660218, 2407931400915394245,
        2305843009213693952]
PI = math.pi
CAP = PI / 4

p, e = 8.0, 0.1
k = 1.0 / (1.0 + e)
q = 1.0 / p
eta = 1.0 - k
ONE = 1.0

def cut(x):
    # acos((x-k)/(1-k)) via the shipped half-angle; float equivalent here.
    return math.acos((x - k) / (1.0 - k))

def simulate(cut_mode):
    xa = 2 * k - 1
    knots = [0.0]
    band = 1
    delta = ONE - q * (6 * k + 2 * eta)
    qa = q * eta
    while True:
        edge = (EDGE[band % 16] / 2**62) / 2 ** (band // 16)
        if edge <= xa:
            break
        end = cut(edge)
        start = knots[-1]
        if cut_mode == "sqrt_over_4":
            c = math.sqrt(delta / qa) / 4 if qa > 0 and delta < 64 * qa else PI
        elif cut_mode == "sqrt_over_64":
            c = math.sqrt(delta / qa) / 64 if qa > 0 and delta < 64 * qa else PI
        elif cut_mode == "sqrt_2delta_over_4":
            c = math.sqrt(2 * delta / qa) / 4 if qa > 0 and delta < 64 * qa else PI
        elif cut_mode == "fourth_root":
            c = (delta / qa) ** 0.25 / 4 if qa > 0 and delta < 64 * qa else PI
        while c <= start:
            c *= 2
        lo = start
        while lo < end:
            hi = min(end, c)
            n = math.ceil((hi - lo) / CAP)
            for i in range(n):
                a = lo + (hi - lo) * i / n
                b = lo + (hi - lo) * (i + 1) / n
                knots.append(b)
            lo = hi
            c *= 2
        band += 1
    # final append(PI)
    start = knots[-1]
    c = math.sqrt(delta / qa) / 4 if qa > 0 and delta < 64 * qa else PI
    if cut_mode == "sqrt_over_64":
        c = math.sqrt(delta / qa) / 64 if qa > 0 and delta < 64 * qa else PI
    while c <= start:
        c *= 2
    lo = start
    while lo < PI:
        hi = min(PI, c)
        n = math.ceil((hi - lo) / CAP)
        for i in range(n):
            b = lo + (hi - lo) * (i + 1) / n
            knots.append(b)
        lo = hi
        c *= 2
    return knots

dumped = [0.0, 0.503951, 1.007902, 1.060660, 1.483642, 1.918365, 2.121320, 2.419069, 3.141593]
for mode in ["sqrt_over_4", "sqrt_over_64", "sqrt_2delta_over_4", "fourth_root"]:
    sim = simulate(mode)
    print(f"{mode}: n={len(sim)}")
    print("  sim:", " ".join(f"{x:.4f}" for x in sim))
print("dump:", " ".join(f"{x:.4f}" for x in dumped))
