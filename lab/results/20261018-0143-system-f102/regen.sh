#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped tree + work/patch.diff.
# Linux/x86; the box is shared, so timings move with load — the digests and the
# memo counters' zeros (soundness, both_hit) are load-independent. ~2 min.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # the repo root (the run's tree, patch applied)
B=/home/glmlab/lab-target-2/release/examples/scan_memo
cargo build --release -p emergent-universe --example scan_memo 2>&1 | grep -E '^error' -A5 && exit 1 || true
uptime   # the load record, printed with the numbers
for arm in "1000 burn 2 100" "1000 coast 2 100"; do
  for m in "" "1" "verify"; do
    echo "=== [ES_MEMO_FIRST=${m:-off}] $arm ==="
    ES_MEMO_FIRST=$m timeout 120 "$B" $arm | grep -E 'scene|flight:|engine_ms:|memo_stats'
  done
done
echo "=== HELDOUT [verify] 10000 burn 2 100 ==="
ES_MEMO_FIRST=verify timeout 240 "$B" 10000 burn 2 100 | grep -E 'scene|flight:|memo_stats'
