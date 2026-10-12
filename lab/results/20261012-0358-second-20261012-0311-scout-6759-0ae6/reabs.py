#!/usr/bin/env python3
"""Steady-state reabsorption experiment — second author on run
20261012-0311-scout-6759 (checker's named gold experiment).

Question: with a population program recompiled every k orbits and only
residual integer scars carried, what is the steady-state per-body store
cost of a Jupiter-kicked belt, and what is the largest k (and, failing
that, the smallest per-population quantum coarsening c) that keeps it
within the 34.4 bits/body live budget (4 GiB / 10^9) at belt quanta?

Physics: verbatim kick layer from the scout run's h_live2.py (analytic
two-body program, Encke deviation only, 6-pt Gauss-Legendre, 32 kicks per
orbit at the reference cadence, Jupiter m/M=9.54e-4, a=5.2, e=0.048,
cold belt seed 6759, N=16384) extended to 16 orbits with unwrapped
angle bookkeeping. Floats evolve the truth; quanta only measure the
store. Program variants (all program-derivable arguments):
  P1  : Fourier(8) in lam-lamJ (TRUE-phase anchor) x Cheb(2,e) x Cheb(2,w)
        — the checker's disturbing-function basis (153 cols). Optimistic
        anchor (read path would need a fixed point; disclosed).
  P1B : same basis at the BASE program's phase (non-circular read path).
  P2  : generator deformation: Fourier(10) in initial lam (M0+w0)
        x Cheb(2) in initial (a, e, w) — 567 cols, time-independent.
  P3  : P1 + P2 joint least squares (720 cols).
Payload (what the store carries per body): S = rint(wrap(el_true -
program_prediction) / Q), angles wrapped to (-pi, pi]; before the first
refit the program is the bare generator (D=0), so the payload is the raw
quantized deviation, as in the scout run. The program is refit from
scratch on the TOTAL deviation at each refit (the strongest program
semantics; incremental fits can only do worse).

Metrics: W = sum_e log2(1 + 2*median|S_e|)  (the scout run's headline
instrument, scar_word_bits_median); H = sum_e ent_bits(S_e) (ideal
entropy coding; saturates at 4*log2(N)=56 bits for N=16384 — reported,
never used for verdicts).

Usage:
  python3 reabs.py evolve    # ~60 s: trajectory -> /tmp/hlive_reabs_traj.npz
  python3 reabs.py analyze   # ~4 min: all fits, k-scan, c-scan, controls
  python3 reabs.py control   # ~15 s: perturber-off, payload must be 0
  python3 reabs.py smoke     # instrument checks on synthetic data
"""
import json
import sys
import time

import numpy as np

N = 16384
N_ORB = 16
KICKS_PER_ORB = 32
QUAD = 6
A_REF = 2.7
MJ = 9.54e-4
A_J, E_J = 5.2, 0.048

Q_A = 6.6846e-8            # 1 km in AU
Q_E = 1e-7
Q_ANG = 2 * np.pi / 2**24
Q = np.array([Q_A, Q_E, Q_ANG, Q_ANG])

DT = 2 * np.pi * A_REF**1.5 / KICKS_PER_ORB
N_EPOCH = N_ORB * KICKS_PER_ORB
GX, GW = np.polynomial.legendre.leggauss(QUAD)
GX = 0.5 * DT * (GX + 1.0)
GW = 0.5 * DT * GW

TRAJ = "/tmp/hlive_reabs_traj.npz"


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


def pert_acc(x, y, t, mj=MJ):
    if mj == 0.0:
        return 0.0, 0.0
    MM = np.mod(nJ * t + MJ_M0, 2 * np.pi)
    EJ = kepler_E(MM, E_J)
    xJ = A_J * (np.cos(EJ) - E_J)
    yJ = A_J * np.sqrt(1 - E_J**2) * np.sin(EJ)
    dx, dy = x - xJ, y - yJ
    d3 = (dx * dx + dy * dy) ** -1.5
    return -mj * dx * d3, -mj * dy * d3


def ent_bits(n):
    c = np.bincount(n - n.min())
    p = c[c > 0] / n.size
    return float(-(p * np.log2(p)).sum())


