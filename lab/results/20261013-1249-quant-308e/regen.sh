#!/usr/bin/env bash
# Regenenerates every number in dossier.md from the shipped tree plus work/patch.diff.
# Wall numbers are on a shared Linux box: orders of magnitude, arms compared within one
# epoch (the dossier's interleaved protocol). Total well under 15 minutes.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

echo "== apply patch =="
git apply --3way "$(dirname "$0")/work/patch.diff" || echo "(patch already applied)"

echo "== 1. primitives: shipped cos / tuned / cos4 lane / isqrt ref (fuzz 2M built in) =="
cargo test --release -p emergent-space --lib cos_variants -- --ignored --nocapture 2>&1 | grep -E "cos shipped|test result"

echo "== 2. compile sweep, interleaved epochs on a pinned core (B=shipped cos, I=cos4) =="
cargo build --release -p emergent-space --example prim_compile
for i in 1 2 3 4; do
  COS4=0 taskset -c 2 cargo run --release -q -p emergent-space --example prim_compile 2>/dev/null | head -1 | sed 's/^/B(cos) /'
  COS4=1 taskset -c 2 cargo run --release -q -p emergent-space --example prim_compile 2>/dev/null | head -1 | sed 's/^/I(cos4) /'
done

echo "== 3. identity: plane digest, both arms =="
cargo build --release -p emergent-universe --example quant_digest
COS4=0 taskset -c 2 cargo run --release -q -p emergent-universe --example quant_digest 10000000000 2>/dev/null
COS4=1 taskset -c 2 cargo run --release -q -p emergent-universe --example quant_digest 10000000000 2>/dev/null

echo "== 4. suite with the patch live (cos4 default on) =="
taskset -c 2 cargo test --release -p emergent-space 2>&1 | grep -E "test result" | head -8
