#!/bin/bash
cd "$(dirname "$0")"
python3 hlive2.py --tag belt_s1 --seed 1 --N 4000 --po 300 &
python3 hlive2.py --tag belt_s2 --seed 2 --N 4000 --po 300 &
python3 hlive2.py --tag belt_s3 --seed 3 --N 4000 --po 300 &
python3 hlive2.py --tag ctl_s1 --seed 1 --N 4000 --po 300 --mu 0 &
wait
echo PHASE1_DONE
python3 hlive2.py --tag belt_long_s1 --seed 1 --N 4000 --po 1200 &
python3 hlive_big.py --tag big --seed 11 --N 1048576 --po 100 &
wait
echo PHASE2_DONE
