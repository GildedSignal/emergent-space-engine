#!/bin/bash
# Decisive grid: the wall-reflection train question for the game case (fleet x belt).
# 15 flights, each a separate process. Regenerates every number in the dossier.
set -u
BIN=${BIN:-/home/glmlab/lab-target-3/release/examples/fleetburst}
cd "$(dirname "$0")"
mkdir -p work

# bounce arms: the 4w clock (n-rung at bs2, boxscale ladder at n=1600)
$BIN --scene mixed --n 400  --boxscale 2 --nojitter --horizon 8192  --seed 1 --out work/mb400_bs2_s1.tsv &
$BIN --scene mixed --n 400  --boxscale 2 --nojitter --horizon 8192  --seed 2 --out work/mb400_bs2_s2.tsv &
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --horizon 16384 --seed 1 --out work/mb1600_bs2_s1.tsv &
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --horizon 16384 --seed 2 --out work/mb1600_bs2_s2.tsv &
$BIN --scene mixed --n 1600 --boxscale 1 --nojitter --horizon 16384 --seed 1 --out work/mb1600_bs1_s1.tsv &
$BIN --scene mixed --n 6400 --boxscale 2 --nojitter --horizon 16384 --seed 1 --out work/mb6400_bs2_s1.tsv &
wait
$BIN --scene mixed --n 1600 --boxscale 3 --nojitter --horizon 16384 --seed 1 --out work/mb1600_bs3_s1.tsv &
# free space: one crossing by geometry
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --free --horizon 8192 --seed 1 --out work/mf1600_s1.tsv &
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --free --horizon 8192 --seed 2 --out work/mf1600_s2.tsv &
$BIN --scene mixed --n 400  --boxscale 2 --nojitter --free --horizon 4096 --seed 1 --out work/mf400_s1.tsv &
# cloud-only controls (must be flat: the instrument's negative control)
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --nofleet --horizon 16384 --seed 1 --out work/co1600_bs2_s1.tsv &
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --nofleet --horizon 16384 --seed 2 --out work/co1600_bs2_s2.tsv &
$BIN --scene mixed --n 400  --boxscale 2 --nojitter --nofleet --horizon 8192  --seed 1 --out work/co400_bs2_s1.tsv &
wait
# generic formation (galaxy jitter) and hot belt (checker2-comparable cloudvmax q/4)
$BIN --scene mixed --n 1600 --boxscale 2 --horizon 16384 --seed 1 --out work/mj1600_bs2_s1.tsv &
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --cloudvmax 262144 --horizon 16384 --seed 1 --out work/mh1600_bs2_s1.tsv &
wait
echo GRID_DONE
