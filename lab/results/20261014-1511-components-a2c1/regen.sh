#!/usr/bin/env bash
# Regen (20261014-1511-components-a2c1): every number in dossier.md, from the shipped tree
# plus work/patch.diff. ~6-9 min on 8 vCPU (two builds, seven short flights, the aggregate).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # the repo root
RUN=lab/results/20261014-1511-components-a2c1

# 1. The probe (digest-neutral census + the example's Linux footprint cfg).
if ! git diff --quiet -- crates/universe/src/radial.rs crates/universe/src/encounter.rs 2>/dev/null; then
  echo "tree already carries radial/encounter edits; NOT applying the patch again" >&2
else
  git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" \
    || echo "patch already applied or tree moved; continuing" >&2
fi

mkdir -p "$RUN/raw"
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}/release/examples/nladder

# 2. The census arms (the dossier's table + the rad/cap lines).
for arm in "1000 coast" "10000 coast" "100000 coast" "10000 burn" "100000 burn"; do
  set -- $arm
  ES_SCAN_CENSUS=1 timeout 90 "$BIN" "$1" "$2" 20 > "$RUN/raw/n$1-$2.txt" 2> "$RUN/raw/n$1-$2.census"
  grep "^scan census" "$RUN/raw/n$1-$2.census"
done

# 3. The stage prices (prof build; capture and held-answer µs/call).
cargo build --release -p emergent-universe --example nladder --features prof 2>&1 | tail -1
for arm in "100000 coast" "1000 coast"; do
  set -- $arm
  echo "== prof $1 $2"
  timeout 90 "$BIN" "$1" "$2" 20 2>/dev/null | sed -n '/stages/,/^$/p' | grep -E "capture|held scans"
done

# 4. The aggregate (the dossier's table rows).
python3 "$RUN/aggregate.py" "$RUN"/raw/*.census
echo "regen done"
