#!/usr/bin/env bash
# Regen 20261020-0440-library-3c03: pin the stride-gate survivor's mechanism (the regroup
# mint), price the mint-block arm, and verify the five quotes. ~4 minutes.
# INCIDENCE IS A WALL-CLOCK RACE, LOAD-COUPLED (bf83/bc0f/da23): the fire chase repeats
# arm 1 until it fires; if the box is quiet it may need more tries than budgeted — the
# state law (PRE/FIREWHY/RB) regenerates from any single fire, the incidence table from
# the interleaved rounds only.
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
cd "$R/../../.."
git apply "$R/work/patch.diff" 2>/dev/null || echo "(patch already applied — skipped)"
cargo build --release --offline -p emergent-allocator --example exposure 2>&1 | tail -1
cargo test --release --offline -p emergent-allocator 2>&1 | grep -E "test result" | sort | uniq -c
EX=${CARGO_TARGET_DIR:-target}/release/examples/exposure
cd "$R" && rm -rf regen && mkdir regen && cd regen
PROTO="battle 19 2400 32 8192 0.5 24 8704 4.5"
# 1. Fire chase on arm 1 (da23's gate v2), instrumented: the pin.
for i in $(seq 1 8); do
  ES_FIRE_WHY=1 timeout 90 $EX $PROTO 1 > chase.$i.out 2> chase.$i.err && continue
  [ $? -eq 101 ] || continue
  echo "== arm1 chase try$i FIRED; the pin:"; break
done
grep -h -m1 "PRE id=.*D=Some((32, 44, 944))\|PRE id=.*D=Some((32" chase.*.err || true
grep -h -m2 "FIRE id=" chase.*.err || echo "(no fire this window — see header note)"
grep -h -m3 "FIREWHY id=" chase.*.err || true
grep -h -m2 "RB lid=.*m=3[12]" chase.*.err || true
echo "DECIDED lines on battle, arm1 (expect 0): $(cat chase.*.err | grep -c DECIDED)"
# 2. Interleaved paired rounds: the incidence table (arms 1/2/3, same window).
for i in 1 2 3; do for a in 1 2 3; do
  ES_FIRE_WHY=1 timeout 90 $EX $PROTO $a > ix.$i.a$a.out 2> ix.$i.a$a.err || echo "ix round$i arm$a exit=$? (101 = fire)"
done; done
for a in 1 2 3; do
  echo "arm$a: fires $(cat ix.*.a$a.err | grep -c 'FIRE id')/3 | DEFER $(cat ix.*.a$a.err | grep -c DEFER) | $(grep -h 'done battle' ix.*.a$a.err | grep -o 'present [0-9]*' | sort | uniq -c | tr -d '\n' | sed 's/  */ /g')"
done
grep -h "done battle" ix.1.a3.err | cut -c1-165
# 3. The churn class (P5): gates inert, no starvation.
for a in 0 1 3; do ES_FIRE_WHY=1 timeout 90 $EX gas 11 600 1 8192 2.0 12 4352 4.5 $a > gas.a$a.out 2> gas.a$a.err; done
grep -h "done gas" gas.a*.err | cut -c1-150
# 4. The quotes (fresh fetch when the token is set, kept copy otherwise).
cd "$R" && python3 fetch_readwise.py && python3 work/check_quotes.py
uptime
