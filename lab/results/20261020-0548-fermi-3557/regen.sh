#!/usr/bin/env bash
# Regenerate every dossier number from shipped code + work/patch.diff. ~1.5 min on this box.
set -e
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/regen.sh)
RUN=lab/results/20261020-0548-fermi-3557
BIN="${CARGO_TARGET_DIR:-target}/release/examples"

# Apply the patch exactly once, whatever state we start from: lab/run.sh's regen() applies
# work/patch.diff BEFORE this script runs, so applying it again would fail (that was the
# 06:09 regen failure). Force the canonical state instead: tracked files back to shipped,
# the patch's new (untracked) example removed, then apply.
git checkout -q -- crates/universe
rm -f crates/universe/examples/scoped_alloc.rs
git apply --allow-empty "$RUN/work/patch.diff"
cargo build --release -p emergent-universe --example scoped_alloc --example nladder

# Neutrality control: the shipped counters are identical without ITEM_SCOPE.
git checkout -- crates/universe/src/universe.rs
cargo build --release -p emergent-universe --example nladder
"$BIN/nladder" 10000 coast 10 100 12 | grep -E "^game " > /tmp/A_unpatched.txt
git apply --include=crates/universe/src/universe.rs "$RUN/work/patch.diff"
cargo build --release -p emergent-universe --example nladder
"$BIN/nladder" 10000 coast 10 100 12 | grep -E "^game " > /tmp/B_patched.txt
diff /tmp/A_unpatched.txt /tmp/B_patched.txt && echo IDENTICAL_CANONICAL
cp /tmp/A_unpatched.txt /tmp/B_patched.txt "$RUN/work/logs/"

# The five decisive arms (~35 s wall total on a quiet box).
: > "$RUN/work/logs/decisive2.log"
for arm in "10000 coast 240" "10000 burn 240" "30000 coast 240" "30000 burn 240" "10000 coast 480"; do
  set -- $arm
  echo "=== $1 $2 $3 ===" >> "$RUN/work/logs/decisive2.log"
  timeout 170 "$BIN/scoped_alloc" $1 $2 $3 100 12 2>&1 | grep -v "^hist" >> "$RUN/work/logs/decisive2.log"
done

# The composition (ledger rows from the logs' constants).
python3 "$RUN/work/compose.py" | tee "$RUN/work/logs/compose.out"
