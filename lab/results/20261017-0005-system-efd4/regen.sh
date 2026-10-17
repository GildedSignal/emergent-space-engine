#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# The patch adds only the test file crates/universe/tests/cache_duty.rs; no library code changes.
# run.sh restores the tree before regen, so apply the patch here (idempotently).
set -e
RUN_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# repo root = nearest ancestor holding Cargo.toml
ROOT=$RUN_DIR
while [ "$ROOT" != "/" ] && [ ! -f "$ROOT/Cargo.toml" ]; do ROOT=$(dirname -- "$ROOT"); done
[ -f "$ROOT/Cargo.toml" ] || { echo "no Cargo.toml above $RUN_DIR" >&2; exit 1; }
cd "$ROOT"
if [ ! -f crates/universe/tests/cache_duty.rs ]; then
  git apply --check "$RUN_DIR/work/patch.diff"
  git apply "$RUN_DIR/work/patch.diff"
  echo "applied work/patch.diff"
fi
cargo test --release -p emergent-universe --test cache_duty -- --nocapture --test-threads=1
echo "---"
echo "grep control (callers of the plane catalogue's get, expect none outside bind.rs):"
grep -rn "\.cat\.get\|cat\.get(" crates/universe/src crates/universe/tests || echo "none"
