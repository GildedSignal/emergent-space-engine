#!/usr/bin/env bash
# Regen: rebuild and rerun the kick attribution probe (work/patch.diff adds the example).
# ~40 s build (warm), ~2 s run. Every dossier number comes from this output.
cd "$(dirname "$0")/../../.."        # repo root (lab/results/<run>)
cargo run --release -p emergent-universe --example kick_fermi 2>/dev/null \
  | tee lab/results/20261013-0236-fermi-061f/regen_out.txt
echo "--- key lines (compare with kick_fermi_raw.txt) ---"
grep -E "armA|armB_allocs|armB_bytes|armB_class|armC|armD|unit_ns|pair_ns (16|256|512) |attribution" \
  lab/results/20261013-0236-fermi-061f/regen_out.txt
