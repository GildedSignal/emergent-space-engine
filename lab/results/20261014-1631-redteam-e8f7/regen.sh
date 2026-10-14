#!/usr/bin/env bash
# Regen: every dossier number, from the run's own script (shipped code is read at source,
# cited in the dossier; this run made no tree edits, so work/patch.diff is empty).
set -euo pipefail
cd "$(dirname "$0")"
if [ -s work/patch.diff ]; then git apply work/patch.diff; fi
python3 falsifier_key_depth2.py
python3 - <<'EOF'
import json
d = json.load(open("results.json"))
g = d["kill_grid"]
n1 = sum(1 for r in g if max(abs(r["err1"]), abs(r["err2"])) >= 1.0)
n10 = sum(1 for r in g if max(abs(r["err1"]), abs(r["err2"])) >= 10.0)
assert n1 == 79 and n10 == 52 and len(g) == 108, (n1, n10, len(g))
assert d["controls"]["depth1_beta2_0"]["err1"] == 0.0 and d["controls"]["depth1_beta2_0"]["err2"] == 0.0
assert abs(d["controls"]["depth2_moon_speed"]["err1"] - 3.094e-3) < 1e-4
assert d["oracle_check"] < 1e-9
assert [round(r["err1"], 2) for r in d["named"]] == [15.18, 178.63, 130.07, 0.0]
assert round(d["tb_channel"]["unscaled_error"], 1) == 6666.7
assert [round(r["err1"], 2) for r in d["depth"]] == [15.18, 78.12, 227.5]
print("regen: all dossier numbers reproduced and asserted")
EOF
