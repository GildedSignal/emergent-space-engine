#!/usr/bin/env python3
"""Re-anchoring the time-to-ceiling on a stated belt-mass premise (checker item 2).

The original headline ("~9 orbits to ceiling at N=1e9, m=1e-10") held per-body mass
fixed, which makes the 1e9-body belt total 0.1 M* — a disk, where the test-particle
linearization breaks. The admissible premises are:
  (a) fixed TOTAL belt mass M_belt = 2e-7 (the simulated belt's own mass):
      m = M/n and sigma^2 ~ m^2 * lam * t with lam ~ n  =>  sigma^2 ~ M^2 t / n,
      so time-to-ceiling GROWS proportional to N;
  (b) the embedded-perturber channel: lam_p = 0.1475/body/orbit has no n in it,
      so that walk (and its ceiling time) is N-independent.
This script MEASURES both scaling laws across two decades of n (plus the n=2000
anchors from hlive_sig.json) and computes the re-anchored game-scale numbers.
Instrument: Gaussian sigma (measure_sig.py's), cold belt, t=30 orbits.
Run: python3 rescale.py   (~2 min)
"""
import json, sys
import numpy as np

sys.argv = ["hlive"]
import hlive

G = hlive.G
A0, W_, SE = 2.1, 0.05, 0.01
W = 2 * W_ / A0                 # belt relative width 0.0477
T_ORB = A0 ** 1.5               # game-years per orbit (3.0432)
S_YR = 3.156e7                  # seconds per game-year
Q = 2 ** -20                    # scar quantum for the bit accounting
SQ = float(np.sqrt(2 * np.pi * np.e))  # 4.1327: Gaussian sigma -> entropy width
CAP_E = float(np.log2(W / Q))   # 15.61 uniform cap, E field
CAP_L = CAP_E                   # (checker: L-range ~ W/2, cap ~1 bit generous)
CAP_W = float(-np.log2(Q))      # 20.00 uniform cap, varpi field
CAP_TOT = 2 * CAP_E + CAP_W     # 51.22 = the belt's own element entropy


def lam_of(n):
    e_bar = SE * np.sqrt(np.pi / 2)
    return n * (A0 * 2 * e_bar) / (2 * W_) * (1.5 * (A0 * 2 * e_bar * 2 / 3) / A0)


LAM_P = 1.5 * (2 * np.pi / A0 ** 1.5) * (2 * W_) / A0  # 0.1475, n-independent


def sig_at(n, m_body, m_pert, orbits, seeds):
    """Mean sigma_E/L/W of the scar walk after `orbits` orbits, over seeds."""
    sE, sL, sW = [], [], []
    for sd in seeds:
        a, e, vp = hlive.belt(n, SE, W_, A0, sd)
        E = -G / (2 * a)
        L = np.sqrt(G * a * (1 - e ** 2))
        Ax, Ay = e * np.cos(vp), e * np.sin(vp)
        E0, L0, A0x, A0y = E.copy(), L.copy(), Ax.copy(), Ay.copy()
        rg = np.random.default_rng(sd + 777)
        lam = lam_of(n)
        for _ in range(orbits):
            for li, mi in ((lam, m_body), (LAM_P, m_pert)):
                if mi <= 0:
                    continue
                d, _ = hlive.kick_deltas(None, (a, e, E, L, Ax, Ay), mi, SE, li, A0, rg)
                if d is None:
                    continue
                E, L, Ax, Ay = E + d[0], L + d[1], Ax + d[2], Ay + d[3]
        dE, dL = E - E0, L - L0
        dvp = np.angle(Ax + 1j * Ay) - np.angle(A0x + 1j * A0y)
        dvp = (dvp + np.pi) % (2 * np.pi) - np.pi
        sE.append(dE.std() / (G / (2 * A0)))
        sL.append(dL.std() / np.sqrt(G * A0))
        sW.append(dvp.std() / (2 * np.pi))
    return [float(np.mean(x)) for x in (sE, sL, sW)], [float(np.std(x)) for x in (sE, sL, sW)]


