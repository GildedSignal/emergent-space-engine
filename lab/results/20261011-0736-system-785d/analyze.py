"""Analyze scans against the certificate. Writes metrics.json and prints tables."""
import json
import numpy as np

OUT = "/home/glmlab/actions-runner/_work/emergent-space-engine/lab-2/lab/results/20261011-0736-system-785d"
NSEED = 8

quad = json.load(open(OUT + "/quad.json"))
cases = [("j1", 1, 3e-4), ("j1", 1, 1e-3), ("j1", 1, 3e-3), ("j2", 2, 3e-4), ("j2", 2, 1e-3)]
metrics = {"per_case": {}, "P1_violations": [], "P4a_violations": []}

for tag, j, mu in cases:
    S = np.load(OUT + ("/scan-j%d-mu%g.npy" % (j, mu)), allow_pickle=True).item()
    q = quad["j%d_mu%g" % (j, mu)]
    dgrid = np.array(S["dgrid"]); a1l = np.array(S["a1"])
    qgrid = np.array(S["qgrid"]); Tage = np.array(S["Tage"]); band = np.array(S["band"])
    thnet = np.array(S["theta_net"]); thamp = np.array(S["theta_amp"])
    T = S["T"]
    cert = {}
    for i, d in enumerate(dgrid):
        v = q["%+.5f" % d]
        cert[i] = {"pdot": v["pdot_coh"], "thdot": v["thdot"],
                   "exc": 2 * v["pdot_coh"] / abs(v["thdot"]) if v["thdot"] != 0 else np.inf}
    rows = []
    Fs = []
    for i, d in enumerate(dgrid):
        sl = slice(i * NSEED, (i + 1) * NSEED)
        circ = np.abs(thnet[sl]) > 2 * np.pi
        b_med = float(np.median(band[sl]))
        F_med = float(np.median(band[sl][circ] / cert[i]["exc"])) if circ.any() else np.nan
        if circ.any():
            Fs.append((d, float(np.median(band[sl][circ] / cert[i]["exc"]))))
            for s in np.nonzero(circ)[0]:
                F = band[sl][s] / cert[i]["exc"]
                if not (0.3 <= F <= 3.0):
                    metrics["P1_violations"].append(
                        {"case": tag, "mu": mu, "d": float(d), "F": float(F)})
        rows.append({"d": float(d), "band_med": b_med, "cert_exc": cert[i]["exc"],
                     "circ_frac": float(circ.mean()), "F_med": F_med,
                     "failfrac_q10": float(np.mean(Tage[5, sl] > 0)),
                     "emax_med": float(np.median(np.array(S["emax"])[sl]))})
    # P3: kappa at exact resonance for each q_e (linearity check)
    i0 = len(dgrid) // 2
    sl0 = slice(i0 * NSEED, (i0 + 1) * NSEED)
    pdot0 = cert[i0]["pdot"]
    kappas = {}
    for qi, qe in enumerate(qgrid):
        tf = Tage[qi, sl0]
        tf = tf[tf > 0]
        if tf.size:
            kappas["%.4f" % qe] = float(np.median(tf) / (qe / pdot0))
    # P4a: failures where cert excursion < q_e/2
    for qi, qe in enumerate(qgrid):
        for i, d in enumerate(dgrid):
            sl = slice(i * NSEED, (i + 1) * NSEED)
            fails = np.nonzero(Tage[qi, sl] > 0)[0]
            if fails.size and cert[i]["exc"] < qe / 2:
                metrics["P4a_violations"].append(
                    {"case": tag, "mu": mu, "d": float(d), "q_e": float(qe),
                     "exc": cert[i]["exc"], "n_fail": int(fails.size)})
    # P4c: boundary map
    bmap = []
    for qi, qe in enumerate(qgrid):
        fail_ds = [abs(dgrid[i]) for i in range(len(dgrid))
                   if np.any(Tage[qi, i * NSEED:(i + 1) * NSEED] > 0)]
        meas = max(fail_ds) if fail_ds else -1.0
        # predicted boundary: smallest |d| with cert exc >= qe, interp in log-log
        ex = np.array([cert[i]["exc"] for i in range(len(dgrid))])
        dd = np.abs(dgrid)
        pred = -1.0
        if np.any(ex >= qe):
            idx = np.nonzero(ex >= qe)[0]
            # interpolate between idx[0]-1 and idx[0] on |d| (ex decreasing in |d|)
            i1 = idx[0]
            if i1 == 0:
                pred = dd[0]
            else:
                e0_, e1_ = np.log(ex[i1 - 1]), np.log(ex[i1])
                pred = np.exp(np.log(dd[i1 - 1]) + (np.log(qe) - e0_) * (np.log(dd[i1]) - np.log(dd[i1 - 1])) / (e1_ - e0_))
        bmap.append({"q_e": float(qe), "meas_maxd": float(meas), "pred_maxd": float(pred)})
    # P5: asymmetry at matched |d| (largest with both signs, circulating)
    asym = None
    for k in range(1, len(dgrid) // 2):
        im, ip = len(dgrid) // 2 - k, len(dgrid) // 2 + k
        cm = np.abs(thnet[im * NSEED:(im + 1) * NSEED]) > 2 * np.pi
        cp = np.abs(thnet[ip * NSEED:(ip + 1) * NSEED]) > 2 * np.pi
        if cm.any() and cp.any():
            r_meas = np.median(band[ip * NSEED:(ip + 1) * NSEED][cp]) / np.median(band[im * NSEED:(im + 1) * NSEED][cm])
            r_cert = cert[ip]["exc"] / cert[im]["exc"]
            asym = {"d": float(abs(dgrid[im])), "ratio_meas_band+": float(r_meas),
                    "ratio_cert": float(r_cert)}
            break
    metrics["per_case"]["%s_mu%g" % (tag, mu)] = {
        "rows": rows, "kappas_exact": kappas, "boundary_map": bmap, "asym": asym,
        "Edrift": S["Edrift"], "T": T, "wall_s": S["wall_s"],
        "F_med_overall": float(np.median([f for _, f in Fs])),
        "F_min": float(np.min([f for _, f in Fs])), "F_max": float(np.max([f for _, f in Fs])),
    }
    print("\n=== %s mu=%g  (pdot_exact=%.3g)  F: med=%.2f min=%.2f max=%.2f" %
          (tag, mu, pdot0, np.median([f for _, f in Fs]), np.min([f for _, f in Fs]),
           np.max([f for _, f in Fs])))
    print("  d       band   cert_exc  F_med  circ  fail(q10)")
    for r in rows:
        print("  %+.4f  %.4f  %.4f  %5.2f  %.2f  %.2f" %
              (r["d"], r["band_med"], r["cert_exc"], r["F_med"] if r["F_med"] == r["F_med"] else -1,
               r["circ_frac"], r["failfrac_q10"]))
    print("  kappa(q_e) at exact:", {k: round(v, 2) for k, v in kappas.items()})
    print("  boundary map (q_e, meas, pred):",
          [(round(b["q_e"], 3), round(b["meas_maxd"], 4), round(b["pred_maxd"], 4))
           for b in bmap if b["pred_maxd"] > 0])
    if asym:
        print("  asymmetry at |d|=%.4f: meas %.2f vs cert %.2f" %
              (asym["d"], asym["ratio_meas_band+"], asym["ratio_cert"]))

json.dump(metrics, open(OUT + "/metrics.json", "w"), indent=1)
print("\nP1 violations:", len(metrics["P1_violations"]))
print("P4a violations:", len(metrics["P4a_violations"]))
