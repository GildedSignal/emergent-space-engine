#!/bin/sh
# Regenerates every number in dossier.md (20261014-0000-redteam-f3ce).
# Requires: cargo, a checkout of this repo at the run's base commit.
# Total runtime ~5-6 min (gas arms dominate). Each command < 60 s where possible
# is violated by gas-mixed (5 seeds ~135 s); run per-seed below to stay under it.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261014-0000-redteam-f3ce

# 1. restore the probe (work/patch.diff carries the example; the .rs copy is the fallback)
if [ -f "$R/work/patch.diff" ] && grep -q rt_carry "$R/work/patch.diff"; then
  git apply "$R/work/patch.diff" || echo "patch already applied"
else
  cp "$R/rt_carry.rs" crates/lattice/examples/rt_carry.rs
fi

# 2. build
(cd crates/lattice && cargo build --release --example rt_carry)

# 3. run every arm with the run's seeds (logs overwrite the stored ones)
cd crates/lattice
run() { cargo run --release --quiet --example rt_carry -- "$@" 2>/dev/null; }
run self            | tee ../../$R/self.log
run gas-cold        | tee ../../$R/gas-cold.log
run gas-hot         | tee ../../$R/gas-hot.log
run gas-mixed 1 2   | tee ../../$R/gas-mixed.log
run gas-mixed 3     | tee -a ../../$R/gas-mixed.log
run gas-mixed 4 5   | tee -a ../../$R/gas-mixed.log
run gas-mixed 11 12 13 | tee ../../$R/gas-mixed-heldout.log
run gas-mixed 14 15 | tee -a ../../$R/gas-mixed-heldout.log
run label           | tee ../../$R/label.log
run label-slow      | tee ../../$R/label-slow.log
run perm            | tee ../../$R/perm.log

# 4. the dossier's summary lines
grep -h MEDIAN ../../$R/self.log ../../$R/gas-cold.log ../../$R/gas-hot.log \
  ../../$R/gas-mixed.log ../../$R/gas-mixed-heldout.log ../../$R/label.log \
  ../../$R/label-slow.log ../../$R/perm.log
grep -h "RESULT" ../../$R/gas-mixed.log ../../$R/gas-mixed-heldout.log
grep -h "label seed" ../../$R/label.log | grep -v series
grep -h "perm seed" ../../$R/perm.log
