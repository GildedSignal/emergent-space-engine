#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (the prof sub-stage
# instrument, the ES_MEMBERS clamp lift and the bench's prof dump). ~4 min on 8 vCPU.
#
# Why a private snapshot: this worktree is shared by the window's runs. A sibling's run.sh
# can hold live edits (then every hunk fails to apply) or restore the tree mid-run (then
# regen builds unpatched code and the prof stages vanish). Both happened. So the patch is
# applied inside a throwaway export of HEAD; the shared tree is never touched.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
T="$PWD"
R=lab/results/20261014-0450-quant-1845

SNAP=$(mktemp -d /tmp/regen-1845-XXXXXX)
trap 'rm -rf "$SNAP"' EXIT
git archive HEAD | tar -x -C "$SNAP"
cd "$SNAP"
git apply "$T/$R/work/patch.diff"
# Warm the private target from the lab's dir (copied, never shared); cold fallback is fine.
[ -d /home/glmlab/lab-target-3 ] && cp -a /home/glmlab/lab-target-3 "$SNAP/target"
export CARGO_TARGET_DIR="$SNAP/target"
XT="$CARGO_TARGET_DIR/release/xtask"
build_prof()  { cargo build --release -p xtask --features emergent-universe/prof 2>&1 | tail -1; }
build_plain() { cargo build --release -p xtask 2>&1 | tail -1; }
mkdir -p out
export ES_MEMBERS=1000000
# The identity control (prof changes nothing): m400/s3, prof binary vs pristine binary.
build_prof
"$XT" universe --bench --seed 3 --rtf 1 --seconds 8 --members 400 > out/m400-s3-prof.json
build_plain
"$XT" universe --bench --seed 3 --rtf 1 --seconds 8 --members 400 > out/m400-s3-pristine.json
# The decisive arms (battle, rtf 1, 8 game-s; ad26's scene class) on the prof binary.
build_prof
for arm in "4000 3" "1500 3" "4000 7"; do set -- $arm
  "$XT" universe --bench --seed $2 --rtf 1 --seconds 8 --members $1 > "out/m$1-s$2-prof.json"
done
cd "$T"
cp "$SNAP"/out/*.json "$R/work/"
python3 "$R/work/table.py"
