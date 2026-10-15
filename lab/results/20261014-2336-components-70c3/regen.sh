#!/bin/sh
# Regenerates every number in dossier.md (20261014-2336-components-70c3).
# Run from anywhere; it finds the repo root itself. ~75 s on the lab box (release build cached after the first run).
set -e
cd "$(dirname "$0")/../../.."   # repo root: lab/results/<run> sits three levels below it
RUN=lab/results/20261014-2336-components-70c3

# The shipped side needs the run's nladder patch (Linux /proc memory read), which the runner
# applies as work/patch.diff before this script; if the tree is clean (a bare checker run), apply it now.
if ! grep -q 'target_os = "linux"' crates/universe/examples/nladder.rs 2>/dev/null; then
  git apply "$RUN/work/patch.diff"
fi

echo '== shipped ladder rungs (build us/body, B/body, frame p50; Linux VmRSS domain) =='
for n in 1000 10000 100000; do
  cargo run --release -p emergent-universe --example nladder -- "$n" coast 20 2>/dev/null | grep '^ladder:'
done

echo '== the floor probe (calibration, cost, bytes, error disciplines) =='
cd "$RUN"
rustc -O -o mini mini.rs
./mini
