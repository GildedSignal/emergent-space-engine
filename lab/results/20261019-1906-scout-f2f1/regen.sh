#!/bin/bash
# Regen every number in the dossier (20261019-1906-scout-f2f1) from the patch.
# ~7 min on the lab box: build ~5 s; law grid 6 arms x 3 seeds x 2.5 s ~ 50 s
# (P=16 arms ~3x slower); survive census ~70 s/arm at 20k pairs; fit < 1 s.
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261019-1906-scout-f2f1
# prerequisites: work/patch.diff (this run's edits: 1176's harness verbatim + the
# print-only survive/law modes) is applied by the runner before regen starts.
grep -q '"survive"' crates/encounters/examples/epoch_leak.rs || { echo "patch.diff not applied"; exit 1; }
cargo build --release --example epoch_leak -p emergent-encounters
BIN=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/epoch_leak
# (1) the law grid: miss_frac(E) per (P, kappa), 3 seeds pooled (seeds 20261018, 777, 424242)
for arm in "1 -23" "4 -23" "16 -23" "4 -26" "4 -14" "4 -100"; do set -- $arm
  $BIN law $1 $2 > $RUN/work/law_p$1_k$2.csv 2>/dev/null
done
# (2) the survival census (mechanism): E_ARM=2 catch-provenance, E_ARM=64 the q_direct primitive
$BIN survive 4 -23 20261018 20000 2  > $RUN/work/surv_e2_p4.txt  2>/dev/null
$BIN survive 4 -23 20261018 20000 64 > $RUN/work/surv_p4_q.txt   2>/dev/null
# (3) the pair geometry + kick-delta anchors (1176's anchors reproduce on this tree)
$BIN anchors > $RUN/work/anchors.txt 2>/dev/null
# (4) the closed-form fit: fit on E<=8, predict E in {16,64,256,1024}
python3 $RUN/work/fit.py "$RUN/work/law_*.csv" | tee $RUN/work/fit_final.txt
echo "REGEN DONE — dossier numbers: fit_final.txt (model/meas), surv_e2_p4.txt (SPLIT, GPERSIST), law_*.csv (raw)"
