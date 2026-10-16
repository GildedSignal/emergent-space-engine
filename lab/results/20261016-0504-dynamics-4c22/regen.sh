#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (the runner applies the
# patch before this runs). ~9 min on 8 vCPU: two example builds + 7 flights + 3 digest runs.
set -u
cd "$(git rev-parse --show-toplevel)"
D=lab/results/20261016-0504-dynamics-4c22
cargo build --release -p emergent-universe --example nladder --example ladder_digest 2>&1 | tail -1
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
LD=${CARGO_TARGET_DIR:-target}/release/examples/ladder_digest
[ -x "$BIN" ] || BIN=/home/glmlab/lab-target-1/release/examples/nladder
[ -x "$LD" ] || LD=/home/glmlab/lab-target-1/release/examples/ladder_digest
{ uptime; free -m | head -2; } > "$D/data/machine.txt"
fly() { local name=$1 env=$2; shift 2; if [ -n "$env" ]; then env $env=1 ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" "$@" > "$D/data/$name.txt" 2>&1; else ES_ROWS=1 ES_ATTRIB=1 ES_TLIMIT=200 timeout 300 "$BIN" "$@" > "$D/data/$name.txt" 2>&1; fi; }
fly base_n1e3_60s  ""          1000 coast 60 100 100000
fly stag_n1e3_60s  ES_LOCAL_STAGGER 1000 coast 60 100 100000
fly phase_n1e3_60s ES_LOCAL_PHASE   1000 coast 60 100 100000
fly base_n0_20s    ""             0 coast 20 100 100000
fly base_n600_20s  ""           600 coast 20 100 100000
fly base_n1e4_20s  ""         10000 coast 20 100 100000
fly phase_n1e4_20s ES_LOCAL_PHASE 10000 coast 20 100 100000
timeout 300 "$LD" coast > "$D/data/digest_off.txt" 2>&1
ES_LOCAL_STAGGER=1 timeout 300 "$LD" coast > "$D/data/digest_stag.txt" 2>&1
ES_LOCAL_PHASE=1  timeout 300 "$LD" coast > "$D/data/digest_phase.txt" 2>&1
python3 "$D/scripts/summarize.py"
echo "--- digests (off must equal the record: N=100 4b822570, N=1000 6895ce06, N=3000 ddd5b1cc)"
for a in off stag phase; do grep " coast " "$D/data/digest_$a.txt" | head -3; done
echo REGEN_DONE
