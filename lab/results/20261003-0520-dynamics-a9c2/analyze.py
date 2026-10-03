#!/usr/bin/env python3
"""Analyse results.npz against predictions.md.  Everything per-orbit."""
import json
import numpy as np

KS = [1, 2, 4, 8, 16, 32, 64]
WINDOW = 32

d = np.load("results.npz")
grid = d["grid"]
mu = grid[:, 0]
det = grid[:, 3]              # detuning in units of W (last col = far control ~20W)
N = len(grid)

def metrics(name):
    e_s = d[f"{name}__e_s"]; phi_s = d[f"{name}__phi_s"]; lam = d[f"{name}__lam"][:, 10:]  # discard twin warmup
    up = np.unwrap(phi_s, axis=1)
    wind = np.abs(up[:, -1] - up[:, 0])
    j = np.arange(up.shape[1])[None, :]
    slope = (up[:, -1] - up[:, 0]) / (up.shape[1] - 1)
    detr = up - up[:, :1] - slope[:, None] * j
    amp = np.max(detr, axis=1) - np.min(detr, axis=1)
    regime = np.where(wind < 2 * np.pi, 1, 0)          # 1 = librate
    nz = lam != 0
    lmean = np.where(nz.any(axis=1), np.divide(lam.sum(axis=1), np.maximum(nz.sum(axis=1), 1)), 0.0)
    # windowed lambda: mean of nonzero entries per window
    nw = lam.shape[1] // WINDOW
    lw = np.full((N, nw), np.nan)
    for w in range(nw):
        blk = lam[:, w * WINDOW:(w + 1) * WINDOW]
        nz = blk != 0
        cnt = nz.sum(axis=1)
        lw[:, w] = np.divide(blk.sum(axis=1), np.maximum(cnt, 1)) * (cnt > 0)
    return e_s, regime, amp, lmean, lw

e_ref, reg_ref, amp_ref, lam_ref, lw_ref = metrics("truth")
e_l16, reg_l16, amp_l16, lam_l16, lw_l16 = metrics("layer16")

# floor and threshold from far controls / low percentiles
floor = np.percentile(lam_ref, 10)
theta = 10 * max(floor, 1e-6)
hot = lam_ref >= theta

# K* per config
emax_ref = e_ref.max(axis=1)
Kstar = np.full(N, 999)
gate_tab = {}
for K in KS:
    e_k, reg_k, amp_k, _, _ = metrics(f"lay{K}")
    emax_k = e_k.max(axis=1)
    pump = emax_k / np.maximum(emax_ref, 1e-9)
    ok = np.where(emax_ref <= 0.05,
                  np.abs(emax_k - emax_ref) <= 0.03,
                  (pump >= 0.8) & (pump <= 1.25))
    ok &= (reg_k == reg_ref)
    gate_tab[K] = ok
    first = ok & (Kstar == 999)
    Kstar[first] = K
unmeet = Kstar == 999

def auc(score, label):
    """Mann-Whitney AUC of score predicting boolean label."""
    if label.sum() == 0 or label.sum() == len(label):
        return float("nan")
    pos = score[label]; neg = score[~label]
    order = np.concatenate([pos, neg])
    ranks = np.argsort(np.argsort(order)) + 1.0
    rp = ranks[:len(pos)]
    return float((rp.sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))

# toggles of windowed lambda across theta (only meaningful series)
def toggles(lw):
    tg = np.zeros(N, int)
    for i in range(N):
        s = lw[i]
        s = s[np.isfinite(s)]
        if len(s) < 4:
            continue
        b = (s >= theta).astype(int)
        tg[i] = int(np.abs(np.diff(b)).sum())
    return tg
tg_ref = toggles(lw_ref)

# static rule: inside +-W
inside = np.abs(det) <= 1.0

def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

rep = {}
rep["n_configs"] = N
rep["floor_lambda"] = float(floor)
rep["theta"] = float(theta)
rep["n_hot"] = int(hot.sum())
rep["n_unmeetable"] = int(unmeet.sum())
rep["n_esc"] = int(d["truth__esc"].sum() + d["truth__col"].sum())

# P1
far = np.abs(det) >= 2.0
rep["P1_far_hot"] = int((hot & far).sum())
rep["P1_far_lambda_max"] = float(lam_ref[far].max())
rep["P1_inband_hot"] = int((hot & inside).sum())
for m in sorted(set(mu)):
    sel = mu == m
    rep[f"P1_hot_mu{m:g}"] = int((hot & sel).sum())
    rep[f"P1_width_mu{m:g}"] = float(np.abs(det[hot & sel]).max()) if (hot & sel).any() else 0.0

# P2
quiet = ~hot
rep["P2_quiet_frac_Kle8"] = float((Kstar[quiet] <= 8).mean())
rep["P2_hot_frac_Kge32_or_unmeet"] = float(((Kstar[hot] >= 32) | unmeet[hot]).mean())
rep["P2_inband_Kle8"] = int((inside & (Kstar <= 8)).sum())
rep["P2_out_unmeet_mu_ge1e-3"] = int((~inside & unmeet & (mu >= 1e-3)).sum())
rep["P2_quiet_frac_unmeet"] = float(unmeet[quiet].mean())
rep["P2_hot_frac_unmeet"] = float(unmeet[hot].mean())
rep["Kstar_table"] = {f"{m:g}": [int(Kstar[(mu == m) & (np.abs(det) < 5) & (det >= -2) & (det <= 2)][i])
                                 for i in range(len(Kstar[(mu == m) & (det >= -2) & (det <= 2)]))]
                      for m in sorted(set(mu))}

# P3
ab = lam_ref > 3 * floor
rep["P3_spearman_abovefloor"] = spearman(lam_l16[ab & (lam_l16 > 0)], lam_ref[ab]) if (ab & (lam_l16 > 0)).sum() > 3 else float("nan")
rep["P3_spearman_all"] = spearman(lam_l16, lam_ref)
rep["P3_auc_lambda_layer_vs_unmeet"] = auc(lam_l16, unmeet)
rep["P3_auc_static_vs_unmeet"] = auc(inside.astype(float), unmeet)

# P4
tg_hot = tg_ref[hot]
rep["P4_frac_hot_toggle_ge3"] = float((tg_hot >= 3).mean())
rep["P4_max_toggle_quiet"] = int(tg_ref[quiet].max())
rep["P4_median_toggle_hot"] = float(np.median(tg_hot)) if len(tg_hot) else float("nan")

# P5
sel = mu == 3e-5
rep["P5_all_Kle8"] = bool((Kstar[sel] <= 8).all())
rep["P5_all_floor"] = bool((lam_ref[sel] <= 3 * floor).all())

with open("summary.json", "w") as f:
    json.dump(rep, f, indent=1)
for k, v in rep.items():
    if k != "Kstar_table":
        print(f"{k}: {v}")
print("Kstar by mu (detunings -2..2 in thirds of W):")
for k, v in rep["Kstar_table"].items():
    print(f"  mu={k}: {v}")
