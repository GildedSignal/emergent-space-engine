# regen.sh — regenerates every dossier number from shipped code + this run's patch.
# The patch adds one print-only example (crates/universe/examples/belt_scan_probe.rs); the tree
# carries no other change. Budget: ~1 min of build (warm) + ~45 s of runs.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
OUT=lab/results/20261016-1740-spacex-3999

# Apply this run's patch if the tree was restored (idempotent: skip when the example is present).
if [ ! -f crates/universe/examples/belt_scan_probe.rs ] && [ -f "$OUT/work/patch.diff" ]; then
  git apply --whitespace=nowarn "$OUT/work/patch.diff"
fi

cargo build --release -p emergent-universe --example belt_scan_probe --message-format=short >/dev/null
BIN="${CARGO_TARGET_DIR:-target}/release/examples/belt_scan_probe"
[ -x "$BIN" ] || BIN=$(find "${CARGO_TARGET_DIR:-$HOME/lab-target-2}" target -type f -name belt_scan_probe 2>/dev/null | head -1)

for n in 0 1000 10000 100000; do "$BIN" $n 1 > "$OUT/belt_${n}_seed1.txt" 2>&1; done
"$BIN" 1000 2     > "$OUT/belt_1000_seed2.txt"     2>&1
"$BIN" 100000 2   > "$OUT/belt_100000_seed2.txt"   2>&1

echo "--- headline lines ---"
grep -hE "^extra|^window.player_home|^window.belt|^belt_answer|^latch" "$OUT"/belt_{1000,10000,100000}_seed1.txt "$OUT"/belt_{1000,100000}_seed2.txt | sed "s/^/$(basename ${OUT}) /"
