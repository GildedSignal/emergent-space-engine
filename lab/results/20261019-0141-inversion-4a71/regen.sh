#!/bin/sh
# 4a71: regenerate every dossier number. Assumes work/patch.diff is applied (the runner applies
# it before this runs): the print-only /proc probe + ES_WALL_CAP_S/ES_PROBE_EVERY_GS knobs in
# crates/universe/examples/nladder.rs, and the disclosed env-gated pin + probe accessors in
# crates/universe/src/universe.rs. ~4 min cold.
set -e
cd "$(dirname "$0")/../../.."   # repo root
HERE=lab/results/20261019-0141-inversion-4a71
BIN_TARGET="${CARGO_TARGET_DIR:-$HOME/lab-target-2}/release/examples/nladder"

cargo build --release -p emergent-universe --example nladder


# the three decisive arms (identical to the author's flights; deterministic counts)
ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000 "$BIN_TARGET" 30000 coast 100 800 > "$HERE/logs/ctrl-70k.log" 2>&1
ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000 ES_PIN_OLDEST=6000000000 "$BIN_TARGET" 30000 coast 100 800 > "$HERE/logs/pin6e9.log" 2>&1
ES_WALL_CAP_S=130 ES_PROBE_EVERY_GS=2000 ES_PIN_OLDEST=12000000000 "$BIN_TARGET" 30000 coast 100 800 > "$HERE/logs/pin12e9.log" 2>&1
# the controls and the negative arm
ES_WALL_CAP_S=25 ES_PROBE_EVERY_GS=1000 "$BIN_TARGET" 30000 coast 15 100 5 > "$HERE/logs/ctrl-5ms.log" 2>&1
ES_WALL_CAP_S=35 ES_PROBE_EVERY_GS=1000 "$BIN_TARGET" 30000 burn 25 100 > "$HERE/logs/ctrl-burn.log" 2>&1
ES_WALL_CAP_S=30 ES_PROBE_EVERY_GS=2000 ES_PIN_OLDEST=67108864 "$BIN_TARGET" 30000 coast 25 800 > "$HERE/logs/pin67M.log" 2>&1

python3 "$HERE/analyze.py"
echo "--- pin67M (negative control, not in analyze.py's table):"
grep -E "prune:|probe:" "$HERE/logs/pin67M.log" | tail -3
echo "--- wiki page: python3 $HERE/wiki/build_page.py rebuilds it from lab/wiki/nladder.md (the run"
echo "    started from the page WITH its two standing conflicts; the checked-in wiki/nladder.md here"
echo "    is the built resolution — build_page.py is kept for provenance, not needed for the numbers)."
