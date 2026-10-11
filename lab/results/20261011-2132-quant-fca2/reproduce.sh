#!/bin/bash
# Reproduces every number in dossier.md (each command <= 60 s, total ~3 min).
# Needs this run's patch (saved by run.sh): --members clamp lifted to 4e6, --csv added.
# Build first: cargo build --release -p xtask
set -e
X=${X:-/home/glmlab/lab-target-2/release/xtask}
cd "$(dirname "$0")"
mkdir -p data

# A. members sweep (rtf 100, unpaced, 10 s). M=8000 peaks ~2.1 GB RSS: mind the machine's budget.
for M in 48 500 2000 8000; do
  /usr/bin/time -v $X universe --bench --unpaced --rtf 100 --seconds 10 --members $M --csv data/A-m$M.csv \
    > data/A-m$M.json 2> data/A-m$M.time
done

# B. time-factor sweep (M=48, unpaced, 5 s)
for R in 1000 10000; do
  $X universe --bench --unpaced --rtf $R --seconds 5 --members 48 --csv data/B-r$R.csv > data/B-r$R.json
done

# C. the player's burst (paced, level 15 = 11,561 g) and its level-0 baseline
$X universe --bench --rtf 100 --seconds 20 --members 48 --level 15 --csv data/C-l15.csv > data/C-l15.json
$X universe --bench --rtf 100 --seconds 20 --members 48 --csv data/C-l0.csv > data/C-l0.json

# D. controls: digest invariance (paced vs unpaced vs engine budget), memory attribution
$X universe --bench --rtf 100 --seconds 10 --members 48 --csv data/D-paced.csv > data/D-paced.json
$X universe --bench --unpaced --rtf 100 --seconds 10 --members 48 --engine-ms 0.5 --csv data/D-eng05.csv > data/D-eng05.json
/usr/bin/time -v $X universe --bench --unpaced --rtf 100 --seconds 2 --members 2000 \
  > data/D-m2000-s2.json 2> data/D-m2000-s2.time

echo "digests (must match):"
python3 -c "
import json
for f in ['data/A-m48.json','data/D-paced.json','data/D-eng05.json']:
    print(' ', json.load(open(f))['digest'])
"
