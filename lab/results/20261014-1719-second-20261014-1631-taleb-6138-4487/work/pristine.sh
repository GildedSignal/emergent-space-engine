#!/bin/bash
# The pristine control: shipped engine (universe.rs) with only the flight instruments kept.
# The runner has work/patch.diff applied (fix + instruments); this reverts the engine fix and
# the two set_pull_hold hooks, builds into work/target-pristine, then restores the fix.
set -eu
R="$(cd "$(dirname "$0")/.." && pwd)"
D="$(cd "$R/../../.." && pwd)"
cp "$D/crates/universe/src/universe.rs" "$R/work/universe.fixed.rs"
cp "$D/crates/universe/examples/nladder.rs" "$R/work/nladder.fixed.rs"
cp "$D/crates/universe/examples/frame_digest.rs" "$R/work/frame_digest.fixed.rs"
git -C "$D" checkout -- crates/universe/src/universe.rs
# the instruments only: drop the hold hooks the shipped engine does not have
sed -i '/if let Some(hold) = std::env::var("NLADDER_HOLD")/,/^    }$/d' "$D/crates/universe/examples/nladder.rs"
sed -i 's/        p\.u\.set_pull_hold(0);/        let _ = \&p;/' "$D/crates/universe/examples/frame_digest.rs"
CARGO_TARGET_DIR="$R/work/target-pristine" cargo build --release --manifest-path "$D/Cargo.toml" -p emergent-universe --example nladder --example frame_digest --example belt_first
cp "$R/work/universe.fixed.rs" "$D/crates/universe/src/universe.rs"
cp "$R/work/nladder.fixed.rs" "$D/crates/universe/examples/nladder.rs"
cp "$R/work/frame_digest.fixed.rs" "$D/crates/universe/examples/frame_digest.rs"
