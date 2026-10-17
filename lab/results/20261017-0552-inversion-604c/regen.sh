#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus work/patch.diff
# (applied by the runner before this runs). Linux/x86; orders of magnitude only.
# Total: one release build (~1-2 min warm, ~4 min cold) + ~30 s of flights. < 15 min.
set -e
cd "$(dirname "$0")/../../.."
echo "machine: $(uname -srm) cpus=$(nproc) load=$(cat /proc/loadavg)"
cargo build --release --features prof -p emergent-universe --example scanprobe 2>&1 | tail -1
B=$(cargo metadata --format-version 1 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | head -1 | cut -d'"' -f4)/release/examples/scanprobe
[ -x "$B" ] || B=target/release/examples/scanprobe
OUT="$(dirname "$0")/raw"
mkdir -p "$OUT"
# The matrix: formation sweep (extra=0), the census's belt controls (form=0),
# the composition tiers (formation beside the belt), each coast 10 s at rtf 100.
for args in "0 0 10" "50 0 10" "111 0 10" "200 0 10" "1000 0 10" "0 10000 10" "0 100000 6" "200 10000 10" "3000 10000 10"; do
  set -- $args
  echo "=== form=$1 extra=$2 s=$3"
  "$B" "$1" "$2" "$3" 100 | tee "$OUT/f$1_e$2_s$3.txt" | grep -E "^(scan:|window:|probe:)"
done
# Instrument stability: the census lines must be bit-identical across reruns (digests are
# wall-paced at rtf and end at different ticks; the census is the claim's instrument).
echo "=== census stability (3 reruns, form=200)"
for i in 1 2 3; do "$B" 200 0 10 100 | grep "^scan:" | md5sum; done
echo "done."
