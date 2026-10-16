#!/usr/bin/env bash
# Regen (lab 20261016-1120-components-cdf0): rebuild the ladder example with the print-only
# census patch (work/patch.diff, applied by the runner before this runs), fly the four census
# flights, and print the aggregates the dossier quotes. < 15 min: build ~5 min cold, runs ~35 s.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # the repo root (lab/results/<run>/regen.sh)
RUN=lab/results/20261016-1120-components-cdf0

if ! git diff --quiet -- crates/universe/src/encounter.rs 2>/dev/null; then :; else
  git apply "$RUN/work/patch.diff"
fi
cargo build --release -p emergent-universe --example nladder

export ES_SCAN_CENSUS=1
mkdir -p "$RUN/raw"
for spec in "0 burn" "1000 burn" "1000 coast" "100000 burn"; do
  set -- $spec
  /home/glmlab/lab-target-1/release/examples/nladder "$1" "$2" 20 \
    > "$RUN/raw/n$1_$2.out" 2> "$RUN/raw/n$1_$2.err" || true
done

echo "== per flight: capture half (fallback vs kept) and answer half"
for f in "$RUN"/raw/*.err; do
  echo "== ${f#"$RUN"/raw/}"
  grep SCAN_CAP "$f" | awk '{doll=$3; sub("doll=","",doll); near=$5; sub("near=","",near); cu=$7; sub("cap_us=","",cu); key=doll"/"(near==-1?"FB":"kept"); c[key]++; s[key]+=cu; if(cu+0>m[key])m[key]=cu+0} END{for(k in c) printf "%s n=%d cap_us_mean=%.0f cap_us_max=%.0f\n", k, c[k], s[k]/c[k], m[k]}' | sort
  grep SCAN_ANS "$f" | awk '{c=$3; sub("cand=","",c); h=$4; sub("hits=","",h); u=$6; sub("us_per_cand=","",u); mm=$8; sub("min_miss_reach=","",mm); n++; sc+=c; sh+=h; su+=u; if(n==1||mm+0<minm)minm=mm+0; if(c+0>cm)cm=c+0} END{printf "ANS scans=%d reads=%d hits=%d us_per_read_mean=%.2f cand_max=%d min_miss_min=%.3g reads_per_hit=%.0f\n", n, sc, sh, su/n, cm, minm, (sh?sc/sh:0)}'
done
echo "== per doll medians (analyze.py)"
python3 "$RUN/analyze.py" "$RUN"/raw/*.err
