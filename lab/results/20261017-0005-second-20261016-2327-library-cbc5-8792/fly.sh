#!/bin/bash
# The checker's named gold experiment: standalone mint+demote (promote_us/demote_us) at
# dwell classes {~0 (seam), 100, 1000, next-kick (retain)} in both regimes, plus identity
# controls (every arm prints the ctl digest of its scene; dwell without the seam is inert).
# One process at a time (10^5 scenes peak ~650 MB).
set -u
cd "$(dirname "$0")"
BIN=${BIN:-/home/glmlab/lab-bin-8792}
mkdir -p flights
fly() { # name scene... (arms fixed per name)
  local name=$1; shift
  local scene=$(echo "$*" | tr ' ' '_')
  local f="flights/${name}_${scene}.txt"
  echo "== $name $*"
  case $name in
    ctl)    env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT -u ES_RETAIN_DWELL $BIN "$@" > "$f" 2>&1 ;;
    seam)   env -u ES_RETAIN -u ES_RETAIN_HOT -u ES_RETAIN_DWELL ES_LAZY_ENTRY=1 $BIN "$@" > "$f" 2>&1 ;;
    retain) env -u ES_RETAIN_HOT -u ES_RETAIN_DWELL ES_LAZY_ENTRY=1 ES_RETAIN=1 $BIN "$@" > "$f" 2>&1 ;;
    dwell100)  env -u ES_RETAIN -u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN_DWELL=100 $BIN "$@" > "$f" 2>&1 ;;
    dwell1000) env -u ES_RETAIN -u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN_DWELL=1000 $BIN "$@" > "$f" 2>&1 ;;
    noseam) env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT ES_RETAIN_DWELL=100 $BIN "$@" > "$f" 2>&1 ;;
    dwell17)  env -u ES_RETAIN -u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN_DWELL=17 $BIN "$@" > "$f" 2>&1 ;;
  esac
  grep -h "^digest\|bodies\|retain hits\|demote_us" "$f"
}
for scene in "100000 coast 20000 1" "100000 burn 20000 1" "10000 coast 20000 1" "10000 burn 20000 1"; do
  for arm in ctl seam retain dwell100 dwell1000; do fly $arm $scene; done
done
fly noseam 100000 coast 20000 1
for scene in "100000 coast 20000 1" "100000 burn 20000 1" "10000 burn 20000 1"; do
  fly dwell17 $scene
done
echo DONE
