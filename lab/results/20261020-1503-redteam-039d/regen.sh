#!/bin/sh
# Regen for 20261020-1503-redteam-039d: every dossier number from this script.
# Runtime ~40 s (float64, one process, well under the 15-min budget and the 2-GB cap).
set -e
cd "$(dirname "$0")"
python3 rim_occlusion.py > regen_stdout.json
python3 - <<'EOF'
import json
d = json.load(open("results.json"))
c = d["controls"]
assert abs(c["shadow_relerr_r6.0"]) < 1e-8, "shadow control failed"
assert c["deflection_relerr"] < 1e-3, "deflection control failed"
assert abs(c["turn_at_bc"] - 3.0) < 1e-5, "turning-point control failed"
s = d["scenes"]
assert abs(s["r6p0_30p0"]["naive_fab_frac"] - 2/3) < 0.02, "naive fabrication at 6M"
assert s["r20p0_30p0"]["naive_fab_frac"] > 0.10, "negative control (20M fabrication)"
o = d["occluder_chord_vs_path"]
assert o["phi2.6"]["ray_blocked_frac"] == 0.0 and o["phi2.6"]["path_blocked_frac"] > 0.05
print("controls + negatives verified; full numbers in results.json")
EOF
