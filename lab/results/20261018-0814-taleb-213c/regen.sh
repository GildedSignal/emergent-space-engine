#!/usr/bin/env bash
# Regenerates every dossier number: builds the probe example (patch already applied) and runs
# the control smoke plus all arms. ~8-10 min warm, ~13 min cold. Cloud box; orders of magnitude.
set -e
cd "$(dirname "$0")"/../../..
cargo build --release --example ruin_mint
B=/home/glmlab/lab-target-1/release/examples/ruin_mint
[ -x "$B" ] || B=$(cargo metadata --no-deps --format-version 1 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release/examples/ruin_mint
echo "== smoke (control D) =="
"$B" smoke
echo "== all arms =="
"$B" all
