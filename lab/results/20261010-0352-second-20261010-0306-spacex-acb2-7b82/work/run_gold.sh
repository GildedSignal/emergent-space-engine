#!/bin/bash
# Gold experiment runner: 20 jobs (incl. the 10-min xhi escalation), 4 workers, ~30 min wall on the lab machine.
# Each job is deterministic in its seed; outputs land in gold_*.npz + gold_summary.jsonl
cd "$(dirname "$0")"
JOBS=$(mktemp)
for k in 0 1 2 3 4 5; do
  echo "cold_k$k 0.02 0.01 $((20261010+k)) hires gold"
  echo "hot_k$k 0.02 0.1 $((20261010+k)) hires gold"
done >> $JOBS
for k in 0 1 2; do
  echo "w004_k$k 0.04 0.01 $((20261010+k)) hires gold"
  echo "w010_k$k 0.1 0.01 $((20261010+k)) hires gold"
done >> $JOBS
echo "conv_ultra 0.02 0.01 20261010 ultra gold" >> $JOBS
echo "conv_xhi 0.02 0.01 20261010 xhi gold" >> $JOBS
OMP_NUM_THREADS=2 xargs -P 4 -L 1 python3 gold_probe.py < $JOBS 2>&1 | tee gold_summary.txt
rm -f $JOBS
python3 gold_controls.py
