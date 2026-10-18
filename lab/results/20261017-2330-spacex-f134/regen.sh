#!/usr/bin/env bash
# Regen: every number in dossier.md from pristine main + work/patch.diff.
# ~10 min: two ladder_digest passes (~3 min each) dominate; flights are ~2 s each (budget-free,
# unpaced — the nladder example runs its frames as fast as the CPU allows).
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."  # repo root

# 1. Apply the composed patch if the tree is clean of it.
if ! grep -q "ES_SECULAR" crates/universe/src/step.rs || ! grep -q "ES_CHAIN" crates/universe/src/step.rs; then
  git apply "$RUN/work/patch.diff"
  grep -q "ES_SECULAR" crates/universe/src/step.rs && grep -q "ES_CHAIN" crates/universe/src/step.rs \
    || { echo "ERROR: patch did not apply"; exit 1; }
fi
echo "tree: $(git rev-parse HEAD) (composed patch applied)"

# 2. Build.
cargo build --release -p emergent-universe --example nladder --example ladder_digest
B="${CARGO_TARGET_DIR:-target}/release/examples"
mkdir -p "$RUN/flights" "$RUN/work"

run () {  # run <label> <n> <seconds> <flight> <env...>
  local label=$1 n=$2 secs=$3 flight=$4; shift 4
  rm -f "$RUN/work/dump_$label.csv"
  echo "=== $label: nladder $n $flight $secs 100 (budget-free)"
  env "$@" ES_DUMP="$RUN/work/dump_$label.csv" "$B/nladder" "$n" "$flight" "$secs" 100 1000000 \
    > "$RUN/flights/$label.txt" 2>&1
  grep -hE "frames after|game .* s after" "$RUN/flights/$label.txt" | sed 's/; scans.*//;s/, stats.*//'
}

# 3. The four arms at N=1000 coast, 5,400 game-s (the dossier's main table).
run n1000_5400_off        1000 55 coast
run n1000_5400_secular    1000 55 coast ES_SECULAR=1
run n1000_5400_chainstag  1000 55 coast ES_CHAIN=1 ES_LOCAL_STAGGER=1
run n1000_5400_both       1000 55 coast ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1

# 4. Held-out: N-flat (N=0/600/10^4) and the 2x horizon (10,900 game-s), all under BOTH.
run both_n0      0    55 coast  ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1
run both_n600    600  55 coast  ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1
run both_n10000  10000 55 coast ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1
run both_10900   1000 110 coast ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1
run off_10900    1000 110 coast
run secular_10900 1000 110 coast ES_SECULAR=1

# 5. Held-out: the burn arm at 1,900 game-s (all four arms).
run burn_off       1000 20 burn
run burn_chainstag 1000 20 burn ES_CHAIN=1 ES_LOCAL_STAGGER=1
run burn_secular   1000 20 burn ES_SECULAR=1
run burn_both      1000 20 burn ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1

echo "--- envelope (max events per 500-frame slice, 5,400 game-s) ---"
for a in off secular chainstag both; do
  f="$RUN/work/dump_n1000_5400_$a.csv"
  echo -n "$a: "; awk '{b=int($1/500); if($3>m[b])m[b]=$3} END{for(i=0;i<=b;i++)printf "%d ", m[i]; print ""}' "$f"
done
echo "--- beats >= 40 events (frame:events) ---"
for a in off secular chainstag both; do
  echo -n "$a: "; awk '$3>=40{printf "%d:%d ", $1,$3}' "$RUN/work/dump_n1000_5400_$a.csv"; echo
done

# 6. Controls: patched-OFF digests vs the frozen record; the composed law's schedule-determinism.
"$B/ladder_digest" > "$RUN/flights/digest_off_patched.txt" 2>&1
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 "$B/ladder_digest" > "$RUN/flights/digest_both.txt" 2>&1
norm(){ grep -E '^N=' "$1" | sed 's/ *\[[0-9.]* s\] *//;s/  */ /g;s/ $//' | sort; }
if diff <(norm "$RUN/flights/digest_off_patched.txt") <(norm artifacts/runs/nladder/ladder_digests_wave.txt); then
  echo "OFF == FROZEN RECORD: all 13 cases identical (digest, kicks, encounters, contacts)"
else
  echo "WARNING: OFF digest differs from the frozen record"; exit 1
fi
echo "composed-arm schedule agreement: $(grep -c 'schedules agree' "$RUN/flights/digest_both.txt")/13 cases"
