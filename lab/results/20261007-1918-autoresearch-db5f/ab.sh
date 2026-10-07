#!/bin/bash
# Interleaved A/B: current tree (B) vs pristine crates/space (A), alternating, min per side.
R=$(dirname $0); B=/home/glmlab/lab-target-3/release/bench-compile
one() { taskset -c 2 $B --reps 51 2>/dev/null | grep -oP 'geomean_ns_per_compile \K[0-9.]+'; }
best() { python3 -c "import sys; print(min(float(x) for x in sys.argv[1:]))" "$@"; }
cd $R/bench && cargo build --release 2>/dev/null | grep -qE '^error' && { echo BUILD_FAIL_B; exit 1; }
bb=$(best $(one) $(one) $(one))
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-3
git stash push -- crates/space >/dev/null
cd $R/bench && cargo build --release 2>/dev/null | grep -qE '^error' && { echo BUILD_FAIL_A; exit 1; }
ba=$(best $(one) $(one) $(one))
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-3 && git stash pop >/dev/null
echo "pristine_A $ba  current_B $bb"
