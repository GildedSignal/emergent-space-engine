#!/usr/bin/env python3
"""Why the sigma instrument is n-unstable, and the re-anchoring on a floored instrument.

rescale.py found the population sigma_E growing with n even at FIXED per-body kick
rate (perturber channel: 4.2e-3 -> 1.3e-2 over n = 100..1e4). Diagnosis: the impulse
kick dv = 2Gm/(b v_rel), b = sqrt(U) b_max has p(dv) ~ dv^-3 — log-divergent variance —
so the empirical sigma is an order statistic of the closest approach ever drawn, which
grows with sample size. Physically that tail sits at b < mutual Hill radius, where the
no-collision impulse premise is wrong anyway (that regime is the exact encounter
subsystem's, m-meso-motion / r8).

This script (run ~3 min):
  1. LOCALIZES: unfloored pert channel — bulk (IQR) vs tail (p99, max) across n, and
     sigma over the first 100 bodies of the n=1e4 run vs an n=100 run.
  2. FLOORS b at the pair's mutual Hill radius R_H = (2 m_pair / 3 M*)^(1/3) a0 and
     repeats scans A (fixed m), B (fixed total belt mass), C (perturber), with floored
     n=2000 anchors (t=30 and t=300), restoring n-stability if the diagnosis is right.
  3. Re-anchors the game-scale numbers on the floored instrument.
Floored close encounters keep the maximum impulse the linear law would give (an upper
bound on their scar); they are NOT collisions here.
"""
import json, sys
import numpy as np

sys.argv = ["hlive"]
import hlive

G = hlive.G
A0, W_, SE = 2.1, 0.05, 0.01
W = 2 * W_ / A0
T_ORB = A0 ** 1.5
S_YR = 3.156e7
Q = 2 ** -20
SQ = float(np.sqrt(2 * np.pi * np.e))
CAP_E = float(np.log2(W / Q)); CAP_L = CAP_E; CAP_W = float(-np.log2(Q)); CAP_TOT = 2 * CAP_E + CAP_W
E_TYP = G / (2 * A0); L_TYP = float(np.sqrt(G * A0))


def lam_of(n):
    e_bar = SE * np.sqrt(np.pi / 2)
    return n * (A0 * 2 * e_bar) / (2 * W_) * (1.5 * (A0 * 2 * e_bar * 2 / 3) / A0)


LAM_P = 1.5 * (2 * np.pi / A0 ** 1.5) * (2 * W_) / A0


def kick_deltas_f(base, m_i, m_pair, sigma_e, lam_i, a0, rg, hill):
    """hlive.kick_deltas verbatim (same RNG draw order) except the b floor."""
    a, e, E, L, Ax, Ay = base
    n = a.size
    k = rg.poisson(lam_i, n)
    tot = int(k.sum())
    if tot == 0:
        return None, 0
    idx = np.repeat(np.arange(n), k)
    ej = rg.rayleigh(sigma_e, tot)
    bmax = (e[idx] + ej) * a0
    b = np.sqrt(rg.uniform(0, 1, tot)) * bmax
    if hill:
        rh = (2 * m_pair / 3.0) ** (1.0 / 3.0) * a0   # mutual Hill radius of the pair
        b = np.maximum(b, rh)
    else:
        b = np.maximum(b, 1e-9)
    vK = 2 * np.pi / np.sqrt(a[idx])
    vrel = vK * np.sqrt(e[idx] ** 2 + ej ** 2 + (0.75 * sigma_e) ** 2)
    dv = 2 * G * m_i / (b * vrel)
    ang = rg.uniform(-np.pi, np.pi, tot)
    dvx, dvy = dv * np.cos(ang), dv * np.sin(ang)
    M = rg.uniform(-np.pi, np.pi, tot)
    ei = e[idx]
    Ecc = M.copy()
    for _ in range(4):
        Ecc -= (Ecc - ei * np.sin(Ecc) - M) / (1 - ei * np.cos(Ecc))
    c, s = np.cos(Ecc), np.sin(Ecc)
    r = 1.0 - ei * c
    n_mot = 2 * np.pi / a[idx] ** 1.5
    rx = a[idx] * (c - ei)
    ry = a[idx] * np.sqrt(1 - ei ** 2) * s
    vpx = -n_mot * a[idx] * s / r
    vpy = n_mot * a[idx] * np.sqrt(1 - ei ** 2) * c / r
    dE = vpx * dvx + vpy * dvy
    dL = rx * dvy - ry * dvx
    Ln = L[idx] + dL
    dAx = (vpy * dL + dvy * Ln) / G
    dAy = (-vpx * dL - dvx * Ln) / G
    out = (np.bincount(idx, dE, minlength=n), np.bincount(idx, dL, minlength=n),
           np.bincount(idx, dAx, minlength=n), np.bincount(idx, dAy, minlength=n))
    return out, tot


