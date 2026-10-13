#!/bin/sh
# Regenerates every number in dossier.md (the probe-out.txt table) from the shipped tree
# plus this run's patch (work/patch.diff, applied by the runner before this runs).
# Total time: ~1–2 min on the lab's Linux/x86 (build ~15 s warm, ~2 min cold; run ~15 s).
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release -p emergent-universe --example quad_slot
cargo run --release -p emergent-universe --example quad_slot -- 8
echo "---"
echo "Expected table (probe-out.txt): 6 scenes; e_p99 <= 7.2e-6 root ticks on every scene;"
echo "e exactly 0 on coast / forward L8 / brake L8 / turn-then-burn L8; clock% ~43; rd/body/f 2.5-3.8."
echo "The 'no-stor' column may wobble by a few counts (the frame budget's wall cut is machine-dependent);"
echo "the e quantile columns are stable to 2 digits."
