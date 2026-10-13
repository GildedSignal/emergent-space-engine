#!/bin/sh
# Regenenerates every number in the dossier from the patched tree.
# The patch (work/patch.diff) is applied by the runner before this runs.
# Total wall: ~3-4 min on the shared Linux runner.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261013-0459-spacex-1c0d

# 1. The acceptance grid, both arms (shipped bits = ES_INVDOMAIN=0 on the patched tree).
cargo build --release -p emergent-space --example far_wall
B=/home/glmlab/lab-target-1/release/examples/far_wall
[ -x "$B" ] || B=$(find target -path "*release/examples/far_wall" -type f | head -1)
ES_INVDOMAIN=0 "$B" > "$R/out/grid_base.txt"
"$B" > "$R/out/grid_fallback.txt"
echo "--- summaries (base, fallback):"
tail -1 "$R/out/grid_base.txt"; tail -1 "$R/out/grid_fallback.txt"
echo "--- rows changed between arms (expect: only formerly-refused rows):"
diff "$R/out/grid_base.txt" "$R/out/grid_fallback.txt" | grep -c '^[<>]' || true

# 2. Stage isolation + key-bit agreement at sampled corners.
cargo build --release -p emergent-space --example far_diag
D=/home/glmlab/lab-target-1/release/examples/far_diag
[ -x "$D" ] || D=$(find target -path "*release/examples/far_diag" -type f | head -1)
"$D" | tee "$R/out/diag.txt"

# 3. Digest identity: the space suite in both arms (fallback default-on vs shipped bits).
cargo test --release -p emergent-space 2>&1 | tail -3 | tee "$R/out/suite_fb.txt"
ES_INVDOMAIN=0 cargo test --release -p emergent-space 2>&1 | tail -3 | tee "$R/out/suite_base.txt"

# 4. The plane digests (shipped scenes never reach the wall; both arms must agree).
cargo test --release -p emergent-universe --test plane 2>&1 | tail -3 | tee "$R/out/plane_fb.txt"
ES_INVDOMAIN=0 cargo test --release -p emergent-universe --test plane 2>&1 | tail -3 | tee "$R/out/plane_base.txt"
