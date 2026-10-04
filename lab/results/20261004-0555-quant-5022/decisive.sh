#!/bin/bash
# Held-out decisive sweep. References at 1024; control kdk-64; ladder kdk 32/16/8/4/2; y4 8/4/2.
cd "$(dirname "$0")"
declare -A S=( [H1]="0.62 0.30 1e-3 2.5" [H2]="0.48 0.10 3e-4 1.0" [H3]="1.95 0.20 3e-3 0.3"
               [H4]="0.80 0.10 1e-3 1.7" [H5]="0.55 0.60 1e-3 1.0" [B1]="0.6299 0.02 1e-3 1.0" )
for k in H1 H2 H3 H4 H5 B1; do
  ./cadence ${S[$k]} kdk 1024 | sed "s/^{/\"seed\":\"$k\",{/"
  for c in 64 32 16 8 4 2; do ./cadence ${S[$k]} kdk $c 2>/dev/null | sed "s/^{/\"seed\":\"$k\",{/" || echo "{\"seed\":\"$k\",\"kdk\":$c,\"crash\":1}"; done
  for c in 8 4 2; do ./cadence ${S[$k]} y4 $c 2>/dev/null | sed "s/^{/\"seed\":\"$k\",{/" || echo "{\"seed\":\"$k\",\"y4\":$c,\"crash\":1}"; done
done
