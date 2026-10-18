#!/bin/sh
# Regen for 20261018-1530-components-e87d. Assumes work/patch.diff (the beatstore
# example) is applied. Builds the example and reruns every mode; ~40 s, 1 core, <100 MB.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release --example beatstore -p emergent-encounters 2>&1 | grep -E "^error" && exit 1 || true
R=/home/glmlab/lab-target-2/release/examples/beatstore
if [ ! -x "$R" ]; then R=$(find / -name beatstore -type f -path "*release/examples*" 2>/dev/null | head -1); fi
D=lab/results/20261018-1530-components-e87d
timeout 280 $R anchors 20261018 1e-4 > $D/anchors.txt
timeout 280 $R control 20261018 1e-4 > $D/control.txt
timeout 280 $R sweep   20261018 1e-4 > $D/sweep.txt
timeout 280 $R slack   20261018 1e-4 > $D/slack.txt
timeout 280 $R timing  20261018 1e-4 > $D/timing.txt
timeout 280 $R stale   20261018 1e-4 > $D/stale.txt
# held-out: second seed, 10x tighter cell
timeout 280 $R anchors 777 1e-5 > $D/anchors-heldout.txt
timeout 280 $R control 777 1e-5 > $D/control-heldout.txt
echo REGEN-DONE
