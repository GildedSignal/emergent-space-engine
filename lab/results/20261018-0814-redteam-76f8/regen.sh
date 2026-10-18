#!/bin/sh
# Regenerates every number in dossier.md (the sweep table in sweep.txt) from shipped
# code plus work/patch.diff (applied by the runner before this runs).
# One cargo test run, ~50 s wall on this box, < 2 GB RAM.
set -e
out="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$out/../../.." && pwd)"
cd "$root"
cargo test --release --test xdense the_crossover -- --nocapture 2>&1 | tee "$out/sweep.txt" | grep -E "^gas |^slam |^miss |machine |test result"
grep -q "test result: ok" "$out/sweep.txt"
echo "regen ok: $(grep -cE '^gas |^slam |^miss ' "$out/sweep.txt") scene rows, digests asserted equal in every cell by the test itself"
