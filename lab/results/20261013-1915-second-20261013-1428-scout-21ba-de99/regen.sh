#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's patch.
# The runner applies work/patch.diff (adds crates/space/examples/elliptic_kernel.rs)
# BEFORE invoking this script, so the apply here is guarded: it runs only when the
# patch is not already in the tree (also lets the script work on a bare checkout).
# Builds, runs; output lands in probe-out.txt next to this script. Physics columns
# are deterministic; walls are medians on a shared box (orders of magnitude only).
set -e
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN_DIR/../../.." && pwd)"
cd "$ROOT"
if git apply --check "$RUN_DIR/work/patch.diff" 2>/dev/null; then
    git apply "$RUN_DIR/work/patch.diff"
else
    # Already applied by the runner: the example must exist; refuse otherwise.
    test -f crates/space/examples/elliptic_kernel.rs || {
        echo "patch not applied and example missing" >&2; exit 1; }
fi
cd crates/space
cargo build --release --example elliptic_kernel
cargo run --release --example elliptic_kernel > "$RUN_DIR/probe-out.txt" 2>/dev/null
echo "regen ok: $(grep -c . "$RUN_DIR/probe-out.txt") lines"
