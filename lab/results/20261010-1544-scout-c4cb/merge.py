#!/usr/bin/env python3
"""Merge shard metrics into metrics.json and print the summary table."""
import glob
import json

parts = {}
for f in sorted(glob.glob("metrics_[ABCD].json")):
    parts[f[-6]] = json.load(open(f))

runs, extra = {}, {}
for k in "ABCD":
    runs.update(parts[k]["runs"])
    for ek in parts[k]:
        if ek.startswith("H4_"):
            extra[ek] = parts[k][ek]

out = {
    "claim_config": dict(lmax=2, rate_per_Pref=8, bits=32, live_reals=8,
                         news_bits_per_Pref=8 * 32 * 8,
                         news_bytes_per_Pref=8 * 32 * 8 / 8),
    "pass_rule": "pos_err_final <= 1e-3 AND |dE_final| <= "
                 "max(0.01*|work_true|, 1e-6*|E0|)",
    "runs": runs,
    "extra": extra,
    "loadavg": {k: parts[k]["loadavg"] for k in parts},
}
with open("metrics.json", "w") as f:
    json.dump(out, f, indent=1)

hdr = f"{'run':<12} {'pass':<5} {'pos_err':>9} {'dE_final':>10} " \
      f"{'work_true':>10} {'field_rms':>9}"
print(hdr)
print("-" * len(hdr))
for name, r in runs.items():
    print(f"{name:<12} {str(r['pass']):<5} {r['pos_err_final']:9.2e} "
          f"{r['dE_final']:+10.2e} {r['work_true']:+10.2e} "
          f"{r['field_rms_rel']:9.2e}")
if "H4_growth_exponent" in extra:
    print("H4 dist-growth exponent:", round(extra["H4_growth_exponent"], 3))
