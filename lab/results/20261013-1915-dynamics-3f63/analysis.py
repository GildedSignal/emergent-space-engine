#!/usr/bin/env python3
"""The crash basin's ruler: analysis of the r-sweep (run 20261013-1915-dynamics-3f63).

Inputs (typed from the run logs, each a bisection bracket in Home radii):
  r*(L): the smallest circular-start radius from which the held retro brake at level L lives.
Constants from the shipped code: Home's doll is its own geometric units (M = c = 1), surface at
4313*2^18 doll units; the burn's proper acceleration in doll units is 2^(L-62), so
Lambda(r, L) = a/g_local = 2^(L-62) * r_doll^2  (checks: Lambda(1.099R, L5) = 10.70 = the page's).
"""
import math

R_DOLL = 4313 * 2**18  # Home's surface, doll units


def lam(radii: float, level: int) -> float:
    r = radii * R_DOLL
    return 2.0 ** (level - 62) * r * r


def kappa(radii: float, level: int) -> float:
    return lam(radii, level) * math.sqrt(radii**2 - 1.0)


# Measured bisection brackets (lo, hi) in Home radii, from the sweep log.
SWEEP = {
    0: (2.8235, 2.8446),
    1: (2.1071, 2.1185),
    2: (1.6186, 1.6285),
    3: (1.2993, 1.3093),
    4: (1.1197, 1.1297),
    5: (1.0378, 1.0434),
    6: (1.0100, 1.0156),
}
# Held-out arms (radius, level, outcome), flown after the predictions were written.
HELDOUT = [(2.30, 0, False), (2.50, 0, False), (1.55, 2, False), (1.70, 2, True)]

print(f"{'L':>2} {'r* mid (R)':>11} {'Lambda* (bracket)':>24} {'kappa (bracket)':>24} {'margin r*-1':>11}")
rows = []
for L, (lo, hi) in sorted(SWEEP.items()):
    mid = 0.5 * (lo + hi)
    klo, khi = kappa(lo, L), kappa(hi, L)
    rows.append((L, mid, klo, khi))
    print(f"{L:>2} {mid:>11.4f} ({lam(lo, L):>9.3f},{lam(hi, L):>9.3f})   ({klo:>9.3f},{khi:>9.3f})   {mid-1:>11.4f}")

# Lambda's total variation across the sweep: is Lambda = a/g_local the ruler?
lams = [lam(0.5 * (lo + hi), L) for L, (lo, hi) in SWEEP.items()]
print(f"\nLambda* across the sweep: {lams[0]:.2f} -> {lams[-1]:.2f}  (x{lams[-1]/lams[0]:.1f} over r {rows[-1][1]:.3f}->{rows[0][1]:.3f} R)")

# The tangent collapse kappa(r): plateau where the boundary is near the surface (r* < 1.13R).
plateau = [(L, m, klo, khi) for (L, m, klo, khi) in rows if m < 1.13]
pm = [0.5 * (klo + khi) for _, _, klo, khi in plateau]
print(f"plateau (r* < 1.13R, levels {[p[0] for p in plateau]}): kappa = {sum(pm)/len(pm):.3f} +- {0.5*(max(pm)-min(pm)):.3f} (midpoints), bracket half-widths <= {max(khi-klo for _,_,klo,khi in plateau)/2:.2f}")

# The drift: d ln kappa / d ln r over the whole sweep (consecutive-level slopes).
import statistics
slopes = []
for (L1, m1, _, _), (L2, m2, _, _) in zip(rows, rows[1:]):
    k1, k2 = kappa(m1, L1), kappa(m2, L2)
    slopes.append(math.log(k2 / k1) / math.log(m2 / m1))
print(f"d ln kappa / d ln r, consecutive: {[f'{s:+.2f}' for s in slopes]}; the L5->L6 pair is bracket-dominated (its bracket is 12% wide), median of the five clean {statistics.median(slopes[:5]):+.2f}")

# The margin parametrization: kappa = k0 + s*(r/R - 1), fitted on all midpoints.
xs = [m - 1 for _, m, _, _ in rows]
ys = [kappa(m, L) for (L, m, _, _) in rows]
n = len(xs)
sx, sy = sum(xs), sum(ys)
sxx = sum(x * x for x in xs)
sxy = sum(x * y for x, y in zip(xs, ys))
s = (n * sxy - sx * sy) / (n * sxx - sx * sx)
k0 = (sy - s * sx) / n
res = [y - (k0 + s * x) for x, y in zip(xs, ys)]
print(f"margin fit: kappa ~ {k0:.2f} + {s:.2f}*(r/R - 1); residual rms {math.sqrt(sum(r*r for r in res)/n):.3f}")

# Cross-checks against the page's published brackets (tracking nose, raised apoapsis; 8574).
print("\npage cross-checks (their brackets, my curve):")
for radii, blo, bhi in [(1.445, 1.16, 9.26), (1.665, 1.54, 3.07), (2.228, 1.38, 2.75)]:
    mine = k0 + s * (radii - 1)
    t = math.sqrt(radii**2 - 1)
    print(f"  r={radii}R: their Lambda* in ({blo},{bhi}) -> kappa in ({blo*t:.2f},{bhi*t:.2f}); my kappa {mine:.2f} -> Lambda* {mine/t:.2f}")

# The D row at 1.099R (fixed nose, this run's anchors): crash L<=4, live L>=5.
k_d = kappa(1.099, 4), kappa(1.099, 5)
print(f"\nD-row consistency: kappa(1.099R) must lie between kappa(L4)={k_d[0]:.2f} (crashes) and kappa(L5)={k_d[1]:.2f} (lives)")
print(f"  my curve at 1.099R: {k0 + s * 0.099:.2f}; plateau {sum(pm)/len(pm):.2f}")

# Held-out verdicts against (a) the pre-registered constant kappa=3.5, (b) the fitted curve.
print("\nheld-out arms:")
for radii, L, seen in HELDOUT:
    reg = lam(radii, L) > 3.5 / math.sqrt(radii**2 - 1)
    fit = lam(radii, L) > (k0 + s * (radii - 1)) / math.sqrt(radii**2 - 1)
    print(f"  ({radii}R, L{L}): seen {'ALIVE' if seen else 'DEAD':>5} | registered(kappa=3.5) {'LIVE' if reg else 'DEAD':>4} {'OK' if reg == seen else 'MISS'} | fitted curve {'LIVE' if fit else 'DEAD':>4} {'OK' if fit == seen else 'MISS'}")
