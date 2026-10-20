#!/usr/bin/env bash
# Regen 20261020-0143-taleb-da23: the stride gate vs the finality fire, on shipped code.
# Applies work/patch.diff (c749's base: e517 instrument + bf83 exposure harness, plus this
# run's Config::stride_gate and the three-part gate in alone_at/final_through), builds, and
# flies the battle fire protocol with both arms from the one build. ~3 minutes.
# INCIDENCE IS A WALL-CLOCK RACE, LOAD-COUPLED: a quiet machine may fire less on the shipped
# arm (bf83: 0/8 quiet-loop). The regenerable claim is the paired comparison on the same
# machine in the same minutes, plus the state law on every fire.
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
cd "$R/../../.."
git apply "$R/work/patch.diff" 2>/dev/null || echo "(patch already applied — skipped)"
cargo build --release --offline -p emergent-allocator --example exposure 2>&1 | tail -1
cargo test --release --offline -p emergent-allocator 2>&1 | tail -3
EX=${CARGO_TARGET_DIR:-target}/release/examples/exposure
cd "$R" && rm -rf draws && mkdir draws
# The fire protocol (bf83/c749): galaxy 8704, 24 fleets, rate 2400, min_region 32, margin 0.5,
# 4.5 s per draw, one process per draw; arm 0 = shipped (gate off), arm 1 = stride gate on.
for s in 11 19 21 23 25 27 29 31; do
  timeout 90 $EX battle $s 2400 32 8192 0.5 24 8704 4.5 0 > draws/g8704_s$s.0.out 2> draws/g8704_s$s.0.err || echo "shipped s$s exit=$? (101 = fire)"
  timeout 90 $EX battle $s 2400 32 8192 0.5 24 8704 4.5 1 > draws/g8704_s$s.1.out 2> draws/g8704_s$s.1.err || echo "gate s$s exit=$? (101 = fire)"
done
# The hottest seed three more times under the gate (incidence is a race, not a seed law).
for i in 1 2 3; do timeout 90 $EX battle 19 2400 32 8192 0.5 24 8704 4.5 1 > draws/s19t$i.1.out 2> draws/s19t$i.1.err || echo "gate s19 try$i exit=$?"; done
echo "=== fires (FIRE lines / exit 101) ==="
grep -c FIRE draws/*.0.err draws/*.1.err | sed 's/:0$//' || true
echo "=== arm summaries ==="
grep -h "done battle" draws/*.0.err | cut -c1-150
grep -h "done battle" draws/*.1.err | cut -c1-150
echo "=== equality law under the gate: every RB m<=0, no FIRE expected ==="
grep -h "RB lid" draws/*.1.err | grep -v "m=-\|m=0 " | head -5 || echo "(all RB lines at m<=0)"
uptime
