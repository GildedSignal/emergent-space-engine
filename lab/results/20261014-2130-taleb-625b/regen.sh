#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus work/patch.diff (applied by the runner before
# this runs). ~8 min wall. The four main arms fly in parallel exactly as in the run (the box is shared either way;
# all order-of-magnitude). The band L8 burn at 1e5 is EXPECTED to be killed (exit 137, ~11 GB): that kill is the
# number; its RSS curve lands in work/band_burn_rss.txt.
set -e
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261014-2130-taleb-625b
mkdir -p "$R/work"
BIN=/home/glmlab/lab-target-3/release/examples/wave_band
[ -x "$BIN" ] || BIN=./target/release/examples/wave_band
cargo build --release -p emergent-universe --features prof --example wave_band
cargo build --release -p emergent-universe --example belt_first
cargo run --release -p emergent-universe --example belt_first -- 100000 > "$R/work/belt_first.txt" 2>&1
for arm in "home 1 100000 160 1 8:home_burn" "band 1 100000 160 1 8:band_burn" "band 1 100000 160 0 0:band_coast" "home 1 100000 160 0 0:home_coast"; do
  spec="${arm%:*}"; name="${arm#*:}"
  "$BIN" $spec > "$R/work/$name.txt" 2>&1 &
done
wait || true   # band_burn is killed by the memory cap: its partial file is not an error
# The kill arm, watched from the outside (the RSS curve and the exit code are the evidence).
"$BIN" band 1 100000 160 1 8 > "$R/work/band_burn_watch.txt" 2>&1 &
KPID=$!
: > "$R/work/band_burn_rss.txt"
for i in $(seq 1 40); do
  sleep 2
  RSS=$(awk '/VmRSS/{print $2}' /proc/$KPID/status 2>/dev/null) || break
  [ -z "$RSS" ] && break
  echo "rss_mb $((RSS/1024))" >> "$R/work/band_burn_rss.txt"
done
wait $KPID || echo "band_burn exit $?" >> "$R/work/band_burn_rss.txt"
# The schedule certificate (P5): the same band coast, unlimited budget -> one digest with the budgeted arm.
"$BIN" band 1 100000 160 0 0 1000000 > "$R/work/band_coast_free.txt" 2>&1
# Held-out seeds: coast at 1e5 (the monster), burn at 1e4 (the seam's other face).
"$BIN" band 2 100000 160 0 0 > "$R/work/band_coast_s2.txt" 2>&1
"$BIN" band 2 10000 160 1 8 > "$R/work/band_burn_s2_1e4.txt" 2>&1
# The population control: in-band burn at 1e4 completes flat.
"$BIN" band 1 10000 160 1 8 > "$R/work/band_burn_1e4.txt" 2>&1
echo done
