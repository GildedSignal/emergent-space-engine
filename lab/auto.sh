#!/usr/bin/env bash
# The autonomous lab: start three free-lens runs, rotating through the lenses once per 5-hour GLM window,
# and print their run ids. Cloud only (run.sh refuses macOS).
cd "$(git rev-parse --show-toplevel)"
lenses=(dynamics system components scout autoresearch quant spacex taleb library redteam)
n=${#lenses[@]}; k=$(( $(date -u +%s) / 18000 ))
for j in 0 1 2; do bash lab/run.sh start "${lenses[$(( (k * 3 + j) % n ))]}" 60 | tail -1; done
