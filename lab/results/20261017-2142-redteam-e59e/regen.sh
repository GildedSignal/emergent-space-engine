#!/bin/sh
# Regen: every number in dossier.md, from this folder's scripts only.
# No tree edits were made outside lab/results/20261017-2142-redteam-e59e/
# (work/patch.diff is empty), so nothing else is applied.
set -e
cd "$(dirname "$0")"
python3 falsifier.py > evidence.json
# P7: the gap is total — ray-side capture gated, view-side opacity absent.
echo "--- rung/gate mentions of capture (ray dynamics only):"
grep -ril "captur" ../../../lab/rungs/ ../../../docs/law.md 2>/dev/null || true
echo "--- occlusion/shadow/eclipse anywhere in the view spec or rungs (expect none):"
grep -riE "occlu|eclipse" ../../../docs/representation.md ../../../docs/law.md ../../../lab/rungs/ || echo "NONE"
echo "--- shipped gather is straight light:"
grep -n "no lensing yet" ../../../crates/universe/src/view.rs
echo "done"
