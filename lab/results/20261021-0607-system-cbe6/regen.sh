#!/bin/sh
# Regenerates every number in dossier.md from a clean tree.
# ~1-3 min cold build + ~25 s of flights on 8 vCPU Linux.
set -e
cd "$(dirname "$0")/../../.."   # repo root
git apply "$(dirname "$0")/work/patch.diff" 2>/dev/null || echo "patch already applied"
cargo build --release -p emergent-universe --example beltcad
B=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/beltcad
R="$(dirname "$0")/evidence"
mkdir -p "$R"
{
  for s in 6 5 4 3 2; do echo "=== strong s$s ==="; "$B" $s 100 6 strong; done
  for s in 7 5 4 3 2 1; do echo "=== belt s$s seed1 ==="; "$B" $s 100 6 belt; done
  for s in 4 3 2; do echo "=== belt s$s seed2 ==="; SEED=16045690984833335032 "$B" $s 100 6 belt; done
} > "$R/ladder.txt" 2>&1
grep "step 2" "$R/ladder.txt"
echo "---- deaths/refusals in the strong control (s4) ----"
grep -A1 "read refusals" "$R/ladder.txt" | head -0 || true
awk '/=== strong s4 ===/{f=1} f&&/is gone|read refusals/{print} /=== strong s3 ===/{f=0}' "$R/ladder.txt"
