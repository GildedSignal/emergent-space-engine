#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the
# runner before this runs). ~7 minutes: build, shipped tests, probe, flight sweep, analysis.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
OUT=lab/results/20261018-2040-second-20261018-1617-spacex-37c1-3ac3

# 37c1's lesson: never share the ambient target dir with sibling runs. A private temp dir.
export CARGO_TARGET_DIR="$(mktemp -d)"
echo "== build (own target dir)"
cargo build --release -p xtask 2>&1 | tail -1
cargo build --release -p emergent-lattice --example rt_skipfix 2>&1 | tail -1
echo "== shipped tests with the patch (flag off must be bit-identical)"
cargo test --release -p emergent-lattice 2>&1 | grep -E "test result" | sort | uniq -c
cargo test --release -p emergent-lattice-event --test equality 2>&1 | grep -E "test result"

echo "== probe: gates (a)+(b), the random sweep, the ship-scale gas (parts A/B/C)"
SPACEX_CENSUS=1 SPACEX_ORACLE=1 timeout 300 "$CARGO_TARGET_DIR/release/examples/rt_skipfix" \
  > "$OUT/probe.txt" 2> "$OUT/cens/probe.cens"
tail -6 "$OUT/probe.txt"

echo "== flight sweep (the flown plane: census, fix, oracle)"
bash "$OUT/sweep.sh" "$OUT/cens" "$CARGO_TARGET_DIR/release/xtask"

echo "== the two 3-s identity arms (the battle is over in 3 s of game; the dense arm exits
# 124 by timeout like 37c1's — its census is complete and is the identity check)"
SPACEX_CENSUS=1 SPACEX_ORACLE=1 SPACEX_FIX=1 SPACEX_SPEED_DIV=2 timeout 90 \
  "$CARGO_TARGET_DIR/release/xtask" universe --bench --unpaced --rtf 100 --seconds 3 --seed 1 --members 48 \
  >/dev/null 2> "$OUT/cens/sd2on3s.cens" || true
SPACEX_CENSUS=1 SPACEX_ORACLE=1 SPACEX_FIX=1 SPACEX_SPEED_DIV=2 SPACEX_ORDER=dense timeout 90 \
  "$CARGO_TARGET_DIR/release/xtask" universe --bench --unpaced --rtf 100 --seconds 3 --seed 1 --members 48 \
  >/dev/null 2> "$OUT/cens/sd2denseon3s.cens" || true
cmp "$OUT/cens/sd2on3s.cens" "$OUT/cens/sd2denseon3s.cens" && echo "3s dense/sparse with the fix: IDENTICAL"
cmp "$OUT/cens/sd2on3s.cens" "$OUT/cens/sd2on.cens" && echo "3s == 30s sparse: the battle is over in 3 s"

echo "== analysis"
python3 "$OUT/analyze.py"
