#!/bin/sh
# Record part 2 (long economics, exactness carried by part 1 and the crate tests):
# the 256-orbit amortization, N=10^4, and fleet 1e-4. Appends to results.jsonl.
T=${1:-/home/glmlab/lab-target-0/release}
for cmd in \
  "belt 1e-6 0.3 4 orb=256 notruth" \
  "belt10k 1e-6 0.3 4 notruth" \
  "fleet 1e-4 0.3 4" \
  ; do
  echo "# $T/skin $cmd" >> results.jsonl
  $T/skin $cmd >> results.jsonl 2>&1
done
echo DONE2
