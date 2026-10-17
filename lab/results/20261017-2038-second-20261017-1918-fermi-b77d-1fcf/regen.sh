#!/bin/bash
# Regenerates every dossier number from shipped code + work/patch.diff (applied first).
# ~9 min: build (~15 s warm, longer cold) + ten crowd flights (<= 55 s each) + analysis.
# Linux only. The load arms bring their own 7 spinners (cores 1-7); the quiet arms run
# on whatever the box gives — every log head records the loadavg it flew under.
set -eu
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."   # repo root

echo "== machine state: $(cat /proc/loadavg) ; $(grep MemAvailable /proc/meminfo)"

echo "== patch (adds the print-only example crates/universe/examples/flowcrowd.rs)"
if [ -f crates/universe/examples/flowcrowd.rs ]; then
  echo "flowcrowd.rs already present; assuming the probe patch is applied"
else
  git apply "$RUN/work/patch.diff"
fi

echo "== build"
cargo build --release -p emergent-universe --example flowcrowd
BIN="${CARGO_TARGET_DIR:-target}/release/examples/flowcrowd"
ls -la "$BIN"

echo "== flights (crowd rung: MEMBERS in {1000,1600,2400,4000,10000} x {quiet, 7-spinner loaded},"
echo "   paced player loop, pin in real bytes via the counting GlobalAlloc)"
"$RUN/flights.sh" "$BIN" 1000 1600 2400 4000 10000

echo "== analysis (every number in dossier.md's table and the pin-law fit)"
python3 "$RUN/analyze.py" "$RUN/flights"
