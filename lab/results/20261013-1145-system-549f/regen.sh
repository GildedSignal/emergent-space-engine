#!/bin/sh
# Regenerates every number in dossier.md from the shipped code + this run's probe.
# The probe (crates/universe/examples/a_word.rs) arrives via work/patch.diff; if the
# tree is pristine, restore it from this folder. ~15 s of compute after the build.
set -e
cd "$(dirname "$0")/../../.."
if [ ! -f crates/universe/examples/a_word.rs ]; then
  cp lab/results/20261013-1145-system-549f/a_word.rs crates/universe/examples/a_word.rs
fi
cargo run --release -p emergent-universe --example a_word 2>/dev/null \
  | tee lab/results/20261013-1145-system-549f/census.txt
echo "--- code facts cited in the dossier (shipped tree) ---"
grep -n "force::field" crates/universe/src/observe.rs crates/universe/src/step.rs | head -5
grep -n "let dv = scale2(f.accel" crates/universe/src/step.rs
