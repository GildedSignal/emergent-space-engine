#!/usr/bin/env python3
"""Post-run analysis: escape attribution on the real path (C1, C3),
honest D(t) inflow fits over a wide window, the m=1e-8 saturation store,
and the corrected alpha_partial for the original toy metrics."""
import json, math, os
import numpy as np
import hlive_real as hr

here = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(here, "metrics-real.json")))
out = {}

# ---- honest inflow fits over a wide window (D < 0.3 N) ----
inflow = {}
for name in ("C1_m1e-10", "C5_S1e4", "C6_seed2"):
    v = R[name]["eps"]["0.001"]
    Dt = np.array(v["Dt"], float)
    t = np.arange(1, len(Dt) + 1, dtype=float)
    sel = (Dt > 0) & (Dt < 0.3 * R[name]["N"]) & (t > 1)
    inflow[name] = dict(
        Dt=[int(x) for x in Dt],
        exp_wide=(float(np.polyfit(np.log(t[sel]), np.log(Dt[sel]), 1)[0])
                  if sel.sum() > 5 else None),
        exp_stored=v["inflow_exp"], n_fit=int(sel.sum()))
out["inflow_wide"] = inflow
print("inflow wide:", json.dumps(inflow, indent=1), flush=True)

# ---- m=1e-8 saturation store (the belt-mass case for a real 1e9 belt) ----
for cfg in ("C2_m1e-8", "C3_m1e-6"):
    v = R[cfg]["eps"]["0.001"]
    N = R[cfg]["N"]; D = v["D"]
    ef_bits = D * math.log2(N / max(D, 1)) + 2.0 * D if D < N else 2.0 * N
    store_bits = ef_bits + D * (v["id_bits"] + v["H_delta"])
    store_B = store_bits / N / 8.0
    out[f"B18_store_{cfg}"] = dict(
        D=D, D_over_N=v["D_over_N"], H_delta=v["H_delta"], Hj1=v["Hj1"],
        store_bytes_per_body=store_B,
        floor_hist_bytes=v["Hj1"] / 8.0,
        floor_prog_bytes=(0.126 + v["H_delta"] * D / N) / 8.0,
        total_GB_at_1e9=store_B,
        B18_ok=bool(store_B <= 2 * v["Hj1"] / 8.0 + 2))
    print(cfg, "store:", json.dumps(out[f"B18_store_{cfg}"], indent=1), flush=True)

# ---- corrected alpha_partial for the ORIGINAL toy metrics (fixed filter) ----
orig = json.load(open(os.path.join(here, "orig-metrics.json")))
fix = {}
for key, blk in orig.items():
    if not key.startswith("S2_m"): continue
    rows = blk["rows"]
    xs = np.array([float(r[0]) for r in rows])
    ys = np.array([float(r[1]) for r in rows])
    sel = (xs >= 1e-4) & (xs <= 1e-2)
    if key == "S2_m1e-10" and sel.sum() >= 3:
        ok = sel & (ys > 0)
        a = float(np.polyfit(np.log(xs[ok]), np.log(ys[ok]), 1)[0])
        fix[key] = dict(alpha_partial=a, stored_mislabeled=blk["alpha_partial"],
                        n_rows=int(ok.sum()))
    else:
        fix[key] = dict(alpha_partial=None, saturated=True,
                        stored_mislabeled=blk["alpha_partial"])
out["alpha_partial_toy_corrected"] = fix
print("toy alpha corrected:", json.dumps(fix), flush=True)

json.dump(out, open(os.path.join(here, "analysis.json"), "w"), indent=1)
print("wrote analysis.json", flush=True)
