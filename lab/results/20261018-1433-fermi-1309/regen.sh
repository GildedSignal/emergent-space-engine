#!/bin/sh
# Regenerates every number in dossier.md (the audit table, the cliff, the geometry).
# No flight: the audited object is arithmetic on frozen-measured constants; the
# shipped-code constants are re-verified against the tree (scenario.rs, ctx.rs).
set -e
cd "$(dirname "$0")"

# the shipped constants the geometry and cadence rest on (fail loudly if they move):
grep -q 'name: "Cinder", mass_log2: -21, periapsis: 35_600_000' ../../../crates/universe/src/scenario.rs
grep -q 'name: "Giant", mass_log2: -10, periapsis: 500_000_000' ../../../crates/universe/src/scenario.rs
grep -q 'step_log2: 7' ../../../crates/universe/src/ctx.rs
grep -q '36,000 a wall second at rtf 100' ../../../artifacts/runs/nladder/ladder.txt
python3 compose_check.py > work/regen.out
sed -n '/== A/,$p' work/regen.out > work/regen.a
sed -n '/== A/,$p' work/fermi-check.out > work/recorded.a
if cmp -s work/regen.a work/recorded.a; then
  echo "REGEN: identical to the recorded run"
else
  echo "REGEN: DIFFERS from the recorded run"; diff work/recorded.a work/regen.a; exit 1
fi
