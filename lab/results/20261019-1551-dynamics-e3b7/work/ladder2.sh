#!/bin/sh
B=/home/glmlab/lab-target-3/release/examples/gravitybelt
R=/home/glmlab/actions-runner/_work/emergent-space-engine/lab-3/lab/results/20261019-1551-dynamics-e3b7/work
$B --n 1600 --seed 1 --horizon 49152 --nofleet --slim --out $R/C_s1_h49152.tsv 2>/dev/null
$B --n 1600 --seed 2 --horizon 16384 --slim --out $R/G_s2_h16384.tsv 2>/dev/null
$B --n 1600 --seed 2 --horizon 16384 --nofleet --slim --out $R/C_s2_h16384.tsv 2>/dev/null
$B --n 1600 --seed 1 --horizon 24576 --boxhalf 150 --slim --out $R/GW_s1_h24576.tsv 2>/dev/null
echo LADDER2-DONE
