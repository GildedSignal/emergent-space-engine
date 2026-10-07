#!/usr/bin/env bash
# Reproduces the whole record from shipped code (no numbers that the code cannot regenerate).
# ~60 s on the lab's Linux x86 runner; every step prints what the dossier quotes.
set -euo pipefail
cd "$(dirname "$0")"
R=$(cd ../../../../.. && pwd)

echo "== 1. the shipped gate's own verdicts (the anchors) =="
XT="${CARGO_TARGET_DIR:-$R/target}/release/xtask"
if [ ! -x "$XT" ]; then ( cd "$R" && cargo build -p xtask --release -j 6 ); fi
for law in echo planted-bounded planted-compound planted-drift plane; do
  "$XT" behave --law "$law" --gates B12 2>/dev/null | grep -E "^B12|^behave" || true
done

echo
echo "== 2. dump the real series (the gate's own code, verbatim copies; regenerates step 1's numbers) =="
( cd b12dump && CARGO_TARGET_DIR=./target cargo build --release -j 6 >/dev/null && ./target/release/b12dump series )

echo
echo "== 3. the frozen-triple classification matrix + adversarials (predictions.md was written first) =="
python3 b12_matrix.py | tee matrix-out.txt
