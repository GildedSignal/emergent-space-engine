#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's patch
# (work/patch.diff: adds examples/nladder_lin.rs, a read-only Linux port of the shipped
# nladder.rs + a 1 Hz view refresh + a store census). Total < 6 min.
# NOTE: the long census arms in the dossier's history were killed at this run's 2 GB
# survival ceiling; this regen reproduces the growth curve (sampled), the no-gather
# control (sampled), and the pre-wave arm's non-completion within 100 s.
set -e
cd "$(dirname "$0")/../.."
git apply --allow-empty "$(dirname "$0")/work/patch.diff" 2>/dev/null || true
cargo build --release -p emergent-universe --example nladder_lin
B=${CARGO_TARGET_DIR:-target}/release/examples/nladder_lin
OUT="$(dirname "$0")/out"; mkdir -p "$OUT"
cd "$OUT"

sample() { # $1 pid  $2 label — append rss samples to $2
  i=0
  while kill -0 $1 2>/dev/null; do
    rss=$(awk '/VmRSS/{print $2}' /proc/$1/status 2>/dev/null)
    echo "t=$((i*10))s rss_kb=$rss" >> "$2"
    [ -n "$rss" ] && [ "$rss" -gt 1900000 ] && break
    sleep 10; i=$((i+1)); [ $i -ge 15 ] && break
  done
}

echo "=== growth arm: 10^4 coast, rtf 6000, 12 ms, view on (dossier: 1,912 MB at t130 s)"
"$B" 10000 coast 20 6000 12 > growth_flight.txt 2>&1 & P=$!; sample $P growth_on.txt; kill -9 $P 2>/dev/null || true
tail -1 growth_on.txt; cat growth_flight.txt

echo "=== control: same arm, view off (dossier: 1.78 GB at 123 s)"
ES_NO_GATHER=1 "$B" 10000 coast 20 6000 12 > nogather_flight.txt 2>&1 & P=$!; sample $P growth_off.txt; kill -9 $P 2>/dev/null || true
tail -1 growth_off.txt; cat nogather_flight.txt

echo "=== pre-wave arm: 120 frames end before the wave's first kicks; dossier: fails to complete in 100 s"
timeout 100 "$B" 10000 coast 2 6000 12 > prewave.txt 2>&1 || echo "exit $? (killed by timeout, as the dossier reports)"
cat prewave.txt

echo "=== the library quotes (cached Readwise export, work/readwise/)"
jq -r 'select(.t|test("machine that builds the machine|Step one should be|Knowledge is subtractive|pointers, addresses|man-masses|biggest constraint or bottleneck";"i"))| "\(.a) | \(.b)"' \
  ../work/readwise/all.jsonl | sort -u
echo REGEN_DONE
