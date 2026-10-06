#!/usr/bin/env python3
"""Belt-heating information floor (Fermi run 20261006-0437-fermi-c26d) v2.

Live-information floor per body of a program+scars store as mutual encounters
heat a belt. Oepik impulsive kicks aggregated by CLT, applied through the
impulsive Gauss equations at random phase. Scar of a body = deviation from its
PROGRAM-EVOLVED state (Kepler drift from the program's own initial elements is
program, not scar): a, e_vec, i_vec deltas from initial; M delta from
M0 + n(a0) t.

Columns: a, e1, e2, i1, i2, M. Entropy: Gaussian formula log2(s*sqrt(2*pi*e)/q)
per column (CLT walks; M capped at wrapped-uniform log2(2pi/q_M)); joint =
0.5*log2 det(2*pi*e*Cov) in quantum units (exact for Gaussian walks), plus a
Kozachenko-Leonenko kNN cross-check and explicit mutual information.

v2 fixes: program-referenced M (kappa=0 control now 0 bits), uncapped joint,
mass x density sweep, crossing time and repack cadence.

Usage: python3 belt_heat.py  ->  work/heat.json + tables on stdout.
"""
import json
import numpy as np

AU = 1.496e11
GM = 1.327e20
G = 6.674e-11
RHO = 2500.0
TWO_PI = 2 * np.pi
T_ORB_S = TWO_PI * np.sqrt((2.5 * AU) ** 3 / GM)   # s per orbit at belt centre
A_LO, A_HI = 2.2, 2.8
SIG_E, SIG_I = 0.05, 0.02
NB = 8192
Q_LIST = (1e-5, 1e-6, 1e-7)


def quanta(q):
    return np.array([q * 2.5 * AU, q, q, q, q, q * TWO_PI])


def belt_volume():
    a_mid = 0.5 * (A_LO + A_HI) * AU
    return TWO_PI * a_mid * (A_HI - A_LO) * AU * (SIG_I * np.sqrt(2) * a_mid * 2)


def kappa_of(m_ast, n_body, v_rel, a_mid_au):
    mu = G * m_ast
    r_c = (3 * m_ast / (4 * np.pi * RHO)) ** (1 / 3)
    b_min, b_max = 2 * r_c, 1e10
    T_orb = TWO_PI * np.sqrt((a_mid_au * AU) ** 3 / GM)
    k2 = 8 * np.pi * mu**2 * n_body * T_orb * np.log(b_max / b_min) / v_rel
    coll = n_body * np.pi * b_min**2 * v_rel * T_orb
    return np.sqrt(k2), T_orb, coll, r_c


def gauss_kick(r, a, e1, e2, i1, i2, kappa, dt):
    sc = kappa * np.sqrt(dt) / np.sqrt(3.0)
    dR, dT_, dN = r.normal(0, sc, (3, NB))
    f = r.uniform(0, TWO_PI, NB)
    e = np.hypot(e1, e2)
    h = np.sqrt(GM * a * (1 - e**2))
    p_ = a * (1 - e**2)
    rr = p_ / (1 + e * np.cos(f))
    varpi = np.arctan2(e2, e1)
    u = f + varpi
    da = (2 * a**2 / h) * (e * np.sin(f) * dR + (p_ / rr) * dT_)
    de = (1 / h) * (p_ * np.sin(f) * dR + ((p_ + rr) * np.cos(f) + rr * e) * dT_)
    edp = (-p_ * np.cos(f) * dR + (p_ + rr) * np.sin(f) * dT_) / h
    di = (rr * np.cos(u) * dN) / h
    idO = (rr * np.sin(u) * dN) / h
    cp, sp = np.cos(varpi), np.sin(varpi)
    Om = np.arctan2(i2, i1)
    co, so = np.cos(Om), np.sin(Om)
    return (a + da, e1 + de * cp - sp * edp, e2 + de * sp + cp * edp,
            i1 + di * co - so * idO, i2 + di * so + co * idO)


