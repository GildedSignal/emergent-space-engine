#!/bin/sh
# 1b3f decisive flights, sequential. Each prints probe lines every 2000 game-s + the ladder summary.
set -e
cd "$(dirname "$0")/../../.."   # repo root
BIN=${BIN:-$HOME/lab-target-1b3f/release/examples/nladder}
OUT=lab/results/20261019-0435-second-20261019-0325-library-9147-1b3f/logs
mkdir -p "$OUT"
KNOB="ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000"

echo "== ctrl-70k: coast, rtf 800, cap 130 =="
env $KNOB "$BIN" 30000 coast 100 800 > "$OUT/ctrl-70k.log" 2>&1
echo "== pin6e9 (global arm): ES_PIN_OLDEST=6000000000 =="
env $KNOB ES_PIN_OLDEST=6000000000 "$BIN" 30000 coast 100 800 > "$OUT/pin6e9.log" 2>&1
echo "== pin12e9 (global arm): ES_PIN_OLDEST=12000000000 =="
env $KNOB ES_PIN_OLDEST=12000000000 "$BIN" 30000 coast 100 800 > "$OUT/pin12e9.log" 2>&1
echo "== reader-pin6e9: per-reader + far pin =="
env $KNOB ES_PIN_OLDEST=6000000000 ES_READER_OLDEST=1 "$BIN" 30000 coast 100 800 > "$OUT/reader-pin6e9.log" 2>&1
echo "== reader-pin12e9: per-reader + far pin =="
env $KNOB ES_PIN_OLDEST=12000000000 ES_READER_OLDEST=1 "$BIN" 30000 coast 100 800 > "$OUT/reader-pin12e9.log" 2>&1
echo "== reader-nopin-70k: soundness at one star =="
env $KNOB ES_READER_OLDEST=1 "$BIN" 30000 coast 100 800 > "$OUT/reader-nopin.log" 2>&1
echo "== negative: reader + D=2^26 (below the natural gap) =="
env ES_WALL_CAP_S=30 ES_PROBE_EVERY_GS=2000 ES_PIN_OLDEST=67108864 ES_READER_OLDEST=1 "$BIN" 30000 coast 25 800 > "$OUT/reader-pin67M.log" 2>&1
echo "== ctrl-burn: SOI doll switch =="
env ES_WALL_CAP_S=35 ES_PROBE_EVERY_GS=1000 "$BIN" 30000 burn 25 100 > "$OUT/ctrl-burn.log" 2>&1
echo "== reader-burn+pin12e9: doll-edge crossings under the rule and the far pin =="
env ES_WALL_CAP_S=35 ES_PROBE_EVERY_GS=1000 ES_PIN_OLDEST=12000000000 ES_READER_OLDEST=1 "$BIN" 30000 burn 25 100 > "$OUT/reader-burn.log" 2>&1
echo "== reader 5 ms corner + pin12e9 =="
env ES_WALL_CAP_S=25 ES_PROBE_EVERY_GS=1000 ES_PIN_OLDEST=12000000000 ES_READER_OLDEST=1 "$BIN" 30000 coast 15 100 5 > "$OUT/reader-5ms.log" 2>&1
echo "== done =="
