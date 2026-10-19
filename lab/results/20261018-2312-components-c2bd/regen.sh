#!/bin/sh
# Regen for 20261018-2312-components-c2bd: rebuilds the probe (from work/patch.diff, applied
# by the runner before this runs) and regenerates every dossier number: 9 flights (~35 s)
# plus the analysis. < 15 min on the lab box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261018-2312-components-c2bd
echo "== machine state =="; date; uptime; grep -E "MemTotal|MemAvailable" /proc/meminfo | head -2
echo "== build =="; cargo build --release -p emergent-universe --example quantum 2>&1 | grep -E "^error" && exit 1 || true
echo "== the sweep (belt 2.5 AU orbits: 2-orbit arms k in 7 5 3 2 1 0 -2; long arms k in 7 2) =="
mkdir -p $R/raw
for k in 7 5 3 2 1 0 -2; do
  timeout 55 cargo run --release -p emergent-universe --example quantum -- $k 2 > $R/raw/q${k}_o2.log 2>&1 || echo "k=$k FAILED/timeout"
done
for k in 7 2; do
  timeout 100 cargo run --release -p emergent-universe --example quantum -- $k 6 > $R/raw/q${k}_o6.log 2>&1 || echo "long k=$k FAILED/timeout"
done
echo "== the shipped plane's own belt cadence, independent witness (belt_first, 5 s) =="
timeout 55 cargo run --release -p emergent-universe --example belt_first -- 300 2>&1 | grep belt
echo "== analysis =="
python3 $R/analyze.py
