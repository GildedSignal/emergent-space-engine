#!/bin/sh
# 20261020-1729-quant-077c — regenerates every dossier number from shipped code + work/patch.diff.
# ~3 min warm (builds ~1 min, three 27 s belt flights, two 4 s grids, instant kick-bench).
set -e
cd "$(dirname "$0")/../../.."   # repo root
git apply "$(dirname "$0")/work/patch.diff" 2>/dev/null || echo "patch already applied (in-tree run)"
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-$HOME/lab-target-2}
O="$(dirname "$0")/out"; mkdir -p "$O"
cargo build --release -p emergent-space --example rebind_stages
cargo build --release -p xtask
cargo build --release -p emergent-universe --example nladder

{ cat /proc/loadavg; grep MemAvailable /proc/meminfo; } > "$O/machine.txt"

# Plane (a765's scene), audit on twice + off once: digests must be identical (print-only).
for i in 1 2; do
  ES_REBIND_AUDIT=1 "$CARGO_TARGET_DIR/release/xtask" universe --kick-bench --seconds 20 \
    > "$O/kb_on$i.json" 2> "$O/kb_on$i.err"
done
"$CARGO_TARGET_DIR/release/xtask" universe --kick-bench --seconds 20 > "$O/kb_off.json" 2> "$O/kb_off.err"

# Belt (7fd3's scene): N=3e4 and 1e4, coast, audit on; plus the off control.
ES_REBIND_AUDIT=1 "$CARGO_TARGET_DIR/release/examples/nladder" 30000 coast 60 1800 > "$O/belt_on1.txt" 2> "$O/belt_on1.err"
"$CARGO_TARGET_DIR/release/examples/nladder" 30000 coast 60 1800 > "$O/belt_off.txt" 2> "$O/belt_off.err"
ES_REBIND_AUDIT=1 "$CARGO_TARGET_DIR/release/examples/nladder" 10000 coast 60 1800 > "$O/belt10k_on.txt" 2> "$O/belt10k_on.err"

# Controlled e-grid, min-of-5 batches per cell, both timer modes (P4 control).
ES_REBIND_AUDIT=1 "$CARGO_TARGET_DIR/release/examples/rebind_stages" > "$O/grid_on.tsv" 2>/dev/null
"$CARGO_TARGET_DIR/release/examples/rebind_stages" off > "$O/grid_off.tsv" 2>/dev/null

echo '--- audit lines ---'
grep -h rebind_audit "$O"/kb_on*.err "$O"/belt_on1.err "$O"/belt10k_on.err
echo '--- digest identity (print-only control) ---'
grep -E '"(digest|replay_digest)"' "$O/kb_on1.json" "$O/kb_off.json"
echo '--- belt deterministic fields, on vs off ---'
for f in belt_on1 belt_off; do grep -oE "(bodies=[0-9]+|frames=[0-9]+|kicks_per_body_gs=[0-9.e-]+|events_per_body_gs=[0-9.e-]+|refusals=[0-9]+|dead=[0-9]+|truncated=(true|false))" "$O/$f.txt" | tr '\n' ' '; echo " <- $f"; done
echo '--- grid (min-of-5) ---'
column -t "$O/grid_on.tsv"
echo '--- grid off-mode bare walls (P4) ---'
awk 'NR>1{print $1, $2, $10}' "$O/grid_off.tsv"
