#!/bin/sh
# Regen for 20261017-0739-taleb-9b46. Applies work/patch.diff is not needed: the runner
# applies it before this runs. Builds the instrument, then regenerates every number in
# dossier.md. Total ~10 min on the shared 8-vCPU box (the G arm alone is ~160 s).
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=/home/glmlab/lab-target-2/release/examples/ruin
cargo build --release --offline -p emergent-allocator --example ruin
cd lab/results/20261017-0739-taleb-9b46
mkdir -p out

# Matrix, H=1500, m=0.5, cannon=128, quiet=1, per=12 (single run_to per arm).
echo "=== A 14k shipped s1 ==="; timeout 240 $R 24 32 36 12 1500 0.5 128 1 1500 230 1 | tee out/A-14k-shipped.txt | tail -2
echo "=== B 14k ES_CAP=64 s1 ==="; ES_CAP=64 timeout 240 $R 24 32 36 12 1500 0.5 128 1 1500 230 1 | tee out/B-14k-cap64.txt | tail -2
echo "=== C 28k shipped s1 ==="; timeout 240 $R 24 32 72 12 1500 0.5 128 1 1500 230 1 | tee out/C-28k-shipped.txt | tail -2
echo "=== C2 28k shipped s1 (replicate) ==="; timeout 240 $R 24 32 72 12 1500 0.5 128 1 1500 230 1 | tee out/D-28k-replicate.txt | tail -2
echo "=== E 28k shipped s7 ==="; timeout 240 $R 24 32 72 12 1500 0.5 128 1 1500 230 7 | tee out/E-28k-shipped-s7.txt | tail -2
echo "=== G 28k shipped s2 (the 160 s draw) ==="; timeout 280 $R 24 32 72 12 1500 0.5 128 1 1500 270 2 | tee out/G-28k-shipped-s2.txt | tail -2
echo "=== F 28k quiet control, traced ==="; timeout 260 $R 24 32 72 12 1500 0.5 1 1 150 250 1 | tee out/F-28k-quiet-traced.txt | tail -3

# The assert: chunked run_to (publish between advances) on the conflict wave.
echo "=== panic probe 864 chunk100 (x2) ==="
for i in 1 2; do timeout 60 $R 24 8 6 12 1200 0.5 128 1 100 50 1 2>&1 | grep -E "panicked at|DONE" | head -1; done
echo "=== panic probe 14k chunk500 ==="; timeout 240 $R 24 32 36 12 1500 0.5 128 1 500 230 1 | tee out/P-14k-chunk500.txt | grep -E "panicked at|DONE" | head -1
echo "=== panic probe 28k chunk500 ==="; timeout 240 $R 24 32 72 12 1500 0.5 128 1 500 230 1 | tee out/P-28k-chunk500.txt | grep -E "panicked at|DONE" | head -1
