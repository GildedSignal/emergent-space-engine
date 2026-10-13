#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped tree plus this run's patch
# (work/patch.diff, applied by the runner before this runs). ~6 min warm, ~10 min cold.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
RUN="$ROOT/lab/results/20261013-2252-components-be78"
OUT="$RUN/work/regen"
mkdir -p "$OUT"
XT="${CARGO_TARGET_DIR:-target}/release/xtask"

# 1. The probe build (stage timers; the probe itself is the ES_WORD_FIRST env var).
cargo build --release -p xtask --features prof

# 2. The seven scenes, shipped arm then probe arm, sequentially (timings on a shared box).
run() { local m=$1 s=$2 rt=$3 arm=$4; local tag="m$m-s$s-rtf$rt"
  if [ "$arm" = on ]; then ES_WORD_FIRST=1 "$XT" universe --bench --seed "$s" --rtf "$rt" --seconds 8 --members "$m" > "$OUT/$tag-on.json" 2>&1
  else "$XT" universe --bench --seed "$s" --rtf "$rt" --seconds 8 --members "$m" > "$OUT/$tag-$arm.json" 2>&1; fi; }
run 1500 1 1 off;  run 1500 1 1 on      # tuning seed
run 1500 3 1 off;  run 1500 3 1 on      # held out
run 1500 5 1 off;  run 1500 5 1 on      # held out
run 1500 7 1 off;  run 1500 7 1 on      # held out
run 4000 3 1 off;  run 4000 3 1 on      # held out
run 8000 3 1 off;  run 8000 3 1 on      # held out
run 400  1 100 off; run 400 1 100 on    # flying pace (collapse edge on this box)
run 400  1 100 off2                    # the wobble control: shipped, run twice

# 3. The plain build (the shipped feature set: no prof), one scene, both arms.
cargo build --release -p xtask
"$XT" universe --bench --seed 3 --rtf 1 --seconds 8 --members 1500 > "$OUT/plain-m1500-s3-off.json" 2>&1
ES_WORD_FIRST=1 "$XT" universe --bench --seed 3 --rtf 1 --seconds 8 --members 1500 > "$OUT/plain-m1500-s3-on.json" 2>&1

# 4. The dossier's table.
python3 "$RUN/compare.py" "$OUT"
