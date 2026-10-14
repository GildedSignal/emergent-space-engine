#!/bin/sh
# Regenerates every number in dossier.md (the table in panel_floor.csv).
# The probe itself (crates/space/examples/panel_floor.rs) is added by work/patch.diff.
# ~10 s build (warm) + ~5 s run on the lab's Linux/x86 box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo run --release --example panel_floor -p emergent-space 2>/dev/null \
  > lab/results/20261014-0450-components-5a3b/panel_floor.csv
echo "wrote lab/results/20261014-0450-components-5a3b/panel_floor.csv"
head -3 lab/results/20261014-0450-components-5a3b/panel_floor.csv
