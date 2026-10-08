#!/bin/bash
# Second-author ladder: the checker's named experiment for gold.
# Regen check (original m192 row), then the real-range ladder (members <= 400), 3 seeds,
# then digest-invariance pairs in the real range. Sequential; one process at a time.
set -u
cd "$(dirname "$0")"
XT=/home/glmlab/lab-target-3/release/xtask
echo "=== binary sha256 $(sha256sum $XT | cut -c1-16)… ; start $(date -u +%H:%M:%S); $(uptime | sed 's/.*load/load/')"

# 0. Regeneration: the original record's m192 row (seed 1, rtf 100, 30 s, defaults).
$XT universe --bench --members 192 --seed 1 --rtf 100 --seconds 30 > regen-m192-s1.json 2> regen-m192-s1.err
echo "regen-m192-s1 done $(date -u +%H:%M:%S)"

# 1. The ladder: members x seeds, paced, defaults otherwise.
for M in 48 96 192 384; do
  for S in 1 7 13; do
    $XT universe --bench --members $M --seed $S --rtf 100 --seconds 30 > m${M}-s${S}.json 2> m${M}-s${S}.err
    echo "m${M}-s${S} done $(date -u +%H:%M:%S)"
  done
done

# 2. Digest invariance inside the real range: engine-ms 0.5 vs 50, unpaced, 15 s.
$XT universe --bench --members 48  --seed 1  --rtf 100 --seconds 15 --unpaced --engine-ms 0.5 > inv-m48-s1-e05.json 2>/dev/null
echo "inv-m48-s1-e05 done $(date -u +%H:%M:%S)"
$XT universe --bench --members 48  --seed 1  --rtf 100 --seconds 15 --unpaced --engine-ms 50 > inv-m48-s1-e50.json 2>/dev/null
echo "inv-m48-s1-e50 done $(date -u +%H:%M:%S)"
$XT universe --bench --members 192 --seed 13 --rtf 100 --seconds 15 --unpaced --engine-ms 0.5 > inv-m192-s13-e05.json 2>/dev/null
echo "inv-m192-s13-e05 done $(date -u +%H:%M:%S)"
$XT universe --bench --members 192 --seed 13 --rtf 100 --seconds 15 --unpaced --engine-ms 50 > inv-m192-s13-e50.json 2>/dev/null
echo "inv-m192-s13-e50 done $(date -u +%H:%M:%S)"

echo "=== all done $(date -u +%H:%M:%S); $(uptime | sed 's/.*load/load/')"
