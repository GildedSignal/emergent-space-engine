#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff
# (f55d's instrument verbatim + this run's ES_LADDER_FORM scene knob).
# ~6 min of flights on this 8-vCPU box after a ~3 min cold build (warm: ~15 s).
# The runner applies work/patch.diff before this runs; if the tree is clean, apply it here.
set -euo pipefail
cd "$(dirname "$0")"
RUNDIR=$(pwd)
ROOT=$(git rev-parse --show-toplevel)
if ! grep -q "ladder_ship_form" "$ROOT/crates/universe/src/scenario.rs" 2>/dev/null; then
  git -C "$ROOT" apply --exclude='lab/wiki/*' "$RUNDIR/work/patch.diff"
fi

# Private target dir: a sibling checkout must not swap the binary mid-run (0757's lesson).
export CARGO_TARGET_DIR="${RUNDIR}/target-private"
cd "$ROOT/crates/universe"
cargo build --release --example lazy_flight
[ -x "$CARGO_TARGET_DIR/release/examples/lazy_flight" ]

cd "$RUNDIR"
bash fly.sh 10k
bash fly.sh 100k
bash fly.sh k10
python3 table.py > flights/table.txt

# The anchors the dossier cites: the belt arms must equal the record's numbers exactly.
python3 - <<'EOF'
import re
t = open("flights/table.txt").read()
rows = {}
for line in t.splitlines():
    m = re.match(r"(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)", line)
    if m and m.group(2) != "arm":
        rows[(m.group(1), m.group(2), m.group(3))] = (int(m.group(4)), int(m.group(5)), float(m.group(6)))
checks = [
    (("belt", "cap16384", "100000"), 130187, 940718, 7.226, "f55d's 7.23"),
    (("belt", "cap65536", "100000"), 130187, 905197, 6.953, "f55d's 6.95"),
    (("belt", "cap131072", "100000"), 130187, 130187, 1.000, "the knee"),
    (("belt", "cap16384", "10000"), 40187, 49994, 1.244, "0619's 1.24"),
    (("belt", "cap4096", "10000"), 40187, 120435, 2.997, "0757's 3.00"),
    (("K100", "cap4096", "100000"), 130187, 132061, 1.014, "the falsifier"),
    (("K10", "cap4096", "100000"), 130187, 131743, 1.012, "the falsifier, K=10"),
]
bad = 0
for key, dem, pro, ratio, why in checks:
    got = rows.get(key)
    if not got or got[0] != dem or got[1] != pro or abs(got[2] - ratio) > 5e-3:
        print(f"ANCHOR FAIL {key}: {got} vs ({dem}, {pro}, {ratio}) — {why}"); bad += 1
assert "all seam arms bit-identical" in t, "identity check failed"
print("anchors + identity OK" if bad == 0 else f"{bad} anchor failures")
EOF
for f in belt_100000_burn_ctl.txt form100_100000_burn_ctl.txt form10_100000_burn_ctl.txt; do
  grep -hE "^(digest|kicks)" "flights/$f"
done
echo "REGEN DONE"
