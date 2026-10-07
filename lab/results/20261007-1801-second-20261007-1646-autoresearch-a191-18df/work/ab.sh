#!/bin/bash
# Interleaved A/B: base (HEAD) vs opt (scope-free deletion). Ratios only (shared box).
set -u
R="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$R/data"
cd "$R/work"
run() { # tag bin extra-args...
  local tag=$1 bin=$2; shift 2
  ./"$bin" universe --kick-bench "$@" --seconds 20 > "$R/data/$tag.json" 2>"$R/data/$tag.err" || echo "EXIT $? $tag"
}
scenes=("tuned:--rtf 100" "m24:--members 24 --rtf 100" "m96:--members 96 --rtf 100" "rtf60:--rtf 60" "m200:--members 200 --rtf 100" "rtf10:--rtf 10")
for s in "${scenes[@]}"; do
  name=${s%%:*}; args=${s#*:}
  pairs=2; [ "$name" = tuned ] && pairs=3
  for p in $(seq $pairs); do
    run "${name}-b$p" bin-base $args
    run "${name}-o$p" bin-opt $args
  done
done
echo DONE
