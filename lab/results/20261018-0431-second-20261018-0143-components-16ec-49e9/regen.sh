#!/bin/sh
# Regen (second author, 20261018-0431-…-49e9): rebuilds every number in dossier.md from the
# pristine tree + work/patch.diff (16ec's fast path + this run's harness additions).
# Author originals are a_*; this regen writes r_* (the first checker's lesson: never overwrite
# the author's flights). ~4 minutes: build + probe + 10 flights (5 concurrent pairs).
# The tree is restored even when a comparison step fails (16ec's checker named the silent
# failure modes; flights.sh fails loudly on a flight with no digest line).
set -e
cd "$(dirname "$0")/../../.."
RUN=lab/results/20261018-0431-second-20261018-0143-components-16ec-49e9
restore() { git checkout -- crates/universe/src/step.rs crates/universe/examples/nladder.rs 2>/dev/null || true
  git clean -f crates/universe/examples/bound_probe.rs 2>/dev/null || true; }
trap restore EXIT
# a leftover bound_probe.rs from an interrupted run would make the atomic apply fail silently
git clean -f crates/universe/examples/bound_probe.rs 2>/dev/null || true
git checkout -- crates/universe/src/step.rs crates/universe/examples/nladder.rs 2>/dev/null || true
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff"
cargo build --release -p emergent-universe --example nladder --example bound_probe
BIN=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples

echo "== exactness probe (16ec's, unchanged) =="
"$BIN/bound_probe" | tee "$RUN/work/r_probe.txt"

echo "== flights (N=10^4, 60 s wall, rtf 1800, cut pinned 1.2e10) =="
./"$RUN/work/flights.sh" "$BIN" "$RUN/work" r

echo "== verdicts (author a_* vs regen r_*) =="
D() { sed -n "s/^bound: digest \([0-9a-f]*\) .*/\1/p" "$RUN/work/$1.txt" 2>/dev/null || echo MISSING; }
cmp() { if [ "$(D $1)" = "$(D $2)" ] && [ "$(D $1)" != MISSING ]; then echo "$1 = $2 : IDENTICAL ($(D $1))"; else echo "$1 vs $2 : DIFFER ($(D $1) vs $(D $2))"; fi; }
echo "-- deterministic arms (must be identical ctl vs fast, author vs regen) --"
cmp a_coast_ctl a_coast_fast; cmp r_coast_ctl r_coast_fast; cmp a_coast_ctl r_coast_ctl
cmp a_pin_ctlA a_pin_ctlB; cmp a_pin_ctlA a_pin_fastA; cmp a_pin_fastA a_pin_fastB
cmp r_pin_ctlA r_pin_ctlB; cmp r_pin_ctlA r_pin_fastA; cmp r_pin_fastA r_pin_fastB; cmp a_pin_ctlA r_pin_ctlA
cmp a_strad_ctl a_strad_fast; cmp r_strad_ctl r_strad_fast; cmp a_strad_ctl r_strad_ctl
echo "-- shipped-harness burn (the instrument: equal logged ticks -> equal digests only) --"
{ grep -h "bound: inject" "$RUN"/work/a_shipA.txt "$RUN"/work/a_shipB.txt "$RUN"/work/r_shipA.txt "$RUN"/work/r_shipB.txt || true; }
cmp a_shipA a_shipB; cmp r_shipA r_shipB; cmp a_shipA r_shipA
echo "-- pinned arms' injection line (same scheduled tick, schedules vary) --"
{ grep -h "bound: inject" "$RUN"/work/a_pin_ctlA.txt "$RUN"/work/a_pin_fastA.txt "$RUN"/work/r_pin_ctlA.txt "$RUN"/work/r_pin_fastA.txt || true; }
echo "-- decomposition (flight window, one shipped command) --"
{ grep -h "bound: decomp" "$RUN"/work/a_*.txt "$RUN"/work/r_*.txt || true; }