def belt_init(rng):
    a0 = rng.uniform(2.1, 3.3, N)
    e0 = np.abs(rng.normal(0, 0.035, N)) + 0.005
    w0 = rng.uniform(0, 2 * np.pi, N)
    M0 = rng.uniform(0, 2 * np.pi, N)
    return a0, e0, w0, M0


def evolve(mode="cold", mj=MJ, n_orb=N_ORB, out=TRAJ):
    rng = np.random.default_rng(6759)
    a0, e0, w0, M0 = belt_init(rng)
    n_ep = n_orb * KICKS_PER_ORB
    A = np.empty((n_ep, N))
    E_ = np.empty((n_ep, N))
    W_ = np.empty((n_ep, N))   # unwrapped omega
    M_ = np.empty((n_ep, N))   # unwrapped mean anomaly
    stock = np.zeros((4, N), dtype=np.int64)
    raw_ent, stock_ent, stock_w = [], [], []
    t_start = time.time()
    a, e, w, M = a0.copy(), e0.copy(), w0.copy(), M0.copy()
    wu, Mu = w0.copy(), M0.copy()
    for k in range(1, n_ep + 1):
        n = a**-1.5
        Jx = np.zeros(N)
        Jy = np.zeros(N)
        for g in range(QUAD):
            x, y, _, _ = state_vec(a, e, w, M + n * GX[g])
            ax, ay = pert_acc(x, y, GX[g], mj)
            Jx += GW[g] * ax
            Jy += GW[g] * ay
        x, y, vx, vy = state_vec(a, e, w, M + n * DT)
        an, en, wn, Mn = elements(x, y, vx + Jx, vy + Jy)
        dM = np.mod(Mn - (M + n * DT) + np.pi, 2 * np.pi) - np.pi
        d = (an - a, en - e,
             np.mod(wn - w + np.pi, 2 * np.pi) - np.pi, dM)
        q = [np.rint(d[i] / Q[i]).astype(np.int64) for i in range(4)]
        raw_ent.append(sum(ent_bits(qq) for qq in q))
        for i in range(4):
            stock[i] += q[i]
        wu = wu + d[2]
        Mu = Mu + n * DT + dM
        A[k - 1], E_[k - 1], W_[k - 1], M_[k - 1] = an, en, wu, Mu
        if k % KICKS_PER_ORB == 0:
            med = [np.median(np.abs(stock[i])) for i in range(4)]
            stock_w.append(float(sum(np.log2(1.0 + 2.0 * m)
                                     for m in med)))
            stock_ent.append(sum(ent_bits(stock[i]) for i in range(4)))
        a, e, w, M = an, en, wn, Mn
    el = time.time() - t_start
    np.savez(out, A=A, E=E_, W=W_, M=M_, a0=a0, e0=e0, w0=w0, M0=M0,
             raw_ent=np.array(raw_ent), stock_ent=np.array(stock_ent),
             stock_w=np.array(stock_w))
    print(json.dumps({
        "wall_s": round(el, 2), "orbits": n_orb, "N": N, "mode": mode,
        "raw_bits_per_kick_med": float(np.median(raw_ent)),
        "stock_raw_bits": [round(v, 4) for v in stock_ent],
        "scar_word_bits_median": [round(v, 4) for v in stock_w],
    }, indent=1))


# ---------------------------------------------------------------- analysis

def cheb_scaled(x, lo, hi, deg):
    s = np.clip((2.0 * x - lo - hi) / (hi - lo), -1, 1)
    return np.polynomial.chebyshev.chebvander(s, deg)


def fourier(u, nf):
    cols = [np.ones_like(u)]
    for k in range(1, nf + 1):
        cols.append(np.cos(k * u))
        cols.append(np.sin(k * u))
    return np.stack(cols, axis=1)


def kron(blocks):
    out = blocks[0]
    for b in blocks[1:]:
        out = (out[:, :, None] * b[:, None, :]).reshape(out.shape[0], -1)
    return out


NF_F = 8    # checker's Fourier order in lam - lamJ
NF_G = 10   # generator-deformation Fourier order in initial lam
DEG = 2     # Chebyshev degree for e, w (and a, e, w in G)


def phi_F(u, e, w):
    return kron([fourier(u, NF_F),
                 cheb_scaled(e, 0.0, 0.30, DEG),
                 cheb_scaled(np.mod(w, 2 * np.pi), 0.0, 2 * np.pi, DEG)])


