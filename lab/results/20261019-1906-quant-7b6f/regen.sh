#!/bin/sh
# Regenerates every number in the dossier: builds the patched example (work/patch.diff is
# applied by the runner before this runs) and flies the four arms, then runs analyze.py.
# Total wall ~4 min on the lab box (8 vCPU, quiet); each flight is a separate process.
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
while [ "$REPO" != "/" ] && [ ! -f "$REPO/Cargo.toml" ]; do REPO="$(dirname "$REPO")"; done
[ -f "$REPO/Cargo.toml" ] || { echo "no Cargo.toml above $(dirname "$0")" >&2; exit 1; }
cd "$REPO"
OUT=lab/results/20261019-1906-quant-7b6f/logs
mkdir -p "$OUT"
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
# A: 10^5, shipped loop — the wall, decomposed (guard-stops like the record's arms)
LADDER_PROBE=2000 LADDER_RSS_MB=1600 LADDER_CAP_S=300 "$BIN" 100000 burn 600 100 12 > "$OUT/a_1e5_shipped.txt" 2>&1 || true
# B: 10^5 + the TTL fence — the falsifier arm (flights the full 120,000 game-s)
LADDER_PROBE=2000 LADDER_RSS_MB=1600 LADDER_CAP_S=240 ES_SCAN_TTL_S=16 "$BIN" 100000 burn 1200 100 12 > "$OUT/b_1e5_ttl16.txt" 2>&1 || true
# C/D: the flightable rung, fence and shipped, for the channel mix cross-check
LADDER_PROBE=2000 LADDER_RSS_MB=1600 LADDER_CAP_S=200 ES_SCAN_TTL_S=16 "$BIN" 30000 burn 900 100 12 > "$OUT/c_3e4_ttl16.txt" 2>&1 || true
LADDER_PROBE=2000 LADDER_RSS_MB=1600 LADDER_CAP_S=200 "$BIN" 30000 burn 400 100 12 > "$OUT/d_3e4_shipped.txt" 2>&1 || true
python3 lab/results/20261019-1906-quant-7b6f/analyze.py "$OUT"/a_1e5_shipped.txt "$OUT"/b_1e5_ttl16.txt "$OUT"/c_3e4_ttl16.txt "$OUT"/d_3e4_shipped.txt
