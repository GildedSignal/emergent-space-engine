#!/bin/sh
# Fly one arm under each seam variant and print one line each. Usage: fly.sh <N> <coast|burn> <seed> [cut-game-s]
LAZY="${LAZY:-/home/glmlab/lab-target-1/release/examples/lazy}"
N="$1"; FL="$2"; SEED="$3"; CUT="${4:-48000}"
for v in off lazy retain; do
  case "$v" in
    off)    env -u ES_LAZY -u ES_LAZY_RETAIN "$LAZY" "$N" "$FL" "$CUT" "$SEED" 2>/dev/null ;;
    lazy)   env ES_LAZY=1 -u ES_LAZY_RETAIN "$LAZY" "$N" "$FL" "$CUT" "$SEED" 2>/dev/null ;;
    retain) env ES_LAZY=1 ES_LAZY_RETAIN=1 "$LAZY" "$N" "$FL" "$CUT" "$SEED" 2>/dev/null ;;
  esac | sed "s/^lazy: /$v /"
done
