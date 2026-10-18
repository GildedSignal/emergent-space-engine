#!/usr/bin/env bash
# Regen 20261018-0932-dynamics-c749: the fire's internal state on the game's fleet battle.
# Applies work/patch.diff (e517's instrument + bf83's exposure harness + this run's
# disclosed extensions: battle args fleets/galaxy/seconds, FIRE bbox print), builds,
# replays the draw protocol, and checks the state law on whatever fires occur.
# INCIDENCE IS A WALL-CLOCK RACE: reruns may fire on different seeds (rep_s11/rep_s19
# did not refire). The regenerable claim is the state law on every fire that occurs;
# the protocol below fires with high probability (3/8 on this class as run).
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
cd "$R/../../.."
git apply "$R/work/patch.diff" 2>/dev/null || echo "(patch already applied — skipped)"
cargo build --release --offline -p emergent-allocator --example exposure 2>&1 | tail -1
EX=${CARGO_TARGET_DIR:-target}/release/examples/exposure
cd "$R" && rm -rf draws && mkdir draws
# Decisive arms: galaxy 8704 / 24 fleets, margin 0.5, rate 2400, min_region 32 (bf83's
# fire protocol; checker2's higher-incidence scene), 8 seeds; the 4352/12 class (6 seeds);
# the shipped-default margin 2.0 negative (2 seeds); 2 replicates of fired seeds.
for s in 11 19 21 23 25 27 29 31; do timeout 90 $EX battle $s 2400 32 8192 0.5 24 8704 > draws/g8704_s$s.out 2> draws/g8704_s$s.err || true; done
for s in 11 12 13 14 15 16;             do timeout 90 $EX battle $s 2400 32 8192 0.5    > draws/g4352_s$s.out 2> draws/g4352_s$s.err || true; done
for s in 11 19;                          do timeout 90 $EX battle $s 2400 32 8192 2.0 24 8704 > draws/neg8704_s$s.out 2> draws/neg8704_s$s.err || true; done
for s in 11 19;                          do timeout 90 $EX battle $s 2400 32 8192 0.5 24 8704 > draws/rep_s$s.out    2> draws/rep_s$s.err    || true; done
python3 analyze.py | tee regen.txt
uptime
