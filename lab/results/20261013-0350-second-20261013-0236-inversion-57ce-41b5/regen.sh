#!/bin/sh
# Regen for 20261013-0350-second-20261013-0236-inversion-57ce-41b5 (the Passage→Cycle
# capture: the checker's named gold experiment for 20261013-0236-inversion-57ce).
# work/patch.diff adds crates/universe/examples/crossing.rs (the parent's A/B modes plus
# modes C/E/F/G/T of this run; applied by the runner before this runs).
# Total wall on the lab's shared x86 runner: ~4 minutes.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release -p emergent-universe --example crossing
B=${CARGO_TARGET_DIR:-target}/release/examples/crossing
OUT=lab/results/20261013-0350-second-20261013-0236-inversion-57ce-41b5/out
mkdir -p "$OUT"

# The capture grid: held forward to the star flip, cut, coast (bcoast), then the scripted
# brake — re-asserted every P = 2^(27−level) ticks (flush quantum alpha*P = 7.6e-6).
for m in C5 C11 C15 C8.23 C8.26 T8; do
  timeout 200 "$B" $m 150000 > "$OUT/$m.txt" 2>&1 || true
  echo "== $m (rc=$?)"
done
# C8 (P = 2^19) twice: determinism of the capture pair below depends on the exact state.
timeout 200 "$B" C8 150000 > "$OUT/C8.txt" 2>&1 || true
echo "== C8 (rc=$?)"

# The held key (ONE assertion, never re-asserted), fine fixed sampling: captures.
for m in E8.0 E8.1 E8.2 E8.3; do
  timeout 200 "$B" $m 120000 > "$OUT/$m.txt" 2>&1 || true
  echo "== $m (rc=$?)"
done
# Fixed-cadence sweep (all capture; the capture tick itself moves with the cadence).
for dt in 19 21 23; do
  HELD_DT_LOG2=$dt timeout 200 "$B" E8.3 120000 > "$OUT/E8.3.dt$dt.txt" 2>&1 || true
  echo "== E8.3 dt=$dt (rc=$?)"
done

# The divergence pair: identical inputs (one reverse assertion at t=399,761,187), only the
# settle-horizon sequence differs. E (fixed 2^20) captures; G (2^20 then x1.25 growth)
# pumps; F (x1.25 ladder) pumps; B8 (the parent's mode, relight +1 tick) pumps to E=4.29.
timeout 200 "$B" G8.3 120000 > "$OUT/G8.3.txt" 2>&1 || true
echo "== G8.3 (rc=$?)"
for m in F8.2 F8.3; do
  timeout 200 "$B" $m 120000 > "$OUT/$m.txt" 2>&1 || true
  echo "== $m (rc=$?)"
done
timeout 260 "$B" B8 40000 > "$OUT/B8repro.txt" 2>&1 || true
echo "== B8 repro (rc=$?)"

echo "--- captures (kind flips to Cycle):"
grep -h "FIXED-NOSE CAPTURE\|T captured\|held: CAPTURED\|grow: CAPTURED\|F CAPTURED" "$OUT"/C*.txt "$OUT"/T8.txt "$OUT"/E8*.txt "$OUT"/G8.3.txt "$OUT"/F8*.txt || true
echo "--- capture brackets and landings:"
grep -h "cap bracket\|capup \|captured apo" "$OUT"/C5.txt "$OUT"/C8.txt "$OUT"/C11.txt "$OUT"/C15.txt "$OUT"/T8.txt || true
echo "--- pumps / silent deaths:"
grep -h "pump\|DEAD\|F stops\|no capture" "$OUT"/G8.3.txt "$OUT"/F8.2.txt "$OUT"/F8.3.txt "$OUT"/B8repro.txt || true
echo "--- capcoast (survival at 2x):"
grep -h "capcoast" "$OUT"/C*.txt "$OUT"/T8.txt || true
echo "--- refusals anywhere (expect none):"
grep -h "refusals=[1-9]" "$OUT"/*.txt || echo "none"
