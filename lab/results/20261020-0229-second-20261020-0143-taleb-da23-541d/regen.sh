#!/usr/bin/env bash
# Regen 20261020-0229-second-...-541d: the stride gate's survivor pinned (the frontier
# advance), and the naive close measured. Applies work/patch.diff (the da23 patch + this
# run's env-gated replay instrument + stride_gate v3: under the gate no publish bypasses
# the coalesce), builds, and flies. ~6 min.
# INCIDENCE IS A WALL-CLOCK RACE: fires are load-coupled; the regenerable claims are the
# publish-path counts, the paired-protocol contrast, and back-to-back determinism.
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
cd "$R/../../.."
git apply "$R/work/patch.diff" 2>/dev/null || echo "(patch already applied — skipped)"
cargo build --release --offline -p emergent-allocator --example exposure 2>&1 | tail -1
EX=${CARGO_TARGET_DIR:-target}/release/examples/exposure
cd "$R" && rm -rf regen-draws && mkdir regen-draws

echo "=== 1. the pin: sequential armed replay (the survivor's publisher) ==="
for i in 1 2 3 4; do
  ESE_STRIDE_DBG=1 timeout 90 $EX battle 19 2400 32 8192 0.5 24 8704 4.5 1 > regen-draws/pin$i.out 2> regen-draws/pin$i.err || echo "pin$i exit=$? (101 = fire)"
  if grep -q "SDBG armed" regen-draws/pin$i.err; then
    echo "pin$i armed:"; grep -m1 "SDBG armed" regen-draws/pin$i.err
    echo "  publish paths in the dump: front=$(grep -c 'SF front' regen-draws/pin$i.err || true) shared=$(grep -c 'SF shared' regen-draws/pin$i.err || true) bisect=$(grep -c 'SF bisect' regen-draws/pin$i.err || true)"
    break
  else
    echo "pin$i: no armed pair this draw (race; trying again)"
  fi
done

echo "=== 2. v3 paired protocol (8 seeds, both arms, one build) ==="
for s in 11 19 21 23 25 27 29 31; do
  timeout 90 $EX battle $s 2400 32 8192 0.5 24 8704 4.5 0 > regen-draws/v_s$s.0.out 2> regen-draws/v_s$s.0.err || echo "shipped s$s exit=$? (101 = fire)"
  timeout 90 $EX battle $s 2400 32 8192 0.5 24 8704 4.5 1 > regen-draws/v_s$s.1.out 2> regen-draws/v_s$s.1.err || echo "v3 s$s exit=$? (101 = fire)"
done
echo "fires shipped arm: $(grep -l FIRE regen-draws/v_s*.0.err 2>/dev/null | wc -l) / fires v3 arm: $(grep -l FIRE regen-draws/v_s*.1.err 2>/dev/null | wc -l)"
grep -h FIRE regen-draws/v_s*.0.err 2>/dev/null | cut -c1-90 || true
echo "shipped present: $(grep -h 'done battle' regen-draws/v_s*.0.err | grep -o 'present [0-9]*' | tr '\n' ' ')"
echo "v3     present: $(grep -h 'done battle' regen-draws/v_s*.1.err | grep -o 'present [0-9]*' | tr '\n' ' ')"
echo "v3 equality law (RB lines with m>0, expect 0): $(grep -h 'RB lid' regen-draws/v_s*.1.err 2>/dev/null | grep -vc 'm=-\|m=0 ' || true)"

echo "=== 3. v3 back-to-back determinism (same seed twice) ==="
timeout 90 $EX battle 19 2400 32 8192 0.5 24 8704 4.5 1 2> regen-draws/d1.err >/dev/null || true
timeout 90 $EX battle 19 2400 32 8192 0.5 24 8704 4.5 1 2> regen-draws/d2.err >/dev/null || true
if diff <(grep "done battle" regen-draws/d1.err | cut -c1-120) <(grep "done battle" regen-draws/d2.err | cut -c1-120) > /dev/null; then echo "v3 s19 back-to-back identical"; else echo "v3 s19 differs across back-to-back runs"; fi

echo "=== 4. lib tests with the switch in (default off) ==="
cd "$R/../../.." && cargo test --release --offline -p emergent-allocator 2>&1 | grep -E "test result" | head -4
uptime
