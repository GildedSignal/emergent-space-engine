#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus work/patch.diff.
# Linux/x86 lab box; orders of magnitude only (the M1 re-measures).
# Total: two release builds (~50 s each here) + five short runs < 2 min.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-0739-spacex-4ea0
OUT=$R/work/regen
mkdir -p "$OUT"

echo "== apply instrument patch =="
git apply --check "$R/work/patch.diff" 2>/dev/null && git apply "$R/work/patch.diff" || echo "patch already applied"

echo "== build patched =="
cargo build --release -p xtask 2>&1 | tail -1
T=${CARGO_TARGET_DIR:-target}/release/xtask

echo "== bench 48 (engine+view+json), seed 1 =="
"$T" universe --bench --seed 1 --rtf 100 --seconds 20 --unpaced --no-record 2>&1 \
  | grep -E 'shapecensus|"digest"|"bodies"|bytes_per_body|events_per_second' > "$OUT/bench48.txt"

echo "== bench 400 members (held-out arm) =="
"$T" universe --bench --seed 1 --rtf 100 --seconds 20 --members 400 --unpaced --no-record 2>&1 \
  | grep -E 'shapecensus|"digest"|"bodies"|bytes_per_body' > "$OUT/bench400.txt"

echo "== bench seed 7 (held-out seed) =="
"$T" universe --bench --seed 7 --rtf 100 --seconds 20 --unpaced --no-record 2>&1 \
  | grep -E 'shapecensus|"digest"' > "$OUT/bench-seed7.txt"

echo "== kick-bench (pure resolver) =="
"$T" universe --kick-bench --seed 1 --rtf 100 --seconds 20 2>&1 \
  | grep -E 'shapecensus|replay_digest|"median"|kick_us' > "$OUT/kickbench.txt"

echo "== pristine digest control (tree restored, then patch re-applied) =="
git checkout -- crates xtask
rm -f crates/universe/src/census.rs
cargo build --release -p xtask 2>&1 | tail -1
{ "$T" universe --bench --seed 1 --rtf 100 --seconds 20 --unpaced --no-record 2>&1 | grep '"digest"';
  "$T" universe --bench --seed 1 --rtf 100 --seconds 20 --members 400 --unpaced --no-record 2>&1 | grep '"digest"';
  "$T" universe --bench --seed 7 --rtf 100 --seconds 20 --unpaced --no-record 2>&1 | grep '"digest"';
  "$T" universe --kick-bench --seed 1 --rtf 100 --seconds 20 2>&1 | grep replay_digest; } > "$OUT/pristine-digests.txt"
git apply "$R/work/patch.diff"
cargo build --release -p xtask 2>&1 | tail -1

echo "== patched digests (must equal the pristine list above, line for line) =="
for f in bench48 bench400 bench-seed7; do grep '"digest"' "$OUT/$f.txt"; done
grep replay_digest "$OUT/kickbench.txt"
echo "done: output in $OUT"
