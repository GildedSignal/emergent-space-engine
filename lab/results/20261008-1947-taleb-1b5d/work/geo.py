#!/usr/bin/env python3
"""Per-pair analysis: is the measured partner rank explained by the geometric
mean-longitude displacement at conjunction (Kepler M-f offset at Binet
crossings), and would any a-concentration trigger see these cases coming?"""
import json, sys
import numpy as np
sys.path.insert(0, '.')
from probe import truth, TAU

def analyze(name, N, T_periods, rho, spp, e_base, w_mode, sig_a, lam_mode, seed):
    rng = np.random.default_rng(seed)
    a = 1.0 + sig_a * (rng.random(N) - 0.5)
    e = np.full(N, e_base)
    idx = np.arange(N)
    if w_mode == "uniform":
        w = rng.uniform(0, TAU, N)
    else:
        w = np.where(idx < N // 2, 0.0, np.pi)
    M0 = rng.uniform(0, TAU, N) if lam_mode == "uniform" else None
    enc, dt, _ = truth(a, e, w, M0, T_periods * TAU, rho, spp)
    lam0 = (M0 + w) % TAU
    nn = a ** -1.5
    rows = []
    for (i, j), (t, d) in enc.items():
        dls = abs((lam0[j] + nn[j] * t - lam0[i] - nn[i] * t + np.pi) % TAU - np.pi)
        dl0 = abs((lam0[j] - lam0[i] + np.pi) % TAU - np.pi)
        di = np.abs((lam0 - lam0[i] + np.pi) % TAU - np.pi)
        r = 1 + int((di < dl0).sum())
        rows.append((dl0, dls, r))
    rows = np.array(rows)
    pred_rank = rows[:, 1] / (2 * np.pi) * N  # uniform-lambda prediction
    return {
        "name": name, "n": len(rows),
        "dlambda_star_p50": float(np.percentile(rows[:, 1], 50)),
        "dlambda_star_max": float(rows[:, 1].max()),
        "pred_rank_p50": float(np.percentile(pred_rank, 50)),
        "measured_rank_p50": float(np.percentile(rows[:, 2], 50)),
        "corr_rank_vs_pred": float(np.corrcoef(rows[:, 2], pred_rank)[0, 1]) if len(rows) > 2 else None,
        "frac_dlstar_gt_1spacing": float((rows[:, 1] > 2 * np.pi / N).mean()),
    }

if __name__ == "__main__":
    out = []
    for spec in [
        ("B_e06_s1", 256, 2, 0.001, 16384, 0.6, "uniform", 0.0001, "uniform", 1),
        ("B_e08_s1", 256, 2, 0.001, 32768, 0.8, "uniform", 0.0001, "uniform", 1),
        ("D_battle_s1", 256, 2, 0.001, 16384, 0.4, "two_cluster", 0.0001, "uniform", 1),
    ]:
        r = analyze(*spec)
        print(json.dumps(r))
        out.append(r)
    with open("results_geo.json", "w") as f:
        json.dump(out, f, indent=1)
