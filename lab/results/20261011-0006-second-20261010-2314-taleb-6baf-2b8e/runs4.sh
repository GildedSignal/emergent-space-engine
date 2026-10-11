#!/bin/bash
cd "$(dirname "$0")"
python3 hlive2.py --tag belt_long_s1 --seed 1 --N 4000 --po 1200
echo LONG_DONE
python3 hlive_big.py --tag big --seed 11 --N 1048576 --po 100
echo BIG_DONE
