#!/usr/bin/env python3
"""Analysis for the second-author decisive run: horizon ladder, rate
spectrum, boundary body, and the held-out scar cross-validation."""
import json
import numpy as np
from hlive import classify

import os
HERE = os.path.dirname(os.path.abspath(__file__))
W = f"{HERE}"
d = np.load(f"{W}/perbody-T3e4.npz")
ref = np.load(f"{W}/perbody-A005.npz")
bits, cp_t, counts, D = d["bits"], d["cp_t"], d["counts"], d["D"]
n = len(D)
T = cp_t[-1]
BST = (8.0, 16.0)
out = {}

# ---------- cross-check vs shipped record at ~1e4 ----------
j1e4 = np.searchsorted(cp_t, 1e4)
delta = bits[j1e4] - ref["bits_end"]
out["bits_at_1e4_vs_A005_median_abs_diff"] = float(np.median(np.abs(delta)))
out["bits_at_1e4_vs_A004_max_abs_diff"] = float(np.abs(delta).max())

# ---------- S1: horizon ladder ----------
lad = {}
prev_idx = None
for Th in (1e3, 3e3, 1e4, 3e4):
    m = cp_t <= Th * 1.0001
    if m.sum() < 6:
        m[:6] = True
    ch, sat, lam, r2 = classify(bits[:m.sum()], cp_t[:m.sum()])
    lad[str(int(Th))] = {"frac_chaotic": float(ch.mean()),
                         "n_chaotic": int(ch.sum()),
                         "idx": np.where(ch)[0].tolist()}
c1e3 = set(lad["1000"]["idx"]); c3e4 = set(lad["30000"]["idx"])
out["ladder"] = {k: {kk: vv for kk, vv in v.items() if kk != "idx"}
                 for k, v in lad.items()}
out["ladder_reclass_1e3_to_3e4"] = len(c1e3 - c3e4)
out["ladder_new_chaotic_at_3e4"] = len(c3e4 - c1e3)
out["ladder_idx_1e3"] = sorted(c1e3)
out["ladder_idx_3e4"] = sorted(c3e4)

# final classes (full horizon) drive the rest
chaotic, sat, lam_bit, r2 = classify(bits, cp_t)
reg = ~chaotic
out["n_chaotic_3e4"] = int(chaotic.sum())
out["lam_bit_range_chaotic"] = [float(lam_bit[chaotic].min()),
                                float(lam_bit[chaotic].max())]
out["lyap_range_periods"] = [1.0 / float(lam_bit[chaotic].max()),
                             1.0 / float(lam_bit[chaotic].min())] \
    if lam_bit[chaotic].min() > 0 else None
out["D_max_chaotic"] = float(D[chaotic].max()) if chaotic.any() else None

# ---------- S3: boundary body ----------
bleak = np.where(~ref["chaotic"] & (ref["bits_end"] > 40))[0]
out["boundary_body_A005_idx"] = bleak.tolist()
out["boundary_body_bits_end_3e4"] = [float(bits[-1, i]) for i in bleak]
out["boundary_body_chaotic_3e4"] = [bool(chaotic[i]) for i in bleak]
out["boundary_body_D"] = [float(D[i]) for i in bleak]

# ---------- S2: rate spectrum ----------
half = T / 2.0
m2 = cp_t > half
slope2 = np.zeros(n)
for i in range(n):
    y = bits[m2, i]
    ok = y < 42.5 - 1.0
    if ok.sum() >= 3:
        slope2[i] = np.polyfit(cp_t[m2][ok], y[ok], 1)[0]
# first-half log-fit alpha
m1 = (cp_t > 0) & (cp_t <= half)
alpha1 = np.zeros(n)
for i in range(n):
    y = bits[m1, i]
    ok = y < 42.5 - 1.0
    if ok.sum() >= 4:
        alpha1[i] = np.polyfit(np.log2(cp_t[m1][ok]), y[ok], 1)[0]
pred_slope = np.where(alpha1 > 0, alpha1 / (half * np.log(2)), 0.0)
out["median_slope2_regular_bits_per_period"] = float(np.median(slope2[reg]))
out["median_pred_log_slope_regular"] = float(np.median(pred_slope[reg]))
excess = slope2 - 3.0 * pred_slope
hot = reg & (excess > 0) & (slope2 > 1e-4)
out["n_regular_above_3x_log_floor"] = int(hot.sum())
out["frac_regular_above_3x_log_floor"] = float(hot.mean()) if reg.any() else 0.0
k = hot.sum(); N = reg.sum()
out["binom95_upper_frac_hidden_exp_among_regular"] = (
    3.0 / N if k == 0 else float(1 - 0.05 ** (1.0 / N)))
