#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261013-1145-components-9384.
# Runs on the patched tree (work/patch.diff applied by the runner); the BASE arms
# restore num.rs's shipped isqrt from HEAD (read-only git), then restore the patch.
# Total wall ~6 min on the shared 8-vCPU box. Each stage prints its own numbers.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"        # repo root
RUN="$ROOT/lab/results/20261013-1145-components-9384"
cd "$ROOT"

echo "== machine state (the lab measures with it recorded) =="
uptime; nproc

echo "== [1] primitive fuzz: 24M cases + edges, candidates vs shipped (expect 0 mismatches) =="
cd "$RUN" && rustc -O bench_isqrt.rs -o bench_isqrt 2>/dev/null && ./bench_isqrt fuzz
cd "$ROOT"

echo "== [2] primitive bench: shipped vs B vs C on the compile's operand domains =="
"$RUN/bench_isqrt"

echo "== [3] compile sweep A/B/A (digest must be equal in all three arms) =="
NUM=crates/space/src/num.rs
cp "$NUM" /tmp/num_patched_arm.rs
echo "-- PATCHED arm:"
cargo run --release -p emergent-space --example isqrt_sweep 40 | tail -1
git show HEAD:"$NUM" > "$NUM"
echo "-- BASE arm (x2):"
cargo run --release -p emergent-space --example isqrt_sweep 40 | tail -1
cargo run --release -p emergent-space --example isqrt_sweep 40 | tail -1
cp /tmp/num_patched_arm.rs "$NUM"
echo "-- PATCHED arm again:"
cargo run --release -p emergent-space --example isqrt_sweep 40 | tail -1

echo "== [4] the law's own frozen-oracle tests on the patched tree (70 tests, all must pass) =="
cargo test --release -p emergent-space 2>&1 | grep -E "test result"

echo "== [5] plane digest A/B/A (tail 10s rtf100 seed1 48 members; digests must be equal) =="
echo "-- PATCHED arm:"
cargo run --release -p emergent-universe --example tail 10 100 1 48 | grep -i digest
git show HEAD:"$NUM" > "$NUM"
echo "-- BASE arm:"
cargo run --release -p emergent-universe --example tail 10 100 1 48 | grep -i digest
cp /tmp/num_patched_arm.rs "$NUM"
echo "-- PATCHED arm again:"
cargo run --release -p emergent-universe --example tail 10 100 1 48 | grep -i digest

echo "DONE"
