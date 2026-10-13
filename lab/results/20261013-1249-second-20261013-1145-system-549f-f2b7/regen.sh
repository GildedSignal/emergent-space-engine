#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree + work/patch.diff (applied by the
# runner before this runs). ~8 min: builds the wired probes, runs the gates and both census sides
# (the wired side on this tree, the control side by stashing the three wired source files), the
# A/B bench, and the strong-field scene. Everything lands in regen.txt.
set -e
cd "$(dirname "$0")/../../.."
R=lab/results/20261013-1249-second-20261013-1145-system-549f-f2b7
E=crates/universe/examples
mkdir -p /tmp/ab/wired2
{
# the probes arrive via work/patch.diff; if the tree is pristine, restore them from this folder
for f in a_word.rs word_wired.rs word_strong.rs; do
  [ -f $E/$f ] || cp $R/$f $E/$f
done
echo "### the wiring (work/patch.diff) ###"
git diff --stat crates/universe/src/ || true

echo; echo "### gates on the wired tree ###"
cargo test --release -p emergent-universe --test motion --test clock 2>&1 | grep -E "test result|FAILED|largest jump|worst ratio" || true

echo; echo "### wired census (the tree's readout vs the by-hand shipped readout; digests) ###"
cargo build --release -p emergent-universe --example word_wired --example word_strong --example view_cost --example a_word 2>&1 | grep -E "^error" -A4 || true
for f in word_wired word_strong view_cost a_word; do cp /home/glmlab/lab-target-0/release/examples/$f /tmp/ab/wired2/; done
/tmp/ab/wired2/word_wired

echo; echo "### the 549f census itself (unchanged probe, wired tree) ###"
/tmp/ab/wired2/a_word coast

echo; echo "### control side: stash the wiring, rebuild, same probes ###"
git stash push crates/universe/src/bind.rs crates/universe/src/step.rs crates/universe/src/observe.rs -m regen >/dev/null
cargo build --release -p emergent-universe --example word_wired --example view_cost 2>&1 | grep -E "^error" -A4 || true
mkdir -p /tmp/ab/base
for f in word_wired view_cost; do cp /home/glmlab/lab-target-0/release/examples/$f /tmp/ab/base/; done
echo "-- control word_wired (must read err 0.0 and the same digests) --"
/tmp/ab/base/word_wired
git stash pop >/dev/null
cargo build --release -p emergent-universe --example word_wired --example word_strong --example view_cost --example a_word 2>&1 | grep -E "^error" -A4 || true

echo; echo "### A/B bench, interleaved, 3 rounds (base then wired) ###"
for i in 1 2 3; do
  echo "-- round $i --"
  /tmp/ab/base/view_cost 100 48 | tail -2
  /tmp/ab/wired2/view_cost 100 48 | tail -2
done

echo; echo "### strong field: r=20M and the weak control ###"
/tmp/ab/wired2/word_strong 20
/tmp/ab/wired2/word_strong 4000
} 2>&1 | tee $R/regen.txt
echo "REGEN_OK"
