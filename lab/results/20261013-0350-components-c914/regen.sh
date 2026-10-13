#!/bin/sh
# Regen for 20261013-0350-components-c914 (run from repo root; <= 15 min).
# The tree already carries this run's patch (work/patch.diff, applied by the runner):
# the div_bench example and the env-gated timing stand-ins in fast_quad.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261013-0350-components-c914
OUT=$R/regen-out.txt
: > "$OUT"
echo "== machine ==" | tee -a "$OUT"
uname -m | tee -a "$OUT"
cat /proc/loadavg | tee -a "$OUT" || true
echo "== division floor + compile (default path; checksums must match dossier) ==" | tee -a "$OUT"
cargo run --release -q -p emergent-space --example div_bench -- all 2>&1 | tee -a "$OUT"
echo "== interior split, env-gated stand-ins (min of 3 medians per arm) ==" | tee -a "$OUT"
for arm in ES_DIV_HACK ES_SQRT_HACK ES_COS_HACK; do
  for i in 1 2 3; do env $arm=1 cargo run --release -q -p emergent-space --example div_bench -- compile 2>/dev/null | grep "compile\[" | tee -a "$OUT"; done
done
for i in 1 2 3; do env ES_DIV_HACK=1 ES_SQRT_HACK=1 ES_COS_HACK=1 cargo run --release -q -p emergent-space --example div_bench -- compile 2>/dev/null | grep "compile\[" | tee -a "$OUT"; done
for i in 1 2 3; do cargo run --release -q -p emergent-space --example div_bench -- compile 2>/dev/null | grep "compile\[" | tee -a "$OUT"; done
echo "== identity: space crate suite ==" | tee -a "$OUT"
cargo test --release -p emergent-space 2>&1 | grep -E "^test result" | tee -a "$OUT"
echo "done" | tee -a "$OUT"