def entropies(d, q):
    qs = quanta(q)
    z = d / qs
    sig = np.std(z, axis=0)
    hm = np.log2(np.maximum(sig, 1e-12) * np.sqrt(TWO_PI * np.e))
    hm[5] = min(hm[5], np.log2(1.0 / q))          # wrapped-uniform cap
    hm = np.maximum(hm, 0.0)
    C = np.cov(z.T)
    _, logdet = np.linalg.slogdet(C + 1e-12 * np.eye(6))
    hj_raw = 0.5 * (6 * np.log(TWO_PI * np.e) + logdet) / np.log(2)
    hj = max(min(hj_raw, hm.sum()), hm.max())
    return hm, hj, hj_raw


def kl_knn(d, q, k=4):
    from scipy.spatial import cKDTree
    from scipy.special import digamma, gammaln
    X = d / quanta(q)
    X = X[:, np.std(X, axis=0) > 1e-9]
    if X.shape[1] < 2:
        return float("nan")
    dd = X.shape[1]
    tree = cKDTree(X)
    dist, _ = tree.query(X, k=k + 1)
    eps = np.maximum(dist[:, -1], 1e-12)
    cd = np.pi ** (dd / 2) / gammaln(dd / 2 + 1)
    return (digamma(len(eps)) - digamma(k) + np.log(cd)
            + dd * np.mean(np.log(eps))) / np.log(2)


def run(kappa, T_max=2.5e9, n_ck=30, seed=7):
    r = np.random.default_rng(seed)
    a = r.uniform(A_LO, A_HI, NB) * AU
    ee = r.rayleigh(SIG_E, NB)
    varpi = r.uniform(0, TWO_PI, NB)
    ii = r.rayleigh(SIG_I, NB)
    Om0 = r.uniform(0, TWO_PI, NB)
    e1, e2 = ee * np.cos(varpi), ee * np.sin(varpi)
    i1, i2 = ii * np.cos(Om0), ii * np.sin(Om0)
    M = r.uniform(0, TWO_PI, NB).copy()
    s0 = np.stack([a, e1, e2, i1, i2, M]).T.copy()
    n0 = np.sqrt(GM / a**3)                       # program mean motion
    Mref = M.copy()                               # program-evolved M

    Ts = np.unique(np.round(np.logspace(3, np.log10(T_max), n_ck)))
    out, t = [], 1.0
    for T in Ts:
        T = max(T, t + 1.0)
        dt = T - t
        a, e1, e2, i1, i2 = gauss_kick(r, a, e1, e2, i1, i2, kappa, dt)
        M = np.mod(M + np.sqrt(GM / a**3) * dt * T_ORB_S, TWO_PI)
        Mref = np.mod(Mref + n0 * dt * T_ORB_S, TWO_PI)
        t = T
        d = np.stack([a, e1, e2, i1, i2, M]).T - s0
        d[:, 5] = M - Mref                        # deviation from program drift
        d[:, 5] = (d[:, 5] + np.pi) % TWO_PI - np.pi
        rec = {"T": float(T),
               "sig": [float(np.std(d[:, 0]) / (2.5 * AU)), float(np.std(d[:, 1])),
                       float(np.std(d[:, 5]))]}
        for q in Q_LIST:
            hm, hj, hjr = entropies(d, q)
            rec[f"marg{q:g}"] = [round(float(x), 2) for x in hm]
            rec[f"margsum{q:g}"] = round(float(hm.sum()), 2)
            rec[f"joint{q:g}"] = round(float(hj), 2)
            rec[f"jointraw{q:g}"] = round(float(hjr), 2)
        rec["knn1e-6"] = round(float(kl_knn(d, 1e-6)), 2)
        out.append(rec)
    return out


def crossing(recs, key, thr):
    xs = [r_["T"] for r_ in recs]
    ys = [r_[key] for r_ in recs]
    if max(ys) < thr:
        return None
    for i in range(1, len(ys)):
        if ys[i] >= thr > ys[i - 1]:
            # log-linear interpolation
            lx = np.log(xs[i]) + (thr - ys[i]) / (ys[i] - ys[i - 1]) * (
                np.log(xs[i]) - np.log(xs[i - 1]))
            return float(np.exp(lx))
    return None


