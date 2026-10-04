#!/bin/bash
# Tuning sweep: seeds T1-T3 only. References: kdk 1024 and y4 8-macro must agree on domdt.
cd "$(dirname "$0")"
for seed in "0.55 0.05 1e-3 1.0" "0.70 0.20 1e-3 1.0" "1.70 0.05 1e-3 1.0"; do
  ./cadence $seed kdk 64; ./cadence $seed kdk 32; ./cadence $seed kdk 16; ./cadence $seed kdk 8; ./cadence $seed kdk 4
  ./cadence $seed y4 8; ./cadence $seed y4 4; ./cadence $seed y4 2
done
./cadence 0.55 0.05 1e-3 1.0 kdk 1024; ./cadence 0.70 0.20 1e-3 1.0 kdk 1024; ./cadence 1.70 0.05 1e-3 1.0 kdk 1024
./cadence 0.55 0.05 1e-3 1.0 y4 8 2>/dev/null
