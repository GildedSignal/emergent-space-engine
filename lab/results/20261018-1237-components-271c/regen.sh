#!/usr/bin/env bash
# Regen 20261018-1237-components-271c: every dossier number, from a restored tree + work/patch.diff.
# Total wall: about 2 minutes (build) + about 10 s of benches + the crate's test suite.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$(git rev-parse --show-toplevel)"

# 1. Apply the run's patch (the instrument + the bit-identical isqrt arm).
git apply --check "$RUN_DIR/work/patch.diff" && git apply "$RUN_DIR/work/patch.diff"
trap 'git apply -R "$RUN_DIR/work/patch.diff" 2>/dev/null || true' EXIT

# 2. Build the bench (shared CARGO_TARGET_DIR if the runner sets one).
cargo build --release -p emergent-space --example isqrtbench
B="${CARGO_TARGET_DIR:-target}/release/examples/isqrtbench"

# 3. The decisive arms. isolated = the slice prices (110.6/80.6, 27.8/10.0 ns);
#    exact = 3e6-operand fuzz + 34 compile hashes (0 mismatches, ALL MATCH);
#    pairs = the in-situ -2.6..-13.0% table; census = the class/node/wide-isqrt table;
#    heldout = the pre-registered near-separatrix sweep and belt2 band.

# 3a. The runner freezes captured outputs read-only (444); the dir is writable,
#     so clear stale outputs before regenerating them.
for f in loadavg.txt bench-main.txt bench-heldout.txt tests.txt; do rm -f "$RUN_DIR/$f"; done
cat /proc/loadavg > "$RUN_DIR/loadavg.txt"
"$B" all     | tee "$RUN_DIR/bench-main.txt"
"$B" heldout | tee "$RUN_DIR/bench-heldout.txt"

# 4. The bit-identity guard on the crate's own suite (both arms exercised by the
#    fuzz above; the suite itself runs the shipped arm). Keep every binary's
#    result line so the pass count is visible, not just the last one.
cargo test --release -p emergent-space 2>&1 | grep -E 'test result|^error' | tee "$RUN_DIR/tests.txt"
