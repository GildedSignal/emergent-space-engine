#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (~40 s).
set -euo pipefail
ID=20261014-0201-library-4df1
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"
P="lab/results/$ID/work/patch.diff"
if git apply --check "$P" 2>/dev/null; then git apply "$P"; else echo "patch already applied or tree changed"; fi
cargo build --release -p emergent-shipmem --example measure
M="$(cargo metadata --format-version 1 --no-deps | jq -r '.target_directory')/release/examples/measure"
O="lab/results/$ID/measure.jsonl"
: > "$O"
for pop in battle convoy stream formation traders; do
  for sl in 0 1; do
    if [ "$sl" = 0 ]; then
      env -u SHIPMEM_SLICE "$M" "$pop" 4e5 1e5 128 "$O" > /dev/null
    else
      SHIPMEM_SLICE="$sl" "$M" "$pop" 4e5 1e5 128 "$O" > /dev/null
    fi
    tail -1 "$O" | jq -c --arg pop "$pop" --argjson sl "$sl" \
      '{pop:$pop,slice:$sl,n,updates:.updates,hot_p99:.hot_ns_p99,compact_per_upd:.compact_ns_per_update,max_step:.compact_max_step_ns,slices:.compact_slices,max_slice:.compact_max_slice_ns,p99_slice:.compact_p99_slice_ns,repacks,roundtrip:.updates_roundtrip}'
  done
done
