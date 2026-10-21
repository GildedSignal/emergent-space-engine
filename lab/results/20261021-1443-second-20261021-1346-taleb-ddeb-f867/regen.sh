#!/usr/bin/env bash
# Regenerates every number in dossier.md from a clean tree at the run's base.
# Wall ~6 min on 8 vCPU Linux (cold build ~40 s + ~5 min of flights); peak memory < 200 MB.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # the repo root
git apply --allow-empty "$(dirname "$0")/work/patch.diff" 2>/dev/null || echo "patch already applied"
cargo build --release -p emergent-universe --example zonecad --example beltcensus
B=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples
R="$(dirname "$0")/evidence"
mkdir -p "$R"

# 0. Instrument control: cbe6's belt circles verbatim — must reproduce cbe6's step-4 numbers.
{ echo "=== beltc s4 (cbe6 control) ==="; "$B/zonecad" 4 100 6 beltc; } > "$R/regen-control.txt" 2>&1

# 1. The zone ladder (the decisive arm): steps 8..3, seeds 1/2, 16 ships, 100 planet periods;
#    walk check at the floor (400 P); seed 3; the zone centre (adversarial).
{ for s in 8 7 6 5 4 3; do for seed in 1 2; do echo "=== zone31 s$s seed$seed ==="; "$B/zonecad" $s 100 16 zone31 $seed; done; done
  echo "=== zone31 s4 seed3 ==="; "$B/zonecad" 4 100 16 zone31 3
  echo "=== zone31 s4 400P seed1 ==="; "$B/zonecad" 4 400 16 zone31 1
  echo "=== zone31 s5 400P seed1 ==="; "$B/zonecad" 5 400 16 zone31 1
  for s in 4 3; do for seed in 1 2; do echo "=== zone31c s$s seed$seed ==="; "$B/zonecad" $s 100 12 zone31c $seed; done; done
  echo "=== zone31c s4 400P seed1 ==="; "$B/zonecad" 4 400 12 zone31c 1
} > "$R/zone-ladder.txt" 2>&1

# 2. The bridge arms, the e-tail, the clean eccentric control.
{ for s in 5 4 3; do for seed in 1 2; do echo "=== bridge s$s seed$seed ==="; "$B/zonecad" $s 100 16 bridge $seed; done; done
  for s in 4 3; do for seed in 1 2; do echo "=== bridge2 s$s seed$seed ==="; "$B/zonecad" $s 100 12 bridge2 $seed; done; done
  for s in 4 3; do for seed in 1 2; do echo "=== etail s$s seed$seed ==="; "$B/zonecad" $s 100 12 etail $seed; done; done
  for s in 4 3; do echo "=== clean s$s seed1 ==="; "$B/zonecad" $s 100 16 clean 1; done
  echo "=== bridge s4 400P seed1 ==="; "$B/zonecad" 4 400 16 bridge 1
  echo "=== bridge2 s4 400P seed1 ==="; "$B/zonecad" 4 400 12 bridge2 1
  echo "=== etail s4 400P seed1 ==="; "$B/zonecad" 4 400 12 etail 1
  echo "=== clean s4 400P seed1 ==="; "$B/zonecad" 4 400 16 clean 1
} > "$R/bridge-clean.txt" 2>&1

# 3. The composition: ddeb's census verbatim (defaults must match its record), then the measured floors.
{ echo "### ddeb defaults (reproduces its 115.4/78x record)"
  cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2,3 1.0 shipped 2>/dev/null | grep 'arm='
  echo "### measured floors zone/etail/bridge = 16/16/16 kicks per Giant-period"
  for s in 1 2 3; do cargo run --release -p emergent-universe --example beltcensus -- 1000002 $s 1.0 shipped 16 16 16 2>/dev/null | grep 'arm='; done
  echo "### bracket: zone one octave finer (32)"
  cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 1.0 shipped 32 16 16 2>/dev/null | grep 'arm='
  echo "### the plane's own 2,700"
  for s in 1 2; do cargo run --release -p emergent-universe --example beltcensus -- 3000 $s 1.0 shipped 16 16 16 2>/dev/null | grep 'arm='; done
  echo "### ddeb's width and placement arms still regenerate"
  cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 0.5 shipped 2>/dev/null | grep 'arm='
  cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 4 shipped 2>/dev/null | grep 'arm='
  cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2 1.0 3.0:3.5 2>/dev/null | grep 'arm='
} > "$R/compose.txt" 2>&1

echo "==== verdicts (worst per arm; PASS = worst <= 1e-4, B12's frozen bar) ===="
for f in regen-control zone-ladder bridge-clean; do
  awk -v F="$f" '/^===/{name=$0} /step 2/{ match($0, /worst jacobi \[[^]]*\]/); mj=substr($0, RSTART+15, RLENGTH-15); split(mj, v, "\""); w=0; for(i in v){ if(v[i]+0>w) w=v[i]+0}; printf "%-13s %-26s worst %.1e %s\n", F, name, w, (w<=1e-4 ? "PASS" : "FAIL") }' "$R/$f.txt"
done
grep "arm=" "$R/compose.txt"
