#!/bin/sh
# Regenerates every dossier number from the shipped tree + work/patch.diff (applied before this
# runs; run.sh saves the author's edits as that patch and restores the tree, so apply it here
# idempotently). Builds once (~1 min warm, ~4 min cold), then: 5 formation arms (seconds each),
# 2 formation controls, 1 four-fold-fleet probe, 4 belt arms (~20-55 s each), 1 flag-off belt
# control. Total ~5 min warm, ~12 min cold. Every number in dossier.md's evidence tables is in
# these outputs (kicknews: lines and form: lines).
set -e
RUN_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
ROOT=$RUN_DIR
while [ "$ROOT" != "/" ] && [ ! -f "$ROOT/Cargo.toml" ]; do ROOT=$(dirname "$ROOT"); done
[ -f "$ROOT/Cargo.toml" ] || { echo "no Cargo.toml above $RUN_DIR" >&2; exit 1; }
cd "$ROOT"
if ! grep -q "pub mod news" crates/universe/src/lib.rs; then
  git apply --check "$RUN_DIR/work/patch.diff"
  git apply "$RUN_DIR/work/patch.diff"
  echo "applied work/patch.diff"
fi
BIN="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples"
cargo build --release -p emergent-universe --example nladder --example form_news 2>&1 | tail -1
OUT="$RUN_DIR/work"
mkdir -p "$OUT"

# ---- the co-orbital formation (efd4's 99.6% case, rebuilt to survive), across the shipped
# Δs dial ES_STEP_LOG2 (7 = shipped; 5 = 4x coarser = the BELT_SPLIT=8 bulk effect; 9 = 4x finer)
for S in 5 6 7 8 9; do
  ES_KICK_NEWS=1 ES_STEP_LOG2=$S "$BIN/form_news" 512 500000 8000 > "$OUT/formS$S.txt" 2>&1
done
# scatter control (512 distinct orbits: the intern's null) and flag-off control
ES_KICK_NEWS=1 ES_SCATTER=1 "$BIN/form_news" 512 500000 8000 > "$OUT/formScatter.txt" 2>&1
"$BIN/form_news" 512 500000 8000 > "$OUT/formOff.txt" 2>&1
# the four-fold fleet probe (pigeonhole bound on the key spread)
ES_KICK_NEWS=1 "$BIN/form_news" 2048 500000 8000 > "$OUT/form2048.txt" 2>&1

# ---- the belt (9edc's own scene), same dial: S=7 reproduces its arm A; 5/6 coarser; 9 finer
for S in 5 6 7 9; do
  ES_KICK_NEWS=1 ES_STEP_LOG2=$S "$BIN/nladder" 10000 coast 150 1800 2>&1 | grep -E "ladder:|kicknews:" > "$OUT/beltS$S.txt"
done
# flag-off control on the belt scene
"$BIN/nladder" 10000 coast 20 100 2>&1 | grep -E "kicknews:" > "$OUT/beltOff.txt"

for f in formS5 formS6 formS7 formS8 formS9 formScatter formOff form2048 beltS5 beltS6 beltS7 beltS9 beltOff; do
  echo "--- $f"; grep -h "kicknews:\|form: scene\|form: scan@0.6\|form: end\|form: stats" "$OUT/$f.txt"
done
