#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Linux box, < 15 min total (build ~2 min, runs ~2 min).
set -e
cd "$(dirname "$0")/../../.." || exit 1
R="$(pwd)/lab/results/20261015-1615-spacex-1343"

echo "== build =="
cargo build --release -p emergent-space --example passage_tail
cargo build --release -p emergent-universe --example nladder

echo "== bench: the passage tail on the law's bind path =="
cargo run --release -p emergent-space --example passage_tail | tee "$R/bench.txt"

echo "== flights: standard (the plane's own passage mints) and the comet stream =="
run() { timeout 90 cargo run --release -p emergent-universe --example nladder -- "$@" 2>&1 | tee -a "$R/flights.txt" | grep -E "^comets|^census|^rung|^ladder:|^memory:"; }
: > "$R/flights.txt"
run 1000 coast 20
run 10000 coast 20
run 10000 burn 20
run 2000 comet12 20
run 2000 comet13 20
echo "== done: see $R/bench.txt and $R/flights.txt =="
