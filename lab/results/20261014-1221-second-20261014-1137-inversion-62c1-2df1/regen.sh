#!/bin/bash
# Regenerates every number in dossier.md from the shipped code plus this run's patch
# (work/patch.diff, applied by the runner before this runs).
# Trimmed to ~5 min unloaded (was >15 min under load: the audit re-runs the shipped
# gather on audited frames and the 1e5 sky/base rows cost ~2.4 s per frame, so frame
# counts are cut where the per-frame statistics do not need them; the 1e6 fills,
# which carry the claim, are kept whole).
set -e
cd "$(dirname "$0")/../../.." || exit 1
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}"
B=$CARGO_TARGET_DIR/release/examples/flyframe2
cargo build --release -p emergent-universe --example flyframe2 2>&1 | tail -1
R=lab/results/20261014-1221-second-20261014-1137-inversion-62c1-2df1
: > $R/regen.txt
echo "=== baselines (the shipped frame: engine + gather_cached + view_json wire) ===" >> $R/regen.txt
$B base 0 240 100 2>/dev/null | grep '^base' >> $R/regen.txt || true
$B base 1000 120 100 2>/dev/null | grep '^base:' >> $R/regen.txt || true
$B base 10000 48 100 2>/dev/null | grep '^base:' >> $R/regen.txt || true
$B base 100000 10 100 2>/dev/null | grep '^base:' >> $R/regen.txt || true
echo "=== display, map, fitted zoom, coast ===" >> $R/regen.txt
$B disp 0 240 100 map fit coast 1 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 1000 120 100 map fit coast 1 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 10000 80 100 map fit coast 4 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 100000 32 100 map fit coast 8 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 1000000 120 100 map fit coast 0 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
echo "=== display, map, belt zoom, coast ===" >> $R/regen.txt
$B disp 1000 120 100 map belt coast 1 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 10000 80 100 map belt coast 4 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 100000 32 100 map belt coast 8 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 1000000 120 100 map belt coast 0 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
echo "=== display, map, fitted, one turn ===" >> $R/regen.txt
$B disp 0 240 100 map fit turn 1 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 10000 80 100 map fit turn 4 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
echo "=== display, map, fit -> belt zoom-out ===" >> $R/regen.txt
$B disp 1000 120 100 map fit zoomout 1 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 10000 80 100 map fit zoomout 4 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 100000 32 100 map fit zoomout 8 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 1000000 120 100 map fit zoomout 0 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
echo "=== display, sky, coast ===" >> $R/regen.txt
$B disp 1000 120 100 sky fit coast 1 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 10000 80 100 sky fit coast 4 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
$B disp 100000 12 100 sky fit coast 8 2>/dev/null | grep '^disp:' >> $R/regen.txt || true
echo "=== digest (the view.rs refactor leaves gather_cached byte-identical; deterministic budget) ===" >> $R/regen.txt
$B digest 1000 200 100 2>/dev/null | grep final >> $R/regen.txt || true
echo DONE >> $R/regen.txt
tail -5 $R/regen.txt
