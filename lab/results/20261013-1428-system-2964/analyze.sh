#!/bin/bash
# The readout staleness envelope: the largest burn-owed dv a reader sees between canonical
# flushes, per flight and arm, from the probe's readout grids (max over the grid of |dv|).
# Usage: analyze.sh <dir with burn_cadence_*.tsv>
cd "$1" || exit 1
for f in burn_cadence_*.tsv; do
  arm=${f#burn_cadence_}; arm=${arm%.tsv}
  echo "== $arm: max owed |dv| per flight (c)"
  awk -F'\t' 'NR>1 {d=sqrt($7*$7+$8*$8); if(d>m[$1]) m[$1]=d; n[$1]++} END {for (k in m) printf "  %-18s %.3e c (%d rows)\n", k, m[k], n[k]}' "$f" | sort
done
