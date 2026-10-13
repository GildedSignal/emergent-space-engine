#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the runner
# before this runs). Total wall: under 2 minutes on the lab's 8-vCPU runner.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$HOME/lab-target-1}"

echo "== build (the harness example + the one-switch patch) =="
cargo build --release -p emergent-universe --example rekey_scout
B="$CARGO_TARGET_DIR/release/examples/rekey_scout"

echo
echo "== E1: digest at one canonical cut under shipped / never / lazy rekey (P1) =="
echo "-- seed 1, 48 members, starved (1 event/frame), 8 game-s --"
"$B" digest 1 48 1 8
echo "-- seed 3, 48 members, starved, 8 game-s --"
"$B" digest 3 48 1 8
echo "-- seed 1, 400 members, starved, 8 game-s --"
"$B" digest 1 400 1 8
echo "-- seed 1, 48 members, starved, 60 game-s (kicks + encounters) --"
"$B" digest 1 48 1 60
echo "-- seed 3, 48 members, starved, 60 game-s --"
"$B" digest 3 48 1 60
echo "-- seed 1, 48 members, unstarved (5 ms wall), 8 game-s --"
"$B" digest 1 48 0 8

echo
echo "== E2: the session's presented-tick key logging vs grid-quantized decisions (P2, P3) =="
"$B" leak 1 100
"$B" leak 3 100

echo
echo "== E0: the fixed tier's rekey share (P4), quiet frames, events=0 =="
"$B" pop 1000 300
"$B" pop 10000 300
echo "-- the plane itself (28 bodies; view off, engine advance only) --"
"$B" cost 48 600
"$B" cost 400 600
