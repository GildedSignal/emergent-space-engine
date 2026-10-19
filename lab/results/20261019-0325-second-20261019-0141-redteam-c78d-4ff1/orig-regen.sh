#!/bin/sh
# Regen: every number in dossier.md, from this folder's script. ~20 s, < 1 GB.
set -e
cd "$(dirname "$0")"
python3 occlusion.py | tee regen-output.txt
echo "--- controls ---"
python3 - <<'EOF'
import json
d = json.load(open("results.json"))
print("single_member_max_err", d["controls"]["single_member_max_err"])
r3 = next(r for r in d["arms"] if r["config"] == "rf3_impact0")
print("rf3 err_gt80_window_path", round(r3["err_gt80_window_path"], 3),
      "| randmember mid median", round(r3["err_at_mid_randmember"], 3),
      "| randmember path peak (mean over draws)", round(r3["peak_err_randmember_meanpath"], 3))
for r in d["beta_arms"]:
    print(r["config"], "peak", round(r["peak_err_centre"], 3),
          "f_true_min", round(r["f_true_min"], 3))
EOF
