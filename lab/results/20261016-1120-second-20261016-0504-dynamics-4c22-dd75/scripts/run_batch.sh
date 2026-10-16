#!/usr/bin/env bash
# Run 20261016-1120 batch: every number in the dossier, one file per flight (budget-free coast,
# rtf 100, seed 1, one thread), with the DEDUPLICATED ES_ATTRIB instrument.
set -u
R="$(cd "$(dirname "$0")/.." && pwd)"
D=$R/data
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
[ -x "$BIN" ] || BIN=target/release/examples/nladder
[ -x "$BIN" ] || BIN=/home/glmlab/lab-target-1/release/examples/nladder
{ uptime; free -m | head -2; } > "$D/machine.txt"
fly() { local name=$1 env=$2; shift 2; if [ -n "$env" ]; then env $env=1 ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" "$@" > "$D/$name.txt" 2>&1; else ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" "$@" > "$D/$name.txt" 2>&1; fi; }
fly base_n1e3_60s  ""              1000 coast 60 100 100000
fly stag_n1e3_60s  ES_LOCAL_STAGGER 1000 coast 60 100 100000
fly phase_n1e3_60s ES_LOCAL_PHASE   1000 coast 60 100 100000
fly base_n1e3_coast ""             1000 coast 20 100 100000
fly base_n0_20s    ""                 0 coast 20 100 100000
fly base_n600_20s  ""               600 coast 20 100 100000
fly base_n1e4_20s  ""             10000 coast 20 100 100000
fly phase_n1e4_20s ES_LOCAL_PHASE 10000 coast 20 100 100000
LD=${CARGO_TARGET_DIR:-target}/release/examples/ladder_digest
[ -x "$LD" ] || LD=/home/glmlab/lab-target-1/release/examples/ladder_digest
timeout 300 "$LD" coast > "$D/digest_off.txt" 2>&1
ES_LOCAL_STAGGER=1 timeout 300 "$LD" coast > "$D/digest_stag.txt" 2>&1
ES_LOCAL_PHASE=1  timeout 300 "$LD" coast > "$D/digest_phase.txt" 2>&1
echo BATCH_DONE
