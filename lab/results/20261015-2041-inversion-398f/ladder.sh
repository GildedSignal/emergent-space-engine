#!/bin/sh
# The depth ladder: does the per-body record stack (history segments) saturate or grow
# with play, per class, past the first settle wave (~26-28k game-s)? Arms: ctl (shipped)
# and all (ES_LAZY_ALL). Each flight prints digest + census + history + rss at its cut.
# Usage: ladder.sh <run-folder-abs> <binary-abs>
set -e
R="$1"; B="$2"
mkdir -p "$R/flights"
run() { # name env... -- args...
  name="$1"; shift
  envout=""
  while [ "$1" != "--" ]; do envout="$envout $1"; shift; done; shift
  echo "== $name: $* ($envout)" >&2
  env $envout timeout 900 "$B" "$@" > "$R/flights/$name.txt" 2>&1 || echo "FAIL/TIMEOUT $name" >> "$R/flights/$name.txt"
  grep -hE "^arm|^digest|^kicks|census |^history|^bodies|^reached" "$R/flights/$name.txt"
}
# Belt: 3 settle waves of depth under all, ctl control at the deepest cut.
run belt_all_32k  ES_LAZY_ENTRY=1 ES_LAZY_ALL=1 -- 10000 coast 32000 1 1000
run belt_all_48k  ES_LAZY_ENTRY=1 ES_LAZY_ALL=1 -- 10000 coast 48000 1 1000
run belt_all_96k  ES_LAZY_ENTRY=1 ES_LAZY_ALL=1 -- 10000 coast 96000 1 1000
run belt_ctl_96k  ES_LAZY_ENTRY=0               -- 10000 coast 96000 1 1000
# Stargraze comets: the worst record class, past one and two settles.
run comet_ctl_32k  ES_LAZY_ENTRY=0               -- 100 stargraze 32000 3 1000
run comet_all_32k  ES_LAZY_ENTRY=1 ES_LAZY_ALL=1 -- 100 stargraze 32000 3 1000
run comet_ctl_64k  ES_LAZY_ENTRY=0               -- 100 stargraze 64000 3 1000
run comet_all_64k  ES_LAZY_ENTRY=1 ES_LAZY_ALL=1 -- 100 stargraze 64000 3 1000
echo LADDER DONE
