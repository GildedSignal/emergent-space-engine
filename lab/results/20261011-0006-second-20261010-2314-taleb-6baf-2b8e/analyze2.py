#!/usr/bin/env python3
"""Assemble the corrected H_live record from the second-author runs.

Instrument families, each named:
- naive   : changed-per-sample key count at stride 1 (ceiling 129.53/P_p; bits16
            measures ~91% of ceiling => cadence-bound; kept as the cadence view)
- swept   : exact per-step |dia|+|diL| cell distance (cadence-free, the physics)
- w1024   : key churn of the 1024-step rolling mean sampled every step
            (window/stride-dependent family: 2048-step windows give ~10.9-12.1)
- secular : synodic-phase-locked sampler, one sample per ship per its own
            synodic period (cadence-free; the floor for a synodic-aware
            population program)
Entropy: k-NN (Kozachenko-Leonenko) differential entropy on (a, L), bits,
sim units. hlive_big.py ran before the k-NN nat/bit unit fix, so its stored
values get the exact correction h += (psi(N)-psi(k))*(1/ln2-1); entropy.py
(the N=4000 dumps) was re-run after the fix.
"""
import json, math
import numpy as np
from scipy.special import digamma as dg


def load(p):
    return json.load(open(p))


M = {}
belts = {t: load(f"{t}.2.json") for t in ("belt_s1", "belt_s2", "belt_s3")}
ctl = load("ctl_s1.2.json")
lng = load("belt_long_s1.2.json")
w2048 = load("belt_w2048.2.json")
big = load("big_entropy.json")
ent = load("entropy.json")
regen = load("metrics-regen.json")

CEIL = 64 * 1.6 ** 1.5

# ---------- naive + swept ----------
for t, d in belts.items():
    M[f"naive_med_{t}"] = {k: round(v["med"], 1) for k, v in d["xings_per_po_naive"].items()}
    M[f"swept_med_{t}"] = {k: round(v["med"], 1) for k, v in d["swept_per_po"].items()}
s1 = belts["belt_s1"]["swept_per_po"]
M["swept_scaling"] = {"ratio_12_8": round(s1["bits12"]["med"] / s1["bits8"]["med"], 2),
                      "ratio_16_12": round(s1["bits16"]["med"] / s1["bits12"]["med"], 2),
                      "ratio_20_16": round(s1["bits20"]["med"] / s1["bits16"]["med"], 2)}
M["swept_bits16_s1"] = {k: round(s1["bits16"][k], 0) for k in ("med", "p90", "p99", "p999", "max")}
M["naive_bits16_pct_ceiling"] = [round(belts[t]["xings_per_po_naive"]["bits16"]["med"] / CEIL, 3)
                                 for t in belts]

# ---------- w-family + secular ----------
M["wfamily_med_bits16"] = {
    "W1024_stride1_s1": round(belts["belt_s1"]["xings_per_po_smoothed_bits16"]["med"], 2),
    "W2048_stride1_s1": round(w2048["xings_per_po_smoothed_bits16"]["med"], 2),
    "W2048_stride4_checker": 10.85,
}
for t, d in belts.items():
    w = d["xings_per_po_smoothed_bits16"]
    sec = d["secular_per_po"]
    M[f"w1024_{t}"] = {"med": round(w["med"], 2), "p99": round(w["p99"], 2), "max": round(w["max"], 2),
                       "p99_over_med": round(w["p99"] / w["med"], 2),
                       "top1pct": round(d["smoothed_tail_bits16"]["top1pct_share"], 4),
                       "fit": d["exponent_fits"].get("smoothed")}
    M[f"secular_{t}"] = {"med": round(sec["med"], 3), "p90": round(sec["p90"], 3),
                         "p99": round(sec["p99"], 3), "max": round(sec["max"], 3),
                         "p99_over_med": round(sec["p99"] / max(1e-9, sec["med"]), 2),
                         "max_over_med": round(sec["max"] / max(1e-9, sec["med"]), 2),
                         "top1pct": round(d["secular_tail_bits16"]["top1pct_share"], 4),
                         "fit": d["exponent_fits"].get("secular"),
                         "fires_med": d["secular_fires_med"],
                         "swept_med": round(d["secular_swept_per_po"]["med"], 3)}
