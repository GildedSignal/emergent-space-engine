#!/bin/sh
# Regenerates every dossier number from the pristine tree + work/patch.diff.
# ~6 min on this 8-vCPU box (build ~1 min, seven flights ~4 min, settle included).
set -e
cd "$(dirname "$0")/../../.."   # repo root
P=lab/results/20261017-1535-quant-35f6/work/patch.diff
# The patch's preimages are the run's base commit (== HEAD). A regen may start on a tree
# that still carries this run's edits — the first attempt died exactly there: `git apply`
# found the postimage, not the preimage, and --reject half-applied it. So: apply atomically,
# and if that fails, restore the five files the patch touches to base, drop reject litter,
# and apply once more.
git apply "$P" 2>/dev/null || {
    git checkout -- crates/universe/examples/nladder.rs crates/universe/src/ctx.rs \
        crates/universe/src/observe.rs crates/universe/src/prof.rs crates/universe/src/universe.rs
    rm -f crates/universe/examples/*.rej crates/universe/src/*.rej
    git apply "$P"
}
cargo build --release -p emergent-universe --example nladder --features prof
E=./target/release/examples/nladder
[ -x "$E" ] || E=/home/glmlab/lab-target-1/release/examples/nladder
R=lab/results/20261017-1535-quant-35f6/work
mkdir -p "$R"
# census (pure observation, recomputes every value): the two conflicts sides' arms
ES_SEC_CENSUS=1 $E 10000 coast 60 600 > "$R/census_1e4_600.txt" 2>&1
ES_SEC_CENSUS=1 $E 30000 coast 60 600 > "$R/census_3e4_600.txt" 2>&1
# A/B at three arms (digest at the common absolute tick, printed as `digest:`)
for arm in "10000 600 40000" "30000 600 40000" "10000 100 40000"; do
  set -- $arm
  ES_DIGEST_GS=$3 $E $1 coast 60 $2 > "$R/off_$1_$2.txt" 2>&1
  ES_SEC_MEMO=1 ES_DIGEST_GS=$3 $E $1 coast 60 $2 > "$R/on_$1_$2.txt" 2>&1
done
echo "== census (repeat, conflicts)"
grep -h sec_memo "$R"/census_*.txt
echo "== digests (off vs on, per arm)"
for a in 10000_600 30000_600 10000_100; do
  printf '%s off=%s on=%s\n' "$a" "$(grep -o '^digest: [0-9a-f]*' "$R/off_$a.txt" | cut -d' ' -f2)" "$(grep -o '^digest: [0-9a-f]*' "$R/on_$a.txt" | cut -d' ' -f2)"
done
echo "== stages off vs on (SEC, state_of, kicks, fit) and engine ms"
for a in 10000_600 30000_600 10000_100; do
  echo "-- $a OFF"; grep -E "engine ms|read stream|item: kick \(Wisdom|item: kick \(clock\)|fit: bind_surface" "$R/off_$a.txt"
  echo "-- $a ON";  grep -E "engine ms|read stream|item: kick \(Wisdom|item: kick \(clock\)|fit: bind_surface|sec_memo" "$R/on_$a.txt"
done
