#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff
# (b172's instrument verbatim + this run's ES_LADDER_FORM_W matched-fills knob).
# Phases run three-wide (each flight is single-threaded, <= ~600 MB rss): ~10 min of
# flights after a ~25 s warm / ~4 min cold build. Belt arms never set the scene knobs.
set -euo pipefail
cd "$(dirname "$0")"
RUNDIR=$(pwd)
ROOT=$(git rev-parse --show-toplevel)
if ! grep -q "ES_LADDER_FORM_W" "$ROOT/crates/universe/src/scenario.rs" 2>/dev/null; then
  git -C "$ROOT" apply --exclude='lab/wiki/*' "$RUNDIR/work/patch.diff"
fi

# Private target dir: a sibling checkout must not swap the binary mid-run (0757's lesson).
export CARGO_TARGET_DIR="${RUNDIR}/target-private"
cd "$ROOT/crates/universe"
cargo build --release --example lazy_flight
[ -x "$CARGO_TARGET_DIR/release/examples/lazy_flight" ]

cd "$RUNDIR"
bash fly2.sh core   & P1=$!
bash fly2.sh depth  & P2=$!
bash fly2.sh fills  & P3=$!
wait $P1 $P2 $P3
bash fly2.sh bracket
bash flyek.sh
python3 table2.py > flights/table.txt  # table2.py tolerates the missing none; all 23 arms present

# The anchors the dossier cites (P5: the published record; P1/P3: the depth ladder).
python3 - <<'EOF'
import re
t = open("flights/table.txt").read()
rows = {}
for line in t.splitlines():
    m = re.match(r"(\S+)\s+(\S+k)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)", line)
    if m and m.group(3) != "arm":
        rows[(m.group(1), m.group(2), m.group(3))] = dict(kicks=int(m.group(4)), dem=int(m.group(5)),
            pro=int(m.group(6)), ratio=float(m.group(7)), hits=int(m.group(8)), fills=int(m.group(9)))
bad = 0
def near(key, val, tol, why):
    global bad
    got = rows.get(key)
    if not got or abs(got["ratio"] - val) > tol:
        print(f"ANCHOR FAIL {key}: {got and got['ratio']} vs {val} — {why}"); bad += 1
def exact(key, field, val, why):
    global bad
    got = rows.get(key)
    if not got or got[field] != val:
        print(f"ANCHOR FAIL {key}.{field}: {got and got[field]} vs {val} — {why}"); bad += 1
# P5: the published matched-cut record
exact(("belt", "20k", "retain"), "hits", 1528451, "f55d/0619 saturated hits")
near(("belt", "20k", "cap16384"), 7.226, 5e-3, "b172/f55d 7.23")
exact(("belt", "20k", "ctl"), "kicks", 132278, "b172's scene-invariant kicks")
near(("form100", "20k", "cap4096"), 1.014, 5e-3, "b172's falsifier")
# P1: the depth inversion, landed
d48f = rows.get(("form100", "48k", "cap4096")); d48b = rows.get(("belt", "48k", "cap4096"))
if not d48f or not (20 <= d48f["ratio"] <= 40): print(f"ANCHOR FAIL form100 48k cap4096 ratio: {d48f and d48f['ratio']} vs checker's 29.3"); bad += 1
if not d48b or not (40 <= d48b["ratio"] <= 60): print(f"ANCHOR FAIL belt 48k cap4096 ratio: {d48b and d48b['ratio']} vs checker's 48.5"); bad += 1
exact(("form100", "48k", "cap273200"), "evict_check", None, "") if False else None
m = re.search(r"form100\s+48k\s+cap273200\s+\d+\s+(\d+)\s+(\d+)\s+([\d.]+)\s+\d+\s+\d+\s+[\d.]+\s+(\d+)", t)
if not m or float(m.group(3)) != 1.000 or int(m.group(4)) != 0:
    print(f"ANCHOR FAIL form100 48k cap273200: ratio/evict {m and (m.group(3), m.group(4))} vs 1.000/0"); bad += 1
assert "all seam arms bit-identical" in t, "identity check failed"
print("anchors + identity OK" if bad == 0 else f"{bad} anchor failures")
EOF
echo "REGEN DONE"
