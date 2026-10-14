#!/usr/bin/env bash
# Regen for 20261014-1137-fermi-1738: every dossier number regenerates in <= 2 min
# (build cached: ~5 s; anchor run ~5 s; ledger < 1 s). Run from the repo root.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root (this file is lab/results/<run>/regen.sh)
RUN=lab/results/20261014-1137-fermi-1738

echo "== 1. shipped anchor: the kick-cascade constants on this box =="
cargo build --release -p emergent-encounters
cargo run --release -p emergent-encounters -- kick > "$RUN/kick-anchor.jsonl"
cat "$RUN/kick-anchor.jsonl"

echo "== 2. code constant the cadence axis rides on =="
grep -n "step_log2: 7" crates/universe/src/ctx.rs

echo "== 3. the corrected ledger (dossier table, audit, walls) =="
python3 "$RUN/ledger2.py" | tee "$RUN/ledger2-out.txt"

echo "== 4. the stored evidence the audit reads (90fb's own rows, on its branch) =="
git show "origin/claude/lab-20261009-0401-second-20261009-0208-fermi-fe6b-90fb:lab/results/20261009-0401-second-20261009-0208-fermi-fe6b-90fb/budget-table.md" | grep -E "per CELL|max rtf on 4 cores: averaged \+ skin|SINGLE BELT"
git show "origin/claude/lab-20261009-0401-second-20261009-0208-fermi-fe6b-90fb:lab/results/20261009-0401-second-20261009-0208-fermi-fe6b-90fb/cascade.jsonl" | grep '"exp":"verify"'
git show "origin/claude/lab-20261014-0059-fermi-effb:lab/results/20261014-0059-fermi-effb/ledger.py" | grep -n "enc_skin"
echo "== done: compare with dossier.md sections Evidence 1-6 =="
