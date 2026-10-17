#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's patch (work/patch.diff,
# = 1a46's ES_SECULAR patch + this run's instruments: ES_TRACE, ES_WALLCAP, ES_THREADS, ES_REKICK).
#
# Default ~10 min: build, the record calibration flights (5,400/11,000 gs, both arms),
# the decisive OFF/ES_SECULAR pair with the angle trace to 1.5e6 game-s (the verdict is decided
# inside that range: the measured debt is ~1 deg at 5e5 gs against 19 deg power-law and 0.11 deg
# linear predictions), the re-kick bench, and the analysis.
# REGEN_FULL=1 flies the flown 8e6-gs target instead (~26 min wall; the shipped artifacts
# work/trace_{off,arm}.txt reached 6.4e6/8e6 gs under ES_WALLCAP=1560).
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."

if ! grep -q "ES_SECULAR" crates/universe/src/step.rs; then
  git apply "$RUN/work/patch.diff"
  grep -q "ES_SECULAR" crates/universe/src/step.rs || { echo "ERROR: patch did not apply"; exit 1; }
fi
echo "tree: $(git rev-parse HEAD) + work/patch.diff"
cargo build --release -p emergent-universe --example nladder --example ladder_digest
B="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
mkdir -p "$RUN/flights"

# 1. Calibration: reproduce the published record at both horizons; the 11,000-gs arm's end
#    states give the traced set (477 deleted: 274 belt, 200 in-situ, 3 doll-3) and the record's
#    own end-state probe. Thread-4 determinism control on the 5,400 arm.
ES_WALLCAP=300 ES_STATES="$RUN/work/states_5400_off.csv"  "$B" 1000 coast 55  100 1000000 > "$RUN/flights/n1000_5400_off.txt"  2>&1
ES_WALLCAP=300 ES_SECULAR=1 ES_STATES="$RUN/work/states_5400_arm.csv" "$B" 1000 coast 55  100 1000000 > "$RUN/flights/n1000_5400_arm.txt" 2>&1
ES_WALLCAP=300 ES_THREADS=4 ES_SECULAR=1 ES_STATES="$RUN/work/states_5400_arm_t4.csv" "$B" 1000 coast 55 100 1000000 > "$RUN/flights/t4check.txt" 2>&1
ES_WALLCAP=300 ES_STATES="$RUN/work/states_11000_off.csv" "$B" 1000 coast 110 100 1000000 > "$RUN/flights/n1000_11000_off.txt" 2>&1
ES_WALLCAP=300 ES_SECULAR=1 ES_STATES="$RUN/work/states_11000_arm.csv" "$B" 1000 coast 110 100 1000000 > "$RUN/flights/n1000_11000_arm.txt" 2>&1
for f in n1000_5400_off n1000_5400_arm n1000_11000_off n1000_11000_arm; do
  echo "== $f"; grep -hE "events/frame|game .* s after" "$RUN/flights/$f.txt" | sed 's/; scans.*//;s/, stats.*//;s/; refus.*//'
done
diff <(grep -v '^#' "$RUN/work/states_5400_arm_t4.csv") <(grep -v '^#' "$RUN/work/states_5400_arm.csv") >/dev/null \
  && echo "T4 STATES IDENTICAL (threads deterministic)" || echo "T4 STATES DIFFER"
python3 - "$RUN" <<'EOF'
import sys
R = sys.argv[1]
ids = []
for ln in open(f"{R}/work/states_11000_arm.csv"):
    p = ln.split()
    if p[0] == 'B' and p[3] == 's' and p[4] == '0' and p[5] == '1':
        ids.append(p[1])
open(f"{R}/work/ids.txt", 'w').write('\n'.join(ids) + '\n')
print(f"traced set: {len(ids)} deleted bodies")
EOF

# 2. The decisive pair: OFF and ES_SECULAR, angle trace of the deleted set at matched
#    log-spaced horizons. REGEN_FULL=1 -> the flown 8e6 target and wall cap.
END="${REGEN_FULL:-1500000}"; CAP="${REGEN_WALLCAP:-600}"
ES_WALLCAP=$CAP ES_STATES="$RUN/work/long_regen_off_states.csv" ES_TRACE="5400:$END:97" \
  ES_IDS="$RUN/work/ids.txt" ES_TRACE_PATH="$RUN/work/trace_regen_off.txt" \
  "$B" 1000 coast 1600 5000 1000000 > "$RUN/flights/long_regen_off.txt" 2>&1 &
OFF=$!
ES_WALLCAP=$CAP ES_SECULAR=1 ES_STATES="$RUN/work/long_regen_arm_states.csv" ES_TRACE="5400:$END:97" \
  ES_IDS="$RUN/work/ids.txt" ES_TRACE_PATH="$RUN/work/trace_regen_arm.txt" \
  "$B" 1000 coast 1600 5000 1000000 > "$RUN/flights/long_regen_arm.txt" 2>&1 &
ARM=$!
wait $OFF $ARM
for f in long_regen_off long_regen_arm; do echo "== $f"; grep -hE "game .* s after" "$RUN/flights/$f.txt" | sed 's/; scans.*//;s/, stats.*//' | cut -c1-160; done
# 3. The re-kick cost bench (attack 4): one sweep every 5,000 gs over 595,000 gs.
ES_WALLCAP=240 ES_SECULAR=1 ES_REKICK=5000 "$B" 1000 coast 120 5000 1000000 > "$RUN/flights/bench.txt" 2>&1
grep -E "es_bench" "$RUN/flights/bench.txt"

# 4. The analysis: the debt curve, the law fits, the fence quanta, k*, the record probe,
#    the spared-set check.
TRACE_OFF="$RUN/work/trace_regen_off.txt" TRACE_ARM="$RUN/work/trace_regen_arm.txt" \
LONG_OFF="$RUN/work/long_regen_off_states.csv" LONG_ARM="$RUN/work/long_regen_arm_states.csv" \
FLIGHT_OFF="$RUN/flights/long_regen_off.txt" FLIGHT_ARM="$RUN/flights/long_regen_arm.txt" \
python3 "$RUN/work/analyze.py" | tee "$RUN/work/analyze_regen.out"
echo "DONE. (Flown full-length artifacts: work/trace_{off,arm}.txt, work/analyze.out — both arms to"
echo " the 8e6-gs target with matched end ticks. Default regen stops OFF at the 600-s cap, so its"
echo " spared-set check self-skips (arms at different ticks); REGEN_FULL=1 REGEN_WALLCAP=1560"
echo " reproduces the full matched-end run, ~26 min.)"
