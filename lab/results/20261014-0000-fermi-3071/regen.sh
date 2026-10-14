#!/usr/bin/env bash
# Regenerates every number in dossier.md: builds shipped code with the census probe
# (work/patch.diff = ea91's published ES_SURPRISE probe, applied verbatim), runs the
# held-out scenes, refreshes the two prior runs' saved data from their result branches,
# and prints the tables. ~2 min warm, ~8 min cold. Linux/x86 shared runner.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261014-0000-fermi-3071

# 0. the census probe (ea91's published patch, stored verbatim in this run) if the
#    runner has not already applied it via work/patch.diff
if ! grep -q census_on crates/universe/src/universe.rs; then
  git apply "$R/ea91/work.patch.diff"
fi
cargo build --release -p xtask
X=${CARGO_TARGET_DIR:-target}/release/xtask

# 1. this run's scenes (each <= 60 s): held-out A, reproduction control, doubled window B
ES_SURPRISE=1 "$X" universe --bench --seed 11 --members 120 --rtf 100 --seconds 55 --unpaced > "$R/census-hoA.json"
ES_SURPRISE=1 "$X" universe --bench --seed  3 --members 400 --rtf 100 --seconds 55 --unpaced > "$R/census-ho1rep.json"
ES_SURPRISE=1 "$X" universe --bench --seed  3 --members 400 --rtf 200 --seconds 55 --unpaced > "$R/census-hoB.json"

# 2. the two prior runs' saved data, refreshed from their immutable result branches when present
EA=origin/claude/lab-20261013-2252-dynamics-ea91
P7=origin/claude/lab-20261013-2252-second-20261013-2130-library-ae3d-7497
if git rev-parse --verify -q "$EA" >/dev/null; then
  for f in census-tune.json census-ho1.json census-ho2.json census-ho3.json; do
    git show "$EA:lab/results/20261013-2252-dynamics-ea91/$f" > "$R/ea91/$f"
  done
fi
if git rev-parse --verify -q "$P7" >/dev/null; then
  git show "$P7":lab/results/20261013-2252-second-20261013-2130-library-ae3d-7497/probe/idle-s1-m48.jsonl > "$R/p7497/idle-s1-m48.jsonl"
fi

# 3. the tables
python3 "$R/analyze.py"
