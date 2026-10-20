#!/usr/bin/env python3
"""Cross-arm analysis for the belt cadence floor: per-body final (a,e) vs the S=7 arm,
each arm's own drift vs birth, the one-orbit arm's boundedness, and the composed ledger row."""

def load(p):
    d = {}
    for line in open(p):
        i, a0, e0, a1, e1 = line.split()
        d[int(i)] = (float(a0), float(e0), float(a1), float(e1))
    return d

def q(v, p):
    v = sorted(v)
    return v[int((len(v) - 1) * p)]

ref = load("data/belt_floor_s7_seed1.txt")
print("cross-arm vs S=7 (seed 1, 267k game-s):")
print(f"{'arm':>4} {'|da|/a p50':>12} {'p99':>12} {'max':>12} {'|de| p50':>12} {'p99':>12} {'own drift da/a p99':>20}")
for S in (7, 5, 3, 1):
    arm = load(f"data/belt_floor_s{S}_seed1.txt")
    da = [abs(arm[i][2] - ref[i][2]) / ref[i][2] for i in ref if i in arm]
    de = [abs(arm[i][3] - ref[i][3]) for i in ref if i in arm]
    own = [abs(arm[i][2] - arm[i][0]) / arm[i][0] for i in arm]
    print(f"S={S:<2} {q(da,.5):12.3e} {q(da,.99):12.3e} {max(da):12.3e} {q(de,.5):12.3e} {q(de,.99):12.3e} {q(own,.99):20.3e}")

long = load("data/belt_floor_s1long_seed1.txt")
la = [abs(long[i][2] - ref[i][0]) / ref[i][0] for i in long]
print(f"\none full belt orbit (1.26e8 game-s) at S=1, drift vs birth: |da|/a p50 {q(la,.5):.3e} p99 {q(la,.99):.3e} max {max(la):.3e}")
lr = [abs(long[i][3] - ref[i][1]) for i in long]
print(f"one orbit |de| p99 {q(lr,.99):.3e} max {max(lr):.3e}")

# The composed CPU row of the 10^9 ledger (budget-1e9 3aec's constants), at each floor.
print("\ncomposed belt-stream cores at 10^9, rtf 100 (3aec's anchors, x86 orders):")
for name, cut, cost in [("shipped S=7", 1, 82.5), ("split8 S=5", 4.92, 82.5), ("this run S=1", 66.8, 82.5), ("checker belt item S=1", 66.8, 44.7)]:
    print(f"  {name:<22} 193/{cut:.0f} at {cost:.1f} us -> {193 / cut * cost / 82.5:5.1f} cores")
print("  stream ratio S=7/S=1 measured here: 499095/7471 = %.1f" % (499095 / 7471))
