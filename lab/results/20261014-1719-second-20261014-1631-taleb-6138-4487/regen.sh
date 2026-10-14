#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (the runner has it
# applied: the fix, the flight instruments, the digest cuts and the deterministic-budget mode).
# About 12 min: two release builds, the wave flights (fixed and pristine control), the frame_digest
# certificate, and the summary table. Every process stays under 2 GB.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
R="$here/raw"
mkdir -p "$R"

# 1. the fixed build (the tree as the runner hands it over)
mkdir -p "$here/work/target-fixed"
CARGO_TARGET_DIR="$here/work/target-fixed" cargo build --release --manifest-path "$(cd "$here/../../.." && pwd)/Cargo.toml" \
  -p emergent-universe --example nladder --example frame_digest --example belt_first || exit 1
F="$here/work/target-fixed/release/examples"

# 2. the pristine control (shipped engine, flight instruments only) — restores the fix after
"$here/work/pristine.sh" || exit 1
P="$here/work/target-pristine/release/examples"

# 3. the certificate: frame_digest, 8 scripted flights x 4 schedules, pristine vs fixed vs forced
"$P/frame_digest" 20 > "$R/fd_pristine.txt" 2>&1
"$F/frame_digest" 20 > "$R/fd_fixed_default.txt" 2>&1
FORCE_HOLD=1 "$F/frame_digest" 20 > "$R/fd_fixed_forced.txt" 2>&1

# 4. the wave flights, wall budget (the frame metrics; cuts for the stable arms)
fly() { # engine n flight seed extra...
  local eng="$1" n="$2" flight="$3" seed="$4"; shift 4
  env NLADDER_MAX_S=260 NLADDER_TRACE=1 NLADDER_SEED="$seed" "$@" \
    "$here/work/target-$eng/release/examples/nladder" "$n" "$flight" 200 100 \
    > "$R/${eng}_n$(( n / 1000 ))k_${flight}_s${seed}.txt" 2>&1
}
CUTS="NLADDER_DIGEST=16000,21000"
fly fixed 200000 burn 1 "$CUTS"
fly fixed 200000 coast 1 "$CUTS"
fly fixed 200000 burn 2
fly fixed 100000 burn 1 "$CUTS"
fly fixed 300000 burn 1 "NLADDER_DIGEST=21000"
fly pristine 200000 burn 1 "$CUTS"
fly pristine 200000 coast 1 "$CUTS"
env NLADDER_MAX_S=120 NLADDER_DIGEST=12000,16000,21000 "$F/nladder" 2000 burn 200 100 > "$R/fixed_n2k_burn_s1.txt" 2>&1
env NLADDER_MAX_S=120 NLADDER_DIGEST=12000,16000,21000 "$P/nladder" 2000 burn 200 100 > "$R/pristine_n2k_burn_s1.txt" 2>&1

# the instrument's own control: the same pristine flight twice differs at these cuts on main
fly pristine 200000 burn 1 "$CUTS" && mv "$R/pristine_n200k_burn_s1.txt" "$R/pristine_n200k_burn_s1_b.txt"
# 5. the deterministic-budget digest comparison (a wall-budgeted belt flight's digest is not
#    schedule-stable even on shipped main at 2x10^5; 25 events a frame is)
for eng in pristine fixed; do
  env NLADDER_MAX_S=400 NLADDER_EBUDGET=25 NLADDER_DIGEST=16000,21000 \
    "$here/work/target-$eng/release/examples/nladder" 200000 burn 200 100 \
    > "$R/${eng}_n200k_burn_s1_eb25.txt" 2>&1
done

# 6. the belt's first-kick wave (unchanged by the fix, kept for the record's completeness)
"$P/belt_first" 200000 > "$R/belt_first_200k.txt" 2>&1 || true

python3 "$here/table.py"
