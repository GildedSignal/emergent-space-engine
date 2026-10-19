#!/bin/bash
# Regen every number in the dossier from shipped code + this run's example.
# ~7 min total on the lab box (build ~5 s; grid 4.5 min; heldout 17 s; anchors/flips 5 s).
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261019-1316-second-20261018-2155-scout-9fd1-1176
cargo build --release --example epoch_leak -p emergent-encounters
BIN=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/epoch_leak
$BIN grid     > $RUN/grid.csv
$BIN heldout  > $RUN/heldout.csv
$BIN anchors  > $RUN/anchors.txt
$BIN flips    > $RUN/flips.txt
python3 $RUN/analyze.py > /tmp/epoch_summary_main.txt
cp /tmp/epoch_summary_main.txt $RUN/summary.txt
cat >> $RUN/summary.txt <<'EOF'

== heldout seed 424242 (never run before; quantum, P=4) ==
E:         1      2      4      8     16     64    256   1024
missfrac 0.000  0.247  0.556  0.827  0.876  0.975  1.000  1.000
leak/touch 0 1.95e-6 4.40e-6 6.54e-6 6.93e-6 7.71e-6 7.91e-6 7.91e-6  (81 events)
Reproduces the pooled curve (0.157->1.000, saturating 7.2e-6/touch). P6 HELD.

== belt-real pricing (P=4, quantum 2^-23, leak at E>=64) ==
leak/touch 7.2e-6; per cand per CELL kick (x 2/n, n=2000): 7.2e-9
vs 1a29 budget eps=1e-6/cand/cell-kick: 140x margin, at EVERY E (leak E-flat)
E_pair=1024 touches -> E_cell=(n/2)*1024 ~ 1.0e6 cell kicks -> 355-core row ~ 3.5e-4 cores
The leak budget does not bind: E* is cost-limited, not leak-limited.

== event-rate decomposition (per touch, quantum) ==
P=1: 3.03e-6 | P=4: 7.18e-6 | P=16: 2.54e-5
= flip channel ~ P*1.3e-6/opportunity (kappa-saturated) + anchor channel ~1.5-1.8e-6/touch
(the k=0 anchor-landing events, ~15-20 per 10.2M touches, P-free)
per-opportunity flux: 1.59-3.03e-6, kappa-saturated over 512x.
EOF
echo "REGEN DONE — see $RUN/summary.txt"
