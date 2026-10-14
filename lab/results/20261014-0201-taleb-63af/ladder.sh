#!/bin/bash
# The decisive ladder: fit on seed 1, predict held-out seeds 2 and 3 with the seed-1 (k, C).
# One JSON line per run into ladder.jsonl. Generic specs + manufactured controls.
set -u
cd "$(dirname "$0")/../../.."
BIN=${BIN:-/home/glmlab/lab-target-2/release/belttail}
OUT=lab/results/20261014-0201-taleb-63af/ladder.jsonl
: > "$OUT"
run() { echo "## $*" >> "$OUT"; timeout 90 "$BIN" "$@" >> "$OUT" 2>>"$OUT.err" || echo "TIMEOUT/ERR: $*" >> "$OUT"; }

GEN="g-s3e-3-r1e-3 g-mid g-s3e-2-r1e-3 g-hi g-dense3k g-wide g-hot"
# fits (seed 1) for all specs incl. controls
for s in $GEN p-keys p-coorbital; do run fit "$s" 1; done
# held-out predictions with the seed-1 model
for s in $GEN; do
  line=$("$BIN" fit "$s" 1 | tail -1)
  k=$(echo "$line" | sed 's/.*"k_fit":\([0-9.]*\).*/\1/')
  C=$(echo "$line" | sed 's/.*"C_fit":\([0-9.e+-]*\).*/\1/')
  for seed in 2 3; do run pred "$s" "$seed" "$k" "$C"; done
done
echo done
