#!/usr/bin/env bash
# Follow-ups: digest control under a biting budget; unpaced raw ceiling; pure kick resolver cost.
set -u
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-3
OUT=lab/results/20261008-1859-quant-19d6/work
[ -s "$OUT/burn-rtf100-L15-ms1.json" ] || timeout 58 ./target/release/xtask universe --bench --seed 1 --rtf 100 --level 15 --seconds 30 --engine-ms 1 > "$OUT/burn-rtf100-L15-ms1.json" 2> "$OUT/burn-rtf100-L15-ms1.err" || echo "ms1 FAILED"
[ -s "$OUT/knee-rtf1p6e4-unpaced.json" ] || timeout 58 ./target/release/xtask universe --bench --seed 1 --rtf 16000 --seconds 30 --unpaced > "$OUT/knee-rtf1p6e4-unpaced.json" 2> "$OUT/knee-rtf1p6e4-unpaced.err" || echo "unpaced FAILED"
[ -s "$OUT/kickbench-rtf100.json" ] || timeout 58 ./target/release/xtask universe --kick-bench --seed 1 --rtf 100 --seconds 20 > "$OUT/kickbench-rtf100.json" 2> "$OUT/kickbench-rtf100.err" || echo "kickbench FAILED"
echo done
