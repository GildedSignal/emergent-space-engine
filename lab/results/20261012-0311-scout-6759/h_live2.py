#!/usr/bin/env python3
"""H_live falsifier v2: how much of a kicked belt's state growth is shared
(absorbable into one program deformation) versus per-body (scars)?

Model: analytic two-body program (GM=1, AU, time yr/2pi); kick layer =
perturber impulse per cadence interval (32/orbit, H0190), 6-pt Gauss-Legendre
along the program arc (Encke: only the deviation is computed). Planar.

Shared structure test: the per-kick delta field and the cumulative scar field
are projected on Chebyshev tensor products in the scaled INITIAL elements
(a, e, omega, M), degree 3 each (256 columns) — the basis a recompiled
program could represent. Residual integer entropy = per-body floor.

Usage: h_live2.py <name> <mode>   mode in {control, cold, resonant}
Writes h_live2-<name>.json
"""
import json
import sys
import time

import numpy as np

N = 16384
N_ORB = 8
KICKS_PER_ORB = 32
QUAD = 6
A_REF = 2.7
MJ = {"control": 0.0, "cold": 9.54e-4, "resonant": 9.54e-4}[sys.argv[2]]
A_J, E_J = 5.2, 0.048

Q_A = 6.6846e-8            # 1 km in AU
Q_E = 1e-7
Q_ANG = 2 * np.pi / 2**24
Q = (Q_A, Q_E, Q_ANG, Q_ANG)

DT = 2 * np.pi * A_REF**1.5 / KICKS_PER_ORB
N_EPOCH = N_ORB * KICKS_PER_ORB
GX, GW = np.polynomial.legendre.leggauss(QUAD)
GX = 0.5 * DT * (GX + 1.0)
GW = 0.5 * DT * GW

rng = np.random.default_rng(6759)


def kepler_E(M, e, iters=6):
    E = M + e * np.sin(M)
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def state_vec(a, e, w, M):
    E = kepler_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    xo = a * (cE - e)
    yo = a * np.sqrt(1.0 - e * e) * sE
    n = a**-1.5
    fac = a * n / (1.0 - e * cE)
    vxo = -fac * sE
    vyo = fac * np.sqrt(1.0 - e * e) * cE
    cw, sw = np.cos(w), np.sin(w)
    return (xo * cw - yo * sw, xo * sw + yo * cw,
            vxo * cw - vyo * sw, vxo * sw + vyo * cw)


def elements(x, y, vx, vy):
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


nJ = A_J**-1.5
MJ_M0 = 1.1


def pert_acc(x, y, t):
    if MJ == 0.0:
        return 0.0, 0.0
    MM = np.mod(nJ * t + MJ_M0, 2 * np.pi)
    EJ = kepler_E(MM, E_J)
    xJ = A_J * (np.cos(EJ) - E_J)
    yJ = A_J * np.sqrt(1 - E_J**2) * np.sin(EJ)
    dx, dy = x - xJ, y - yJ
    d3 = (dx * dx + dy * dy) ** -1.5
    return -MJ * dx * d3, -MJ * dy * d3


def ent_bits(n):
    c = np.bincount(n - n.min())
    p = c[c > 0] / n.size
    return float(-(p * np.log2(p)).sum())


def cheb_scaled(x, lo, hi, deg):
    s = np.clip((2.0 * x - lo - hi) / (hi - lo), -1, 1)
    return np.polynomial.chebyshev.chebvander(s, deg)


if sys.argv[2] == "resonant":
    a0 = 2.50 + rng.uniform(-0.004, 0.004, N)
else:
    a0 = rng.uniform(2.1, 3.3, N)
e0 = np.abs(rng.normal(0, 0.035, N)) + 0.005
w0 = rng.uniform(0, 2 * np.pi, N)
M0 = rng.uniform(0, 2 * np.pi, N)

# tensor basis over initial (a, e, omega, M), degree 3 each
DEG = 3
Ta = cheb_scaled(a0, 2.0, 3.4, DEG)
Te = cheb_scaled(e0, 0.0, 0.30, DEG)
Tw = cheb_scaled(np.mod(w0, 2 * np.pi), 0.0, 2 * np.pi, DEG)
Tm = cheb_scaled(M0, 0.0, 2 * np.pi, DEG)
COLS = (DEG + 1) ** 4
BASIS = np.empty((N, COLS))
for ia in range(DEG + 1):
    for ie in range(DEG + 1):
        for iw in range(DEG + 1):
            for im in range(DEG + 1):
                BASIS[:, ((ia * 4 + ie) * 4 + iw) * 4 + im] = (
                    Ta[:, ia] * Te[:, ie] * Tw[:, iw] * Tm[:, im])
