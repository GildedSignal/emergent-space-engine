#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's patch.
# Applies work/patch.diff, builds, flies every table's flight, and runs the analyses.
# ~12 min: the two full ladder_digest passes dominate (~3 min each).
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."  # repo root

# 1. Apply the run's patch if the tree is clean of it.
if ! grep -q "ES_SECULAR" crates/universe/src/step.rs; then
  git apply "$RUN/work/patch.diff"
  grep -q "ES_SECULAR" crates/universe/src/step.rs || { echo "ERROR: patch did not apply"; exit 1; }
fi
echo "tree: $(git rev-parse HEAD) (patch applied)"

# 2. Build (nladder needs the patch for Linux; ladder_digest is the digest control).
cargo build --release -p emergent-universe --example nladder --example ladder_digest
B="${CARGO_TARGET_DIR:-target}/release/examples"
mkdir -p "$RUN/flights"

run () {  # run <label> <env...> -- <nladder args...>
  local label=$1; shift
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done; shift
  echo "=== $label: nladder $* ==="
  env ${envs[@]+"${envs[@]}"} "$B/nladder" "$@" > "$RUN/flights/$label.txt" 2>&1
  grep -hE "events/frame|game .* s after" "$RUN/flights/$label.txt" | sed 's/; scans.*//;s/, stats.*//'
}

# 3. The dossier's table: both horizons, the N-ladder, the floor, the RES control.
rm -f "$RUN/work/dump_long_off.csv" "$RUN/work/dump_long_arm.csv"
run n1000_1900_off  -- 1000 coast 20 100 1000000
ES_STATES="$RUN/work/states_1900_off.csv" "$B/nladder" 1000 coast 20 100 1000000 > "$RUN/flights/n1000_1900_off.txt" 2>&1
ES_SECULAR=1 ES_STATES="$RUN/work/states_1900_arm.csv" "$B/nladder" 1000 coast 20 100 1000000 > "$RUN/flights/n1000_1900_arm.txt" 2>&1
grep -hE "events/frame|game .* s after" "$RUN/flights/n1000_1900_arm.txt" | sed 's/; scans.*//;s/, stats.*//'
run n1000_1900_arm_res  ES_SECULAR=1 ES_SECULAR_RES=1 -- 1000 coast 20 100 1000000
run n0_1900_off         -- 0 coast 20 100 1000000
run n0_1900_arm         ES_SECULAR=1 -- 0 coast 20 100 1000000
run n10000_off          -- 10000 coast 20 100 1000000
run n10000_arm          ES_SECULAR=1 -- 10000 coast 20 100 1000000
ES_DUMP="$RUN/work/dump_long_off.csv" "$B/nladder" 1000 coast 55 100 1000000 > "$RUN/flights/n1000_5400_off.txt" 2>&1
ES_SECULAR=1 ES_DUMP="$RUN/work/dump_long_arm.csv" ES_STATES="$RUN/work/states_5400_arm.csv" \
  "$B/nladder" 1000 coast 55 100 1000000 > "$RUN/flights/n1000_5400_arm.txt" 2>&1
for f in n1000_5400_off n1000_5400_arm; do echo "== $f"; grep -hE "events/frame|game .* s after" "$RUN/flights/$f.txt" | sed 's/; scans.*//;s/, stats.*//'; done

echo "--- envelope (max events per 500-frame slice, 5,400 game-s) ---"
for arm in off arm; do
  echo -n "$arm: "; awk '{b=int($1/500); if($3>m[b])m[b]=$3} END{for(i=0;i<=b;i++)printf "%d ", m[i]; print ""}' "$RUN/work/dump_long_$arm.csv"
done
echo "--- the beat frame ---"
awk '$3>=100 {print "arm >=100:", $1, $3}' "$RUN/work/dump_long_arm.csv"
awk '$3>300 {print "off >300:", $1, $3}' "$RUN/work/dump_long_off.csv"

# 4. The digest control: patched OFF vs pristine main, 13 cases x 4 schedules.
if [ ! -x "$RUN/bin/ladder_digest_pristine" ]; then
  # (built from pristine main before the patch; rebuild by checking out the tree clean)
  echo "WARNING: pristine control binary missing; building from stash is manual" >&2
else
  "$B/ladder_digest" > "$RUN/flights/digest_off_patched.txt" 2>&1
  "$RUN/bin/ladder_digest_pristine" > "$RUN/flights/digest_off_pristine.txt" 2>&1
  if diff <(sed 's/ \[[0-9.]* s\]$//' "$RUN/flights/digest_off_patched.txt") \
          <(sed 's/ \[[0-9.]* s\]$//' "$RUN/flights/digest_off_pristine.txt") >/dev/null; then
    echo "DIGESTS IDENTICAL (all cases, wall times aside)"
  else
    echo "DIGESTS DIFFER"; diff "$RUN/flights/digest_off_patched.txt" "$RUN/flights/digest_off_pristine.txt" | head
  fi
fi

# 5. The analyses: legality cross-check + B14-class probe; corrected domain + wall ladder.
python3 "$RUN/work/analyze.py" | tee "$RUN/work/analyze.out"
python3 "$RUN/work/legality2.py" | tee "$RUN/work/legality2.out"
echo "DONE. Every dossier table is above."
