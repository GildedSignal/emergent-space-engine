#!/usr/bin/env bash
# Regen for 20261020-0036-components-6b9a. The runner applies work/patch.diff (the
# sched_census getter + the two examples) before this runs. ~2 min on 8 cores.
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== sizes, exact calendar bytes, heap-op CPU (shipped Calendar, counting allocator)"
cargo build --release -p emergent-space --example schedbytes -q
BIN=$(find "${CARGO_TARGET_DIR:-target}" -name 'schedbytes-*' -type f ! -name '*.d' | head -1)
"$BIN"

echo "== occupancy census, shipped flight path (plane_extra, frame_to, 12 ms budget)"
cargo build --release -p emergent-universe --example schedcensus -q
CEN=$(find "${CARGO_TARGET_DIR:-target}" -name 'schedcensus-*' -type f ! -name '*.d' | head -1)
"$CEN" 10000 1000 25
"$CEN" 30000 1000 12
echo "load:"; uptime

echo "== composition arithmetic (measured slot bytes x sizing policies)"
python3 - <<'EOF'
slot, pos_row = 28.0, 16.0          # measured: schedbytes
lam, tau = 4.0e-5, 43.6             # cited: 0659 (lambda, dwell)
for n in (10_000, 30_000, 1_000_000, 1_000_000_000):
    cap = (5 * slot + pos_row) * n / 1e9
    live = lam * tau * n
    sized = (5 * slot + pos_row) * live / 1e9
    content = (2 * 1.002 * slot + pos_row) * n / 1e9  # census: two whole-population containers
    print(f"n={n:>11,} body_cap={cap:8.2f} GB  live_content={content:8.2f} GB  "
          f"live_sized(L={live:,.0f})={sized:6.3f} GB  machine_frac(cap@1e9)={cap/8:.1f}x")
print("flip body_cap/live_sized at 1e9: %.0fx" % (((5*slot+pos_row)*1e9)/((5*slot+pos_row)*lam*tau*1e9)))
EOF
echo "== done"