PINV = np.linalg.pinv(BASIS)


def fit_resid(vals):
    return vals - BASIS @ (PINV @ vals)


raw_hist, res_hist = [], []
stock = np.zeros((4, N), dtype=np.int64)
stock_res, stock_raw, scar_word_bits = [], [], []
shuffle_check = None
t_start = time.time()
a, e, w, M = a0.copy(), e0.copy(), w0.copy(), M0.copy()
for k in range(1, N_EPOCH + 1):
    n = a**-1.5
    Jx = np.zeros(N)
    Jy = np.zeros(N)
    for g in range(QUAD):
        x, y, _, _ = state_vec(a, e, w, M + n * GX[g])
        ax, ay = pert_acc(x, y, GX[g])
        Jx += GW[g] * ax
        Jy += GW[g] * ay
    x, y, vx, vy = state_vec(a, e, w, M + n * DT)
    an, en, wn, Mn = elements(x, y, vx + Jx, vy + Jy)
    dM = np.mod(Mn - (M + n * DT) + np.pi, 2 * np.pi) - np.pi
    d = (an - a, en - e,
         np.mod(wn - w + np.pi, 2 * np.pi) - np.pi, dM)
    q = [np.rint(d[i] / Q[i]).astype(np.int64) for i in range(4)]
    for i in range(4):
        j = int(np.argmax(q[i]))
        if abs(q[i][j]) > 10**9 or q[i][j] < -10**10:
            print(f"TRIP ep{k} elem{i} body{j} q={q[i][j]}", file=sys.stderr)
            sys.exit(9)
    raw_hist.append(sum(ent_bits(qq) for qq in q))
    re_ = [np.rint(fit_resid(d[i]).astype(float) / Q[i]).astype(np.int64)
           for i in range(4)]
    res_hist.append(sum(ent_bits(r) for r in re_))
    if k == 16 and MJ > 0:  # shuffle control on the same field
        rng2 = np.random.default_rng(4242)
        rawp = resp = 0.0
        for i in range(4):
            dp = rng2.permutation(d[i])
            rawp += ent_bits(np.rint(dp / Q[i]).astype(np.int64))
            rp = np.rint(fit_resid(dp) / Q[i]).astype(np.int64)
            resp += ent_bits(rp)
        shuffle_check = {"raw": rawp, "resid": resp,
                         "absorbed": 1 - resp / rawp}
    for i in range(4):
        stock[i] += q[i]
    if k % KICKS_PER_ORB == 0:
        sr = [np.rint(fit_resid(stock[i].astype(float))).astype(np.int64)
              for i in range(4)]
        stock_res.append(sum(ent_bits(s) for s in sr))
        stock_raw.append(sum(ent_bits(stock[i]) for i in range(4)))
        med = [np.median(np.abs(stock[i])) for i in range(4)]
        scar_word_bits.append(sum(np.log2(1.0 + 2.0 * m) for m in med))
    a, e, w, M = an, en, wn, Mn

el = time.time() - t_start
out = {
    "name": sys.argv[1], "mode": sys.argv[2], "N": N, "orbits": N_ORB,
    "kicks_per_orbit": KICKS_PER_ORB, "basis_cols": COLS,
    "quanta": [Q_A, Q_E, Q_ANG, Q_ANG], "wall_s": round(el, 2),
    "raw_bits_per_kick_med": float(np.median(raw_hist)),
    "resid_bits_per_kick_med": float(np.median(res_hist)),
    "absorbed": 1 - np.median(res_hist) / np.median(raw_hist),
    "shuffle_control": shuffle_check,
    "stock_raw_bits": stock_raw,
    "stock_resid_bits": stock_res,
    "scar_word_bits_median": scar_word_bits,
}
with open(f"h_live2-{sys.argv[1]}.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k2: out[k2] for k2 in list(out)[:9]}, indent=1))
print("stock_raw:", [round(s, 2) for s in stock_raw])
print("stock_resid:", [round(s, 2) for s in stock_res])
print("scar_word_bits:", [round(s, 2) for s in scar_word_bits])
print(f"wall {el:.1f}s")
