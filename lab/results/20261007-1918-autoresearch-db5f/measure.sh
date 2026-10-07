#!/bin/bash
# min-of-5 geomean on a pinned core; prints "geomean<TAB>digest"
B=/home/glmlab/lab-target-3/release/bench-compile
cd "$(dirname "$0")/bench" && cargo build --release 2>/dev/null | grep -E "^error" -A3 && exit 1
best=999999999
for i in 1 2 3 4 5; do
  g=$(taskset -c 2 $B --reps 51 2>/dev/null | grep -oP 'geomean_ns_per_compile \K[0-9.]+')
  best=$(python3 -c "print(min($best,$g))")
done
d=$(taskset -c 2 $B --reps 5 2>/dev/null | grep -oP 'digest \K[0-9a-f]+')
echo -e "$best\t$d"
