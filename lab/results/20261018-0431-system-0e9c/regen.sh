#!/bin/sh
# Regenenerates every number in dossier.md from shipped code + work/patch.diff.
# Total wall: ~9 min (build ~30 s; census arms ~15 s; two full digest runs ~4 min each).
set -e
cd "$(dirname "$0")"/../../..   # the repo root
R=lab/results/20261018-0431-system-0e9c/work/out
mkdir -p "$R"

# The patch: apply it if the tree is restored (pristine); skip if already applied.
if git apply --check lab/results/20261018-0431-system-0e9c/work/patch.diff 2>/dev/null; then
  git apply lab/results/20261018-0431-system-0e9c/work/patch.diff
  echo "patch applied"
else
  echo "patch already present"
fi
cargo build --release -p emergent-universe --example nladder --example ladder_digest 2>&1 | tail -1
B=/home/glmlab/lab-target-1/release/examples

# Census arms (print-only; off-arm is the pristine scan path, on-arm adds ES_LOCAL_BAIL).
for arm in off on; do
  extra=""; [ "$arm" = on ] && extra="ES_LOCAL_BAIL=1"
  env SCAN_CENSUS=1 $extra $B/nladder 0     coast 40 100 > "$R/n0_coast_$arm.log"   2>&1
  env SCAN_CENSUS=1 $extra $B/nladder 10000 coast 40 100 > "$R/n10k_coast_$arm.log" 2>&1
  env SCAN_CENSUS=1 $extra $B/nladder 1000  burn  20 100 > "$R/n1k_burn_$arm.log"   2>&1
done

# The frozen digest record, both arms, census off (the counters print wall ms and would differ).
$B/ladder_digest > "$R/digest_full_off.log" 2>&1
ES_LOCAL_BAIL=1 $B/ladder_digest > "$R/digest_full_on.log" 2>&1

# Digest proof: identical after stripping the per-case wall times.
sed 's/ *\[[0-9.]* s\]$//' "$R/digest_full_off.log" > "$R/digest_full_off.stripped"
sed 's/ *\[[0-9.]* s\]$//' "$R/digest_full_on.log"  > "$R/digest_full_on.stripped"
if diff -q "$R/digest_full_off.stripped" "$R/digest_full_on.stripped" >/dev/null; then
  echo "DIGESTS: the frozen 13-case record is bit-identical under ES_LOCAL_BAIL ($(grep -c 'schedules agree' "$R/digest_full_off.log") cases)"
else
  echo "DIGESTS: DIFFER — the fix moved an outcome"; diff "$R/digest_full_off.stripped" "$R/digest_full_on.stripped" | head; exit 1
fi

# The census headlines (last cumulative line of each arm).
echo; echo "=== census (last cumulative line per arm) ==="
for f in n0_coast_off n0_coast_on n10k_coast_off n10k_coast_on n1k_burn_off n1k_burn_on; do
  echo "$f: $(grep scan_census "$R/$f.log" | tail -1)"
done
echo; echo "=== digest arms (first/last case + verdict lines) ==="
grep -E "belt crossing|every case" "$R/digest_full_off.log" | tail -4
