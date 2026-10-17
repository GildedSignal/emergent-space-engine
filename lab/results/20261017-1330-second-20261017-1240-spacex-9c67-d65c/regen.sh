#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (~12 min on the lab box).
# Arms: pristine = shipped tree; patched = work/patch.diff (9c67's hand-off + the per-kind/magnitude
# verify instrumentation; verify mode only, behaviour = 9c67's deletion). The waveprobe example is
# 5ade's harness (source census stripped); the pristine build drops its two probe lines (those
# symbols exist only in the patch).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
R=$HERE
cd "$HERE/../../.."   # repo root

T=${CARGO_TARGET_DIR:-target}/release
export CARGO_BUILD_JOBS=8   # .cargo/config.toml pins jobs=2; a cold build must fit the 15-min cap
mkdir -p $R/work
PB=/tmp/d65c-regen
mkdir -p $PB

echo "== build pristine =="
git checkout -q -- crates/ || true
grep -v "pos_probe" $R/work/waveprobe.rs > crates/universe/examples/waveprobe.rs
cargo build --release --features prof -p emergent-universe --example waveprobe --example cost_split 2>&1 | tail -1
cp $T/examples/waveprobe $PB/waveprobe-pristine; cp $T/examples/cost_split $PB/cost_split-pristine

echo "== apply patch, build patched =="
git apply $R/work/patch.diff
cp $R/work/waveprobe.rs crates/universe/examples/waveprobe.rs
cargo build --release --features prof -p emergent-universe --example waveprobe --example cost_split 2>&1 | tail -1
cp $T/examples/waveprobe $PB/waveprobe-patched; cp $T/examples/cost_split $PB/cost_split-patched

cd $PB
echo "== plane census (reproduces the checker's per-kind numbers) =="
ES_POS_VERIFY=1 ./cost_split-patched | tee $R/work/plane-census.txt

echo "== belt wave, interleaved 3 pairs + first-wave pair + census =="
./waveprobe-pristine 100000 70000 150000 > $R/work/belt-p1-pristine.txt 2>&1
./waveprobe-patched  100000 70000 150000 > $R/work/belt-p1-patched.txt  2>&1
./waveprobe-pristine 100000 70000 150000 > $R/work/belt-p2-pristine.txt 2>&1
./waveprobe-patched  100000 70000 150000 > $R/work/belt-p2-patched.txt  2>&1
./waveprobe-pristine 100000 70000 150000 > $R/work/belt-p3-pristine.txt 2>&1
./waveprobe-patched  100000 70000 150000 > $R/work/belt-p3-patched.txt  2>&1
./waveprobe-pristine 100000 13000 15000 > $R/work/belt-w1-pristine.txt 2>&1
./waveprobe-patched  100000 13000 15000 > $R/work/belt-w1-patched.txt 2>&1
ES_POS_VERIFY=1 ./waveprobe-patched 100000 70000 150000 > $R/work/belt-census.txt 2>&1

echo "== analysis =="
python3 $R/work/analyze.py | tee $R/work/belt-analysis.txt

echo "== restore tree =="
cd - >/dev/null
rm -f crates/universe/examples/waveprobe.rs
git checkout -q -- crates/
echo "done"
