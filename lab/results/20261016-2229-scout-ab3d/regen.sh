#!/bin/sh
# Regenerates every number in the dossier from the run's own code (no engine patch: this run
# touched no file outside lab/results/20261016-2229-scout-ab3d). ~15 s.
set -e
cd "$(dirname "$0")"
rustc -O falsifier.rs -o falsifier 2>/dev/null
./falsifier > run.jsonl
rows=$(grep -c . run.jsonl)
echo "rows: $rows (expected 32)"
[ "$rows" -eq 32 ]
bad=$(grep -o '"miss":[0-9]*' run.jsonl | grep -v '"miss":0' | wc -l)
echo "scene rows with misses: $bad (expected 0)"
[ "$bad" -eq 0 ]
echo "costs: $(grep 'cost_c1_ns' run.jsonl)"
echo "rock 1e6: $(grep 'rock-n1e6-seed1' run.jsonl)"
echo "compositions:"; grep 'S_ms_readout4200' run.jsonl
rm -f falsifier
