#!/bin/bash
# Regenerates every number in dossier.md: the wave flights on shipped main with work/patch.diff applied
# (the runner applies it first). About 18 min cold: one release build (~1 min) + belt_first + five 200 s flights.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
D="$(cd "$here/../../.." && pwd)"
R="$here/raw"
cargo build --release --manifest-path "$D/Cargo.toml" -p emergent-universe --example nladder --example belt_first || exit 1
B="${CARGO_TARGET_DIR:-$D/target}/release/examples"
$B/belt_first 200000 > "$R/belt_first_200k.txt" 2>&1
fly() { # n flight seed
  env NLADDER_MAX_S=260 NLADDER_TRACE=1 NLADDER_SEED="$3" "$B/nladder" "$1" "$2" 200 100 > "$R/n$(( $1 / 1000 ))k_$2_s$3.txt" 2>&1
}
fly 200000 burn 1
fly 100000 burn 1
fly 200000 coast 1
fly 200000 burn 2
python3 "$here/table.py"
