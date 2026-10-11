#!/bin/sh
# The kick-magnitude rung: admission curve + events at each magnitude.
set -e
cd "$(dirname "$0")"
K=./kickmag/target/release/kickmag
mkdir -p data
: > data/kickmag.jsonl
for mode in k0 k1 k2 k3 k4 k5 uniform; do
  for f in 0.01 0.05 0.1 0.3 0.5 1.0; do
    $K curve $mode 4096 64 $f data/kickmag.jsonl >/dev/null
  done
  $K events $mode 4096 10000 data/kickmag.jsonl >/dev/null
done
# saturation (the checker's adversarial case) at shipped, top stress and family jump
for mode in k0 k5 uniform; do
  $K events $mode 4096 40000 data/kickmag.jsonl >/dev/null
done
# m-scale stability of S at family jump (the checker varied m for k0)
for m in 1024 16384; do
  $K events uniform $m 10000 data/kickmag.jsonl >/dev/null
  $K curve uniform $m 64 0.1 data/kickmag.jsonl >/dev/null
done
echo done
