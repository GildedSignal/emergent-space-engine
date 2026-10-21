#!/usr/bin/env bash
# Regen for 20261021-0429-quant-a97f (~9 min): apply the run's patch (45c0's genesis instrument
# + this run's per-gen census dump), fly the two belts, attribute the standing load excess.
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
# The run folder is <repo>/lab/results/<run>: three levels up is the repo root.
ROOT="$(cd "$RUN/../../.." && pwd)"
cd "$ROOT"
git apply --check --reverse "$RUN/work/patch.diff" 2>/dev/null || git apply "$RUN/work/patch.diff"
cargo build --release -p emergent-universe --example genesis
cd "$RUN"
# The census dump appends, so clear this run's regenerable outputs before flying again.
rm -f census_ship_3000_1.tsv census_ship_12000_1.tsv genesis_birth_ship.tsv \
      excess_source.json excess_source.txt excess_source_2700.json excess_source_11700.json \
      excess_source_11700.txt evolve_g25.txt ship3000_g40.log ship12000_g20.log
# Both flights run with cwd=$RUN: the example writes its census/birth TSVs to its cwd.
ES_GENESIS_WALL=420 cargo run --release --manifest-path "$ROOT/Cargo.toml" -p emergent-universe --example genesis -- ship 3000 40 1 > ship3000_g40.log 2>&1
python3 analyze.py . census_ship_3000_1.tsv ship3000_g40.log 25 5 4 > excess_source.txt
mv -f excess_source.json excess_source_2700.json
python3 evolve.py census_ship_3000_1.tsv ship3000_g40.log 25 > evolve_g25.txt
ES_GENESIS_WALL=1400 cargo run --release --manifest-path "$ROOT/Cargo.toml" -p emergent-universe --example genesis -- ship 12000 20 1 > ship12000_g20.log 2>&1
python3 analyze.py . census_ship_12000_1.tsv ship12000_g20.log 14 5 4 > excess_source_11700.txt
mv -f excess_source.json excess_source_11700.json
grep -E "floor|A6|A0_ident" excess_source.txt excess_source_11700.txt
tail -2 evolve_g25.txt
