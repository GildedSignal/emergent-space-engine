#!/bin/bash
# Falsifier driver: runs one (case, arm) pair in its own scratch dir so baseline-found.txt
# never crosses cases. Usage: sweep.sh NAME n sigma_e rho kappa epochs seed slack widen
set -u
B=/home/glmlab/lab-target-1/release/skin-falsifier
ROOT="$(cd "$(dirname "$0")" && pwd)"
NAME="$1"; shift
N="$1"; SIG="$2"; RHO="$3"; KAP="$4"; EPC="$5"; SEED="$6"; SLACK="$7"; WIDEN="$8"
D="$ROOT/scratch/$NAME-s$SLACK-w$WIDEN"
mkdir -p "$D"
cd "$D" || exit 1
rm -f baseline-found.txt
"$B" baseline "$N" "$SIG" "$RHO" "$KAP" "$EPC" "$SEED" 0 0 > baseline.txt 2>/dev/null
"$B" skin "$N" "$SIG" "$RHO" "$KAP" "$EPC" "$SEED" "$SLACK" "$WIDEN" > skin.txt 2>/dev/null
echo "=== $NAME n=$N sig=$SIG rho=$RHO kappa=$KAP epochs=$EPC seed=$SEED slack=$SLACK widen=$WIDEN"
sed 's/  */ /g' baseline.txt skin.txt
