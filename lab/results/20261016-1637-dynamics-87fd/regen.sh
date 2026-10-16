#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff
# (21a7's ES_CHAIN/ES_LOCAL_STAGGER/ES_LOCAL_PHASE port + this run's doll_probe example).
# Five flights of <= 50 s: ~5 min total.
set -euo pipefail
cd "$(dirname "$0")/../../.."  # repo root

if ! grep -q "ES_CHAIN" crates/universe/src/step.rs; then
  git apply lab/results/20261016-1637-dynamics-87fd/work/patch.diff
  grep -q "ES_CHAIN" crates/universe/src/step.rs || { echo "ERROR: patch did not apply"; exit 1; }
fi
echo "tree: $(git rev-parse HEAD) (patch applied)"
cargo build --release -p emergent-universe --example doll_probe
B="$(cargo metadata --format-version 1 --no-deps | sed -n 's/.*"target_directory":"\([^"]*\)".*/\1/p')/release/examples/doll_probe"
[ -x "$B" ] || { echo "ERROR: no doll_probe binary"; exit 1; }
R=lab/results/20261016-1637-dynamics-87fd/flights
mkdir -p "$R"
run () { local label=$1; shift; local seed=$1; shift
  echo "=== $label (seed $seed) ==="
  env ${1+"$@"} "$B" 1000 45 100 "$seed" | tee "$R/$label.txt"
}
run off_s1       1
run cs_s1        1 ES_CHAIN=1 ES_LOCAL_STAGGER=1
run ph_s1        1 ES_LOCAL_PHASE=1
run off_s2       2
run cs_s2        2 ES_CHAIN=1 ES_LOCAL_STAGGER=1

echo "--- headline table (grep the ensembles) ---"
grep -H -E "frames:|dE/E0|dL/L0|E1|L1|r1" "$R"/*.txt | sed "s|$R/||"
echo "DONE. Compare with dossier.md."
