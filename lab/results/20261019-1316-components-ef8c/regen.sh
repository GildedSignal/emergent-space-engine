#!/bin/sh
# Regenerates every number in the dossier (grid: <1 min of runs after a ~10 s build).
set -e
cd "$(dirname "$0")/../../.." || exit 1
OUT=lab/results/20261019-1316-components-ef8c/belt_cells_grid.txt
: > "$OUT"
for arm in "1 10000" "1 100000" "7 100000" "3 300000" "1 1000000"; do
  set -- $arm
  echo "== seed=$1 extra=$2 ==" >> "$OUT"
  cargo run --release -p emergent-universe --example belt_cells -- "$1" "$2" 2>/dev/null >> "$OUT"
done
grep -c "belt_cells:" "$OUT"   # 5 arms
