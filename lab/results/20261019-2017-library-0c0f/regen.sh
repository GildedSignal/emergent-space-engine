#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (the disclosed,
# print-only Linux /proc footprint probe; no engine change). Wall ≈ 3-4 min on 8 vCPU.
# The corpus cache (work/readwise_pages.json) needs READWISE_TOKEN only if refetched:
# refetch is optional and gated below (quotes are verbatim by highlight id in work/highlights.jsonl).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git -C "$HERE" rev-parse --show-toplevel)"
cd "$ROOT"

# 1. the patch (idempotent: skip if already applied)
if ! grep -q 'cfg(target_os = "linux")' crates/universe/examples/nladder.rs; then
  git apply "$HERE/work/patch.diff"
fi

# 2. build (shipped example)
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"

# 3. the two probe arms (sequential; timeout-capped; digits are schedule-elastic on a shared box)
cd "$HERE/work"
timeout 90  "$BIN" 100000 burn 18 2000 12 > arm_1e5.txt 2> arm_1e5.time || true
timeout 120 "$BIN" 200000 burn 12 2000 12 > arm_2e5.txt 2> arm_2e5.time || true
grep "peak footprint" arm_1e5.txt arm_2e5.txt

# 4. every derived number in the dossier
python3 scorecard.py

# 5. (optional, off by default) refetch the Readwise corpus the lessons quote
if [[ "${REGEN_READWISE:-0}" == "1" && -n "${READWISE_TOKEN:-}" ]]; then
  curl -s -H "Authorization: Token $READWISE_TOKEN" "https://readwise.io/api/v2/export/" -o readwise_p0.json
  echo "refetched page 0 only; pagination in the dossier's fetch command"
fi
echo "regen done"
