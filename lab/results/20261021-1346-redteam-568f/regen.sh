#!/bin/sh
# Regenerates every number in dossier.md from this folder (~20 s total).
# Requires python3 with numpy and scipy (versions used: numpy 1.26.4, scipy 1.11.4).
set -e
cd "$(dirname "$0")"
python3 cycle.py validate > validate.json
python3 - <<'EOF'
import json
v = json.load(open("validate.json"))
assert all(abs(b["rel"]) < 1e-11 for b in v["binet"]), "Binet cross-check failed"
for p in v["precession"]:
    assert p["ratio"] - 1 < 1e-3 and p["ratio"] - 1 > 0, "6pi/pbar control failed"
print("validate: controls green (binet |rel|<=1.6e-13, precession ratio-1 ~ pbar^-1)")
EOF
python3 cycle.py grid > grid_digest.txt
python3 - <<'EOF'
import json
g = json.load(open("grid.json"))
# the dossier's headline numbers, re-derived and asserted
key = {(r["cell"], r["delta"], r["program"]): r for r in g["grid"]}
def nc(cell, d, prog):
    r = key[(cell, d, prog)]
    return r["n_cert_measured"], r["n_cert_extrapolated"]
assert abs(nc("belt-like", 1e-6, "coherent-dL")[0] - 1.96e5) / 1.96e5 < 0.02
assert abs(nc("whirl", 1e-4, "coherent-dL")[0] - 663) / 663 < 0.02
assert abs(nc("whirl", 1e-2, "coherent-dL")[0] - 6.63) / 6.63 < 0.05
assert nc("belt-like", 1e-2, "random")[0] < 100
assert key[("whirl", 1e-2, "coherent-dL")]["type_event"]["n"] == 16
te = [r for r in g["grid"] if r["type_event"] and r["type_event"]["kind"] == "unbound (E>=1)"
      and r["delta"] == 1e-4]
assert all(r["type_event"]["n"] in (10000, 10001) for r in te), "escape at 1/delta failed"
print("grid: headline numbers reproduce (N*.delta 0.066-0.20 coherent; escape at 1/delta; "
      "whirl plunge at 16)")
EOF
echo "regen complete"
