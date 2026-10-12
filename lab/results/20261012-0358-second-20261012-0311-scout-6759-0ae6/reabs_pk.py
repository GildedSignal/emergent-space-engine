#!/usr/bin/env python3
"""Per-kick oracle fit: reproduce the checker's probe instrument.

For kicks in orbits 1 and 8, fit EACH kick's true delta field (across
bodies) on phi_F anchored at the TRUE phase at kick start — exactly the
checker's per-kick energy-absorption instrument (their 0.87/0.70/0.50/
0.50). Then accumulate the per-kick oracle residuals (each kick fitted
separately — a different program per kick, the strongest possible and
NOT time-invariant) and report the residual stock trajectory: the
candidate source of the checker's quoted 61.2 bits at orbit 8.
Usage: python3 reabs_pk.py  (~90 s)
"""
import json
import time

import numpy as np

import reabs as R

N = R.N
KP = R.KICKS_PER_ORB
N_EPOCH = 16 * KP


def main():
    rng = np.random.default_rng(6759)
    a0, e0, w0, M0 = R.belt_init(rng)
    a, e, w, M = a0.copy(), e0.copy(), w0.copy(), M0.copy()
    wu, Mu = w0.copy(), M0.copy()
    # oracle residual stock (integers, per-kick quantized)
    stock = np.zeros((4, N), dtype=np.int64)
    abs_o1, abs_o8 = [], []
    stock_w = []
    t0 = time.time()
    for k in range(1, N_EPOCH + 1):
        t_prev = (k - 1) * R.DT
        n = a**-1.5
        Jx = np.zeros(N)
        Jy = np.zeros(N)
        for g in range(R.QUAD):
            x, y, _, _ = R.state_vec(a, e, w, M + n * R.GX[g])
            ax, ay = R.pert_acc(x, y, R.GX[g])
            Jx += R.GW[g] * ax
            Jy += R.GW[g] * ay
        x, y, vx, vy = R.state_vec(a, e, w, M + n * R.DT)
        an, en, wn, Mn = R.elements(x, y, vx + Jx, vy + Jy)
        dM = np.mod(Mn - (M + n * R.DT) + np.pi, 2 * np.pi) - np.pi
        d = (an - a, en - e,
             np.mod(wn - w + np.pi, 2 * np.pi) - np.pi, dM)
        orb = (k - 1) // KP + 1
        if orb in (1, 8):
            # TRUE phase at kick start (state before the kick)
            u = np.mod(M + w - (R.nJ * t_prev + R.MJ_M0), 2 * np.pi)
            Phi = R.phi_F(u, e, w)
            ab, res = [], []
            for i in range(4):
                c = np.linalg.lstsq(Phi, d[i], rcond=None)[0]
                r = d[i] - Phi @ c
                ab.append(float(1 - np.var(r) / np.var(d[i])))
                res.append(r)
            (abs_o1 if orb == 1 else abs_o8).append(ab)
            for i in range(4):
                stock[i] += np.rint(res[i] / R.Q[i]).astype(np.int64)
        else:
            for i in range(4):
                stock[i] += np.rint(d[i] / R.Q[i]).astype(np.int64)
        wu = wu + d[2]
        Mu = Mu + n * R.DT + dM
        a, e, w, M = an, en, wn, Mn
        if k % KP == 0:
            med = [np.median(np.abs(stock[i])) for i in range(4)]
            stock_w.append(float(sum(np.log2(1.0 + 2.0 * m)
                                     for m in med)))
    out = {
        "note": "per-kick oracle fits only in orbits 1 and 8; other "
                "orbits accumulate raw quantized kicks (stock growth "
                "between checkpoints follows the raw law)",
        "wall_s": round(time.time() - t0, 1),
        "per_kick_absorption_orbit1_median":
            [round(float(np.median(np.array(abs_o1)[:, i])), 4)
             for i in range(4)],
        "per_kick_absorption_orbit8_median":
            [round(float(np.median(np.array(abs_o8)[:, i])), 4)
             for i in range(4)],
        "checker_reference": [0.87, 0.70, 0.50, 0.50],
        "oracle_residual_stock_w_at_checkpoints":
            [round(v, 3) for v in stock_w],
    }
    with open("reabs_pk.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
