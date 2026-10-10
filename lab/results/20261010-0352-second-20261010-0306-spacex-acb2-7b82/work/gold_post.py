#!/usr/bin/env python3
"""Gold post-processing: every headline number with (a) a seed band over the
6 hi-res seeds and (b) a bin-jackknife sigma on the pooled estimator; the
closed form tested as K = Lambda*W/(N*rho*sigma) (the author's closed form is
exactly K = 0.85 for sigma_e < W) with a held-out W validation; q_v* and
re-fit cadence per seed; verdict robustness across seeds.

Reads gold_*.npz written by run_gold.sh. Physics constants identical to the
shipped post_hlive.py: SCAR_BITS=336, BUDGET=64 bits/body, N0=1e4, W=0.02.
"""
import glob
import json

import numpy as np

YEAR = 3.156e7
SCAR_BITS = 336.0
BUDGET_BITS = 64.0
PLAY_RATE = 3600 * 100 / YEAR   # orbits per real hour at rtf 100
SIM_DAYS_PER_REAL_HR = 3600 * 100 / 86400.0  # 4.167
N0 = 1e4
W0 = 0.02
SIG = 0.01
RHO = 1e-4
RHOS = (1e-4, 1e-3, 1e-2)


def load(group):
    """group: list of job names -> dict of stacked arrays."""
    out = []
    for job in group:
        d = np.load(f"gold_{job}.npz")
        out.append({k: d[k] for k in ("edges", "P", "weight", "bmin", "vrel")})
    return out


def bin_coefs(edges, weight):
    centers = np.sqrt(edges[:-1] * edges[1:])
    widths = np.diff(edges)
    return 1.5 * centers * widths * weight  # c_i (per unit n1D)


def lam_of(P, coefs, W, N):
    return float(2.0 * (N / W) * np.sum(P * coefs))


def jackknife_bins(vals_per_bin):
    """Leave-one-bin-out jackknife sigma of a sum-type estimator."""
    total = np.sum(vals_per_bin)
    n = len(vals_per_bin)
    loo = total - vals_per_bin
    return float(np.sqrt((n - 1) / n * np.sum((loo - loo.mean()) ** 2)))


def r_exact_at(data, coefs, W, N, q, M, rho=RHO, drop_bin=None):
    m = M / N
    tot = 0.0
    for i in range(len(coefs)):
        if drop_bin is not None and i == drop_bin:
            continue
        kept = data["bmin"][i] > 0
        if not kept.any():
            continue
        b, v = data["bmin"][i, kept], data["vrel"][i, kept]
        dv = 2 * m / (np.maximum(b, 1e-12) * v)
        tot += np.mean((b < rho) & (dv > q)) * coefs[i]
    return 2.0 * (N / W) * tot



