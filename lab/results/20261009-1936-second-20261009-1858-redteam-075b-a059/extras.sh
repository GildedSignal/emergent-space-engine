#!/bin/bash
cd "$(dirname "$0")"
run(){ ./jet_anchor "$@"; }
export -f run
{
for spec in "9.75 300" "8.666666666666666 300" "8.210526315789474 200"; do set -- $spec
  for sd in 1 2; do echo "run $1 0.9 1e-5 0 $2 1e-6 1 $sd 1e-3 32 1 1e-3"; done; done
for spec in "8.666666666666666 100" "8.210526315789474 100"; do set -- $spec
  for tm in 1 2; do echo "run $1 0.9 1e-4 1 $2 1e-6 1 1 1e-3 32 $tm 1e-3"; done; done
echo "run 8.210526315789474 0.9 1e-9 0 2 1e-6 1 1 1e-3 1 2 1e-4"
echo "run 7.368421052631579 0.5 1e-9 0 2 1e-6 1 1 1e-3 1 2 1e-4"
echo "run 7.070707070707071 0.5 1e-9 0 2 1e-6 1 1 1e-3 1 2 1e-5"
echo "run 7.878787878787879 0.9 1e-9 0 2 1e-6 1 1 1e-3 1 2 1e-5"
} | xargs -P 7 -I{} bash -c '{}' > extras.log 2>&1
