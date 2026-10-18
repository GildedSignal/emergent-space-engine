#!/usr/bin/env python3
"""Re-derive every dossier headline from eclipse_parity-out.json (+ the original run's
JSON, kept here as eclipse_parity-out-orig.json) and check the invariants (PG)."""
import json
import math

new = json.load(open("eclipse_parity-out.json"))
old = json.load(open("eclipse_parity-out-orig.json"))

print("== corrected W2/W2p onset errors (grid) and closed forms ==")
for r in new["arm_a"]["rows"]:
    if r["beta"] in (0.5, 0.9):
        closed = (math.sqrt(r["d_over_R"] ** 2 + 1) - r["d_over_R"]) + \
            (1.0 / r["beta"]) * (math.sqrt(1 + r["beta"] ** 2) - 1)
        print(f"d={r['d_over_R']:5.0f}R b={r['beta']}: W2 {r['dt_on_W2']:+8.4f}s "
              f"(closed {closed:+.4f})  W2p {r['dt_on_W2p']:+8.4f}s  "
              f"artifact col, as quoted in dossier "
              f"{r['artifact_W2_bug_vs_W3']:+10.4f}s")

print("== certificates ==")
certs = new["arm_a"]["certificates"]
print("max |onset - closed form| over all cells/wirings:",
      max(max(abs(x) for x in c["c2_onset_minus_closed"].values()) for c in certs))
print("max |t_quad - t_bisect| over all grids:",
      max(c["c1_quad_vs_bisect"] for c in certs),
      " brackets valid:", all(c["bracket_ok"] for c in certs))
mm = new["arm_arc"]["transverse"] + new["arm_arc"]["oblique"]
print("arc per-row closed-form mismatches (W1/W2/W3), all 11 cells:",
      max(max(m["mismatches"].values()) for m in mm))

print("== the 1/gamma mechanism (10R) ==")
for m in new["arm_arc"]["transverse"]:
    if m["d_over_R"] == 10.0:
        print(f"b={m['beta']}: centre W2 {m['centre_W2_deg']:+7.3f} (-asin b "
              f"{m['minus_asinbeta_deg']:+.3f})  half ratio {m['ratio_W2_W3']:.4f} "
              f"vs 1/gamma {m['one_over_gamma']:.4f}  Jac {m['jac_W2']:.4f} vs "
              f"sqrt(1-b^2) {m['sqrt_1_minus_beta2']:.4f}")

print("== oblique (45 deg, d=10R): fixed W2, exact sprite identity ==")
for m in new["arm_arc"]["oblique"]:
    print(f"b={m['beta']}: sprite dist {m['sprite_dist']:.4f} = light time "
          f"{m['sprite_lighttime']:.4f}  Jac W1 {m['jac_W1']:.3f} W2 {m['jac_W2']:.4f} "
          f"W2p {m['jac_W2p']:.4f}")

print("== rim (b=0.5): bounded, shrinking with d ==")
print(new["arm_a"]["rim"])

print("== W2p alternate letter reading (per-frame CURRENT distance): onset err vs W3 ==")
for beta, d in ((0.5, 100.0), (0.9, 100.0)):
    R = 1.0
    tA = (-R / beta + math.sqrt(R * R + (1 - beta * beta) * d * d)) / (1 - beta * beta)
    tW3 = d - R * math.sqrt(1 + beta * beta) / beta
    print(f"  {d:.0f}R b{beta}: {tA - tW3:+8.2f}s   (constant-d reading: "
          f"{(R/beta)*(math.sqrt(1+beta*beta)-1):+.3f}s)")

print("== PG: unchanged vs the original run (must be no violations) ==")
bad = []
for rn, ro in zip(new["arm_a"]["rows"], old["arm_a"]["rows"]):
    for k in ("d_over_R", "beta", "n_occ_W3", "frac_W3", "jac_W1", "jac_W2", "jac_W2p",
              "n_flip_W1", "on_W1", "on_W3", "dt_on_W1"):
        if rn[k] != ro[k]:
            bad.append((rn["d_over_R"], rn["beta"], k))
for k in new["arm_observer"]:
    for kk, v in new["arm_observer"][k].items():
        if old["observer"][k][kk] != v:
            bad.append(("obs", k, kk))
for k in new["arm_b"]:
    if isinstance(new["arm_b"][k], (int, float)) and old["arm_b"][k] != new["arm_b"][k]:
        bad.append(("armb", k))
print("violations:", bad)

r = [x for x in old["arm_a"]["rows"] if x["d_over_R"] == 100.0 and x["beta"] == 0.9][0]
n = [x for x in new["arm_a"]["rows"] if x["d_over_R"] == 100.0 and x["beta"] == 0.9][0]
print(f"== the tell == original W2/W2p: {r['dt_on_W2']:+.4f}/{r['dt_on_W2p']:+.4f} "
      f"(convergent); fixed: {n['dt_on_W2']:+.4f}/{n['dt_on_W2p']:+.4f} (distinct)")
