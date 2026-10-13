#!/bin/sh
# Stage costs of a held throttle's frame (prof build): coast, forward L8, reverse L8, reverse L15, and the demand-mode
# (unlimited budget) reverse L15. Usage: stages.sh [out-file]
cd "$(dirname "$0")/../../.." || exit 1
cargo build --release -p emergent-universe --features prof --example frame_cost 2>&1 | grep -E "^error" -A8
FC=./target/release/examples/frame_cost
{
  ./artifacts/runs/frame/state.sh
  echo; echo "=== coast: frame_cost 100 20 0 0 8"; $FC 100 20 0 0 8
  echo; echo "=== forward L8: frame_cost 100 20 1 8 8"; $FC 100 20 1 8 8
  echo; echo "=== reverse L8: frame_cost 100 20 2 8 8"; $FC 100 20 2 8 8
  echo; echo "=== reverse L15: frame_cost 100 20 2 15 8"; $FC 100 20 2 15 8
  echo; echo "=== demand mode (budget 100000 ms), reverse L15"; $FC 100 20 2 15 6 100000
  ./artifacts/runs/frame/state.sh
} > "${1:-/dev/stdout}" 2>&1
