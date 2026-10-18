#!/usr/bin/env bash
# Regenerates every dossier number from the restored tree + work/patch.diff (the 2403 probe,
# unchanged). Total ≈ 10 min cold build + ~5 min flights; every flight ≤ 60 s.
# Uses ONLY this run's target dir (shared lab-target-* dirs are mutated by other windows —
# a lesson this run paid for: see dossier, "What the author missed").
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261018-1717-second-20261018-1617-taleb-2403-99da
OUT=$R/out
mkdir -p "$OUT"

if ! git apply --whitespace=nowarn "$R/work/patch.diff" 2>/dev/null; then
  # The runner may pre-apply the patch (2403's first regen failure): proceed only if the
  # tree already carries exactly this patch, otherwise stop loudly.
  git apply --check --reverse --whitespace=nowarn "$R/work/patch.diff" \
    || { echo "work/patch.diff applies neither cleanly nor in reverse"; exit 1; }
  echo "work/patch.diff already applied; continuing"
fi
export CARGO_TARGET_DIR=/home/glmlab/lab-target-99da
X=$CARGO_TARGET_DIR/release/xtask
N=$CARGO_TARGET_DIR/release/examples/nladder
cargo build --release -p xtask
cargo build --release -p emergent-universe --example nladder

uptime

# Digest-neutrality control of the print-only probe (same digest on/off).
$X universe --bench --seed 1 --rtf 100 --seconds 5 --level 8 --no-record 2>/dev/null | grep '"digest"' > "$OUT/smoke-off.txt"
ES_MINT=1 $X universe --bench --seed 1 --rtf 100 --seconds 5 --level 8 --no-record 2>"$OUT/mint-smoke.err" | grep '"digest"' > "$OUT/smoke-on.txt"
diff "$OUT/smoke-off.txt" "$OUT/smoke-on.txt"

# Cross-check arm: the 2403 checker2's exact 10^5 coast flight (20 s, 12 ms) — its ladder
# line and MINT count are the published record; this build must reproduce them.
ES_MINT=1 timeout 58 $N 100000 coast 20 100 12 2> "$OUT/mint-lad-n100k-coast20.err" > "$OUT/lad-n100k-coast20.txt"

# The 10^5 anchor pair (same harness as the slice: 15 wall-s, rtf 100, 12 ms).
ES_MINT=1 timeout 58 $N 100000 coast 15 100 12 2> "$OUT/mint-lad-n100k-coast.err" > "$OUT/lad-n100k-coast.txt"
ES_MINT=1 timeout 58 $N 100000 burn  15 100 12 2> "$OUT/mint-lad-n100k-burn.err"  > "$OUT/lad-n100k-burn.txt"
ES_MINT=1 timeout 58 $N 100000 burn  15 100 24 2> "$OUT/mint-lad-n100k-burn-b24.err" > "$OUT/lad-n100k-burn-b24.txt"

# The slice: K = 6.5e5, the largest plane that fits this window's 2 GB process cap
# (b_per_body ~2.35 kB => 10^6 builds at ~2.3 GB; see P5). Budget pair + squeezed corner.
ES_MINT=1 timeout 58 $N 650000 coast 15 100 12 2> "$OUT/mint-lad-k650-coast.err"    > "$OUT/lad-k650-coast.txt"
ES_MINT=1 timeout 58 $N 650000 burn  15 100 12 2> "$OUT/mint-lad-k650-burn.err"     > "$OUT/lad-k650-burn.txt"
ES_MINT=1 timeout 58 $N 650000 burn  15 100 24 2> "$OUT/mint-lad-k650-burn-b24.err" > "$OUT/lad-k650-burn-b24.txt"
ES_MINT=1 timeout 58 $N 650000 burn  15 100 5  2> "$OUT/mint-lad-k650-burn-b5.err"  > "$OUT/lad-k650-burn-b5.txt"

uptime
python3 "$R/analyze2.py"
