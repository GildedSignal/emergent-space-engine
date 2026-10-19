#!/usr/bin/env bash
# Regen: every dossier number, from a clean tree, ≤ 15 min.
# Applies work/patch.diff (1b3f's engine rule + probes verbatim, plus this run's disclosed
# additions: `held=` and `hwm_mb=` in the probe line and the LADDER_RSS_MB guard), builds the
# nladder example, flies the five arms sequentially, and prints the summaries the dossier cites.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261019-1452-taleb-527a
LOGS=$RUN/work/logs
mkdir -p "$LOGS"
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || echo "patch already applied"
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
# The five arms of the dossier, in order (guard 1600 MB keeps every process < 2 GB):
# 1. OFF burn K=3e4, 60k gs  — the ratchet + channel attribution (P1/P2)
env -u ES_READER_OLDEST ES_PROBE_EVERY_GS=500 ES_WALL_CAP_S=300 LADDER_RSS_MB=1600 "$BIN" 30000 burn 600 100 12 > "$LOGS/off-burn-k3e4.log" 2>&1 || true
# 2. ON burn K=3e4, 60k gs   — same arm under ES_READER_OLDEST=1 (P1/P2)
ES_READER_OLDEST=1 ES_PROBE_EVERY_GS=500 ES_WALL_CAP_S=300 LADDER_RSS_MB=1600 "$BIN" 30000 burn 600 100 12 > "$LOGS/on-burn-k3e4.log" 2>&1 || true
# 3. OFF burn K=3e4 to the memory guard (unboundedness; held/bytes at the guard)
env -u ES_READER_OLDEST ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=600 LADDER_RSS_MB=1600 "$BIN" 30000 burn 7200 100 12 > "$LOGS/off-burn-k3e4-guard.log" 2>&1 || true
# 4. OFF coast K=3e4, same horizon (negative control)
env -u ES_READER_OLDEST ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=600 LADDER_RSS_MB=1600 "$BIN" 30000 coast 600 100 12 > "$LOGS/off-coast-k3e4.log" 2>&1 || true
# 5. OFF burn K=1e5, 60k gs — per-scan bytes is K-linear (the fence's ruin arithmetic)
env -u ES_READER_OLDEST ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=600 LADDER_RSS_MB=1600 "$BIN" 100000 burn 600 100 12 > "$LOGS/off-burn-k1e5.log" 2>&1 || true
python3 "$RUN/work/analyze.py" "$LOGS"/off-burn-k3e4.log "$LOGS"/on-burn-k3e4.log "$LOGS"/off-burn-k3e4-guard.log "$LOGS"/off-coast-k3e4.log "$LOGS"/off-burn-k1e5.log
