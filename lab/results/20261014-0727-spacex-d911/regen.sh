#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Patch: adds the `kick2` experiment (cascade anatomy) to crates/encounters/src/main.rs.
# Total wall: ~20 s (build ~7 s, runs ~9 s). Linux/x86 shared cloud — orders of magnitude only.
set -e
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN/../../.." && pwd)"
cd "$ROOT"
# The first regen run died here: the runner called this script while the tree still carried
# the author's edits (run.sh saves them as this patch, then restores), so the forward apply
# collided with the already-present `Some("kick2")` arm at main.rs:518. Apply only if the
# tree is clean, treat "already applied" as fine, and reverse only what we ourselves applied.
if git apply --check "$RUN/work/patch.diff" 2>/dev/null; then
    git apply "$RUN/work/patch.diff"
    trap 'git apply -R "$RUN/work/patch.diff" || true' EXIT
elif git apply -R --check "$RUN/work/patch.diff" 2>/dev/null; then
    echo "regen: work/patch.diff is already applied; using the tree as-is" >&2
else
    echo "regen: work/patch.diff fits neither the clean tree nor the patched one:" >&2
    git apply --check "$RUN/work/patch.diff" || true
    exit 1
fi
cargo build --release -p emergent-encounters
BIN="$(cargo metadata --no-deps --format-version 1 | python3 -c 'import json,sys; print(json.load(sys.stdin)["target_directory"])')/release/encounters"
# Baseline: the shipped kick cascade (reproduces the published anchor pairs/kick = 812.8).
"$BIN" kick > "$RUN/kick-baseline.json"
# Decisive: the cascade anatomy (armed-set churn, knife edge, transform, cost split).
"$BIN" kick2 > "$RUN/kick2.json"
echo "wrote kick-baseline.json, kick2.json"