def analyze():
    tz = np.load(TRAJ)
    A, E_, W_, M_ = tz["A"], tz["E"], tz["W"], tz["M"]
    a0, e0, w0, M0 = tz["a0"], tz["e0"], tz["w0"], tz["M0"]
    n0 = a0**-1.5
    rep = {
        "raw_bits_per_kick_med": float(np.median(tz["raw_ent"])),
        "scar_word_bits_median":
            [round(float(v), 6) for v in tz["stock_w"][:8]],
        "scout_published": [66.63001813083629, 70.23569886547544,
                            72.16773224552333, 73.6496617941026,
                            74.80461482500695, 75.78514244017934,
                            76.60640136384863, 77.33006706627545],
    }
    t_of = lambda j: j * DT                      # epoch j (1-based)
    lamJ = lambda t: nJ * t + MJ_M0

    def delta(j):
        t = t_of(j)
        return [A[j - 1] - a0, E_[j - 1] - e0,
                W_[j - 1] - w0, M_[j - 1] - (M0 + n0 * t)]

    def anchor_true(j):
        t = t_of(j)
        return (np.mod(M_[j - 1] + W_[j - 1] - lamJ(t), 2 * np.pi),
                E_[j - 1], W_[j - 1])

    def anchor_base(j):
        t = t_of(j)
        return (np.mod(M0 + n0 * t + w0 - lamJ(t), 2 * np.pi),
                e0, w0)

    # fixed generator-deformation block (program-derivable: initial state)
    G = kron([fourier(np.mod(M0 + w0, 2 * np.pi), NF_G),
              cheb_scaled(a0, 2.1, 3.3, DEG),
              cheb_scaled(e0, 0.0, 0.30, DEG),
              cheb_scaled(np.mod(w0, 2 * np.pi), 0.0, 2 * np.pi, DEG)])
    GTG = G.T @ G

    def phi_F_at(j, anchor):
        if anchor == "true":
            return phi_F(*anchor_true(j))
        return phi_F(*anchor_base(j))

    def solve_blocks(pname, PhiF, dlt):
        """Least squares per program; returns (coF, coG) coefficient
        parts. The joint design drops G's constant column (an exact
        duplicate of the F block constant, Fourier k=0 x all Cheb
        deg-0), which is prediction-invariant."""
        if pname == "P1" or pname == "P1B":
            C = PhiF.T @ PhiF
            rhs = np.stack([PhiF.T @ d for d in dlt], axis=1)
            return np.linalg.solve(C, rhs).T, None
        if pname == "P2":
            rhs = np.stack([G.T @ d for d in dlt], axis=1)
            return None, np.linalg.solve(GTG, rhs).T
        Phi = np.hstack([PhiF, G[:, 1:]])
        C = Phi.T @ Phi
        rhs = np.stack([Phi.T @ d for d in dlt], axis=1)
        co = np.linalg.solve(C, rhs).T
        coG = np.zeros((4, G.shape[1]))
        coG[:, 1:] = co[:, PhiF.shape[1]:]
        return co[:, :PhiF.shape[1]], coG

    # ---- fits at every orbit boundary (epoch j = 32 m)
    programs = {
        "P1":  {"anchor": "true",  "blocks": "F"},
        "P1B": {"anchor": "base",  "blocks": "F"},
        "P2":  {"anchor": None,    "blocks": "G"},
        "P3":  {"anchor": "true",  "blocks": "FG"},
    }
    coF = {}    # (prog, m) -> (4, 153) F-coefficients
    coG = {}    # (prog, m) -> (4, 567) G-coefficients
    fit_stats = {}
    t_start = time.time()
    for pname, pcfg in programs.items():
        for m in range(1, N_ORB + 1):
            j = m * KICKS_PER_ORB
            dlt = delta(j)
            PhiF = phi_F_at(j, pcfg["anchor"]) \
                if pcfg["blocks"] != "G" else None
            coF[(pname, m)], coG[(pname, m)] = solve_blocks(pname, PhiF,
                                                             dlt)
            if pname == "P1" and m == 8:
                ab = []
                for i in range(4):
                    r = dlt[i] - PhiF @ coF[(pname, m)][i]
                    ab.append(float(1 - np.var(r) / np.var(dlt[i])))
                fit_stats["energy_absorbed_P1_m8"] = ab
    # precompute G-contribution to the program prediction per refit
    DG = {key: (G @ co.T).T for key, co in coG.items()   # (4, N)
          if co is not None}
    print(f"fits done {time.time()-t_start:.1f}s", file=sys.stderr)

    # ---- shuffle control at m=8 on P1's basis
    rng2 = np.random.default_rng(4242)
    j = 8 * KICKS_PER_ORB
    PhiF8 = phi_F_at(j, "true")
    dlt8 = delta(j)
    sh = []
    for i in range(4):
        dp = rng2.permutation(dlt8[i])
        c = np.linalg.lstsq(PhiF8, dp, rcond=None)[0]
        r = dp - PhiF8 @ c
        s = np.rint(r / Q[i]).astype(np.int64)
        sh.append({"absorbed_energy": float(1 - np.var(r) / np.var(dp)),
                   "resid_word_bits":
                       float(np.log2(1 + 2 * np.median(np.abs(s))))})
    fit_stats["shuffle_control_m8"] = sh

    # ---- payload trajectories
    KS = [1, 2, 4, 8]
    CS_FULL = [1, 4, 16, 64, 256, 1024]   # c-scan at k=1

    def wrap_angles(pf):
        return [pf[0], pf[1],
                np.mod(pf[2] + np.pi, 2 * np.pi) - np.pi,
                np.mod(pf[3] + np.pi, 2 * np.pi) - np.pi]

    def metrics(pf, c):
        s = [np.rint(w / (Q[i] * c)).astype(np.int64)
             for i, w in enumerate(wrap_angles(pf))]
        W = sum(float(np.log2(1 + 2 * np.median(np.abs(si)))) for si in s)
        H = sum(ent_bits(si) for si in s)
        per = [round(float(np.log2(1 + 2 * np.median(np.abs(si)))), 3)
               for si in s]
        return W, H, per

    out = {"fit_stats": fit_stats, "configs": {}}
    for pname, pcfg in programs.items():
        t0 = time.time()
        trajW = {k: [] for k in KS}
        trajH = {k: [] for k in KS}
        trajWc = {c: [] for c in CS_FULL}
        trajHc = {c: [] for c in CS_FULL}
        per_elem = {k: [] for k in KS}
        for j in range(1, N_EPOCH + 1):
            mo = j // KICKS_PER_ORB
            dlt = delta(j)
            PhiF = None
            if pcfg["blocks"] != "G":
                PhiF = phi_F_at(j, pcfg["anchor"])
            for k in KS:
                fi = mo if (mo >= 1 and mo % k == 0) else (mo // k) * k
                pf = [dlt[i] for i in range(4)]
                if fi >= 1:
                    if pcfg["blocks"] == "F":
                        cf = coF[(pname, fi)]
                        pf = [pf[i] - PhiF @ cf[i] for i in range(4)]
                    elif pcfg["blocks"] == "G":
                        pf = [pf[i] - DG[(pname, fi)][i] for i in range(4)]
                    else:
                        cf = coF[(pname, fi)]
                        pf = [pf[i] - PhiF @ cf[i] - DG[(pname, fi)][i]
                              for i in range(4)]
                W, H, per = metrics(pf, 1)
                trajW[k].append(W)
                trajH[k].append(H)
                if j % KICKS_PER_ORB == 0:
                    per_elem[k].append(per)
                if k == 1:
                    for c in CS_FULL:
                        Wc, Hc, _ = metrics(pf, c)
                        trajWc[c].append(Wc)
                        trajHc[c].append(Hc)
        cfgs = {}
        for k in KS:
            Wt, Ht = np.array(trajW[k]), np.array(trajH[k])
            post = [Wt[m * KICKS_PER_ORB - 1] for m in range(1, N_ORB + 1)]
            postH = [Ht[m * KICKS_PER_ORB - 1]
                     for m in range(1, N_ORB + 1)]
            peaks = [float(Wt[cyc * k * KICKS_PER_ORB:
                               (cyc + 1) * k * KICKS_PER_ORB].max())
                     for cyc in range(N_ORB // k)]
            beta = None
            if k == 1:
                lg = np.log2(np.arange(1, N_ORB + 1))
                beta = float(np.polyfit(lg, post, 1)[0])
            cfgs[f"k{k}"] = {
                "sup_W": round(float(Wt.max()), 3),
                "sup_H": round(float(Ht.max()), 3),
                "W_post_refit": [round(v, 3) for v in post],
                "H_post_refit": [round(v, 3) for v in postH],
                "peak_W_per_cycle": [round(v, 3) for v in peaks],
                "W_growth_bits_per_doubling":
                    round(beta, 3) if beta is not None else None,
                "per_elem_W_at_orbit16": per_elem[k][-1],
            }
        for c in CS_FULL:
            Wt, Ht = np.array(trajWc[c]), np.array(trajHc[c])
            post = [Wt[m * KICKS_PER_ORB - 1] for m in range(1, N_ORB + 1)]
            cfgs[f"k1_c{c}"] = {
                "sup_W": round(float(Wt.max()), 3),
                "sup_H": round(float(Ht.max()), 3),
                "W_post_refit": [round(v, 3) for v in post],
            }
        out["configs"][pname] = cfgs
        print(f"{pname} done {time.time()-t0:.1f}s", file=sys.stderr)

    verdict = {}
    for pname in programs:
        row = {f"k{k}": out["configs"][pname][f"k{k}"]["sup_W"]
               for k in KS}
        mc = None
        for c in CS_FULL:
            if out["configs"][pname][f"k1_c{c}"]["sup_W"] <= 34.4:
                mc = c
                break
        row["min_c_supW_le_34.4"] = mc
        verdict[pname] = row
    out["verdict_belt_quanta"] = {
        "budget_bits_per_body": 34.4,
        "largest_k_supW_le_budget": {
            p: max([int(k[1:]) for k in verdict[p]
                    if k.startswith("k") and verdict[p][k] <= 34.4],
                   default=0)
            for p in verdict},
        "sup_W_by_k_and_min_c": verdict,
    }
    out["reproduction"] = rep
    with open("reabs-results.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out["verdict_belt_quanta"], indent=1))
    for p in ("P1", "P2", "P3"):
        print(p, "k1 W_post_refit:",
              out["configs"][p]["k1"]["W_post_refit"])
        print(p, "k1 peak/cycle:",
              out["configs"][p]["k1"]["peak_W_per_cycle"])


def control():
    """Perturber off: the whole harness must yield exactly zero payload."""
    evolve(mode="control", mj=0.0, n_orb=2, out="/tmp/hlive_reabs_ctl.npz")
    tz = np.load("/tmp/hlive_reabs_ctl.npz")
    A, E_, W_, M_ = tz["A"], tz["E"], tz["W"], tz["M"]
    a0, e0, w0, M0 = tz["a0"], tz["e0"], tz["w0"], tz["M0"]
    n0 = a0**-1.5
    nz = 0
    for j in range(1, A.shape[0] + 1):
        t = j * DT
        pf = [A[j - 1] - a0, E_[j - 1] - e0, W_[j - 1] - w0,
              M_[j - 1] - (M0 + n0 * t)]
        s = [np.rint(w / Q[i]).astype(np.int64)
             for i, w in enumerate(pf)]
        nz += int(sum(int(si.max() - si.min()) for si in s))
    print(json.dumps({"control_distinct_values_total": nz,
                      "payload_exactly_zero": nz == 0}))


def smoke():
    """Instrument checks on synthetic data (no belt numbers revealed)."""
    rng = np.random.default_rng(99)
    u = rng.uniform(0, 2 * np.pi, 4096)
    e = rng.uniform(0, 0.3, 4096)
    w = rng.uniform(0, 2 * np.pi, 4096)
    Phi = phi_F(u, e, w)
    ctrue = rng.normal(size=Phi.shape[1])
    y = Phi @ ctrue
    c = np.linalg.lstsq(Phi, y, rcond=None)[0]
    recov = float(np.max(np.abs(y - Phi @ c)) / np.max(np.abs(y)))
    yp = rng.permutation(y)
    cp = np.linalg.lstsq(Phi, yp, rcond=None)[0]
    absorbed_perm = 1 - np.var(yp - Phi @ cp) / np.var(yp)
    print(json.dumps({
        "synthetic_recovery_relerr": recov,
        "shuffled_absorbed_energy": float(absorbed_perm),
        "pass": bool(recov < 1e-10 and abs(absorbed_perm) < 0.01),
    }))


if __name__ == "__main__":
    {"evolve": evolve, "analyze": analyze, "control": control,
     "smoke": smoke}[sys.argv[1]]()