def walk(n, m_body, m_pert, orbits, seed, hill):
    """One seed; returns stats of the scar walk (relative units) and dE optionally."""
    a, e, vp = hlive.belt(n, SE, W_, A0, seed)
    E = -G / (2 * a); L = np.sqrt(G * a * (1 - e ** 2))
    Ax, Ay = e * np.cos(vp), e * np.sin(vp)
    E0, L0, A0x, A0y = E.copy(), L.copy(), Ax.copy(), Ay.copy()
    rg = np.random.default_rng(seed + 777)
    lam = lam_of(n)
    chans = [(lam, m_body, 2 * m_body)] if m_pert <= 0 else \
            [(lam, m_body, 2 * m_body), (LAM_P, m_pert, m_pert + m_body)]
    for _ in range(orbits):
        for li, mi, mp in chans:
            if mi <= 0:
                continue
            d, _ = kick_deltas_f((a, e, E, L, Ax, Ay), mi, mp, SE, li, A0, rg, hill)
            if d is None:
                continue
            E, L, Ax, Ay = E + d[0], L + d[1], Ax + d[2], Ay + d[3]
    dE = (E - E0) / E_TYP
    dL = (L - L0) / L_TYP
    dvp = np.angle(Ax + 1j * Ay) - np.angle(A0x + 1j * A0y)
    dvp = (dvp + np.pi) % (2 * np.pi) - np.pi
    st = {"sigE": float(dE.std()), "sigL": float(dL.std()), "sigW": float(dvp.std() / (2 * np.pi)),
          "iqrE": float(np.subtract(*np.percentile(dE, [75, 25]))),
          "p99E": float(np.percentile(np.abs(dE), 99)), "maxE": float(np.abs(dE).max())}
    return st, dE


def bits_at(sigE, sigL, sigW):
    return float(min(np.log2(max(sigE * SQ, 1e-12) / Q), CAP_E)
                 + min(np.log2(max(sigL * SQ, 1e-12) / Q), CAP_L)
                 + min(np.log2(max(sigW * SQ, 1e-12) / Q), CAP_W))


