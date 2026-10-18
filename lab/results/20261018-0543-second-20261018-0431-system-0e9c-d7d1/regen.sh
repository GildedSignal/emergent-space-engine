#!/bin/sh
# Regenenerates every number in dossier.md from shipped code + work/patch.diff.
# Total wall: ~14 min (build ~45 s; three full 13-case digest runs ~10 min; two seam-census
# belt runs ~3 min; probes ~20 s; formation flights ~15 s). The off-arm is the pristine path.
set -e
cd "$(dirname "$0")"/../../..   # the repo root
R=lab/results/20261018-0543-second-20261018-0431-system-0e9c-d7d1/work/out
mkdir -p "$R"

# The patch: apply it if the tree is restored (pristine); skip if already applied.
if git apply --check lab/results/20261018-0543-second-20261018-0431-system-0e9c-d7d1/work/patch.diff 2>/dev/null; then
  git apply lab/results/20261018-0543-second-20261018-0431-system-0e9c-d7d1/work/patch.diff
  echo "patch applied"
else
  echo "patch already present"
fi
cargo build --release -p emergent-universe --example ladder_digest --example belt_scan_probe --example formprobe 2>&1 | tail -1
B=/home/glmlab/lab-target-1/release/examples

# ---- P1: the frozen 13-case digest record, three arms (off / LT / LT+BAIL) ----
$B/ladder_digest > "$R/digest_off.log" 2>&1
ES_LOCAL_THRESHOLD=1 $B/ladder_digest > "$R/digest_lt.log" 2>&1
ES_LOCAL_THRESHOLD=1 ES_LOCAL_BAIL=1 $B/ladder_digest > "$R/digest_comp.log" 2>&1
for a in off lt comp; do sed 's/ *\[[0-9.]* s\]$//' "$R/digest_$a.log" > "$R/digest_$a.stripped"; done
if diff -q "$R/digest_off.stripped" "$R/digest_lt.stripped" >/dev/null && diff -q "$R/digest_off.stripped" "$R/digest_comp.stripped" >/dev/null; then
  echo "DIGESTS: the frozen 13-case record is bit-identical in all three arms ($(grep -c 'schedules agree' "$R/digest_off.log") cases)"
else
  echo "DIGESTS: DIFFER — a threshold or bail arm moved an outcome"; diff "$R/digest_off.stripped" "$R/digest_lt.stripped" | head; diff "$R/digest_off.stripped" "$R/digest_comp.stripped" | head; exit 1
fi
# The off-arm vs the shipped frozen record: every shared case (11) identical to the digit (names+hash+stats,
# order-insensitive; the run set adds the two wave cases the record lacks).
norm() { grep -E "^N=" "$1" | sed 's/ *\[[0-9.]* s\]$//' | sed 's/  */ /g;s/ $//' | sort; }
norm "$R/digest_off.log" > "$R/off.norm"; norm artifacts/runs/nladder/ladder_digests_newpop.txt > "$R/rec.norm"
if [ "$(comm -23 "$R/off.norm" "$R/rec.norm" | grep -cv 'through the wave')" = 0 ] && [ -z "$(comm -13 "$R/off.norm" "$R/rec.norm")" ]; then
  echo "FROZEN RECORD: all 11 shared cases identical (the run set adds the two wave cases the record lacks)"
else
  echo "FROZEN RECORD: a shared case moved"; exit 1
fi

# ---- P4: the seam census (the command behind the seam numbers), off vs composed ----
for arm in off comp; do
  extra=""; [ "$arm" = comp ] && extra="ES_LOCAL_THRESHOLD=1 ES_LOCAL_BAIL=1"
  env SCAN_CENSUS=1 $extra $B/ladder_digest belt > "$R/beltcensus_$arm.log" 2>&1
  echo "seam $arm: $(grep scan_census "$R/beltcensus_$arm.log" | tail -1)"
done
grep -E "^N=" "$R/beltcensus_off.log" | sed 's/ *\[[0-9.]* s\]$//' | sort > "$R/belt_off.norm"
grep -E "^N=" "$R/beltcensus_comp.log" | sed 's/ *\[[0-9.]* s\]$//' | sort > "$R/belt_comp.norm"
if diff -q "$R/belt_off.norm" "$R/belt_comp.norm" >/dev/null; then
  echo "seam digests: identical in both census arms"
else
  echo "seam digests DIFFER"; exit 1
fi

# ---- P2/P5: 3999's in-band probe at 1e5, three arms (the regime where bails fire at scale) ----
$B/belt_scan_probe 100000 1 > "$R/probe100k_off.log" 2>&1
ES_LOCAL_THRESHOLD=1 $B/belt_scan_probe 100000 1 > "$R/probe100k_lt.log" 2>&1
ES_LOCAL_THRESHOLD=1 ES_LOCAL_BAIL=1 $B/belt_scan_probe 100000 1 > "$R/probe100k_comp.log" 2>&1
for a in off lt comp; do echo "probe $a: $(grep -E '^window.belt_standin|^window.player_home' "$R/probe100k_$a.log" | tr '\n' ' ')"; done
for a in lt comp; do
  if [ "$(grep '^window.belt_standin' "$R/probe100k_$a.log" | grep -oE 'pass=[0-9]+')" = "$(grep '^window.belt_standin' "$R/probe100k_off.log" | grep -oE 'pass=[0-9]+')" ]; then
    echo "probe exactness: belt pass identical ($a)"
  else
    echo "probe exactness: FAIL ($a)"; exit 1
  fi
done

# ---- P3: the formation pair (604c's scene: 200 fleet ships in the player's doll, 1e4 belt in the root doll) ----
for arm in off lt comp; do
  extra=""; [ "$arm" = lt ] && extra="ES_LOCAL_THRESHOLD=1"; [ "$arm" = comp ] && extra="ES_LOCAL_THRESHOLD=1 ES_LOCAL_BAIL=1"
  env SCAN_CENSUS=1 $extra $B/formprobe 200 10000 20 100 > "$R/form200_$arm.log" 2>&1
  echo "form $arm: $(grep '^probe:' "$R/form200_$arm.log")"
  echo "form $arm census: $(grep scan_census "$R/form200_$arm.log" | tail -1)"
done
d=$(grep '^probe:' "$R/form200_off.log" | grep -oE "digest=[0-9a-f]+" | cut -d= -f2)
for a in lt comp; do [ "$(grep '^probe:' "$R/form200_$a.log" | grep -oE "digest=[0-9a-f]+" | cut -d= -f2)" = "$d" ] || { echo "formation digest DIFFERS ($a)"; exit 1; }; done
echo "formation digests: identical in all three arms ($d)"

echo; echo "=== regen complete ==="
