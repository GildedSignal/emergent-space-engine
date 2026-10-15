#!/bin/sh
# Regen: every dossier number, from a clean tree, in ~13 min.
# 1. apply the combined patch (8b89's seam+ALL + this run's history census instrument)
# 2. build the example
# 3. re-fly: anchors, the belt depth ladder (all 32/48/96k + ctl 96k), the comet ladder
#    (N=100 3k/32k; N=25 32k/64k — the N=25 pair keeps every process under the 2 GB budget;
#    the N=100 64k arm needs ~5.7 GB and is deliberately not flown)
# 4. print the summary + growth fits
set -e
cd "$(dirname "$0")/../../.."          # repo root
R="$(cd "$(dirname "$0")" && pwd)"
git apply -R "$R/work/patch.diff" 2>/dev/null || true
git apply "$R/work/patch.diff"
cargo build --release -p emergent-universe --example passage_demote -j 8 2>&1 | tail -1
B="${CARGO_TARGET_DIR:-target}/release/examples/passage_demote"
mkdir -p "$R/flights"
run() { name="$1"; shift; envs="$1"; shift
  env $envs timeout 1500 "$B" "$@" > "$R/flights/$name.txt" 2>&1 || echo "FAIL $name" >> "$R/flights/$name.txt"; }
# anchors (8b89's published: ctl 10^4 coast 20k digest 5e8c9e24…5fbab6f)
run smoke_ctl "ES_LAZY_ENTRY=0" 10000 coast 20000 1 1000
run smoke_all "ES_LAZY_ENTRY=1 ES_LAZY_ALL=1" 10000 coast 20000 1 1000
# the belt ladder (saturation + identity at 96k)
run belt_all_32k "ES_LAZY_ENTRY=1 ES_LAZY_ALL=1" 10000 coast 32000 1 1000
run belt_all_48k "ES_LAZY_ENTRY=1 ES_LAZY_ALL=1" 10000 coast 48000 1 1000
run belt_all_96k "ES_LAZY_ENTRY=1 ES_LAZY_ALL=1" 10000 coast 96000 1 1000
run belt_ctl_96k "ES_LAZY_ENTRY=0" 10000 coast 96000 1 1000
# the comet ladder (linear growth; per-comet counts = segments / comets)
run comet_ctl_3k  "ES_LAZY_ENTRY=0" 100 stargraze 3000 3 1000
run comet_ctl_32k "ES_LAZY_ENTRY=0" 100 stargraze 32000 3 1000
run comet25_ctl_32k "ES_LAZY_ENTRY=0" 25 stargraze 32000 3 1000
run comet25_ctl_64k "ES_LAZY_ENTRY=0" 25 stargraze 64000 3 1000
run comet25_all_64k "ES_LAZY_ENTRY=1 ES_LAZY_ALL=1" 25 stargraze 64000 3 1000
python3 "$R/table.py" "$R" | tee "$R/summary.txt"
