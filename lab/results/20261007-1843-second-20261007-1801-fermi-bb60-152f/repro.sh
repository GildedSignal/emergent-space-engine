#!/bin/sh
# Reproduce this run's record from shipped code (Linux box, cargo + rustc, ~2 min).
set -e
cd "$(dirname "$0")"            # lab/results/20261007-1843-second-20261007-1801-fermi-bb60-152f
ROOT=$(git rev-parse --show-toplevel)
XT="${CARGO_TARGET_DIR:-$ROOT/target}/release/xtask"

# 1. shipped harness: distinct-kick cost + both memo hit rates (regenerates the kickbench-*.json)
(cd "$ROOT" && cargo build --release -p xtask)
for s in 1 2 3; do
  for r in 100 1; do
    "$XT" universe --kick-bench --rtf "$r" --seconds 30 --seed "$s" > "kickbench-s$s-rtf$r.json"
  done
done
# determinism check: rerun seed 1 and diff the digests (timing medians differ; digests must not)
"$XT" universe --kick-bench --rtf 100 --seconds 30 --seed 1 > kickbench-s1-rtf100-repeat.json
python3 - <<'EOF'
import json
a=json.load(open('kickbench-s1-rtf100.json')); b=json.load(open('kickbench-s1-rtf100-repeat.json'))
assert a['replay_digest']==b['replay_digest'] and a['digest']==b['digest'] and a['memo']==b['memo']
print('determinism: digests identical')
EOF

# 2. compile grid: Orbit::compile alone over p = 2^4..2^24 M, e = 0..0.99
# profile feature: emergent-space recompiled into ./tgt with --features profile
TGT_DIR="$(cd "$(dirname "$0")" && pwd)/tgt"
(cd "$ROOT" && CARGO_TARGET_DIR="$TGT_DIR" cargo build --release -p emergent-space --features profile -p emergent-universe)

rustc --edition 2021 -O \
  --extern emergent_space="$(ls tgt/release/deps/libemergent_space-*.rlib | head -1)" \
  -L dependency=tgt/release/deps compile_bench.rs -o cb && ./cb > compile-out.txt
# 3. decomposition: whole kick vs fresh compile on the rebinds' own keys + exact cadence
rustc --edition 2021 -O \
  --extern emergent_universe="$(ls tgt/release/deps/libemergent_universe-*.rlib | head -1)" \
  --extern emergent_space="$(ls tgt/release/deps/libemergent_space-*.rlib | head -1)" \
  -L dependency=tgt/release/deps decompose_bench.rs -o db
for s in 1 2 3; do ./db "$s"; done > decompose-out.txt
rm -rf tgt cb db

# 4. the republished frontier (measured constants + the 2.5e8 tube-memory cap)
python3 budget2.py > budget2-out.txt
echo done