out["floor_bits_per_period"] = float(np.median(pred_slope[reg]))
# projection arithmetic at the floor
fl = out["floor_bits_per_period"]
out["bits_at_1e6_if_at_floor"] = fl * 1e6
out["slope1e4_vs_3e4_ratio_regular"] = float(
    np.median(alpha1[reg]) / max(np.median(slope2[reg]) * half * np.log(2), 1e-12))

# ---------- S4/S5: scar cross-validation ----------
m1c = (cp_t > 0) & (cp_t <= half)
lam1 = np.zeros(n)      # first-half slope, bits/period
khat = np.zeros(n)      # log-model drift coefficient, 1/periods
for i in range(n):
    y = bits[m1c, i]; t = cp_t[m1c]
    ok = y < 42.5 - 1.0
    if ok.sum() >= 4:
        lam1[i] = np.polyfit(t[ok], y[ok], 1)[0]
        tl, yl = t[ok][-1], y[ok][-1]
        khat[i] = (2 ** yl - 1) / tl
exp1 = lam1 >= 1e-3     # first-half exponential candidates
T2 = T - half
pred = {0: np.zeros(n), 1: np.zeros(n)}
for kb, b in enumerate(BST):
    pred[kb] = np.where(exp1, lam1 * T2 / b, khat * T2 / 2 ** b)
act = {kb: counts[1, kb].astype(float) for kb in (0, 1)}
def spear(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])
s4 = {}
for kb, b in enumerate(BST):
    s4[f"b{int(b)}"] = {
        "spearman_all": spear(pred[kb], act[kb]),
        "spearman_regular": spear(pred[kb][reg], act[kb][reg]),
        "pred_total_exp": float(pred[kb][chaotic].sum()),
        "act_total_exp": float(act[kb][chaotic].sum()),
        "pred_total_reg": float(pred[kb][reg].sum()),
        "act_total_reg": float(act[kb][reg].sum()),
    }
out["S4"] = s4
# S5 ratios
rat_act = np.zeros(n); rat_pred = np.zeros(n)
okr = act[0] + act[1] > 0
rat_act[okr] = (act[0][okr] + 1) / (act[1][okr] + 1)
okp = pred[0] + pred[1] > 0
rat_pred[okp] = (pred[0][okp] + 1) / (pred[1][okp] + 1)
out["S5"] = {
    "median_ratio_actual_regular": float(np.median(rat_act[reg & okr])) if (reg & okr).any() else None,
    "median_ratio_actual_chaotic": float(np.median(rat_act[chaotic & okr])) if (chaotic & okr).any() else None,
    "median_ratio_pred_regular": float(np.median(rat_pred[reg & okp])) if (reg & okp).any() else None,
    "n_chaotic_with_any_scar": int((chaotic & okr).sum()),
}
# S6 budget
s6 = {}
for kb, b in enumerate(BST):
    fe = act[kb][chaotic].sum() * b / 8.0
    ftot = act[kb].sum() * b / 8.0
    s6[f"b{int(b)}"] = {"forced_bytes": fe, "total_bytes": ftot,
                        "forced_share": float(fe / ftot) if ftot > 0 else None}
out["S6"] = s6
# per-body table for the exponential class
out["exp_class"] = [
    {"i": int(i), "D": float(D[i]), "lam1": float(lam1[i]),
     "lam_full": float(lam_bit[i]),
     "pred8": float(pred[0][i]), "act8": float(act[0][i]),
     "pred16": float(pred[1][i]), "act16": float(act[1][i])}
    for i in np.where(chaotic)[0]]
# sanity: same-body D vs A005 chaotic
out["A005_chaotic_idx"] = np.where(ref["chaotic"])[0].tolist()
out["A005_lam_range"] = [float(ref["lam_bit"][ref["chaotic"]].min()),
                         float(ref["lam_bit"][ref["chaotic"]].max())]

with open(f"{W}/summary-analysis.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k2: v2 for k2, v2 in out.items()
                  if k2 not in ("ladder_idx_1e3", "ladder_idx_3e4", "exp_class")},
                 indent=1))
print("exp_class:", json.dumps(out["exp_class"], indent=1))
