#!/bin/sh
# Regen: every dossier number, from shipped code + work/patch.diff. Total ~4 min warm, ~15 min cold.
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261016-2229-quant-7343
git apply "$RUN/work/patch.diff" 2>/dev/null || cp "$RUN/read_split.rs.copy" crates/universe/examples/read_split.rs
cargo build --release -p emergent-universe --example read_split
R="cargo run --release -q -p emergent-universe --example read_split --"
echo "=== 10^4 seed 1 (tuned)"
$R 10000 8 1
echo "=== 10^4 seed 2 (held out)"
$R 10000 8 2
echo "=== 10^5 seed 1"
$R 100000 2 1
echo "=== 10^3 seed 1"
$R 1000 8 1
