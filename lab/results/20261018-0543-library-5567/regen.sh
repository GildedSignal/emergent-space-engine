#!/usr/bin/env bash
# Regen for 20261018-0543-library-5567: quote verification + the five flights.
# Work/patpatch.diff (the env-gated --members cap) is applied by the runner before this runs;
# the guard below re-applies it if missing. Everything else is shipped code.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"

# 1. The patch, if not already applied.
if ! grep -q ES_MEMBERS_CAP "$ROOT/xtask/src/universe/mod.rs"; then
  (cd "$ROOT" && git apply "$HERE/work/patch.diff")
fi

# 2. Build (respect the environment's CARGO_TARGET_DIR; ~90 s cold).
cargo build --release -p xtask --manifest-path "$ROOT/Cargo.toml" >/dev/null
X="$(cargo metadata --no-deps --format-version 1 --manifest-path "$ROOT/Cargo.toml" | jq -r .target_directory)/release/xtask"

# 3. The flights (each 2-12 s wall on the shared box; timings wobble with load,
#    counts are the instrument). Same arms as the dossier's table.
mkdir -p "$HERE/work/flights"
export ES_MEMBERS_CAP=8192
for arm in "1 48" "1 192" "1 768" "7 48" "7 192"; do
  set -- $arm
  f="$HERE/work/flights/regen_s$1_m$2.json"
  "$X" universe --bench --seed "$1" --members "$2" --seconds 20 --rtf 100 --unpaced --no-record > "$f"
  echo "seed=$1 m=$2"
  jq -c '.engine_cost_by_kind[] | select(.kind=="fleet")' "$f"
  jq -r '.stats' "$f" | head -1
done

# 4. The quotes.
python3 "$HERE/verify_quotes.py"
