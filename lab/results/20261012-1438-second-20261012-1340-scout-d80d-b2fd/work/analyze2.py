#!/usr/bin/env python3
"""Corrected analysis v2: comparable ladder, three-class decomposition,
retained-memory cross-validation (held-out), traffic decomposition."""
import json
import numpy as np
from hlive import classify

import os
W = os.path.dirname(os.path.abspath(__file__))
d = np.load(f"{W}/perbody-T3e4.npz")
ref = np.load(f"{W}/perbody-A005.npz")
bits, cp_t, counts, D = d["bits"], d["cp_t"], d["counts"], d["D"]
n = len(D)
T = float(cp_t[-1])
out = {}

# ---- S1 ladder, shipped-gate window [T_h/16, T_h] for comparability ----
lad = {}
for Th in (1e3, 3e3, 1e4, 3e4):
    m = (cp_t >= Th / 16.0) & (cp_t <= Th * 1.0001)
    if m.sum() < 4:
        m = np.zeros_like(cp_t, bool); m[:4] = True
    ch, sat, lam, r2 = classify(bits[m], cp_t[m])
    lad[str(int(Th))] = {"frac": float(ch.mean()), "n": int(ch.sum()),
                         "idx": np.where(ch)[0].tolist()}
out["ladder"] = {k: {"frac": v["frac"], "n": v["n"]} for k, v in lad.items()}
c13, c34 = set(lad["1000"]["idx"]), set(lad["30000"]["idx"])
out["reclass_1e3_to_3e4"] = len(c13 - c34)
out["new_at_3e4"] = len(c34 - c13)
out["survivors_from_A005"] = sorted(c34 & set(ref["chaotic"].tolist()))

# ---- full-horizon classes + population histogram ----
chaotic, sat, lam_bit, r2 = classify(bits, cp_t)
b_end = bits[-1]
out["n_chaotic_3e4"] = int(chaotic.sum())
out["A005_chaotic_3e4_bits"] = {int(i): float(b_end[i]) for i in np.where(ref["chaotic"])[0]}
out["A005_chaotic_3e4_status"] = {int(i): bool(chaotic[i]) for i in np.where(ref["chaotic"])[0]}
hist = np.histogram(b_end, bins=[0, 8, 16, 24, 30, 35, 40, 42.6])[0]
out["bits_end_hist"] = {"0-8": int(hist[0]), "8-16": int(hist[1]),
                        "16-24": int(hist[2]), "24-30": int(hist[3]),
                        "30-35": int(hist[4]), "35-40": int(hist[5]),
                        "40+": int(hist[6])}
departed = (b_end >= 35.0) & ~chaotic      # macrostate-scale, flat curves
out["n_departed"] = int(departed.sum())
out["D_max_departed"] = float(D[departed].max()) if departed.any() else None
out["frac_departed_D_lt_1"] = float((D[departed] < 1).mean()) if departed.any() else None
out["frac_all_bodies_D_lt_1"] = float((D < 1).mean())
sticky = chaotic
shear = ~chaotic & ~departed

# ---- S2 spectrum ----
half = T / 2
m2 = cp_t > half
m1 = (cp_t >= T / 64) & (cp_t <= half)    # match the 1e4-window convention
slope2 = np.zeros(n); gam1 = np.zeros(n)
for i in range(n):
    y = bits[m2, i]; ok = y < 41.5
    if ok.sum() >= 3:
        slope2[i] = np.polyfit(cp_t[m2][ok], y[ok], 1)[0]
    y1 = bits[m1, i]; ok1 = y1 < 30.0
    if ok1.sum() >= 4:
        gam1[i] = np.polyfit(np.log2(cp_t[m1][ok1]), y1[ok1], 1)[0]
out["median_slope2_shear_bits_per_period"] = float(np.median(slope2[shear]))
out["median_gam1_shear"] = float(np.median(gam1[shear]))
pred_slope = gam1 / (half * np.log(2))
excess = slope2 - 3.0 * np.maximum(pred_slope, 1e-9)
hot = shear & (excess > 0) & (slope2 > 1e-4)
out["n_shear_above_3x_own_floor"] = int(hot.sum())
out["floor_bits_per_period"] = float(np.median(pred_slope[shear]))
fl = out["floor_bits_per_period"]
out["bits_at_1e6_at_floor"] = fl * 1e6

# ---- S3 boundary body (A005's top regular) ----
bi = int(np.argmax(np.where(ref["chaotic"], -1, ref["bits_end"])))
out["boundary_idx"] = bi
out["boundary_A005_bits"] = float(ref["bits_end"][bi])
out["boundary_3e4_bits"] = float(b_end[bi])
out["boundary_chaotic_3e4"] = bool(chaotic[bi])

# ---- S4 corrected: RETAINED memory cross-validation (held-out) ----
# engine sealed-scar stock per body = envelope bits / quantum (net levels)
for kb, b in enumerate((8.0, 16.0)):
    act_ret = np.floor(b_end / b)
    pred_env = gam1 * np.log2(T / half) + bits[np.searchsorted(cp_t, half) - 1]
    # gamma*log2(T_h)+c with c from the first-half last point
    pred_ret = np.floor(pred_env / b)
    ok = shear | departed | chaotic
    rx = np.argsort(np.argsort(pred_ret[ok])); ry = np.argsort(np.argsort(act_ret[ok]))
    out[f"retained_b{int(b)}"] = {
        "spearman": float(np.corrcoef(rx, ry)[0, 1]),
        "median_ratio_pred_over_act": float(np.median((pred_ret + 1) / (act_ret + 1))),
        "total_pred": int(pred_ret.sum()), "total_act": int(act_ret.sum()),
        "exact_frac": float(np.mean(pred_ret == act_ret))}

# ---- traffic decomposition (gross crossings, the event measure) ----
tr = {}
for kb, b in enumerate((8.0, 16.0)):
    for hi, hn in ((0, "h1"), (1, "h2")):
        c = counts[hi, kb]
        tr[f"b{int(b)}_{hn}"] = {
            "shear": int(c[shear].sum()), "departed": int(c[departed].sum()),
            "sticky": int(c[sticky].sum()), "all": int(c.sum()),
            "n_shear_active": int((c[shear] > 0).sum()),
            "n_dep_active": int((c[departed] > 0).sum())}
out["traffic"] = tr
out["gross_over_net_shear_b8"] = float(counts[:, 0, shear].sum() /
                                       max(np.floor(b_end[shear] / 8).sum(), 1))
# sticky per-body traffic vs lambda prediction
out["sticky_detail"] = [
    {"i": int(i), "lam_full": float(lam_bit[i]),
     "act_b8": int(counts[:, 0, i].sum()), "act_b16": int(counts[:, 1, i].sum()),
     "pred_b8_from_lam": float(lam_bit[i] * np.log2(np.e) * T / 8.0),
     "bits_end": float(b_end[i])} for i in np.where(sticky)[0]]

# ---- S6 budget: forced vs choice memory ----
forced_bits_per_body = np.where(departed, b_end, 0.0) + \
    np.where(sticky, b_end, 0.0)
out["forced_bits_total"] = float(forced_bits_per_body.sum())
out["forced_bits_per_body_avg"] = float(forced_bits_per_body.mean())
out["shear_envelope_bits_total"] = float(b_end[shear].sum())
out["shear_bits_per_body_avg"] = float(b_end[shear].mean())

with open(f"{W}/summary-analysis2.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
