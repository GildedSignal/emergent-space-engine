#!/bin/sh
# Regen: every number in dossier.md, from shipped code + work/patch.diff.
# The runner applies work/patch.diff before this runs; the guard re-applies only if needed.
set -e
cd "$(dirname "$0")/../../.."   # repo root
if [ ! -f crates/universe/examples/beltcensus.rs ]; then
  git apply --check lab/results/20261019-1316-system-f7c3/work/patch.diff && git apply lab/results/20261019-1316-system-f7c3/work/patch.diff
fi
echo "loadavg at start: $(cut -d' ' -f1-3 /proc/loadavg)"
cargo build --release -p emergent-universe --example beltcensus
cd crates/universe
for arm in "3000 1 0 1800" "10000 1 50 1800" "30000 1 50 1800" "100000 1 50 1800" "300000 1 0 1800" "10000 2 50 1800"; do
  echo "=== beltcensus $arm ==="
  if echo "$arm" | grep -q " 0 1800"; then
    timeout 120 cargo run --release -q -p emergent-universe --example beltcensus -- $arm 2>/dev/null
  else
    timeout 70 env ES_CENSUS=1 cargo run --release -q -p emergent-universe --example beltcensus -- $arm 2>/dev/null
  fi
done
echo "=== memo.rs control, hook OFF ==="
cargo test --release -q -p emergent-universe --test memo 2>&1 | tail -2
echo "=== memo.rs control, hook ON (ES_CENSUS=1) ==="
env ES_CENSUS=1 cargo test --release -q -p emergent-universe --test memo 2>&1 | tail -2
