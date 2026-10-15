#!/bin/bash
# The falsifier battery. Usage: fly.sh <phase>  (10k | 100k | k10)
# Belt arms never set ES_LADDER_FORM; formation arms set it. ctl never sets the seam.
set -u
cd "$(dirname "$0")"
BIN=target-private/release/examples/lazy_flight
ctl()     { timeout 120 env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_MAX ${FORM:+ES_LADDER_FORM=$FORM} "$BIN" "$@"; }
retain()  { timeout 120 env -u ES_RETAIN_MAX ES_LAZY_ENTRY=1 ES_RETAIN=1 ${FORM:+ES_LADDER_FORM=$FORM} "$BIN" "$@"; }
bound()   { local S=$1; shift; timeout 120 env ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=$S ${FORM:+ES_LADDER_FORM=$FORM} "$BIN" "$@"; }
phase=$1
case $phase in
10k)
  FORM= ctl     10000 burn 20000 1 > flights/belt_10000_burn_ctl.txt 2>&1
  FORM= retain  10000 burn 20000 1 > flights/belt_10000_burn_retain.txt 2>&1
  for S in 4096 16384; do FORM= bound $S 10000 burn 20000 1 > flights/belt_${S}_10000_burn.txt 2>&1; done
  FORM=100 ctl     10000 burn 20000 1 > flights/form100_10000_burn_ctl.txt 2>&1
  FORM=100 retain  10000 burn 20000 1 > flights/form100_10000_burn_retain.txt 2>&1
  for S in 4096 16384; do FORM=100 bound $S 10000 burn 20000 1 > flights/form100_${S}_10000_burn.txt 2>&1; done ;;
100k)
  FORM= ctl     100000 burn 20000 1 > flights/belt_100000_burn_ctl.txt 2>&1
  FORM= retain  100000 burn 20000 1 > flights/belt_100000_burn_retain.txt 2>&1
  for S in 16384 65536 131072; do FORM= bound $S 100000 burn 20000 1 > flights/belt_${S}_100000_burn.txt 2>&1; done
  FORM=100 ctl     100000 burn 20000 1 > flights/form100_100000_burn_ctl.txt 2>&1
  FORM=100 retain  100000 burn 20000 1 > flights/form100_100000_burn_retain.txt 2>&1
  for S in 4096 16384 65536; do FORM=100 bound $S 100000 burn 20000 1 > flights/form100_${S}_100000_burn.txt 2>&1; done ;;
k10)
  FORM=10 ctl     100000 burn 20000 1 > flights/form10_100000_burn_ctl.txt 2>&1
  FORM=10 retain  100000 burn 20000 1 > flights/form10_100000_burn_retain.txt 2>&1
  for S in 4096 16384 65536; do FORM=10 bound $S 100000 burn 20000 1 > flights/form10_${S}_100000_burn.txt 2>&1; done ;;
esac
echo "phase $phase done"
