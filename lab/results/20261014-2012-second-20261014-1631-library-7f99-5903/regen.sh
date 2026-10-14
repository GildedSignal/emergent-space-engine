#!/usr/bin/env bash
# Regen (run 20261014-2012-second-20261014-1631-library-7f99-5903): every dossier number, from the
# shipped tree + this folder's patches. ~13-14 min on 8 vCPU (three builds — one of them the 18d2
# worktree — seven flights, the universe suite). `work/patch.diff` (pre-applied by the runner) holds
# the final state; the steps below reconstruct both intermediate states from it.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
RUN=$ROOT/lab/results/20261014-2012-second-20261014-1631-library-7f99-5903
RAW=$RUN/raw
BIN=${CARGO_TARGET_DIR:-$ROOT/target}/release/examples/nladder

# 1. Baseline: a2c1's census probe + this run's digest cut (no deletion).
git checkout -- crates/universe/src/radial.rs crates/universe/src/encounter.rs crates/universe/examples/nladder.rs
git apply "$RUN/work/census-a2c1.diff"
python3 "$RUN/work/add_digest.py" crates/universe/examples/nladder.rs
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
for arm in "1000 coast" "10000 burn" "100000 coast"; do
  set -- $arm
  ES_SCAN_CENSUS=1 timeout 300 "$BIN" "$1" "$2" 20 > "$RAW/base-n$1-$2.txt" 2> "$RAW/base-n$1-$2.census" || true
done

# 2. The deletion (census + digest cut + the sensors deleted + the wall-cap probe).
git checkout -- crates/universe/src/radial.rs crates/universe/src/encounter.rs crates/universe/examples/nladder.rs
git apply "$RUN/work/patch.diff"
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
for arm in "1000 coast" "10000 burn"; do
  set -- $arm
  ES_SCAN_CENSUS=1 timeout 300 "$BIN" "$1" "$2" 20 > "$RAW/patched-n$1-$2.txt" 2> "$RAW/patched-n$1-$2.census" || true
done
# the 10^5 deletion arm: the widened registration makes the build ~2 min, so the example's own
# 55 s wall cap must be raised for the flight to run at all (that cost is itself a finding).
ES_SCAN_CENSUS=1 ES_WALL_CAP=400 timeout 500 "$BIN" 100000 coast 20 > "$RAW/patched-n100000-coast.txt" 2> "$RAW/patched-n100000-coast.census" || true
# the horizon guard control: h always beyond the horizon -> walk-all, digest must not move.
ES_SCAN_CENSUS=1 ES_SCAN_H=1 timeout 300 "$BIN" 1000 coast 20 > "$RAW/h0-n1000-coast.txt" 2> "$RAW/h0-n1000-coast.census" || true

# 3. The universe suite on the deletion build (P5).
cargo test --release -p emergent-universe 2>&1 | grep -E "test result" | tee "$RAW/suite.txt" || true

# 4. The chatter arm: 18d2's branch (the lead-graded single surface) + this run's probe.
#    `work/patch-18d2.diff` is a complete diff against the pristine branch: 18d2's own
#    work/patch.diff is already folded in, so it is applied once, to the fresh checkout.
W=/home/glmlab/w18d2
git worktree remove --force "$W" >/dev/null 2>&1 || true
git worktree prune
rm -rf "$W"
git worktree add --detach "$W" origin/claude/lab-20261006-1738-b-handoff-surface-18d2
(
  cd "$W"
  git apply "$RUN/work/patch-18d2.diff"
  export CARGO_TARGET_DIR=/home/glmlab/w18d2-target
  timeout 300 cargo test --release -p emergent-universe --test handoff the_surface_near_rc_retrograde_049 -- --nocapture 2>&1 | grep -E "^chatter" | tee "$RAW/chatter-baseline.txt"
  ES_HANDOFF_GATE=refusal timeout 300 cargo test --release -p emergent-universe --test handoff the_surface_near_rc_retrograde_049 -- --nocapture 2>&1 | grep -E "^chatter" | tee "$RAW/chatter-gate.txt"
)

# 5. The table.
python3 "$RUN/work/aggregate.py" "$RAW"
echo "regen done"
