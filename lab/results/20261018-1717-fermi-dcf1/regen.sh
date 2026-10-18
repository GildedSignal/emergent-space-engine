#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the
# runner before this runs; idempotent guard below). ~5 min: build + 7 flights + analyze.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261018-1717-fermi-dcf1

# The probe patch (print-only /proc footprint + per-frame probe lines) — apply if missing.
if ! grep -q "probe f=" crates/universe/examples/nladder.rs 2>/dev/null; then
  P=$(find lab -name patch.diff -path "*fermi-dcf1*" 2>/dev/null | head -1)
  [ -n "$P" ] && git apply "$P" || echo "regen: patch.diff not found and probe absent — flights will lack probe lines"
fi
cargo build --release -p emergent-universe --example nladder
B="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
mkdir -p "$R/logs"

fly() { timeout 120 "$B" "$@" > "$R/logs/$(echo "$*" | tr ' /' '__').log" 2>&1 || true; }

fly 10000 coast 6
fly 10000 burn 6
fly 100000 burn 6
fly 300000 coast 6
fly 300000 burn 6
fly 300000 burn 16
fly 300000 burn 6 100 5     # the 5 ms adversarial corner

# The log filenames above differ from the author's (spaces vs underscores); rename to the
# dossier's names so analyze.py's table matches summary.txt.
cd "$R/logs"
[ -f k1e4_coast.log ]   || mv 10000_coast_6.log         k1e4_coast.log
[ -f k1e4_burn.log ]    || mv 10000_burn_6.log          k1e4_burn.log
[ -f k1e5_burn.log ]    || mv 100000_burn_6.log         k1e5_burn.log
[ -f k3e5_coast.log ]   || mv 300000_coast_6.log        k3e5_coast.log
[ -f k3e5_burn.log ]    || mv 300000_burn_6.log         k3e5_burn.log
[ -f k3e5_burn16.log ]  || mv 300000_burn_16.log        k3e5_burn16.log
[ -f k3e5_burn5ms.log ] || mv 300000_burn_6_100_5.log  k3e5_burn5ms.log
cd - >/dev/null

python3 "$R/analyze.py" "$R"/logs/k*.log | tee "$R/summary.txt"
echo "regen: done — compare summary.txt against dossier.md's table"
