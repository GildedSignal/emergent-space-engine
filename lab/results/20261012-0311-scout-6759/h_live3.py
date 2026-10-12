#!/usr/bin/env python3
"""H_live repair test: is the per-kick delta field a FOURIER-smooth function
of the initial angles (action-angle structure), i.e. absorbable by a program
with harmonic content, or genuinely per-body?

Basis: Fourier harmonics |k|<=11 in M0 and w0 (complex -> real sin/cos pairs)
x Chebyshev deg 4 in a0 x deg 3 in e0. Cold belt, 2 orbits, shuffle control.
Usage: h_live3.py  -> prints JSON lines; writes h_live3.json
"""
import json
import time

import numpy as np

N = 16384
N_ORB = 2
KICKS_PER_ORB = 32
QUAD = 6
A_REF = 2.7
A_J, E_J, MJ = 5.2, 0.048, 9.54e-4
Q_A, Q_E = 6.6846e-8, 1e-7
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
    yo = a * np.sqrt(1 - e * e) * sE
    n = a**-1.5
    fac = a * n / (1 - e * cE)
    vxo = -fac * sE
    vyo = fac * np.sqrt(1 - e * e) * cE
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
    return a, e, w, E - e * np.sin(E)


nJ = A_J**-1.5
MJ_M0 = 1.1


def pert_acc(x, y, t):
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


a0 = rng.uniform(2.1, 3.3, N)
e0 = np.abs(rng.normal(0, 0.035, N)) + 0.005
w0 = rng.uniform(0, 2 * np.pi, N)
M0 = rng.uniform(0, 2 * np.pi, N)

# Fourier(11) x Fourier(11) x Cheb(4 in a) x Cheb(3 in e)
KF, KA, KE_ = 11, 4, 3
sa = np.clip((2 * a0 - 5.4) / 1.4, -1, 1)
se = np.clip((2 * e0 - 0.3) / 0.3, -1, 1)
Ta = np.polynomial.chebyshev.chebvander(sa, KA)
Te = np.polynomial.chebyshev.chebvander(se, KE_)
cols = []
for km in range(KF + 1):
    fm = np.cos(km * M0)
    sm = np.sin(km * M0) if km else None
    for kw in range(KF + 1):
        fw = np.cos(kw * w0)
        sw = np.sin(kw * w0) if kw else None
        ang = [fm * fw]
        if km:
            ang.append(sm * fw)
        if kw:
            ang.append(fm * sw)
            if km:
                ang.append(sm * sw)
        for A_ in ang:
            for ia in range(KA + 1):
                for ie in range(KE_ + 1):
                    cols.append(A_ * Ta[:, ia] * Te[:, ie])
BASIS = np.stack(cols, axis=1)
PINV = np.linalg.pinv(BASIS)


def fit_resid(vals):
    return vals - BASIS @ (PINV @ vals)


print("basis columns:", BASIS.shape[1])
raw_hist, res_hist = [], []
stock = np.zeros((4, N), dtype=np.int64)
stock_res = []
shuffle_check = None
t0 = time.time()
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
    raw_hist.append(sum(ent_bits(qq) for qq in q))
    re_ = [np.rint(fit_resid(d[i]) / Q[i]).astype(np.int64) for i in range(4)]
    res_hist.append(sum(ent_bits(r) for r in re_))
    if k == 16:
        rng2 = np.random.default_rng(4242)
        rawp = resp = 0.0
        for i in range(4):
            dp = rng2.permutation(d[i])
            rawp += ent_bits(np.rint(dp / Q[i]).astype(np.int64))
            resp += ent_bits(np.rint(fit_resid(dp) / Q[i]).astype(np.int64))
        shuffle_check = {"raw": rawp, "resid": resp, "absorbed": 1 - resp / rawp}
    for i in range(4):
        stock[i] += q[i]
    if k % KICKS_PER_ORB == 0:
        sr = [np.rint(fit_resid(stock[i].astype(float))).astype(np.int64)
              for i in range(4)]
        stock_res.append(sum(ent_bits(s) for s in sr))
    a, e, w, M = an, en, wn, Mn

out = {
    "raw_bits_per_kick_med": float(np.median(raw_hist)),
    "resid_bits_per_kick_med": float(np.median(res_hist)),
    "absorbed": 1 - np.median(res_hist) / np.median(raw_hist),
    "shuffle_control": shuffle_check,
    "stock_resid_bits": stock_res,
    "wall_s": round(time.time() - t0, 2),
}
with open("h_live3.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