def main():
    res = {}
    cold = load([f"cold_k{k}" for k in range(6)])
    hot = load([f"hot_k{k}" for k in range(6)])
    w004 = load([f"w004_k{k}" for k in range(3)])
    w010 = load([f"w010_k{k}" for k in range(3)])
    conv = load(["conv_ultra"])[0]

    # ---------------- Lambda, seed band + pooled bin-jackknife -------------
    def lam_stats(group, W, rho_idx):
        lams = [lam_of(d["P"][:, rho_idx], bin_coefs(d["edges"], d["weight"]),
                       W, N0) for d in group]
        Pp = np.mean([d["P"][:, rho_idx] for d in group], axis=0)
        cp = np.mean([bin_coefs(d["edges"], d["weight"]) for d in group], axis=0)
        per_bin = Pp * cp

        jk = jackknife_bins(per_bin) * 2 * N0 / W
        pooled = float(np.sum(per_bin) * 2 * N0 / W)
        return np.array(lams), pooled, jk

    print("== Lambda per body per orbit: 6 seeds, hi-res 4000 pairs/bin ==")
    for tag, group, W in (("cold", cold, W0), ("hot", hot, W0)):
        for k, rho in enumerate(RHOS):
            lams, pooled, jk = lam_stats(group, W, k)
            print(f"  [{tag}] rho={rho:g}: seeds {lams.mean():.3f} "
                  f"+/- {lams.std(ddof=1):.3f} [{lams.min():.3f},{lams.max():.3f}]"
                  f" | pooled {pooled:.3f} bin-JK +/- {jk:.3f} "
                  f"({100*jk/pooled:.0f}%)")
            res[f"lam_{tag}_{rho:g}"] = {
                "mean": lams.mean(), "std": lams.std(ddof=1),
                "min": lams.min(), "max": lams.max(),
                "pooled": pooled, "bin_jk": jk}

    # ---------------- rho exponent ----------------------------------------
    print("\n== rho exponent (3-point log-log fit per seed) ==")
    for tag, group in (("cold", cold), ("hot", hot)):
        exps = []
        for d in group:
            lams = [lam_of(d["P"][:, k], bin_coefs(d["edges"], d["weight"]),
                           W0, N0) for k in range(3)]
            exps.append(np.polyfit(np.log(RHOS), np.log(lams), 1)[0])
        exps = np.array(exps)
        print(f"  [{tag}] exponent {exps.mean():.3f} +/- {exps.std(ddof=1):.3f} "
              f"[{exps.min():.3f},{exps.max():.3f}]")
        res[f"rho_exp_{tag}"] = {"mean": exps.mean(), "std": exps.std(ddof=1),
                                 "min": exps.min(), "max": exps.max()}

    # ---------------- <v_rel | encounter> ---------------------------------
    print("\n== <v_rel|b<1e-4> per seed + pooled bin-jackknife ==")
    for tag, group in (("cold", cold), ("hot", hot)):
        vs = [float(d["vrel"][(d["bmin"] > 0) & (d["bmin"] < RHO)].mean())
              for d in group]
        ns = [int(((d["bmin"] > 0) & (d["bmin"] < RHO)).sum()) for d in group]
        # pooled with bin-JK: encounters weighted by bin coefs (rate-weighted)
        cs = [bin_coefs(d["edges"], d["weight"]) for d in group]
        # leave-one-bin-out on the rate-weighted pooled mean
        def vbar(drop=None):
            num, den = 0.0, 0.0
            for d, c in zip(group, cs):
                for i in range(22):
                    if i == drop:
                        continue
                    sel = (d["bmin"][i] > 0) & (d["bmin"][i] < RHO)
                    num += (d["vrel"][i][sel] * c[i]).sum()
                    den += c[i] * sel.sum()
            return num / den if den else 0.0
        vp = vbar()
        jk = float(np.sqrt((22 - 1) / 22 * np.sum(
            [(vbar(i) - vp) ** 2 for i in range(22)])))
        print(f"  [{tag}] mean-of-seeds {np.mean(vs):.4f} (n_enc/seeds {ns}) "
              f"| rate-weighted pooled {vp:.4f} bin-JK +/- {jk:.4f}")
        res[f"v_{tag}"] = {"mean": np.mean(vs), "min": np.min(vs),
                           "max": np.max(vs), "pooled": vp, "bin_jk": jk,
                           "n_enc": ns}

    # ---------------- corr = R_exact / R_product at (M=1e-7, q=1e-4) -------
    print("\n== tail correlation corr = R_exact/R_product (M=1e-7, q=1e-4) ==")
    corrs = []
    for d in cold:
        co = bin_coefs(d["edges"], d["weight"])
        lam = lam_of(d["P"][:, 0], co, W0, N0)
        v_enc = float(d["vrel"][(d["bmin"] > 0) & (d["bmin"] < RHO)].mean())
        m = 1e-7 / N0
        dv_typ = 2 * m / (RHO * v_enc)
        Re = r_exact_at(d, co, W0, N0, 1e-4, 1e-7)
        Rp = lam * min(1.0, dv_typ / 1e-4)
        corrs.append(Re / Rp)
    corrs = np.array(corrs)
    corr_mean = float(corrs.mean())
    print(f"  seeds: {np.round(corrs, 3).tolist()}")
    print(f"  mean {corr_mean:.3f} +/- {corrs.std(ddof=1):.3f} "
          f"[{corrs.min():.3f},{corrs.max():.3f}]  (shipped seed point: 2.20)")
    res["corr"] = {"mean": corr_mean, "std": corrs.std(ddof=1),
                   "min": corrs.min(), "max": corrs.max(),
                   "seeds": corrs.tolist()}
    # bin-JK: per seed, leave one bin out of BOTH R_exact and R_product, then
    # average corr over seeds (thresholding seed-averaged bmin would be wrong)
    def corr_drop(drop):
        vals = []
        for d in cold:
            co = bin_coefs(d["edges"], d["weight"])
            coefs = np.delete(co, drop) if drop is not None else co
            d2 = {"bmin": (np.delete(d["bmin"], drop, axis=0)
                           if drop is not None else d["bmin"]),
                  "vrel": (np.delete(d["vrel"], drop, axis=0)
                           if drop is not None else d["vrel"]),
                  "P": (np.delete(d["P"], drop, axis=0)
                        if drop is not None else d["P"])}
            lam = lam_of(d2["P"][:, 0], coefs, W0, N0)
            v_enc = float(d2["vrel"][(d2["bmin"] > 0)
                                     & (d2["bmin"] < RHO)].mean())
            m = 1e-7 / N0
            Rp = lam * min(1.0, 2 * m / (RHO * v_enc) / 1e-4)
            Re = r_exact_at(d2, coefs, W0, N0, 1e-4, 1e-7)
            vals.append(Re / Rp)
        return float(np.mean(vals))

    corr_pool = corr_drop(None)
    jk = float(np.sqrt(21 / 22 * np.sum([(corr_drop(i) - corr_pool) ** 2
                                         for i in range(22)])))
    print(f"  seed-mean with bin-JK: {corr_pool:.3f} +/- {jk:.3f}")
    res["corr"]["pooled"] = corr_pool
    res["corr"]["bin_jk"] = jk

    # ---------------- W scaling: K = Lambda W/(N rho sigma) ---------------
    print("\n== W-scaling: K(W) = Lambda*W/(N*rho*sigma); closed form says "
          "K = 0.85 ==")
    Ks = {}
    for tag, group, W in (("W=0.02", cold, W0), ("W=0.04", w004, 0.04),
                          ("W=0.1", w010, 0.1)):
        lams = np.array([lam_of(d["P"][:, 0], bin_coefs(d["edges"], d["weight"]),
                                W, N0) for d in group])
        K = lams * W / (N0 * RHO * SIG)
        Ks[W] = K
        print(f"  {tag}: Lambda {lams.mean():.3f}+/-{lams.std(ddof=1):.3f} "
              f"-> K {K.mean():.3f} [{K.min():.3f},{K.max():.3f}] "
              f"(closed form 0.85: {'OK' if abs(K.mean()-0.85)<0.26 else 'MISS'})")
        res[f"K_{W}"] = {"mean": K.mean(), "std": K.std(ddof=1),
                         "min": K.min(), "max": K.max()}
    rK = Ks[0.1].mean() / Ks[W0].mean()
    print(f"  K(0.1)/K(0.02) = {rK:.2f}  -> 1/W scaling "
          f"{'KILLED' if rK > 1.5 else 'SURVIVES'} as an adoption path")
    res["K_ratio_01_002"] = rK
    # log-fit on W=0.02 and W=0.1, predict held-out W=0.04
    x = np.log(np.array([W0, 0.1]) / SIG)
    y = np.array([Ks[W0].mean(), Ks[0.1].mean()])
    b = (y[1] - y[0]) / (x[1] - x[0])
    a = y[0] - b * x[0]
    pred04 = a + b * np.log(0.04 / SIG)
    meas04 = Ks[0.04].mean()
    print(f"  log-fit K = {a:.3f} + {b:.3f}*ln(W/sigma): predicts K(0.04)="
          f"{pred04:.3f}, measured {meas04:.3f} "
          f"({'validated' if abs(pred04-meas04) < 2*Ks[0.04].std(ddof=1)+0.15 else 'NOT validated'})")
    res["logfit"] = {"a": a, "b": b, "pred_K004": pred04,
                     "meas_K004": meas04}

    # ---------------- convergence control ----------------------------------
    lam_conv = lam_of(conv["P"][:, 0], bin_coefs(conv["edges"], conv["weight"]),
                      W0, N0)
    lam_hi_cold = res["lam_cold_0.0001"]["mean"]
    lam_hi_k0 = lam_of(cold[0]["P"][:, 0],
                       bin_coefs(cold[0]["edges"], cold[0]["weight"]), W0, N0)
    ladder = [("shipped 128/12/4", 0.4018), ("hires 512/24/6", lam_hi_k0),
              ("ultra 2048/48/8", lam_conv)]
    import os
    if os.path.exists("gold_conv_xhi.npz"):
        dx = np.load("gold_conv_xhi.npz")
        ladder.append(("xhi 8192/96/10",
                       lam_of(dx["P"][:, 0],
                              bin_coefs(dx["edges"], dx["weight"]), W0, N0)))
    print("\n== convergence ladder, SAME seed k0 (instrument only changes) ==")
    prev = None
    for name, v in ladder:
        step = f" (+{100*(v/prev-1):.1f}%)" if prev else ""
        print(f"  {name:18s} Lambda(1e-4) = {v:.4f}{step}")
        prev = v
    print(f"  hi-res 6-seed mean {lam_hi_cold:.3f} +/- "
          f"{res['lam_cold_0.0001']['std']:.3f}; bin-JK +/-35%")
    res["convergence"] = {"ladder": ladder, "hires_mean": lam_hi_cold}

    # ------------- design table + q_v* + cadence, per seed -----------------
    print("\n== design table (bits/body/hr at rtf 100): median [min,max] "
          "over 6 seeds ==")

    def qstar_and_bits(seed_idx, M):
        d = cold[seed_idx]
        co = bin_coefs(d["edges"], d["weight"])
        lam = lam_of(d["P"][:, 0], co, W0, N0)
        v_enc = float(d["vrel"][(d["bmin"] > 0) & (d["bmin"] < RHO)].mean())
        corr = corrs[seed_idx]

        def R(N, q):
            m = M / N
            lam_N = lam * N / N0
            cf = corr * 1.7 * M * SIG / (W0 * v_enc * q)
            return min(lam_N, max(r_exact_at(d, co, W0, N, q, M), cf))

        bits = {q: R(1e9, q) * PLAY_RATE * SCAR_BITS
                for q in (2.0 ** -32, 1e-6, 1e-5, 1e-4)}
        lo, hi = 1e-12, 1e-2
        for _ in range(200):
            mid = np.sqrt(lo * hi)
            if R(1e9, mid) * PLAY_RATE * SCAR_BITS > BUDGET_BITS:
                lo = mid
            else:
                hi = mid
        qs = np.sqrt(lo * hi)
        T = 0.38 / R(1e9, 1e-5) if R(1e9, 1e-5) > 0 else np.inf
        return bits, qs, T

    for M in (1e-7, 1e-5):
        allbits = {q: [] for q in (2.0 ** -32, 1e-6, 1e-5, 1e-4)}
        qss, Ts = [], []
        for s in range(6):
            bits, qs, T = qstar_and_bits(s, M)
            for q in allbits:
                allbits[q].append(bits[q])
            qss.append(qs)
            Ts.append(T)
        for q in allbits:
            arr = np.array(allbits[q])
            verdict = "FITS" if arr.max() < BUDGET_BITS else "BREAKS"
            print(f"  M={M:.0e} q={q:.2e}: bits(1e9) "
                  f"{np.median(arr):.3g} [{arr.min():.3g},{arr.max():.3g}] "
                  f"-> {verdict} (budget {BUDGET_BITS:.0f})")
            res[f"bits_{M:.0e}_{q:.2e}"] = {"median": np.median(arr),
                                            "min": arr.min(), "max": arr.max()}
        qss = np.array(qss)
        Ts = np.array(Ts)
        print(f"  M={M:.0e}: q_v* median {np.median(qss):.3g} "
              f"[{qss.min():.3g},{qss.max():.3g}] v_K "
              f"({np.median(qss)*29.8e3:.3g} m/s at 1 AU)")
        print(f"       re-fit cadence (q=1e-5): median {np.median(Ts):.3g} "
              f"orbits = {np.median(Ts)*YEAR/86400:.3g} sim-days "
              f"= {np.median(Ts)*YEAR/86400/SIM_DAYS_PER_REAL_HR:.2f} real h "
              f"[{Ts.min()*YEAR/86400:.3g},{Ts.max()*YEAR/86400:.3g}] sim-days")
        res[f"qstar_{M:.0e}"] = {"median": np.median(qss), "min": qss.min(),
                                 "max": qss.max()}
        res[f"T_refit_{M:.0e}"] = {"median": np.median(Ts), "min": Ts.min(),
                                   "max": Ts.max()}

    # player floor (unchanged arithmetic, hi-res v_enc)
    v_enc_c = res["v_cold"]["mean"]
    for M in (1e-7, 1e-5):
        dv997 = 2 * (M / N0) / (RHO / 20 * v_enc_c)
        print(f"  player floor M={M:.0e}: strongest 1-in-400 kick "
              f"{dv997:.3g} v_K = {dv997*29.8:.3g} km/s; "
              f"floor/q_v* = {dv997/np.median(res[f'qstar_{M:.0e}']['median']):.0f}x")
        res[f"floor_{M:.0e}"] = dv997

    json.dump(res, open("gold_post.json", "w"), indent=1, default=float)
    print("\nwrote gold_post.json")


if __name__ == "__main__":
    main()
