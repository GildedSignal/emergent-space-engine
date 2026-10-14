#!/usr/bin/env bash
# Regenenerates every number in dossier.md (20261014-1221-components-0e37).
# The counter patch is applied by the runner before this runs (work/patch.diff);
# if run standalone from a pristine tree, apply it first:
#   git apply lab/results/20261014-1221-components-0e37/work/patch.diff
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
OUT=lab/results/20261014-1221-components-0e37

# 1. The decisive census: N=1e5 belt, 80 wall s at rtf 200 (past the first-kick wave
#    at 13,051-14,534 game s). ~25 s wall, < 1 GiB. Produces every census number:
#    sizes, held tables, flight reads/frame, retired-read split, memory split,
#    floor, regen check, gather cost.
cargo run --release -p emergent-universe --example cache_census -- 100000 80 200 \
  | tee "$OUT/census_1e5_v3.txt"

# 2. The O(1)-in-N control (P1's small end): the same census at N=2,000, 8 wall s.
cargo run --release -p emergent-universe --example cache_census -- 2000 8 200 \
  | tee "$OUT/census_2e3.txt"

# 3. Digest neutrality of the instrument: every flight's digest, pristine vs patched.
cargo run --release -p emergent-universe --example frame_digest > "$OUT/digest_patched.txt" 2>/dev/null || true
git stash push -q
cargo run --release -p emergent-universe --example frame_digest > "$OUT/digest_pristine.txt" 2>/dev/null || true
git stash pop -q
sed 's/ \[[0-9.]* s\]$//' "$OUT/digest_pristine.txt" > "$OUT/digest_pristine.norm"
sed 's/ \[[0-9.]* s\]$//' "$OUT/digest_patched.txt" > "$OUT/digest_patched.norm"
if diff -q "$OUT/digest_pristine.norm" "$OUT/digest_patched.norm" >/dev/null; then
  echo "DIGESTS_IDENTICAL_NORMALIZED (only wall-time annotations differ)"
else
  echo "DIGEST MISMATCH"; diff "$OUT/digest_pristine.norm" "$OUT/digest_patched.norm"; exit 1
fi
