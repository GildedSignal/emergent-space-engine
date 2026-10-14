#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus work/patch.diff (applied by the runner before
# this runs). ~8 min wall; every timing-sensitive arm runs solo in sequence (the digest controls run in parallel —
# their digests, not their timings, are the claim). The kill arms self-limit at ES_RSS_LIMIT_MB (default 1800) —
# the box kills at 2 GB; the record's exit-137 kill is caught one step early so the counters survive.
set -e
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261014-2248-second-20261014-2130-taleb-625b-c481
mkdir -p "$R/work"
cargo build --release -p emergent-universe --features prof --example band_site
B=./target/release/examples/band_site
[ -x "$B" ] || B=/home/glmlab/lab-target-0/release/examples/band_site
# The digest controls (parallel; digests only — the instrument must be outcome-neutral).
"$B" ctrl home 1 100000 160 0 0 12 100 > "$R/work/home_coast.txt" 2>&1 &
"$B" ctrl band 1 100000 160 0 0 12 100 > "$R/work/band_coast.txt" 2>&1 &
"$B" ctrl home 1 100000 160 1 8 12 100 > "$R/work/home_burn.txt" 2>&1 &
wait
# The kill arm (solo; self-limited) and its held-out limit-1500 rerun.
"$B" ctrl band 1 100000 160 1 8 12 100 > "$R/work/band_burn_kill.txt" 2>&1
ES_RSS_LIMIT_MB=1500 "$B" ctrl band 1 100000 160 1 8 12 100 > "$R/work/band_burn_kill_1500.txt" 2>&1
# The arm the record calls "completes flat": the drain's freeze and the monotone standing.
"$B" ctrl band 1 10000 160 1 8 12 100 > "$R/work/band_burn_1e4.txt" 2>&1
# The transit's integrand: the radius sweep (parked, L8, 20 s each).
for r in 1.0 1.7 2.0 3.0 3.5; do
  "$B" probe "$r" 1 100000 20 1 8 12 100 > "$R/work/probe_$r.txt" 2>&1
done
for r in 1.75 1.8 1.85 1.9 1.95; do
  "$B" probe "$r" 1 10000 6 1 8 12 100 > "$R/work/probe_$r.txt" 2>&1
done
# The crossing arms: below the band under burn (safe), at the walk-all edge (ruin), and the coast controls.
"$B" cross 2.0 1 100000 60 1 8 0.95 2.0 12 100 > "$R/work/cross_burn.txt" 2>&1        # placed ~1.03 AU (see below)
"$B" cross 2.0 1 100000 40 1 8 0.95 3.7011 12 300 > "$R/work/cross_burn_edge.txt" 2>&1 # placed 1.898 AU
"$B" cross 2.0 1 100000 60 1 8 0.95 3.8903 12 300 > "$R/work/cross_burn_1p995.txt" 2>&1 # placed 1.995 AU
"$B" cross 2.0 1 100000 60 0 0 0.95 3.7011 12 100 > "$R/work/cross_coast.txt" 2>&1
"$B" cross 2.0 2 100000 60 0 0 0.95 3.7011 12 100 > "$R/work/cross_coast_s2.txt" 2>&1
# Note: the engine places `phase` at radius r0/(1+e) on this orbit family (calibrated in the run): pass
# r0 = target x (1+e). The r0=2.0 arm lands at ~1.03 AU (the transit's below-band segment).
grep -H -E "digest" "$R/work"/home_coast.txt "$R/work"/band_coast.txt "$R/work"/home_burn.txt "$R/work"/band_burn_1e4.txt
grep -H -E "scanmem final|SELF" "$R/work"/band_burn_kill.txt "$R/work"/band_burn_1e4.txt
echo done
