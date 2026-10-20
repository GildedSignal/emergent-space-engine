#!/bin/sh
# Regen for 20261019-2339-inversion-1d47. Applies work/patch.diff (the gate at
# universe.rs:770 + the scan-staleness probe + the example's Linux /proc footprint shim,
# all env-gated: unset = shipped bit for bit), builds, and reruns every arm of the dossier.
# ~10 min on the 8 vCPU lab box. Machine state is printed before each flight as the record does.
cd "$(dirname "$0")/../../.." || exit 1
OUT="lab/results/20261019-2339-inversion-1d47/work/regen"
mkdir -p "$OUT"

# 1. The patch (skip when the tree already carries it: the runner applies it before regen).
if git diff --quiet 2>/dev/null; then
  git apply lab/results/20261019-2339-inversion-1d47/work/patch.diff || echo "patch already applied (continuing)"
fi

# 2. Build, then find the examples where cargo put them.
cargo build --release -p emergent-universe --example nladder --example ladder_digest || exit 1
BIN=$(ls -d target/release/examples "$CARGO_TARGET_DIR"/release/examples /home/glmlab/lab-target-2/release/examples 2>/dev/null | head -1)
[ -x "$BIN/nladder" ] || { echo "no examples under $BIN"; exit 1; }

# 3. The law instrument: ladder_digest, off (shipped) and on (the gate).
state() { uptime; free -m | head -2; }
for arm in off on; do
  { state; if [ $arm = on ]; then ES_ROOT_SHIPS_TO_QUEUE=1 "$BIN/ladder_digest"; else "$BIN/ladder_digest"; fi; } \
    > "$OUT/ldigest_${arm}.txt" 2>&1
done
echo "== digests: off vs on ==" > "$OUT/summary.txt"
grep -E '^(N=|every)' "$OUT/ldigest_off.txt" | sed 's/ *\[.*\]$//' > "$OUT/off_dig.txt"
grep -E '^(N=|every)' "$OUT/ldigest_on.txt" | sed 's/ *\[.*\]$//' > "$OUT/on_dig.txt"
if diff "$OUT/off_dig.txt" "$OUT/on_dig.txt" > "$OUT/digest_diff.txt"; then
  echo "ALL 14 DIGEST LINES IDENTICAL (off == on)" >> "$OUT/summary.txt"
else
  echo "DIGESTS DIFFER:" >> "$OUT/summary.txt"; cat "$OUT/digest_diff.txt" >> "$OUT/summary.txt"
fi

# 4. The flights: the ladder's burn arms, off/on, both rungs (2x10^5 is the held-out rung).
for n in 100000 200000; do
  for arm in off on; do
    secs=18; [ $n = 200000 ] && secs=16
    { state
      if [ $arm = on ]; then ES_ROOT_SHIPS_TO_QUEUE=1 ES_FIX_PROBE=1 "$BIN/nladder" $n burn $secs 1000
      else ES_FIX_PROBE=1 "$BIN/nladder" $n burn $secs 1000; fi
    } > "$OUT/n${n}_${arm}.txt" 2>&1
  done
done
echo "" >> "$OUT/summary.txt"
echo "== the four headline arms (ladder: lines) ==" >> "$OUT/summary.txt"
grep -h "^ladder:\|^fixprobe:" "$OUT"/n*_*.txt >> "$OUT/summary.txt"
cat "$OUT/summary.txt"
