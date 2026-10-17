#!/bin/bash
# Regen for 20261017-1447-dynamics-fd35: rebuilds the instrumented allocator from
# work/patch.diff (HAZ/PRE/RB/FIRE in alloc.rs + examples/race.rs), reruns every arm
# of the decisive matrix plus the controls, and recomputes the dossier numbers.
# ~6 min on 8 vCPU (build ~15 s included).
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-1447-dynamics-fd35

# 1. clean tree, then apply the print-only instrument patch
git checkout -- crates/allocator/src/alloc.rs 2>/dev/null || true
rm -f crates/allocator/examples/race.rs
git apply "$R/work/patch.diff"
cargo build -p emergent-allocator --release --offline --example race 2>&1 | grep -E '^error' && exit 1
BIN=$(cargo metadata --format-version 1 --no-deps >/dev/null 2>&1; echo "${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}/release/examples/race")

# 2. the arms (one process each, so a firing assert ends only its own arm)
mkdir -p "$R/regen" && cd "$R/regen"
: > exits.txt
run() { local tag=$1; shift; timeout 60 "$BIN" "$@" > "$tag.out" 2> "$tag.err" && echo "$tag exit=0" >> exits.txt || echo "$tag exit=$?" >> exits.txt; }
for s in 11 15 21 2 11 15; do run "m_churn_$s"  3000 $s  1 2400 4 16 8  64  40 3 1.0; done
for s in 11 15 21 2 11 15; do run "m_disp_$s"   1000 $s  1  600 6 16 8 160 100 3 1.0; done
for s in 11 15;             do run "m_ctl_$s"   3000 $s 32 2400 4 16 8  64  40 3 1.0; done
for s in 11 15 21;          do run "x_$s"       2000 $s  1  900 4 16 8   2   0 0 1.0; done
run "h_128_60" 400 11 1 900 2 16 8 128 60 0 0.3   # the armed-episode probe

# 3. the dossier numbers (same table the dossier cites)
python3 "$R/analyze.py" . | tee regen-summary.txt