def bits_at(sigE, sigL, sigW):
    hE = min(np.log2(max(sigE * SQ, 1e-12) / Q), CAP_E)
    hL = min(np.log2(max(sigL * SQ, 1e-12) / Q), CAP_L)
    hW = min(np.log2(max(sigW * SQ, 1e-12) / Q), CAP_W)
    return float(hE + hL + hW)


def fit_slope(ns, sigs):
    x, y = np.log2(ns), np.log2(sigs)
    return float(np.polyfit(x, y, 1)[0])


def main():
    M_BELT = 2e-7                      # n=2000 x m=1e-10, the simulated belt
    N_BIG = 1e9
    sig = json.load(open("hlive_sig.json"))
    anchor_cold = next(r for r in sig if r["case"] == "cold_m1e-10")["recs"]["30"]
    anchor_pert = next(r for r in sig if r["case"] == "pert_m1e-7")["recs"]["30"]
    anchor_cold300 = next(r for r in sig if r["case"] == "cold_m1e-10")["recs"]["300"]
    sigE_300_2000 = anchor_cold300["sigE"]   # 3.871e-4: t_ceiling anchor

    ns_scan = [100, 1000, 10000]
    seeds = {100: [1, 2, 3, 4], 1000: [1, 2, 3, 4], 10000: [1, 2]}
    out = {"W": W, "T_orb_yr": T_ORB, "cap_bits_q2m20": CAP_TOT, "scans": {}}

    # A: fixed per-body mass m=1e-10 (the original's premise, kept for the record)
    A = {n: sig_at(n, 1e-10, 0.0, 30, seeds[n]) for n in ns_scan}
    A[2000] = ([anchor_cold["sigE"], anchor_cold["sigL"], anchor_cold["sigW"]], None)
    # B: fixed total belt mass M=2e-7 -> m(n)=M/n
    B = {n: sig_at(n, M_BELT / n, 0.0, 30, seeds[n]) for n in ns_scan}
    # C: embedded perturber 1e-7 + mutual 1e-10 (the real belt with a big body)
    C = {n: sig_at(n, 1e-10, 1e-7, 30, seeds[n]) for n in ns_scan}
    C[2000] = ([anchor_pert["sigE"], anchor_pert["sigL"], anchor_pert["sigW"]], None)

    for name, D in (("A_fixed_m", A), ("B_fixed_M", B), ("C_pert", C)):
        ns = sorted(D)
        sE = [D[n][0][0] for n in ns]
        out["scans"][name] = {"n": ns, "sigE_mean": sE,
                              "sigE_std": [D[n][1][0] if D[n][1] else None for n in ns],
                              "slope_log2sigE_vs_log2n": fit_slope(ns, sE)}
    sA, sB, sC = out["scans"]["A_fixed_m"], out["scans"]["B_fixed_M"], out["scans"]["C_pert"]
    sA["ratio_10000_over_100"] = sA["sigE_mean"][-1] / sA["sigE_mean"][0]
    sB["ratio_100_over_10000"] = sB["sigE_mean"][0] / sB["sigE_mean"][-1]
    sB["sigE_x_sqrt_n"] = [s * np.sqrt(n) for s, n in zip(sB["sigE_mean"], sB["n"])]
    sC["max_rel_spread"] = (max(sC["sigE_mean"]) / min(sC["sigE_mean"]) - 1)
    # mutual contamination of the pert walk, per n
    sC["mutual_var_fraction"] = {n: (A[n][0][0] / C[n][0][0]) ** 2 for n in ns_scan}

    # --- re-anchored extrapolations -------------------------------------
    r = {}
    # t_ceiling(n, m) = t_ref * (W/sigma_E(t_ref))^2 * (m_ref/m)^2 * (n_ref/n)
    #   [sigma^2 ~ m^2 n t => ceiling when sigma = W; ceiling = walk spans belt width]
    t_ref, n_ref, m_ref, s_ref = 300, 2000, 1e-10, sigE_300_2000
    t_ceil = lambda n, m: t_ref * (W / s_ref) ** 2 * (m_ref / m) ** 2 * (n_ref / n)
    r["t_ceiling_fixed_m_1e9_orbits"] = t_ceil(N_BIG, 1e-10)       # inadmissible premise
    r["belt_mass_fixed_m_1e9_Msun"] = 1e-10 * N_BIG                # 0.1 M*: the contradiction
    r["t_ceiling_fixedM_1e9_orbits"] = t_ceil(N_BIG, M_BELT / N_BIG)
    r["t_ceiling_fixedM_1e9_years"] = t_ceil(N_BIG, M_BELT / N_BIG) * T_ORB
    r["t_ceiling_fixedM_1e9_seconds"] = r["t_ceiling_fixedM_1e9_years"] * S_YR
    r["H_live_mutual_fixedM_1e9"] = CAP_TOT / r["t_ceiling_fixedM_1e9_seconds"]
    r["H_live_mutual_fixed_m_1e9_INADMISSIBLE"] = CAP_TOT / (t_ceil(N_BIG, 1e-10) * T_ORB * S_YR)
    # perturber channel: bits(t) from sigma ~ sqrt(t), sigma ~ m_p (measured at t=30)
    sigE30p, sigL30p, sigW30p = C[2000][0]
    bits_pert = lambda t, mp=1e-7: bits_at(
        sigE30p * np.sqrt(t / 30) * mp / 1e-7,
        sigL30p * np.sqrt(t / 30) * mp / 1e-7,
        sigW30p * np.sqrt(t / 30) * mp / 1e-7)
    bt = np.array([bits_pert(t) for t in np.logspace(0, 6, 6001)])
    lts = np.logspace(0, 6, 6001)
    i90 = int(np.argmax(bt >= 0.9 * CAP_TOT)); i50 = int(np.argmax(bt >= 50.0))
    r["pert_bits_t30_q2m20"] = bits_pert(30)
    r["pert_t_orbits_at_90pct_cap"] = float(lts[i90])
    r["pert_t_orbits_at_50_bits"] = float(lts[i50])
    r["pert_t_years_at_90pct_cap"] = float(lts[i90] * T_ORB)
    r["H_live_pert_90pct"] = CAP_TOT / (lts[i90] * T_ORB * S_YR)
    # perturber mass that busts 32 bits within a 30-game-year session
    t_ses = 30.0 / T_ORB   # orbits in a 30-year session
    lo, hi = 1e-12, 1e-6
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        if bits_pert(t_ses, mid) > 32:
            hi = mid
        else:
            lo = mid
    r["m_pert_busting_32bits_in_30yr_Msun"] = float(np.sqrt(lo * hi))
    r["m_pert_in_lunar_masses"] = float(np.sqrt(lo * hi) / 3.69e-8)
    out["reanchor"] = r
    json.dump(out, open("rescale_results.json", "w"), indent=1)

    print("caps: E %.2f L %.2f W %.2f  total %.2f bits at q=2^-20" % (CAP_E, CAP_L, CAP_W, CAP_TOT))
    for name in ("A_fixed_m", "B_fixed_M", "C_pert"):
        s = out["scans"][name]
        print("\nscan %s: slope(log2 sigE / log2 n) = %+.3f" % (name, s["slope_log2sigE_vs_log2n"]))
        print("  " + "  ".join("n=%d sigE=%.3e" % (n, v) for n, v in zip(s["n"], s["sigE_mean"])))
    print("\nA ratio sigE(10000)/sigE(100) = %.2f  (predict 10 +/- 1)" % sA["ratio_10000_over_100"])
    print("B ratio sigE(100)/sigE(10000) = %.2f  (predict 10 +/- 1)" % sB["ratio_100_over_10000"])
    print("B sigE*sqrt(n):", ["%.3e" % v for v in sB["sigE_x_sqrt_n"]])
    print("C max rel spread over n = %.3f  (predict < 0.03)" % sC["max_rel_spread"])
    print("C mutual var fraction:", {n: "%.4f" % v for n, v in sC["mutual_var_fraction"].items()})
    print("\nre-anchored:")
    for k, v in r.items():
        print("  %-38s %s" % (k, ("%.4g" % v) if isinstance(v, float) else v))


if __name__ == "__main__":
    main()
