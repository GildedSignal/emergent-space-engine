#!/usr/bin/env bash
# The quant run: capacity knee + burn impact, on the plane's own bench (deterministic, digested).
# Each invocation ≤ 55 s. Usage: driver.sh (runs the whole matrix, skips runs whose json exists).
set -u
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-3
OUT=lab/results/20261008-1859-quant-19d6/work
run() { # name rtf level
  local name=$1 rtf=$2 level=$3
  [ -s "$OUT/$name.json" ] && { echo "skip $name"; return; }
  echo "== $name (rtf $rtf, level $level) $(date +%H:%M:%S)"
  timeout 58 ./target/release/xtask universe --bench --seed 1 --rtf "$rtf" --level "$level" --seconds 30 > "$OUT/$name.json" 2> "$OUT/$name.err" \
    || echo "  FAILED exit=$? (see $name.err)"
}
run knee-rtf10     10     0
run base-rtf100    100    0
run knee-rtf1e3    1000   0
run knee-rtf4e3    4000   0
run knee-rtf1p6e4  16000  0
run burn-rtf100-L5   100  5
run burn-rtf100-L15  100  15
run burn-rtf1e3-L15  1000 15
echo done
