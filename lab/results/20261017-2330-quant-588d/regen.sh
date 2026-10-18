#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (assumed
# already applied by the runner; if not, applied below). ~5-7 min on 8 vCPU.
set -euo pipefail
R="$(cd "$(dirname "$0")/../../.." && pwd)"   # repo root
cd "$R"
W="$R"/lab/results/20261017-2330-quant-588d/work
mkdir -p "$W/ctrl"
if ! grep -q "mod fit_census" crates/space/src/binding.rs; then
  git apply "$W/patch.diff"
fi
D=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys;print(json.load(sys.stdin)['target_directory'])")
cargo build --release -p emergent-universe --example nladder --example ladder_digest
# Pristine control binary: the census lives in space/{binding,orbit}.rs; restore the two
# from git, build ladder_digest pristine, then re-apply just those two files' hunks.
git checkout -- crates/space/src/binding.rs crates/space/src/orbit.rs
cargo build --release -p emergent-universe --example ladder_digest
cp "$D/release/examples/ladder_digest" "$W/ladder_digest.pristine"
git apply --include=crates/space/src/binding.rs --include=crates/space/src/orbit.rs "$W/patch.diff"
cargo build --release -p emergent-universe --example nladder --example ladder_digest
cp "$D/release/examples/nladder" "$W/nladder.census"
cp "$D/release/examples/ladder_digest" "$W/ladder_digest.census"

cd "$W"
echo "== digest controls (fields name|digest|kicks/encounters/contacts)"
./ladder_digest.pristine "N=3000 coast through" > ctrl/pristine.txt 2>&1
./ladder_digest.census   "N=3000 coast through" > ctrl/off.txt     2>&1
FIT_CENSUS=1 ./ladder_digest.census "N=3000 coast through" > ctrl/on.txt 2> ctrl/on.err
cut -d'|' -f1-3 ctrl/pristine.txt > ctrl/p.f3; cut -d'|' -f1-3 ctrl/off.txt > ctrl/o.f3; cut -d'|' -f1-3 ctrl/on.txt > ctrl/n.f3
diff ctrl/p.f3 ctrl/o.f3 && echo OFF_IDENTICAL
diff ctrl/p.f3 ctrl/n.f3 && echo ON_IDENTICAL
grep -c -E "panick|abort" ctrl/on.err || true

echo "== census arms (single-threaded flights, FIT_CENSUS=1)"
for a in "0 25 1800" "3000 55 1800" "10000 55 1800" "3000 55 600"; do
  set -- $a
  FIT_CENSUS=1 ./nladder.census "$1" coast "$2" "$3" > "census_$1_$3.log" 2>&1
  grep "FITCENSUS totals" "census_$1_$3.log"
  grep "FITCENSUS at" "census_$1_$3.log" | tail -2
done
rm -f "$W/nladder.census" "$W/ladder_digest.census" "$W/ladder_digest.pristine"

echo "== shape bytes"
cd "$R" && cargo run --release -p emergent-space --example envelope 2>/dev/null | grep "bytes:"
