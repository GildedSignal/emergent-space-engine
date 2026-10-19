#!/bin/sh
# Regen: every dossier number from shipped code + this run's scripts.
# Patch first (the print-only /proc footprint swap in nladder), then two probe
# flights (~15 s + ~13 s) and the ledger (~0.1 s). Total under 2 minutes.
set -e
cd "$(dirname "$0")/../../.."   # repo root
if git apply --check lab/results/20261019-0141-fermi-097e/work/patch.diff 2>/dev/null; then
  git apply lab/results/20261019-0141-fermi-097e/work/patch.diff
fi
cargo build --release -p emergent-universe --example nladder
NL="cargo run --release -p emergent-universe --example nladder --"
cd lab/results/20261019-0141-fermi-097e
$NL 10000 coast 10 > probe-n1e4.log 2>&1
$NL 100000 coast 10 > probe-n1e5.log 2>&1
grep -h "ladder:" probe-n1e4.log probe-n1e5.log
python3 ledger.py > /dev/null && echo "ledger-out.json written"
