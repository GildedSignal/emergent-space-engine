#!/bin/bash
# The second-author battery (b172's checker named the gold experiment: land the depth arms
# in a regenerable battery + the matched-fills control). Usage: fly2.sh <core|depth|bracket|fills>
# Arms: ctl (no seam) / retain (global retention) / cap<S> (FIFO ring at S). Scene knobs:
# ES_LADDER_FORM=<K>, ES_LADDER_FORM_W=<w> (matched-fills spread). Belt arms set neither.
# Files: flights/<scene>_<cut>k_<arm>.txt; table2.py parses them.
set -u
cd "$(dirname "$0")"
BIN=target-private/release/examples/lazy_flight
scene_env() { # $1 = scene name; sets E to its env prefix
  E=()
  case $1 in
    belt)     ;;
    form100)  E=(ES_LADDER_FORM=100) ;;
    k1w360)   E=(ES_LADDER_FORM=1 ES_LADDER_FORM_W=360) ;;
    k100w360) E=(ES_LADDER_FORM=100 ES_LADDER_FORM_W=360) ;;
    *) echo "unknown scene $1" >&2; exit 2 ;;
  esac
}
ctl()    { local S=$1 C=$2; shift 2; timeout 300 env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_MAX -u ES_LADDER_FORM -u ES_LADDER_FORM_W ${E[@]+"${E[@]}"} "$BIN" "$@"; }
retain() { local S=$1 C=$2; shift 2; timeout 300 env -u ES_RETAIN_MAX -u ES_LADDER_FORM -u ES_LADDER_FORM_W ES_LAZY_ENTRY=1 ES_RETAIN=1 ${E[@]+"${E[@]}"} "$BIN" "$@"; }
bound()  { local SZ=$1 S=$2 C=$2; shift 3; timeout 300 env -u ES_LADDER_FORM -u ES_LADDER_FORM_W ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=$SZ ${E[@]+"${E[@]}"} "$BIN" "$@"; }
# call helpers: <scene> <cut> [arm]; arm defaults per loop below
phase=$1
case $phase in
core)   # matched-cut 20k anchors: the falsifier + the belt contrast + both fills anchors
  for scene in belt form100; do
    scene_env $scene
    ctl    $scene 20k 100000 burn 20000 1 > flights/${scene}_20k_ctl.txt 2>&1
    retain $scene 20k 100000 burn 20000 1 > flights/${scene}_20k_retain.txt 2>&1
  done
  scene_env belt;    bound 16384 belt 20k 100000 burn 20000 1 > flights/belt_20k_cap16384.txt 2>&1
  scene_env form100; bound 4096 form100 20k 100000 burn 20000 1 > flights/form100_20k_cap4096.txt 2>&1 ;;
depth)  # 48k (~2 wave periods): the checker's /tmp probes, landed
  scene_env form100
  ctl    form100 48k 100000 burn 48000 1 > flights/form100_48k_ctl.txt 2>&1
  retain form100 48k 100000 burn 48000 1 > flights/form100_48k_retain.txt 2>&1
  bound 4096   form100 48k 100000 burn 48000 1 > flights/form100_48k_cap4096.txt 2>&1
  bound 273200 form100 48k 100000 burn 48000 1 > flights/form100_48k_cap273200.txt 2>&1
  scene_env belt
  ctl    belt 48k 100000 burn 48000 1 > flights/belt_48k_ctl.txt 2>&1
  bound 4096 belt 48k 100000 burn 48000 1 > flights/belt_48k_cap4096.txt 2>&1 ;;
bracket) # 32k (just past one wave period ~27-28k): where does the revival end?
  scene_env form100
  ctl    form100 32k 100000 burn 32000 1 > flights/form100_32k_ctl.txt 2>&1
  bound 4096 form100 32k 100000 burn 32000 1 > flights/form100_32k_cap4096.txt 2>&1 ;;
fills)  # matched-fills control: angular spread w=360 (uniform in angle) at K=1 (one radius)
        # and K=100 (100 thin annuli): belt-like read volume with clumped radius
  for scene in k1w360 k100w360; do
    scene_env $scene
    ctl    $scene 20k 100000 burn 20000 1 > flights/${scene}_20k_ctl.txt 2>&1
    retain $scene 20k 100000 burn 20000 1 > flights/${scene}_20k_retain.txt 2>&1
    bound 4096 $scene 20k 100000 burn 20000 1 > flights/${scene}_20k_cap4096.txt 2>&1
  done ;;
esac
echo "phase $phase done"
