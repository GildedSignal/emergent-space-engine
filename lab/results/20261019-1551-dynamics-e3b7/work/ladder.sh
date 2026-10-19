#!/bin/sh
# The decisive ladder. One process at a time (shared machine, <2 GB each).
R=/home/glmlab/actions-runner/_work/emergent-space-engine/lab-3
B=$R/target/release/examples/gravitybelt
[ -x $B ] || B=/home/glmlab/lab-target-3/release/examples/gravitybelt
cd $R
$B --n 1600 --seed 1 --horizon 49152 --out lab/results/20261019-1551-dynamics-e3b7/work/G_s1_h49152.tsv
$B --n 1600 --seed 1 --horizon 49152 --nofleet --out lab/results/20261019-1551-dynamics-e3b7/work/C_s1_h49152.tsv
$B --n 1600 --seed 1 --horizon 24576 --boxhalf 150 --out lab/results/20261019-1551-dynamics-e3b7/work/GW_s1_h24576.tsv
$B --n 1600 --seed 2 --horizon 16384 --out lab/results/20261019-1551-dynamics-e3b7/work/G_s2_h16384.tsv
$B --n 1600 --seed 2 --horizon 16384 --nofleet --out lab/results/20261019-1551-dynamics-e3b7/work/C_s2_h16384.tsv
echo LADDER-DONE
