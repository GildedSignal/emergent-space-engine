import json, glob
import numpy as np

def load(tag):
    return json.load(open(f"{tag}.json"))

rows = {}
for tag in sorted(glob.glob("*.json")):
    if tag in ("metrics.json", "metrics-check.json"):
        continue
    d = load(tag[:-5])
    if "snaps" not in d:
        continue
    rows[d["tag"]] = d

# smoothed exponent fit per run (on smx snapshots)
def smfit(d):
    xs = np.array([r["t"] for r in d["snaps"]], float)
    ys = np.array([r.get("smx", 0) for r in d["snaps"]], float)
    sel = (xs > xs[-1] * 0.3) & (ys > 0)
    return float(np.polyfit(np.log(xs[sel]), np.log(ys[sel]), 1)[0]) if sel.sum() > 4 else None

M = {}
b = rows["belt_s1"]
# 1. mechanism: rate ratios across grids
n = b["xings_per_po_naive"]
M["ratio_16_12"] = n["bits16"]["med"] / max(1e-9, n["bits12"]["med"])
M["ratio_12_8"] = n["bits12"]["med"] / max(1e-9, n["bits8"]["med"])
M["ratio_8_4"] = n["bits8"]["med"] / max(1e-9, n["bits4"]["med"])
M["fit_naive_bits16_belt"] = b["exponent_fits"]["bits16"]
# 2. half-lives
M["halflife_po"] = b["halflife_po"]
# 3. residual rates and fits
for tag in ("belt_s1", "belt_s2", "ring21_s1", "ring21_s2", "ringoff_s1", "ringoff_s2"):
    M[f"smoothed_med16_{tag}"] = rows[tag]["xings_per_po_smoothed_bits16"]["med"]
    M[f"smoothed_fit_{tag}"] = smfit(rows[tag])
M["res_ratio_ring21_vs_off"] = (M["smoothed_med16_ring21_s1"] + M["smoothed_med16_ring21_s2"]) / max(
    1e-9, M["smoothed_med16_ringoff_s1"] + M["smoothed_med16_ringoff_s2"])
# 4. tail
sm = b["xings_per_po_smoothed_bits16"]
M["tail_p99_med_smoothed_belt"] = sm["p99"] / max(1e-9, sm["med"])
M["top1pct_share_belt"] = b["per_band"].get("offres", {}).get("top1pct_share")
M["tail_max_med_smoothed_belt"] = sm["max"] / max(1e-9, sm["med"])
# per-band residual is naive-based; record band contrast naive for completeness
M["band_med16_xings"] = {k: v["xings_per_po"]["med"] for k, v in b["per_band"].items()}
M["band_top1pct"] = {k: v.get("top1pct_share") for k, v in b["per_band"].items()}
# 5. controls
c1 = rows["ctl_s1"]
M["ctl_naive_med"] = c1["xings_per_po_naive"]["bits16"]["med"]
M["ctl_naive_p99"] = c1["xings_per_po_naive"]["bits16"]["p99"]
M["ctl_smoothed_med"] = c1["xings_per_po_smoothed_bits16"]["med"]
M["ctl_deadband_med"] = c1["xings_per_po_deadband_bits16"]["med"]
M["ctl_deadband_p99"] = c1["xings_per_po_deadband_bits16"]["p99"]
M["ctl_f_dep_smoothed"] = c1["f_departed_smoothed_bits16"]
M["ctl_p99_reduction_deadband"] = M["ctl_naive_p99"] / max(1e-9, M["ctl_deadband_p99"])
# 6. departure fractions at bits12 after 300 P_p
for tag in ("belt_s1", "belt_s2", "belt_hot_s3"):
    M[f"f_dep_bits12_{tag}"] = rows[tag]["snaps"][-1]["f"][2]
    M[f"f_dep_bits8_{tag}"] = rows[tag]["snaps"][-1]["f"][1]
M["exit_frac_belt_s1"] = b["exited_domain_frac"]
# 7. entropy
e = b["entropy_snaps"]
M["H_first"] = e[0]["H_joint"]
M["H_last"] = e[-1]["H_joint"]
M["H_growth_bits"] = e[-1]["H_joint"] - e[0]["H_joint"]
M["H_a_last"] = e[-1]["H_a"]
M["cells_last"] = e[-1]["cells"]
# 8. budget
M["mature_bits_per_ship_est"] = e[-1]["H_joint"]
M["budget_bits_per_ship_8GB_1e9"] = 8 * 8e9 / 1e9
M["wall_s_max"] = max(d["wall_s"] for d in rows.values())

json.dump(M, open("metrics.json", "w"), indent=1)
for k, v in M.items():
    print(f"{k}: {v}")
