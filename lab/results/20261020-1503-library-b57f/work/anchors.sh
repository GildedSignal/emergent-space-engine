#!/usr/bin/env sh
# P4/P5/P6: code anchors verbatim in-tree, run from the repo root.
set -e
cd "$(dirname "$0")/../../../.."
echo "== P4: anchors =="
grep -n "0..ctx.bodies.len()" crates/universe/src/encounter.rs
grep -n "Replace the encounter finder (the seam): the Binet cone later" crates/universe/src/universe.rs
grep -n "Two orbits meet only if their Binet separation" crates/encounters/src/tier.rs
grep -n "the caller reads every body as before: the filter costs nothing it does not save" crates/universe/src/radial.rs
grep -n "candidates: &\[(usize, Binding, Scalar)\]" crates/universe/src/encounter.rs
echo "== P5: no maintenance signal below the candidate set in the answer path =="
if grep -nE "epoch|generation|dirty|version" crates/universe/src/encounter.rs crates/universe/src/radial.rs; then
  echo "P5 FAIL: a signal exists"; exit 1
else echo "P5 PASS: none found (same_inputs compares the full candidate list)"; fi
echo "== P6: the hull is a body's bindings, not a doll's bodies; no per-doll gate fronts the scan =="
grep -n "hull of their radial ranges" crates/universe/src/radial.rs
grep -n "When the window covers most of what is registered" crates/universe/src/radial.rs
if grep -nE "fn (doll_hull|doll_range|doll_envelope|doll_gate)" crates/universe/src/radial.rs; then
  echo "P6 FAIL: a per-doll gate exists"; else echo "P6 PASS: no per-doll aggregate gate found"; fi
