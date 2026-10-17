#!/bin/sh
# Regen for 20261017-0839-second-20261017-0739-taleb-9b46-5d87 (frames-mode gold probe).
# The runner applies work/patch.diff (ruin.rs with the frames mode + the ES_CAP min line,
# default unbounded = shipped behaviour) before this runs. Builds the instrument, then
# regenerates every dossier number: the frames matrix (864 grid, wave 14k/28k, quiet 14k,
# relativistic 14k) and the batch controls. ~13 min on the shared 8-vCPU box; every process
# < 2 GB.
set -e
cd "$(dirname "$0")/../../.."   # repo root
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-5d87}
cargo build --release --offline -p emergent-allocator --example ruin
cd lab/results/20261017-0839-second-20261017-0739-taleb-9b46-5d87
sh arms.sh
sh arms2.sh
echo "regen complete; summaries above, full traces in out/"
