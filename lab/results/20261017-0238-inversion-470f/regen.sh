#!/usr/bin/env bash
# Regen: every dossier number, from shipped code + work/patch.diff (the ruin probe: RSS + /proc
# maps + a counting GlobalAlloc + the shipped counters, one CSV row per chunk of game time).
# ~8 min wall on the lab's 8-vCPU Linux box, each process < 250 MB RSS. Run on a quiet machine:
# the 400-member coast arm is bimodal run-to-run (the finding) — regen flies it four times.
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$R/../../.." && pwd)"
cd "$ROOT"
if [ -f "$R/work/patch.diff" ] && ! grep -q "fn main" crates/universe/examples/ruin_probe.rs 2>/dev/null; then
  git apply --include='crates/universe/examples/*' "$R/work/patch.diff" || true
fi
cargo build --release -p emergent-universe --example ruin_probe
BIN=$(ls -t /home/glmlab/lab-target-*/release/examples/ruin_probe 2>/dev/null | head -1)
[ -x "$BIN" ] || BIN="target/release/examples/ruin_probe"
fly() { local out=$1 tmo=$2; shift 2; timeout "$tmo" "$BIN" "$@" > "$R/$out" 2>&1 || echo "(arm $out exit $?)" >> "$R/$out"; }
fly out-48-coast-40k.txt        100 40000 100 1 48  1000
fly out-400-coast-40k.txt       150 40000 100 1 400 1000
fly out-400-coast-r1.txt        100  6000 100 1 400 1000
fly out-400-coast-r2.txt        100  6000 100 1 400 1000
fly out-400-coast-r3.txt        100  6000 100 1 400 1000
fly out-400-coast-r4.txt        100  6000 100 1 400 1000
fly out-400-coast-seed2.txt     100  8000 100 2 400 1000
fly out-400-burn-seed1.txt      100  8000 100 1 400 1000 burn
fly out-400-burn-seed2.txt      100 20000 100 2 400 1000 burn
fly out-belt3000-burn-seed3.txt 400  6000 100 3 48  1000 burn "" 3000
echo "regen done: $(ls "$R"/out-*.txt | wc -l) arms"
