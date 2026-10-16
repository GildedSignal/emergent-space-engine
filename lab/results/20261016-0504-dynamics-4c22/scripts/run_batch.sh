#!/usr/bin/env bash
# Every number in the dossier, one file per flight (budget-free coast at rtf 100 unless said).
set -u
D=lab/results/20261016-0504-dynamics-4c22/data
BIN=/home/glmlab/lab-target-1/release/examples/nladder
[ -x "$BIN" ] || BIN=target/release/examples/nladder
{ uptime; free -m | head -2; } > "$D/machine.txt"
run() { local name=$1; shift; echo "== $name: $*" >> "$D/machine.txt"; ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" "$@" > "$D/$name.txt" 2>&1; }
run base_n1e3_60s   1000 coast 60 100 100000
run base_n0_20s        0 coast 20 100 100000
run base_n600_20s    600 coast 20 100 100000
run stag_n1e3_20s   1000 coast 20 100 100000   # ES_LOCAL_STAGGER armed below
ES_LOCAL_STAGGER=1 ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" 1000 coast 20 100 100000 > "$D/stag_n1e3_20s.txt" 2>&1
ES_LOCAL_PHASE=1  ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" 1000 coast 20 100 100000 > "$D/phase_n1e3_20s.txt" 2>&1
ES_LOCAL_PHASE=1  ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" 1000 coast 60 100 100000 > "$D/phase_n1e3_60s.txt" 2>&1
ES_LOCAL_STAGGER=1 ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" 1000 coast 60 100 100000 > "$D/stag_n1e3_60s.txt" 2>&1
run base_n1e4_20s   10000 coast 20 100 100000
ES_LOCAL_PHASE=1  ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" 10000 coast 20 100 100000 > "$D/phase_n1e4_20s.txt" 2>&1
# the digest identity control and the arms' deltas (fast subset of ladder_digest's own cases)
LD=/home/glmlab/lab-target-1/release/examples/ladder_digest
cargo build --release -p emergent-universe --example ladder_digest 2>&1 | tail -1
timeout 300 "$LD" > "$D/digest_off.txt" 2>&1
ES_LOCAL_STAGGER=1 timeout 300 "$LD" coast > "$D/digest_stag.txt" 2>&1
ES_LOCAL_PHASE=1  timeout 300 "$LD" coast > "$D/digest_phase.txt" 2>&1
echo BATCH_DONE