def main():
    out = {"W": W, "cap_bits_q2m20": CAP_TOT}
    M_BELT, N_BIG = 2e-7, 1e9
    ns_scan = [100, 1000, 10000]
    seeds = {100: [1, 2, 3, 4], 1000: [1, 2, 3, 4], 10000: [1, 2]}

    # 1. localization on the UNfloored pert channel
    loc = {}
    for n in (100, 10000):
        st, dE = walk(n, 1e-10, 1e-7, 30, 1, hill=False)
        loc[n] = st
        if n == 10000:
            loc["sub100_of_10000"] = {"sigE": float(dE[:100].std()), "iqrE":
                float(np.subtract(*np.percentile(dE[:100], [75, 25])))}
    out["localization_unfloored"] = loc

    # 2. floored scans
    sc = {}
    for name, mb_fn, mp in (("A_fixed_m", lambda n: 1e-10, 0.0),
                            ("B_fixed_M", lambda n: M_BELT / n, 0.0),
                            ("C_pert", lambda n: 1e-10, 1e-7)):
        sc[name] = {n: [walk(n, mb_fn(n), mp, 30, sd, hill=True)[0] for sd in seeds[n]]
                    for n in ns_scan}
    ancA30 = [walk(2000, 1e-10, 0.0, 30, sd, hill=True)[0] for sd in (1, 2)]
    ancA300 = [walk(2000, 1e-10, 0.0, 300, sd, hill=True)[0] for sd in (1, 2)]
    ancC30 = [walk(2000, 1e-10, 1e-7, 30, sd, hill=True)[0] for sd in (1, 2)]
    for name, D, extra in (("A_fixed_m", sc["A_fixed_m"], ancA30),
                           ("B_fixed_M", sc["B_fixed_M"], ancA30),
                           ("C_pert", sc["C_pert"], ancC30)):
        ns = sorted(D) + [2000]
        sE = [float(np.mean([x["sigE"] for x in D[n]])) for n in sorted(D)] + \
             [float(np.mean([x["sigE"] for x in extra]))]
        slope = float(np.polyfit(np.log2(ns), np.log2(sE), 1)[0])
        out["scans_floored_" + name] = {"n": ns, "sigE_mean": sE, "slope": slope}
    sA, sB, sC = (out["scans_floored_" + k] for k in ("A_fixed_m", "B_fixed_M", "C_pert"))
    sC["max_rel_spread"] = max(sC["sigE_mean"]) / min(sC["sigE_mean"]) - 1
    sA["ratio_10000_over_100"] = sA["sigE_mean"][2] / sA["sigE_mean"][0]
    sB["ratio_100_over_10000"] = sB["sigE_mean"][0] / sB["sigE_mean"][2]
    sB["sigE_x_sqrt_n"] = [s * np.sqrt(n) for s, n in zip(sB["sigE_mean"], sB["n"])]

    # 3. re-anchored numbers on the floored instrument
    r = {}
    s_ref = float(np.mean([x["sigE"] for x in ancA300]))     # floored anchor, t=300
    t_ref, n_ref, m_ref = 300, 2000, 1e-10
    t_ceil = lambda n, m: t_ref * (W / s_ref) ** 2 * (m_ref / m) ** 2 * (n_ref / n)
    r["floored_anchor_sigE_300_n2000"] = s_ref
    r["unfloored_anchor_sigE_300_n2000"] = 3.871e-4
    r["t_ceiling_fixed_m_1e9_orbits_INADMISSIBLE"] = t_ceil(N_BIG, 1e-10)
    r["belt_mass_fixed_m_1e9_Msun"] = 0.1
    r["t_ceiling_fixedM_1e9_orbits"] = t_ceil(N_BIG, M_BELT / N_BIG)
    r["t_ceiling_fixedM_1e9_years"] = r["t_ceiling_fixedM_1e9_orbits"] * T_ORB
    r["t_ceiling_fixedM_1e9_seconds"] = r["t_ceiling_fixedM_1e9_years"] * S_YR
    r["H_live_mutual_fixedM_1e9"] = CAP_TOT / r["t_ceiling_fixedM_1e9_seconds"]
    sigE30p = float(np.mean([x["sigE"] for x in ancC30]))
    sigL30p = float(np.mean([x["sigL"] for x in ancC30]))
    sigW30p = float(np.mean([x["sigW"] for x in ancC30]))
    bits_pert = lambda t, mp=1e-7: bits_at(sigE30p * np.sqrt(t / 30) * mp / 1e-7,
                                           sigL30p * np.sqrt(t / 30) * mp / 1e-7,
                                           sigW30p * np.sqrt(t / 30) * mp / 1e-7)
    lts = np.logspace(0, 6, 6001)
    bt = np.array([bits_pert(t) for t in lts])
    r["pert_sigE30_floored_n2000"] = sigE30p
    r["pert_bits_t30_q2m20"] = bits_pert(30)
    r["pert_t_orbits_at_90pct_cap"] = float(lts[int(np.argmax(bt >= 0.9 * CAP_TOT))])
    r["pert_t_years_at_90pct_cap"] = r["pert_t_orbits_at_90pct_cap"] * T_ORB
    r["pert_t_orbits_at_50_bits"] = float(lts[int(np.argmax(bt >= 50.0))])
    r["H_live_pert_90pct"] = CAP_TOT / (r["pert_t_orbits_at_90pct_cap"] * T_ORB * S_YR)
    t_ses = 30.0 / T_ORB
    lo, hi = 1e-12, 1e-6
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        lo, hi = (lo, mid) if bits_pert(t_ses, mid) > 32 else (mid, hi)
    r["m_pert_busting_32bits_in_30yr_Msun"] = float(np.sqrt(lo * hi))
    r["m_pert_in_lunar_masses"] = float(np.sqrt(lo * hi) / 3.69e-8)
    out["reanchor_floored"] = r
    json.dump(out, open("rescale2_results.json", "w"), indent=1)

    print("== localization (unfloored pert channel, seed 1, t=30) ==")
    for k in (100, 10000):
        st = loc[k]
        print(" n=%5d sigE=%.3e iqrE=%.3e p99E=%.3e maxE=%.3e" % (k, st["sigE"], st["iqrE"], st["p99E"], st["maxE"]))
    print(" first-100 of n=1e4: sigE=%.3e iqrE=%.3e  (vs n=100 above)" %
          (loc["sub100_of_10000"]["sigE"], loc["sub100_of_10000"]["iqrE"]))
    print("\n== floored scans (b >= mutual Hill) ==")
    for name in ("A_fixed_m", "B_fixed_M", "C_pert"):
        s = out["scans_floored_" + name]
        print(" %s slope=%+.3f  " % (name, s["slope"]) +
              "  ".join("n=%d %.3e" % (n, v) for n, v in zip(s["n"], s["sigE_mean"])))
    print(" A ratio(1e4/100) = %.2f   B ratio(100/1e4) = %.2f" % (sA["ratio_10000_over_100"], sB["ratio_100_over_10000"]))
    print(" B sigE*sqrt(n):", ["%.3e" % v for v in sB["sigE_x_sqrt_n"]])
    print(" C max rel spread = %.3f" % sC["max_rel_spread"])
    print("\n== re-anchored (floored instrument) ==")
    for k, v in r.items():
        print("  %-42s %s" % (k, ("%.4g" % v) if isinstance(v, float) else v))


if __name__ == "__main__":
    main()
