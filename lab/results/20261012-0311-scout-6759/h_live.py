#!/usr/bin/env python3
"""H_live falsifier: bits of unshared, per-body distinguishing information
created per kick by a perturbed belt, against the 4 GiB / 10^9-body budget.

Model: analytic two-body program (GM=1, AU, time yr/2pi); kick layer =
perturber impulse over each cadence interval, 6-pt Gauss-Legendre quadrature
along the program arc (Encke: only the deviation is computed). Planar.
Quantized integer deltas on belt-scale quanta; entropies are integer counts.

Usage: h_live.py <name> <mode>   mode in {control, cold, resonant}
  control  : cold belt, perturber mass 0  (instrument floor, must be exactly 0)
  cold     : a in [2.1, 3.3] AU
  resonant : a in 2.50 +/- 0.004 AU (3:1)
Writes h_live-<name>.json
"""
import json
import sys
import time

import numpy as np

GM = 1.0
N = 16384
N_ORB = 8                  # orbits at reference radius
KICKS_PER_ORB = 32         # H0190 cadence
QUAD = 6                   # Gauss-Legendre points per interval
A_REF = 2.7                # AU
MJ = {                     # perturber
    "control": 0.0,
    "cold": 9.54e-4,
    "resonant": 9.54e-4,
}[sys.argv[2]]
A_J, E_J = 5.2, 0.048

# quanta (belt scale; all deltas live well inside 32-bit words)
Q_A = 6.6846e-8            # 1 km in AU
Q_E = 1e-7
Q_ANG = 2 * np.pi / 2**24

DT = 2 * np.pi * A_REF**1.5 / KICKS_PER_ORB
N_EPOCH = N_ORB * KICKS_PER_ORB
# Gauss-Legendre nodes on [0, DT]
GX, GW = np.polynomial.legendre.leggauss(QUAD)
GX = 0.5 * DT * (GX + 1.0)
GW = 0.5 * DT * GW

rng = np.random.default_rng(6759)


def kepler_E(M, e, iters=6):
    """Eccentric anomaly from mean anomaly (vectorized Newton)."""
    E = M + e * np.sin(M)
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def state_vec(a, e, w, M):
    """(x, y, vx, vy) from planar elements."""
    E = kepler_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    b = a * np.sqrt(1.0 - e * e)
    xo = a * (cE - e)
    yo = b * sE
    n = a**-1.5
    fac = a * n / (1.0 - e * cE)
    vxo = -fac * sE
    vyo = fac * np.sqrt(1.0 - e * e) * cE
    cw, sw = np.cos(w), np.sin(w)
    return (xo * cw - yo * sw, xo * sw + yo * cw,
            vxo * cw - vyo * sw, vxo * sw + vyo * cw)


def elements(x, y, vx, vy):
    """Planar osculating (a, e, omega, M) from a state vector."""
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    f = np.arctan2(y, x) - w
    E = 2.0 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2),
                         np.sqrt(1 + e) * np.cos(f / 2))
    M = E - e * np.sin(E)
    return a, e, w, M


def pert_acc(x, y, t):
    """Perturber acceleration at body positions (x, y) at times t (scalar)."""
    if MJ == 0.0:
        return 0.0, 0.0
    MJ_M = np.mod(nJ * t + MJ_M0, 2 * np.pi)
    EJ = kepler_E(MJ_M, E_J)
    xJ = A_J * (np.cos(EJ) - E_J)
    yJ = A_J * np.sqrt(1 - E_J**2) * np.sin(EJ)   # focal frame, peri at +x
    dx, dy = x - xJ, y - yJ
    d3 = (dx * dx + dy * dy) ** -1.5
    return -MJ * dx * d3, -MJ * dy * d3


def ent_bits(n):
    """Zero-order entropy (bits) of an integer array."""
    if n.size == 0:
        return 0.0
    c = np.bincount(n - n.min())
    p = c[c > 0] / n.size
    return float(-(p * np.log2(p)).sum())


def fit_resid(vals, basis_pinv, basis):
    """Residual after least-squares projection on the shared basis."""
    coef = basis_pinv @ vals
    return vals - basis @ coef


nJ = A_J**-1.5
MJ_M0 = 1.1  # arbitrary fixed phase (same for every belt)

# --- belt setup ------------------------------------------------------------
if sys.argv[2] == "resonant":
    a0 = 2.50 + rng.uniform(-0.004, 0.004, N)
else:
    a0 = rng.uniform(2.1, 3.3, N)
e0 = np.abs(rng.normal(0, 0.035, N)) + 0.005
w0 = rng.uniform(0, 2 * np.pi, N)
M0 = rng.uniform(0, 2 * np.pi, N)

