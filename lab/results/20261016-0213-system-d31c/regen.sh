#!/bin/bash
# Regenerates every dossier number from the patch (applied by the runner before this runs).
# Budget: ~4 minutes on the lab box (build ~40 s warm, grid ~50 s, two suites ~5 min total are the tail;
# suites are last so the timing grid flies on a quiet machine).
# NOTE: the repo root is three levels up from this file (lab/results/<run>/regen.sh), and all builds
# go to /home/glmlab/lab-target-3 because grid.sh flies that exact binary (warm on this runner).
set -e
export CARGO_TARGET_DIR=/home/glmlab/lab-target-3
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"   # absolute, so invocation cwd never matters
cd "$RUN_DIR/../../.."                     # the repo root
cargo build --release -p emergent-universe --example birth_rail
cd "$RUN_DIR"
bash grid.sh > out/grid_regen.log 2>&1
echo "--- digests (must pair off/on identically) ---"
grep -E "===|digest=" out/grid_regen.log | sed 's/birth_rail.*digest=/digest=/'
echo "--- pass per body (off -> on) ---"
grep "birth:" out/grid_regen.log
cd "$RUN_DIR/../../.."                     # the repo root
cargo test --release -p emergent-universe --tests 2>&1 | grep -E "test result" | awk '{p+=$4; f+=$6} END {print "suite memo-off: passed="p" failed="f}'
ES_PLANETS_AT_T=1 cargo test --release -p emergent-universe --tests 2>&1 | grep -E "test result" | awk '{p+=$4; f+=$6} END {print "suite memo-on: passed="p" failed="f}'
