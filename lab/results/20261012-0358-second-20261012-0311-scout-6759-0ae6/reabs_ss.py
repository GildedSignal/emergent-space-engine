#!/usr/bin/env python3
"""Steady-state quantum valve: exact per-cycle peaks for P3 and P1 at
k=1 under coarsened quanta, separating the cold-start first orbit (raw
carry before the first recompile) from the steady state (orbits >= 2).
Redoes only the k=1 fits (deterministic) and evaluates the payload
trajectory at each c. Usage: python3 reabs_ss.py  (~3 min)
"""
import json
import time

import numpy as np

import reabs as R

N = R.N
N_ORB = 16
KP = R.KICKS_PER_ORB
N_EPOCH = N_ORB * KP
CS = [1, 16, 64, 256, 1024]
BUDGET = 34.4


def main():
    tz = np.load(R.TRAJ)
    A, E_, W_, M_ = tz["A"], tz["E"], tz["W"], tz["M"]
    a0, e0, w0, M0 = tz["a0"], tz["e0"], tz["w0"], tz["M0"]
    n0 = a0**-1.5
    t_of = lambda j: j * R.DT
    lamJ = lambda t: R.nJ * t + R.MJ_M0

    def delta(j):
        t = t_of(j)
        return [A[j - 1] - a0, E_[j - 1] - e0,
                W_[j - 1] - w0, M_[j - 1] - (M0 + n0 * t)]

    def anchor_true(j):
        t = t_of(j)
        return (np.mod(M_[j - 1] + W_[j - 1] - lamJ(t), 2 * np.pi),
                E_[j - 1], W_[j - 1])

    G = R.kron([R.fourier(np.mod(M0 + w0, 2 * np.pi), R.NF_G),
                R.cheb_scaled(a0, 2.1, 3.3, R.DEG),
                R.cheb_scaled(e0, 0.0, 0.30, R.DEG),
                R.cheb_scaled(np.mod(w0, 2 * np.pi), 0.0, 2 * np.pi,
                              R.DEG)])

    out = {}
    for pname in ("P3", "P1"):
        t0 = time.time()
        coF, coG = {}, {}
        for m in range(1, N_ORB + 1):
            j = m * KP
            dlt = delta(j)
            PhiF = R.phi_F(*anchor_true(j))
            if pname == "P1":
                C = PhiF.T @ PhiF
                rhs = np.stack([PhiF.T @ d for d in dlt], axis=1)
                coF[m] = np.linalg.solve(C, rhs).T
            else:
                Phi = np.hstack([PhiF, G[:, 1:]])
                C = Phi.T @ Phi
                rhs = np.stack([Phi.T @ d for d in dlt], axis=1)
                co = np.linalg.solve(C, rhs).T
                coF[m] = co[:, :PhiF.shape[1]]
                g = np.zeros((4, G.shape[1]))
                g[:, 1:] = co[:, PhiF.shape[1]:]
                coG[m] = g
        DG = {m: (G @ coG[m].T).T for m in coG} if coG else {}

        def wrap_angles(pf):
            return [pf[0], pf[1],
                    np.mod(pf[2] + np.pi, 2 * np.pi) - np.pi,
                    np.mod(pf[3] + np.pi, 2 * np.pi) - np.pi]

        res = {}
        for c in CS:
            Wt = []
            for j in range(1, N_EPOCH + 1):
                mo = j // KP
                dlt = delta(j)
                PhiF = R.phi_F(*anchor_true(j))
                if mo >= 1:
                    cf = coF[mo]
                    if pname == "P1":
                        pf = [dlt[i] - PhiF @ cf[i] for i in range(4)]
                    else:
                        pf = [dlt[i] - PhiF @ cf[i] - DG[mo][i]
                              for i in range(4)]
                else:
                    pf = dlt
                s = [np.rint(w / (R.Q[i] * c)).astype(np.int64)
                     for i, w in enumerate(wrap_angles(pf))]
                Wt.append(sum(float(np.log2(1 + 2 * np.median(np.abs(si))))
                              for si in s))
            Wt = np.array(Wt)
            cyc = [float(Wt[q * KP:(q + 1) * KP].max())
                   for q in range(N_ORB)]
            res[f"c{c}"] = {
                "sup_W_all": round(float(Wt.max()), 3),
                "sup_W_steady_from_orbit2":
                    round(float(Wt[KP:].max()), 3),
                "cycle_peaks": [round(v, 3) for v in cyc],
                "steady_sup_le_budget":
                    bool(Wt[KP:].max() <= BUDGET),
            }
        min_c_ss = None
        min_c_all = None
        for c in CS:
            if res[f"c{c}"]["sup_W_steady_from_orbit2"] <= BUDGET \
                    and min_c_ss is None:
                min_c_ss = c
            if res[f"c{c}"]["sup_W_all"] <= BUDGET and min_c_all is None:
                min_c_all = c
        out[pname] = {"c_scan": res,
                      "min_c_steady_state_le_34.4": min_c_ss,
                      "min_c_including_cold_start_le_34.4": min_c_all,
                      "wall_s": round(time.time() - t0, 1)}
        print(pname, "done", out[pname]["wall_s"], "s", flush=True)
    with open("reabs_ss.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
