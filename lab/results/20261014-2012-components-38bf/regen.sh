#!/bin/sh
# Regenerates every number in dossier.md (the four flights of 20261014-2012-components-38bf).
# Applies work/patch.diff (the ES_PULL_CAP bound + the wave_input bench), builds, flies.
# Wall: about 12 minutes (four flights of up to ~170 s each, sequential, on a quiet 8-vCPU Linux box).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
git apply --allow-empty "$(dirname "$0")/work/patch.diff" 2>/dev/null || true   # already applied by the runner
cargo build --release -p emergent-universe --example wave_input --example belt_first
B="${CARGO_TARGET_DIR:-target}/release/examples/wave_input"
R="$(dirname "$0")"
{
  echo "=== belt_first 200000 (the wave window) ==="
  "${CARGO_TARGET_DIR:-target}/release/examples/belt_first" 200000
  echo "=== P1 plain cap-unset ==="
  timeout 260 "$B" 200000 plain 175 100 12
  echo "=== P2 plain cap64 ==="
  ES_PULL_CAP=64 timeout 260 "$B" 200000 plain 175 100 12
  echo "=== P3 one cap64 ==="
  ES_PULL_CAP=64 timeout 260 "$B" 200000 one 175 100 12
  echo "=== P4 held cap64 ==="
  ES_PULL_CAP=64 timeout 260 "$B" 200000 held 175 100 12
} | tee "$R/out/flights.txt"
