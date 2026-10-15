#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code plus work/patch.diff
# (the two example benches are the patch). < 15 min; each flight is seconds.
set -u
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261015-1926-quant-c4d3
T="${CARGO_TARGET_DIR:-$HOME/lab-target-1}/release/examples"

echo "== build (uses the applied patch's examples) =="
cargo build --release -p emergent-universe --example belt_compile --example belt_bind || exit 1

echo "== decisive: shipped Orbit::compile at true belt keys =="
"$T/belt_compile" 200000 1 3 > "$R/out/belt_s1.txt" || exit 1
echo "== held-out seeds =="
"$T/belt_compile" 100000 5 3  > "$R/out/belt_s5.txt"  || exit 1
"$T/belt_compile" 100000 42 3 > "$R/out/belt_s42.txt" || exit 1

echo "== shipped promotion path (add_body), N-flatness + held-out seed =="
"$T/belt_bind" 25000 1  > "$R/out/bind_s1_25k.txt"  || exit 1
"$T/belt_bind" 100000 1  > "$R/out/bind_s1.txt"     || exit 1
"$T/belt_bind" 200000 1  > "$R/out/bind_s1_200k.txt" || exit 1
"$T/belt_bind" 100000 5  > "$R/out/bind_s5.txt"     || exit 1

echo "== deterministic content (timings wobble; these must not) =="
for f in belt_s1 belt_s5 belt_s42; do
  grep -E "belt e:|e in \[|REFUSED|p=" "$R/out/$f.txt" | md5sum
done
echo "== headline timings =="
grep -H "belt compile" "$R"/out/belt_s*.txt
grep -H "add_body" "$R"/out/bind_s*.txt
echo "REGEN OK"
