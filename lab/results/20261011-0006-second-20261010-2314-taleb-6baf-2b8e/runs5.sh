#!/bin/bash
cd "$(dirname "$0")"
# finish the shipped-code record: rings + analyze
python3 hlive.py --tag ring21_s1 --seed 1 --N 2000 --po 600 --ring 2.54,0.05,0.02
python3 hlive.py --tag ring21_s2 --seed 2 --N 2000 --po 600 --ring 2.54,0.05,0.02
python3 hlive.py --tag ringoff_s1 --seed 1 --N 2000 --po 600 --ring 2.80,0.05,0.02
python3 hlive.py --tag ringoff_s2 --seed 2 --N 2000 --po 600 --ring 2.80,0.05,0.02
cp metrics.json metrics-orig.json
python3 analyze.py
mv metrics.json metrics-regen.json
mv metrics-orig.json metrics.json
echo RINGS_DONE
