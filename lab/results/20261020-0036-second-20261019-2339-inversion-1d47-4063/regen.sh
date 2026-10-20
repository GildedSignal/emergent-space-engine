#!/bin/sh
# Regen for 20261020-0036-second-20261019-2339-inversion-1d47-4063 (second author on 1d47).
# Applies work/patch.diff (the author's gate + probe, plus this run's additions: the reach-gated
# pull ES_ROOT_SHIPS_REACH, the stale-encounter half of the probe, and examples/cut_digest.rs —
# all env-gated: unset = shipped bit for bit), builds, and reruns every arm of the dossier:
# the canonical-cut digests at 10^5 and 2x10^5 (OFF/ON/REACH x schedules + reruns) and the burst
# flights. ~13 min on the 8 vCPU lab box, sequential (each process < 2 GB).
cd "$(dirname "$0")/../../.." || exit 1
RUN=lab/results/20261020-0036-second-20261019-2339-inversion-1d47-4063
OUT="$RUN/work/regen"
mkdir -p "$OUT"

if git diff --quiet 2>/dev/null; then
  git apply "$RUN/work/patch.diff" || echo "patch already applied (continuing)"
fi

cargo build --release -p emergent-universe --example cut_digest --example nladder || exit 1
B=$(ls -d "$CARGO_TARGET_DIR"/release/examples target/release/examples 2>/dev/null | head -1)
[ -x "$B/cut_digest" ] || { echo "no examples under $B"; exit 1; }

state() { uptime; free -m | head -2; }

# 1. The canonical cut at both rungs: OFF (shipped) on four schedules, ON (1d47's gate) and
#    REACH=16 on 12 ms x3 plus unl/3/noflight. Probe on everywhere for the stale/stale_enc counts.
for n in 100000 200000; do
  f=$OUT/cut${n}.txt
  : > "$f"
  for s in unl 12 3 noflight; do { state; ES_FIX_PROBE=1 "$B/cut_digest" $n 17000 $s 1; } >> "$f" 2>&1; done
  for i in 1 2 3; do { state; ES_ROOT_SHIPS_TO_QUEUE=1 ES_FIX_PROBE=1 "$B/cut_digest" $n 17000 12 1; } >> "$f" 2>&1; done
  for i in 1 2 3; do { state; ES_ROOT_SHIPS_REACH=16 ES_FIX_PROBE=1 "$B/cut_digest" $n 17000 12 1; } >> "$f" 2>&1; done
  for s in unl 3 noflight; do { state; ES_ROOT_SHIPS_REACH=16 ES_FIX_PROBE=1 "$B/cut_digest" $n 17000 $s 1; } >> "$f" 2>&1; done
  # The checker's extra axes: 4 threads, and the deeper cut at 18,000 game-s (ON only).
  { state; ES_ROOT_SHIPS_TO_QUEUE=1 ES_FIX_PROBE=1 "$B/cut_digest" $n 18000 12 1; } >> "$f" 2>&1
  { state; ES_FIX_PROBE=1 "$B/cut_digest" $n 18000 12 4; } >> "$f" 2>&1
done

# 2. The burst flights: the ladder's burn arms, OFF and REACH at both rungs.
for n in 100000 200000; do
  secs=18; [ $n = 200000 ] && secs=16
  { state; ES_FIX_PROBE=1 "$B/nladder" $n burn $secs 1000; } > "$OUT/n${n}_off.txt" 2>&1
  { state; ES_ROOT_SHIPS_REACH=16 ES_FIX_PROBE=1 "$B/nladder" $n burn $secs 1000; } > "$OUT/n${n}_reach.txt" 2>&1
done

# 3. The summary: one digest per arm?
{
  echo "== the canonical cut: digest kicks encounters per run =="
  for n in 100000 200000; do
    echo "-- N=$n"
    sed 's/^cut: //' "$OUT/cut${n}.txt" | grep -o 'sched=[a-z0-9]* threads=[0-9] frames=[0-9]* digest [0-9a-f]\{16\} kicks [0-9]* encounters [0-9]* contacts [0-9]* | probe: .*ticks)' \
      | sed 's/ | probe: scans \([0-9]*\) cands \([0-9]*\) stale \([0-9]*\) (max \([0-9]*\)).*/ | scans \1 cands \2 stale \3 (max \4)/'
  done
  echo "== the burst (ladder: lines) =="
  grep -h '^ladder:\|^fixprobe:' "$OUT"/n*_off.txt "$OUT"/n*_reach.txt
} > "$OUT/summary.txt"
cat "$OUT/summary.txt"