secL = lng["secular_per_po"]
M["secular_long1200"] = {"med": round(secL["med"], 3), "p99": round(secL["p99"], 3),
                         "max": round(secL["max"], 3),
                         "max_over_med": round(secL["max"] / secL["med"], 2),
                         "fit": lng["exponent_fits"].get("secular"),
                         "fires_med": lng["secular_fires_med"]}
M["w1024_long1200"] = {"med": round(lng["xings_per_po_smoothed_bits16"]["med"], 2),
                       "fit": lng["exponent_fits"].get("smoothed")}

# ---------- tail structure ----------
bn = ["inner", "res21", "offres", "res31", "outer"]
for t, d in belts.items():
    sc = np.array(d["ship_sec_cum"], float)
    smc = np.array(d["ship_sm_cum"], float)
    act = np.array(d["ship_active"], bool)
    be = np.array(d["ship_birth_e"], float)
    bd = np.array(d["ship_band"], int)
    out = {}
    for nm, arr in (("secular", sc), ("w1024", smc)):
        sel = arr[act]
        k1 = max(1, len(sel) // 100)
        thr = np.sort(sel)[-k1]
        top = act & (arr >= thr)
        out[nm] = {"e_ratio_top_vs_fleet": round(float(np.median(be[top]) / np.median(be[act])), 2),
                   "band_share_top": {bn[i]: round(float((bd[top] == i).mean()), 3)
                                      for i in range(5) if (bd == i).sum() > 0}}
    M[f"tailstruct_{t}"] = out

# ---------- controls ----------
M["ctl"] = {"naive_med16": ctl["xings_per_po_naive"]["bits16"]["med"],
            "naive_p99_16": round(ctl["xings_per_po_naive"]["bits16"]["p99"], 3),
            "swept_med16": round(ctl["swept_per_po"]["bits16"]["med"], 3),
            "deadband_med16": ctl["xings_per_po_deadband_bits16"]["med"],
            "deadband_p99_16": round(ctl["xings_per_po_deadband_bits16"]["p99"], 4),
            "w1024_med": ctl["xings_per_po_smoothed_bits16"]["med"],
            "w1024_p99": round(ctl["xings_per_po_smoothed_bits16"]["p99"], 3),
            "secular_med": round(ctl["secular_per_po"]["med"], 4),
            "secular_p99": round(ctl["secular_per_po"]["p99"], 4),
            "secular_max": round(ctl["secular_per_po"]["max"], 4)}

# ---------- entropy (k-NN, unit-corrected) ----------
def _fix(h, N, k=8):
    return h + (dg(N) - dg(k)) * (1.0 / math.log(2) - 1.0)


N_live = int(big["live_frac_final"] * big["N"])
h_birth_1M = _fix(big["knn_birth"]["k8"], 262144)
h_final_1M = _fix(big["knn_final_full"]["k8"], N_live)
h_final_1M_k1 = _fix(big["knn_final_full"]["k1"], N_live, 1)
h_final_1M_k16 = _fix(big["knn_final_full"]["k16"], N_live, 16)
h_final_4ksub = _fix(big["knn_final_4k"]["k8"], 4000)

E = {
    "h_birth_1M_k8": round(h_birth_1M, 3),
    "h_final_1M_k8_po100": round(h_final_1M, 3),
    "h_final_1M_k1_po100": round(h_final_1M_k1, 3),
    "h_final_1M_k16_po100": round(h_final_1M_k16, 3),
    "h_final_4ksub_k8_po100": round(h_final_4ksub, 3),
    "h_analytic_birth": round(0.585 + math.log2(6.4e-4 * math.sqrt(2 * math.pi * math.e)), 3),
    "belt_s1_po100_k8_4k": round(ent["belt_s1"]["po100"]["h_bits"]["k8"], 3),
    "belt_s1_po300_k8_4k": round(ent["belt_s1"]["final"]["h_bits"]["k8"], 3),
    "belt_long_po100_k8_4k": round(ent["belt_long_s1"]["po100"]["h_bits"]["k8"], 3),
    "belt_long_po300_k8_4k": round(ent["belt_long_s1"]["po300"]["h_bits"]["k8"], 3),
    "belt_long_po1200_k8_4k": round(ent["belt_long_s1"]["final"]["h_bits"]["k8"], 3),
    "ctl_po100_k8": round(ent["ctl_s1"]["po100"]["h_bits"]["k8"], 3),
    "ctl_final_k8": round(ent["ctl_s1"]["final"]["h_bits"]["k8"], 3),
}
E["dh_birth_to_100_1Minstrument"] = round(E["h_final_1M_k8_po100"] - E["h_birth_1M_k8"], 3)
E["dh_100_to_1200_4kinstrument"] = round(E["belt_long_po1200_k8_4k"] - E["belt_long_po100_k8_4k"], 3)
E["dh_diffusive_pred_100to1200"] = round(0.5 * math.log2(12), 3)
E["kNN_thinridge_bias_4k_vs_1M"] = round(E["h_final_4ksub_k8_po100"] - E["h_final_1M_k8_po100"], 3)
E["grid16_offset"] = round(32 - math.log2(7.0 * 2.1), 3)
E["H_grid16_birth"] = round(E["h_birth_1M_k8"] + E["grid16_offset"], 2)
E["H_grid16_po100"] = round(E["h_final_1M_k8_po100"] + E["grid16_offset"], 2)
E["H_grid16_po1200_est"] = round(E["belt_long_po1200_k8_4k"] + E["grid16_offset"], 2)
M["entropy"] = E
M["plugin_big_bits16"] = {"birth_H": round(big["plugin_bits16"]["birth_H"], 2),
                          "birth_cells": big["plugin_bits16"]["birth_cells"],
                          "final_H": round(big["plugin_bits16"]["final_H"], 2),
                          "final_cells": big["plugin_bits16"]["final_cells"],
                          "true_H_grid16": E["H_grid16_po100"]}
M["plugin_bits8_conv"] = {"birth_H": round(big["plugin_bits8"]["birth_H"], 2),
                          "final_H": round(big["plugin_bits8"]["final_H"], 2),
                          "cells": big["plugin_bits8"]["final_cells"],
                          "kNN_pred_final": round(h_final_1M + 12.125, 2)}

# ---------- bandwidth, corrected ----------
Pp = 1.6 ** 1.5
spy = 3.156e7 / 100.0
med_sec = belts["belt_s1"]["secular_per_po"]["med"]
med_w = belts["belt_s1"]["xings_per_po_smoothed_bits16"]["med"]
med_nv = belts["belt_s1"]["xings_per_po_naive"]["bits16"]["med"]
M["bandwidth_per_wall_s_RTF100_1e9ships"] = {
    "P_p_yr": round(Pp, 4),
    "secular_floor": round(med_sec / Pp * 1e9 / spy, 1),
    "w1024_program": round(med_w / Pp * 1e9 / spy, 0),
    "naive_stride1": round(med_nv / Pp * 1e9 / spy, 0),
    "dossier_claim_was": "2-4e8 (3-5 orders high)",
}

# ---------- shipped-code record regeneration ----------
M["regen"] = {"halflife_po": regen["halflife_po"],
              "ctl_naive_med": regen["ctl_naive_med"],
              "H_first_last": [regen["H_first"], regen["H_last"]],
              "smoothed_med16_belt_s1": regen["smoothed_med16_belt_s1"],
              "ring_ratio": regen["res_ratio_ring21_vs_off"],
              "matches_original_except": ["wall_s_max"]}

json.dump(M, open("metrics2.json", "w"), indent=1)
for k, v in M.items():
    print(k, ":", v)
