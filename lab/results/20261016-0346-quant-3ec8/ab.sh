#!/usr/bin/env bash
# The decisive A/B: belt N x seed x arm, arms interleaved (A/B/A/B) to cancel drift.
# Each arm is a fresh process. Prints one JSONL row per flight to stdout.
set -u
# Repo root by Cargo.toml discovery (depth-independent, as in regen.sh).
D="$(cd "$(dirname "$0")" && pwd)"
while [ "$D" != "/" ] && [ ! -f "$D/Cargo.toml" ]; do D="$(dirname "$D")"; done
cd "$D"
BIN="${REGEN_PASS_BENCH:-/home/glmlab/lab-target-2/release/pass_bench}"
export ES_PASS_SPLIT=1
for rep in 1 2; do
  for n in 10000 30000 100000 300000; do
    for seed in 1 7; do
      if [ "$rep" = 2 ] && { [ "$n" != 10000 ] || [ "$seed" != 1 ]; }; then continue; fi
      for arm in 0 1; do
        row=$(ES_ONE_READ=$arm "$BIN" "$n" "$seed" 2>/tmp/pass_$$)
        plan=$(grep -o 'plan_us=[0-9]*' /tmp/pass_$$ | cut -d= -f2)
        requeue=$(grep -o 'requeue_us=[0-9]*' /tmp/pass_$$ | cut -d= -f2)
        rekey=$(grep -o 'rekey_us=[0-9]*' /tmp/pass_$$ | cut -d= -f2)
        echo "$row plan_us=$plan requeue_us=$requeue rekey_us=$rekey rep=$rep"
      done
    done
  done
done
rm -f /tmp/pass_$$
