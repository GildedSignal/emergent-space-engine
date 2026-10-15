#!/bin/sh
# Regenerates every number in the dossier from shipped code + this run's patch
# (work/patch.diff: cfg-gates the macOS footprint call so the example links on Linux).
# Four flights + one parse, ~4 minutes total. Run from the repo root.
set -e
RUN="lab/results/20261015-2041-fermi-99b5"
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || true
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
BIN=$(ls -t /home/glmlab/lab-target-3/release/examples/nladder-* | grep -v '\.d$' | head -1)
mkdir -p "$RUN/work"
# freeze a private binary: sibling runs share lab-target dirs and a rebuild mid-run
# once poisoned a checker's flights (15 October, 0757's checker)
cp "$BIN" "$RUN/work/nladder-frozen"
{
  "$RUN/work/nladder-frozen" 10000 coast 22 900;  echo "=== deep"; \
  "$RUN/work/nladder-frozen" 10000 coast 52 900
} > "$RUN/work/n10000.txt" 2>&1
{
  "$RUN/work/nladder-frozen" 100000 coast 15 3000; echo "=== deep"; \
  "$RUN/work/nladder-frozen" 100000 coast 50 3000
} > "$RUN/work/n100000.txt" 2>&1
python3 "$RUN/compose.py" | tee "$RUN/work/composition.json"
