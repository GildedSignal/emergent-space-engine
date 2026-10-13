#!/bin/sh
# Regen for 20261013-2130-redteam-8398. work/patch.diff (the probe example) is applied
# by the runner before this runs. Regenerates every number in dossier.md in ~6 s
# (plus a one-time release build of crates/space if cold).
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo run -p emergent-space --release --example transit_roundtrip \
  > "$(dirname "$0")/transit.tsv" 2>/dev/null
echo "--- key-identity summary ---"
grep -E "summary|negative" "$(dirname "$0")/transit.tsv"
echo "--- rows keeping the key (expect none) ---"
grep -P "\ttrue\t" "$(dirname "$0")/transit.tsv" || echo "none: 0/112 round trips kept the key"
echo "--- circular row (class loss) ---"
grep -P "^7\t0\t1/4" "$(dirname "$0")/transit.tsv"
echo "--- fixed-point control ---"
grep -A16 "fixed-point" "$(dirname "$0")/transit.tsv"