# shared-basis: Chebyshev in scaled a (deg 10) and scaled e (deg 4);
# well-conditioned (cond ~ 1e2), so the projection is stable at quanta scale
def cheb_basis(x, deg, lo, hi):
    s = (2.0 * x - lo - hi) / (hi - lo)
    return np.polynomial.chebyshev.chebvander(np.clip(s, -1, 1), deg)


def solve_basis(B):
    return B, np.linalg.pinv(B)


E_LO, E_HI = 0.0, 0.30
BASIS_A, PINV_A = solve_basis(cheb_basis(a0, 10, 2.0, 3.4))
_Be = cheb_basis(e0, 4, E_LO, E_HI)
BASIS_AE, PINV_AE = solve_basis(np.hstack([BASIS_A, _Be[:, 1:]]))

Q = (Q_A, Q_E, Q_ANG, Q_ANG)  # quanta per element
raw_hist, res_a_hist, res_ae_hist = [], [], []
stock = np.zeros((4, N), dtype=np.int64)
stock_res = []

t_start = time.time()
a, e, w, M = a0.copy(), e0.copy(), w0.copy(), M0.copy()
for k in range(1, N_EPOCH + 1):
    n = a**-1.5
    # impulse along the program arc over [0, DT]
    Jx = np.zeros(N)
    Jy = np.zeros(N)
    for g in range(QUAD):
        Mg = M + n * GX[g]
        x, y, _, _ = state_vec(a, e, w, Mg)
        ax, ay = pert_acc(x, y, GX[g])
        Jx += GW[g] * ax
        Jy += GW[g] * ay
    # end-of-interval state, kicked
    x, y, vx, vy = state_vec(a, e, w, M + n * DT)
    an, en, wn, Mn = elements(x, y, vx + Jx, vy + Jy)
    dM = np.mod(Mn - (M + n * DT) + np.pi, 2 * np.pi) - np.pi
    d = (an - a, en - e, np.mod(wn - w + np.pi, 2 * np.pi) - np.pi, dM)
    q = [np.rint(d[i] / Q[i]).astype(np.int64) for i in range(4)]
    for i in range(4):
        j = int(np.argmax(q[i]))
        if abs(q[i][j]) > 10**9 or q[i][j] < -10**10:
            print(f"TRIP ep{k} elem{i} body{j} q={q[i][j]} d={d[i][j]} "
                  f"a={a[j]} e={e[j]} an={an[j]} en={en[j]} M={M[j]} Mn={Mn[j]}"
                  f" wn={wn[j]} w={w[j]} nDT={n[j]*DT} J={Jx[j]},{Jy[j]}")
            sys.exit(9)
    raw_hist.append(sum(ent_bits(qq) for qq in q))
    ra = [np.rint(fit_resid(d[i].astype(float), PINV_A, BASIS_A) / Q[i]
                  ).astype(np.int64) for i in range(4)]
    res_a_hist.append(sum(ent_bits(r) for r in ra))
    re = [np.rint(fit_resid(d[i].astype(float), PINV_AE, BASIS_AE) / Q[i]
                  ).astype(np.int64) for i in range(4)]
    res_ae_hist.append(sum(ent_bits(r) for r in re))
    for i in range(4):
        stock[i] += q[i]
    if k % KICKS_PER_ORB == 0:
        sr = [np.rint(fit_resid(stock[i].astype(float), PINV_AE, BASIS_AE)
                      ).astype(np.int64) for i in range(4)]
        stock_res.append(sum(ent_bits(s) for s in sr))
    a, e, w, M = an, en, wn, Mn

el = time.time() - t_start
out = {
    "name": sys.argv[1], "mode": sys.argv[2], "N": N, "orbits": N_ORB,
    "kicks_per_orbit": KICKS_PER_ORB, "quanta": [Q_A, Q_E, Q_ANG, Q_ANG],
    "wall_s": round(el, 2),
    "raw_bits_per_kick_med": float(np.median(raw_hist)),
    "resid_a_bits_per_kick_med": float(np.median(res_a_hist)),
    "resid_ae_bits_per_kick_med": float(np.median(res_ae_hist)),
    "absorbed_a": 1 - np.median(res_a_hist) / np.median(raw_hist),
    "absorbed_ae": 1 - np.median(res_ae_hist) / np.median(raw_hist),
    "raw_bits_per_kick_epochs": raw_hist,
    "resid_ae_bits_per_kick_epochs": res_ae_hist,
    "stock_resid_bits_per_orbit": stock_res,
}
with open(f"h_live-{sys.argv[1]}.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({kk: out[kk] for kk in list(out)[:10]}, indent=1))
print("stock_resid_bits_per_orbit:", [round(s, 2) for s in stock_res])
print(f"wall {el:.1f}s")