def main():
    a_mid = 0.5 * (A_LO + A_HI)
    v_k = np.sqrt(GM / (a_mid * AU))
    v_rel = v_k * 2 * SIG_E
    vol = belt_volume()
    sweep = []
    print("== mass x density sweep (horizon 2.5e9 orbits = 10 Gyr at 2.5 AU) ==")
    print(f"{'m_ast kg':>9} {'N_belt':>8} {'kappa':>9} {'coll/body':>10} "
          f"{'bits q1e-6':>10} {'GB@1e9':>7}")
    mains = {}
    for m_ast, N_belt in [(2e16, 1e9), (2e16, 1e6), (5e12, 1e6), (1.6e8, 1e9)]:
        n_body = N_belt / vol
        kap, T_orb, coll, r_c = kappa_of(m_ast, n_body, v_rel, a_mid)
        recs = run(kap) if (m_ast, N_belt) == (2e16, 1e9) else run(kap, n_ck=6)
        b6 = recs[-1]["margsum1e-06"]
        j6 = recs[-1]["joint1e-06"]
        coll_h = coll * 2.5e9
        sweep.append({"m": m_ast, "N": N_belt, "kappa": kap, "coll_horizon": coll_h,
                      "bits_marg": b6, "bits_joint": j6})
        mains[(m_ast, N_belt)] = recs
        print(f"{m_ast:>9.1e} {N_belt:>8.0e} {kap:>9.1e} {coll_h:>10.1f} "
              f"{b6:>7.1f}|{j6:<3.0f} {b6*1e9/8e9:>7.2f}")

    recs = mains[(2e16, 1e9)]
    res = {"params": {"v_rel": v_rel, "vol": vol, "sweep": sweep},
           "main": recs, "zero": run(0.0, T_max=1e6, n_ck=8),
           "dense": run(kappa_of(2e16, 1e9 / vol, v_rel, a_mid)[0] * 10, T_max=1e6, n_ck=12)}
    with open("work/heat.json", "w") as f:
        json.dump(res, f, indent=1)

    print("\n== main (m=2e16, N=1e9/belt): bits/body, totals, controls ==")
    print(f"{'T':>10} {'marg5':>6} {'marg6':>6} {'joint6':>7} {'MI6':>5} {'knn6':>6} "
          f"{'marg7':>6} {'GB m6':>6}  {'sig_a/a':>8} {'sig_e':>8} {'sig_M':>7}")
    for r_ in recs:
        print(f"{r_['T']:>10.0f} {r_['margsum1e-05']:>6.1f} {r_['margsum1e-06']:>6.1f} "
              f"{r_['joint1e-06']:>7.1f} {r_['margsum1e-06']-r_['jointraw1e-06']:>5.1f} "
              f"{r_['knn1e-6']:>6.1f} {r_['margsum1e-07']:>6.1f} "
              f"{r_['margsum1e-06']*1e9/8e9:>6.2f}  {r_['sig'][0]:>8.1e} {r_['sig'][1]:>8.1e} "
              f"{r_['sig'][2]:>7.2f}")

    for thr in (48.0, 24.0):
        cx = crossing(recs, "margsum1e-06", thr)
        print(f"crossing {thr:.0f} bits/body (q=1e-6, marginal): "
              f"{'never' if cx is None else f'{cx:.2e} orbits'}")
    z, d_ = res["zero"][-1], res["dense"][-1]
    m6_1e6 = [r_ for r_ in recs if r_["T"] <= 1e6][-1]["margsum1e-06"]
    print(f"controls: kappa=0 @1e6 -> {z['margsum1e-06']} bits (must be 0); "
          f"10x kappa @1e6 -> {d_['margsum1e-06']} vs main {m6_1e6} (must exceed)")

    print("\n== per-column marginals q=1e-6 (a,e1,e2,i1,i2,M) ==")
    for r_ in recs:
        if r_["T"] in (1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9) or r_["T"] > 2e9:
            print(f"T={r_['T']:.0e}: {r_['marg1e-06']}  sum={r_['margsum1e-06']}")


if __name__ == "__main__":
    main()
