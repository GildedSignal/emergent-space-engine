#!/usr/bin/env bash
# Regenerates every number in dossier.md from this run's own script (float64, ~8 s).
# work/patch.diff (which contains this folder's files) is applied by the runner before
# this script runs. Requires python3 with numpy and scipy.
set -euo pipefail
cd "$(dirname "$0")"
python3 falsifier.py > run_output.txt
python3 - <<'EOF'
import json
r = json.load(open("results.json"))
sc = {s["name"]: s for s in r["scenes"]}
co = {c["name"]: c for c in r["coeffs"]}
checks = [
    ("cap exit letter [r]", sc["cap circ r=18M (c/4) [r]"]["exit_err_letter"] > 0.20),
    ("cap exit cure [r]", sc["cap circ r=18M (c/4) [r]"]["exit_err_cure"] < 0.01),
    ("cap coeff ratio", abs(abs(co["cap circ r=18M (c/4)"]["ratio_radial"]) - 1.0988) < 0.02),
    ("beta0.5 coeff ratio", abs(abs(co["flyby r=100M b=0.5"]["ratio_radial"]) - 1.5052) < 0.05),
    ("radial-infall cancellation", abs(co["radial infall b=0.5"]["ratio_norm"] - 1.0) < 0.01),
    ("flyby0.9 letter exit [r]", sc["flyby r=100M b=0.9 [r]"]["exit_err_letter"] > 0.05),
    ("control letter exit [r]", sc["control circ r=1000M [r]"]["exit_err_letter"] < 0.01),
]
ok = True
for name, cond in checks:
    print(("PASS " if cond else "FAIL ") + name)
    ok &= cond
print("regen:", "ALL PASS" if ok else "CHECK FAILED")
EOF
