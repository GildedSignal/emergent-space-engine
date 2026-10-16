#!/usr/bin/env bash
# Regen: every number in the dossier, from shipped code + work/patch.diff. ~1 min warm build + ~1 min flights.
set -euo pipefail
cd "$(dirname "$0")"
R=$(pwd)

# 1. the patch (Linux footprint + the 600 s cap) onto the shipped tree, then build.
if git -C ../.. apply --check "$R/work/patch.diff" 2>/dev/null; then
    git -C ../.. apply "$R/work/patch.diff"
elif git -C ../.. apply --check --reverse "$R/work/patch.diff" 2>/dev/null; then
    : # already applied (the author's tree)
else
    echo "patch does not apply cleanly" >&2; exit 1
fi
cargo build --release --example nladder --example belt_first -p emergent-universe

# 2. freeze private copies (a sibling run may rebuild the shared target dir mid-flight).
cp "${CARGO_TARGET_DIR:-../../target}/release/examples/nladder" "$R/nladder.bin"
cp "${CARGO_TARGET_DIR:-../../target}/release/examples/belt_first" "$R/belt_first.bin"

# 3. the flights (state recorded before and after).
mkdir -p "$R/raw"
{ date -u; uptime; free -m | head -2; } > "$R/raw/state_start.txt"
for N in 1000 10000 100000; do "$R/nladder.bin" "$N" coast 20 > "$R/raw/short_n${N}.txt"; done
"$R/nladder.bin" 100000 coast 160 100 100000 > "$R/raw/wave_n100000.txt"
"$R/nladder.bin" 10000  coast 160 100 100000 > "$R/raw/wave_n10000.txt"
"$R/belt_first.bin" 100000 > "$R/raw/belt_first_1e5.txt"
"$R/belt_first.bin" 10000  > "$R/raw/belt_first_1e4.txt"
{ date -u; uptime; free -m | head -2; } > "$R/raw/state_end.txt"

rm -f "$R/nladder.bin" "$R/belt_first.bin"
# 4. the assembled 10^9 budget.
python3 "$R/budget.py" > "$R/budget_table.txt"
echo "regen done:"; tail -14 "$R/budget_table.txt"
