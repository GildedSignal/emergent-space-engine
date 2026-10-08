#!/bin/sh
# usage: crates/encounters/run.sh <out.jsonl> <args...>
# Runs one experiment, killed past 60 s (perl alarm), with max RSS and the machine state before/after.
out=$1; shift
bin=target/release/encounters
tmp=${TMPDIR:-/tmp}/enc-time.$$
state() {
  printf '{"exp":"state","when":"%s","utc":"%s","load":"%s","swap":"%s","batt":"%s","therm":"%s"}\n' \
    "$1" "$(date -u +%FT%TZ)" "$(sysctl -n vm.loadavg)" "$(sysctl -n vm.swapusage)" \
    "$(pmset -g batt | tail -1 | tr -s ' \t' ' ')" "$(pmset -g therm | tr '\n' ' ' | tr -s ' ')"
}
state before >> "$out"
/usr/bin/time -l perl -e 'alarm 60; exec @ARGV' "$bin" "$@" >> "$out" 2> "$tmp"; rc=$?
rss=$(grep "maximum resident" "$tmp" | awk '{print $1}')
real=$(grep " real" "$tmp" | awk '{print $1}')
printf '{"exp":"run","args":"%s","rc":%d,"max_rss_bytes":%s,"real_s":%s}\n' "$*" "$rc" "${rss:-0}" "${real:-0}" >> "$out"
state after >> "$out"
rm -f "$tmp"
