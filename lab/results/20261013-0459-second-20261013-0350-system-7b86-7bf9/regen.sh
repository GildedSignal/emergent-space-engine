#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus this run's patch
# (work/patch.diff, applied by the runner before this runs).
# Total: ~4 min on the lab's Linux/x86 (build ~2 min cold, runs ~2 min; all deterministic
# except wall-time quantiles, stable to ~2 digits on a quiet box).
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release -p emergent-universe --example slot_ab --example quad_slot
# 1. The decisive A/B: digest identity, instrument deltas, gather cost/share, p99 frame, census.
cargo run --release -p emergent-universe --example slot_ab -- 3
# 2. 7b86's own error probe (unchanged), so its bound regenerates in this record too:
#    e_p99 <= 7.92e-6 root ticks on every scene (the dossier's corrected value), e exactly 0
#    on coast / forward L8 / brake L8 / turn-then-burn L8; clock% ~43; rd/body/f 2.5-3.8;
#    no-stor wobbles by a few counts between machines (the frame budget's wall cut).
cargo run --release -p emergent-universe --example quad_slot -- 8
# 3. The held-out attack (dossier's "at 480 frames"): SLOT_DENSE_FRAMES=480, ~10 min — optional;
#    the dossier quotes it from slot-ab-dense480.txt. Uncomment to regenerate:
# SLOT_DENSE_FRAMES=480 cargo run --release -p emergent-universe --example slot_ab -- 1
echo "Expected (slot_ab): digest 'same' on all 7 scenes; dp99 <= 2.8e-6, dmax <= 4.6e-6 root ticks;"
echo "dshift99 <= 5.6e-12; idset 0 everywhere; gather p50 gain fresh/tube 1.2-1.3x at 48 members;"
echo "part/f ~12-14 (12.0 at 400 members, part% 2.2); frame p99 gain 0.9-1.2x (noise);"
echo "gather share 62-94% fresh, dropping 3-6 points tube-only."
