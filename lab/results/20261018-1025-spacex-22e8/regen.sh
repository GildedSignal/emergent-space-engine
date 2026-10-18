#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Linux/x86, one process per arm, each arm well under 60 s. Total < 15 min including the build.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
RUN=lab/results/20261018-1025-spacex-22e8
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || echo "patch already applied (or tree dirty); continuing"
cargo build --release -p emergent-universe --example orbitbytes
B=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/orbitbytes
mkdir -p "$RUN/out"
"$B" 10000 coast 20 100 > "$RUN/out/coast10k.log" 2>&1
"$B" 10000 burn 12 100  > "$RUN/out/burn10k.log"  2>&1
"$B" 1000 coast 20 100  > "$RUN/out/coast1k.log"  2>&1
"$B" 100000 coast 10 100 > "$RUN/out/coast100k.log" 2>&1
echo "--- every headline number:"
grep -hE "orbitbytes:|census\[|engine_decoded|anatomy@|flight:|recompile|memory:|shipped" "$RUN"/out/*.log
