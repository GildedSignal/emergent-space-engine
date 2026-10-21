#!/bin/sh
# Regenenerates every number in the dossier: the family/lattice certificate census (112 s).
# Standalone f64 instrument on the shipped kick formulas' verbatim structure; no engine build.
set -e
cd "$(dirname "$0")"
rustc -O -o family_hill family_hill.rs
./family_hill > census.csv
echo "--- census.csv regenerated (48 arms: 8 domain-radii x 6 separations, K=2^17 kicks each) ---"
