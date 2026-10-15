#!/bin/sh
# Regen: every number in dossier.md, from the shipped tree + work/patch.diff (already applied).
# Build the census-instrumented example, fly the arms, analyse the fire trains. ~2-3 min total.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
R=lab/results/20261015-0724-system-3294/raw
mkdir -p "$R"

cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/nladder"
[ -x "$BIN" ] || BIN=/home/glmlab/lab-target-2/release/examples/nladder

# D1 (decisive): 1e4 coast, rtf 1500, 55 s -> ~82,500 game-s: 3 grid intervals, 3 waves.
CENSUS_TRAIN="$R/train_1e4_coast.txt" "$BIN" 10000 coast 55 1500 > "$R/n1e4_coast.txt" 2>&1
# D2: 1e5 coast, rtf 600 -> ~33,000 game-s: the first wave at 10x the bodies.
CENSUS_TRAIN="$R/train_1e5_coast.txt" "$BIN" 100000 coast 55 600 > "$R/n1e5_coast.txt" 2>&1
# Held-out arms (checker's domain): N=3e4 between the rungs; a burn crossing the wave.
CENSUS_TRAIN="$R/train_3e4_coast.txt" "$BIN" 30000 coast 55 1500 > "$R/n3e4_coast.txt" 2>&1
CENSUS_TRAIN="$R/train_1e4_burn.txt"  "$BIN" 10000 burn  55 1500 > "$R/n1e4_burn.txt"  2>&1

for a in 1e4_coast 1e5_coast 3e4_coast 1e4_burn; do
  echo "== $a =="
  grep -E "census:|ladder:" "$R/n$a.txt"
  python3 lab/results/20261015-0724-system-3294/train.py "$R/train_$a.txt" "$R/train_$a.json" > "$R/train_$a.pretty.json"
  python3 - "$R/train_$a.json" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
b = d["belt"]
print("belt: bodies", b["bodies"], "fires", b["fires"], "interval_s median", round(b["interval_s_median"], 1),
      "waves:", [(c["n"], c["start_s"], c["span_s"]) for c in b.get("absolute_clusters", [])][:6])
EOF
done
echo "machine state:"; uptime
