#!/usr/bin/env bash
# All truth runs for the rung. Each line: belt, orbits override, output.
# (a) 16 regular + 4 adversarial belts at their rung horizons;
# (b) steady belt over 1000 orbits (rate measurement; the process is stationary — the method's
#     own hit rate is flat across a 1000x horizon range — and 1e5 orbits of dense conservative
#     advancement over 543k pairs is ~100x the whole run's budget);
# (c) scaling belts over 100 orbits: full pair set at 1e3 and 1e4, a seeded 1-in-8 pair sample
#     at 1e5 (rate estimate for the oracle's check counts; the sample's stderr is < 1%).
set -u
R="$(cd "$(dirname "$0")" && pwd)"
T=/home/glmlab/lab-target-2/release/rung-truth
cd "$R"
for b in a00 a01 a02 a03 a04 a05 a06 a07 a08 a09 a10 a11 a12 a13 a14 a15 narrow coorbital equalkeys hot; do
  o=$(python3 - "belts.tsv" "$b" <<'EOF'
import sys
for l in open(sys.argv[1]).readlines()[1:]:
    c=l.strip().split('\t')
    if c[0]==sys.argv[2]: print(c[7]); break
EOF
)
  "$T" "$R" "$b" "$o" "$R/truth-$b.bin"
done
"$T" "$R" steady 1000 "$R/truth-steady.bin"
"$T" "$R" scale-n1000 100 "$R/truth-scale-n1000.bin"
"$T" "$R" scale-n10000 100 "$R/truth-scale-n10000.bin"
"$T" "$R" scale-n100000 100 "$R/truth-scale-n100000-sample.bin" sample 8 12345
echo ALL_TRUTH_DONE
