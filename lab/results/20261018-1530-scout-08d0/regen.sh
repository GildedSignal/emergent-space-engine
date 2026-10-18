#!/usr/bin/env bash
# Regen: rebuilds every dossier number from scratch. Rust only, ~6 min.
set -euo pipefail
cd "$(dirname "$0")"
rustc -O -o beat beat.rs
echo "== main arm (seed 1, n 2500) =="
./beat 1 2500 | tee main.txt
echo "== held-out arm (seed 2, n 3000; cases the author did not tune on) =="
./beat 2 3000 | tee heldout-s2.txt
echo "== held-out arm (seed 77, n 1500) =="
./beat 77 1500 | tee heldout-s77.txt
