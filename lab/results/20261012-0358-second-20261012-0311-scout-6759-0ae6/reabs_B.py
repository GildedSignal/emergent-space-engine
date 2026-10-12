#!/usr/bin/env python3
"""Variant B: the PREDICTIVE program (strongest store semantics).

The program integrates its own state (starting from the generator's
elements) and, at every kick, subtracts its PREDICTED kick — a
time-invariant field D(lam-lamJ, e, w) fitted on the observed
(phase -> kick) pairs from the last orbit — from the true kick. The
store carries only S = rint((el_true - el_program)/Q). This is stronger
than orbit-scale refits of the total deviation (reabs.py): it is the
semantics under which a per-kick energy absorption of ~87/70/50/50%
(the checker's probe numbers) translates into a residual stock, and it
tests whether the checker's quoted 61.2 bits at orbit 8 is this
accounting. Refits of D every orbit on a rolling 32-kick window (the
field is synodic-frame invariant to first order; Jupiter's anomaly
cycles, so recent pairs only).

Usage: python3 reabs_B.py   (~3 min, writes reabs_B.json)
"""
import json
import time

import numpy as np

import reabs as R

N = R.N
N_ORB = 16
KP = R.KICKS_PER_ORB
N_EPOCH = N_ORB * KP
W = 32   # rolling fit window: last orbit of (phase, kick) pairs


def main():
    rng = np.random.default_rng(6759)
    a0, e0, w0, M0 = R.belt_init(rng)
    pa, pe, pw, pM = a0.copy(), e0.copy(), w0.copy(), M0.copy()
    a, e, w, M = a0.copy(), e0.copy(), w0.copy(), M0.copy()
    wu, Mu = w0.copy(), M0.copy()

    bu = np.zeros((W, N))
    be = np.zeros((W, N))
    bw = np.zeros((W, N))
    bd = np.zeros((W, 4, N))
    bn = 0
    coefs = None

    Wt, Ht = [], []
    pk_abs8 = None
    t0 = time.time()
    for k in range(1, N_EPOCH + 1):
        t_prev = (k - 1) * R.DT
        # program's predicted kick, anchored at its state at t_prev
        u_p = np.mod(pM + pw - (R.nJ * t_prev + R.MJ_M0), 2 * np.pi)
        if coefs is not None:
            Phi = R.phi_F(u_p, pe, pw)
            dhats = [Phi @ coefs[i] for i in range(4)]
        else:
            dhats = [np.zeros(N) for _ in range(4)]
        # true kick (verbatim layer)
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
        # record pair, advance program and truth
        i = (k - 1) % W
        bu[i], be[i], bw[i] = u_p, pe.copy(), pw.copy()
        for el in range(4):
            bd[i, el] = d[el]
        bn = min(bn + 1, W)
        n_p = pa**-1.5
        pa, pe, pw = pa + dhats[0], pe + dhats[1], pw + dhats[2]
        pM = pM + n_p * R.DT + dhats[3]
        wu = wu + d[2]
        Mu = Mu + n * R.DT + dM
        a, e, w, M = an, en, wn, Mn
        # payload = quantized (true - program)
        pf = [an - pa, en - pe,
              np.mod(wu - pw + np.pi, 2 * np.pi) - np.pi,
              np.mod(Mu - pM + np.pi, 2 * np.pi) - np.pi]
        s = [np.rint(pf[i] / R.Q[i]).astype(np.int64) for i in range(4)]
        Wt.append(sum(float(np.log2(1 + 2 * np.median(np.abs(si))))
                      for si in s))
        Ht.append(sum(R.ent_bits(si) for si in s))
        if k % KP == 0:
            m = k // KP
            # refit D on the rolling window
            rows = bn
            Phi = R.phi_F(bu[:rows].reshape(-1), be[:rows].reshape(-1),
                          bw[:rows].reshape(-1))
            C = Phi.T @ Phi
            coefs = np.stack([np.linalg.solve(
                C, Phi.T @ bd[:rows, el].reshape(-1)) for el in range(4)])
            if m == 8:
                pk_abs8 = []
                for el in range(4):
                    r = bd[:rows, el].reshape(-1) - Phi @ coefs[el]
                    pk_abs8.append(float(
                        1 - np.var(r) / np.var(bd[:rows, el])))
    Wt = np.array(Wt)
    post = [Wt[m * KP - 1] for m in range(1, N_ORB + 1)]
    peaks = [float(Wt[c * KP:(c + 1) * KP].max()) for c in range(N_ORB)]
    lg = np.log2(np.arange(1, N_ORB + 1))
    beta = float(np.polyfit(lg, post, 1)[0])
    out = {
        "program": "B: predictive per-kick subtraction, Fourier(8) in "
                   "lam-lamJ x Cheb(2,e) x Cheb(2,w), refit each orbit "
                   "on last 32 kicks",
        "wall_s": round(time.time() - t0, 1),
        "W_post_refit": [round(v, 3) for v in post],
        "peak_W_per_cycle": [round(v, 3) for v in peaks],
        "sup_W": round(float(Wt.max()), 3),
        "sup_W_steady_state_from_orbit2":
            round(float(Wt[KP:].max()), 3),
        "sup_H": round(float(np.array(Ht).max()), 3),
        "W_growth_bits_per_doubling": round(beta, 3),
        "per_kick_energy_absorption_at_orbit8":
            [round(v, 4) for v in pk_abs8],
        "checker_per_kick_reference": [0.87, 0.70, 0.50, 0.50],
    }
    with open("reabs_B.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
