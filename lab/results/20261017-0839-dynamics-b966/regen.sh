#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261017-0839-dynamics-b966.
# Shipped code + this run's patch (the finframe example). ~4 min on 8 vCPU.
# Scheduling is thread-race-dependent: exact crash/survive counts per arm are draws;
# the regenerable invariants are (a) every chunked run crashes, (b) frames at rate 600
# crashes on most draws, (c) rate 300 and overloaded arms survive.
set -u
cd "$(dirname "$0")/../../.." || exit 1   # repo root
git apply "$(dirname "$0")/work/patch.diff" 2>/dev/null || true   # idempotent if already applied
cargo build -p emergent-allocator --release --offline --example finframe || exit 1
BIN=$(cargo metadata --format-version 1 | jq -r .target_directory)/release/examples/finframe
OUT="$(dirname "$0")/out"; mkdir -p "$OUT"
run() { local name=$1; shift; timeout 120 "$BIN" "$@" > "$OUT/$name.out" 2> "$OUT/$name.err"; local c=$?;
  local msg; msg=$(grep -m1 'would revise its published tick' "$OUT/$name.err" || true);
  echo "$name ($*): exit=$c ${msg:-SURVIVED}"; }
# Positive controls: chunked batch (shipped Regions::advance pattern) — expect crash 3/3.
run c150  drift chunks 120 1800 150
run c75   drift chunks 120 1800 75
run c450  drift chunks 120 1800 450
# Single-call batch control — expect survive.
run b1    drift batch  120 1800
# Decisive arm: frames harness, n=120, rate 600 (the rate the engine just keeps up with).
for r in fA fB fC fD fE; do run $r drift frames 120 6 150 600; done
# Rate sweep: 300 (slack) and 1200 (overload edge).
for r in gA gB gC; do run $r drift frames 120 5 150 300;  done
for r in hA hB hC; do run $r drift frames 120 4 150 1200; done
# Overload arm: n=240 at rate 600 (engine falls behind present) — expect survive + accel drops.
for r in nA nB nC; do run $r drift frames 240 6 150 600; done
# Negative control: quiet islands, both sizes — expect survive.
for r in qA qB qC; do run $r quiet frames 120 4; done
run qD quiet frames 40 2
echo "--- verdict lines (grep summary) ---"
grep -h "would revise its published tick" "$OUT"/*.err | sort | uniq -c | sort -rn | head -20
