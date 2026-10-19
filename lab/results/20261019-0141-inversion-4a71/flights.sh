#!/bin/sh
# 4a71 decisive flights, sequential (deterministic counts before timing quality). Each prints
# probe lines every 2000 game-s + the ladder summary.
set -e
cd "$(dirname "$0")/../../.."   # repo root
BIN=/home/glmlab/lab-target-2/release/examples/nladder
OUT=lab/results/20261019-0141-inversion-4a71/logs
mkdir -p "$OUT"

echo "== ctrl-70k: coast, rtf 800, 100 s wall, cap 130 =="
ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000 "$BIN" 30000 coast 100 800 > "$OUT/ctrl-70k.log" 2>&1
echo "== pin6e9: ES_PIN_OLDEST=6000000000, same =="
ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000 ES_PIN_OLDEST=6000000000 "$BIN" 30000 coast 100 800 > "$OUT/pin6e9.log" 2>&1
echo "== pin12e9: ES_PIN_OLDEST=12000000000, same =="
ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000 ES_PIN_OLDEST=12000000000 "$BIN" 30000 coast 100 800 > "$OUT/pin12e9.log" 2>&1
echo "== ctrl-5ms: coast, 5 ms budget, rtf 100, 15 s =="
ES_WALL_CAP_S=25 ES_PROBE_EVERY_GS=1000 "$BIN" 30000 coast 15 100 5 > "$OUT/ctrl-5ms.log" 2>&1
echo "== ctrl-burn: burn, rtf 100, 25 s (SOI doll switch ~frame 948) =="
ES_WALL_CAP_S=35 ES_PROBE_EVERY_GS=1000 "$BIN" 30000 burn 25 100 > "$OUT/ctrl-burn.log" 2>&1
echo "== done =="
