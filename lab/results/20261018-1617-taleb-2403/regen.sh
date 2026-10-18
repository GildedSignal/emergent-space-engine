#!/usr/bin/env bash
# Regenenerates every dossier number from the restored tree + work/patch.diff.
# Total ≈ 8–10 min cold (build) + ~1 min flights. Each flight ≤ 60 s.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261018-1617-taleb-2403
OUT=$R/out
mkdir -p "$OUT"

if ! git apply --whitespace=nowarn "$R/work/patch.diff" 2>/dev/null; then
  # The runner may pre-apply the patch (that is what failed the first regen): proceed only if
  # the tree already carries exactly this patch, otherwise stop loudly.
  git apply --check --reverse --whitespace=nowarn "$R/work/patch.diff" \
    || { echo "work/patch.diff applies neither cleanly nor in reverse"; exit 1; }
  echo "work/patch.diff already applied; continuing"
fi
T="${CARGO_TARGET_DIR:-target}"
X=$T/release/xtask
N=$T/release/examples/nladder
cargo build --release -p xtask
cargo build --release -p emergent-universe --example nladder

# Digest-neutrality control of the print-only probe (same digest on/off).
$X universe --bench --seed 1 --rtf 100 --seconds 5 --level 8 --no-record 2>/dev/null | grep '"digest"' > "$OUT/smoke-off.txt"
ES_MINT=1 $X universe --bench --seed 1 --rtf 100 --seconds 5 --level 8 --no-record 2>"$OUT/mint-smoke.err" | grep '"digest"' > "$OUT/smoke-on.txt"
diff "$OUT/smoke-off.txt" "$OUT/smoke-on.txt"

# Bench matrix (paced 60 Hz, 5 ms budget, 800 game-s each).
for arm in "b-L0 1 8 0 48" "b-L8 1 8 8 48" "b-L12 1 8 12 48" "b-L8-s2 2 8 8 48" "b-400-L0 1 8 0 400" "b-400-L8 1 8 8 400"; do
  set -- $arm; name=$1; seed=$2; sec=$3; lvl=$4; mem=$5
  ES_MINT=1 timeout 50 $X universe --bench --seed "$seed" --rtf 100 --seconds "$sec" --level "$lvl" --members "$mem" --no-record \
    2> "$OUT/mint-$name.err" > "$OUT/$name.json"
done

# Ladder arms at K = 10^4: coast/burn at the 12 ms default, plus the budget controls.
ES_MINT=1 $N 10000 coast 20        2> "$OUT/mint-n10k-coast.err"     | tee "$OUT/n10k-coast.txt"     >/dev/null
ES_MINT=1 $N 10000 burn  20        2> "$OUT/mint-n10k-burn.err"      | tee "$OUT/n10k-burn.txt"      >/dev/null
ES_MINT=1 $N 10000 burn  20 100 24 2> "$OUT/mint-n10k-burn-b24.err"  | tee "$OUT/n10k-burn-b24.txt"  >/dev/null
ES_MINT=1 $N 10000 coast 20 100 5  2> "$OUT/mint-n10k-coast-b5.err"  | tee "$OUT/n10k-coast-b5.txt"  >/dev/null

python3 "$R/analyze.py"
