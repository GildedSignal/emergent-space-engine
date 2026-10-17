#!/bin/bash
# Regenerates every dossier number from shipped code + work/patch.diff (applied first).
# ~3 min: build (incremental) + six flights (3-25 s each) + analysis. Linux only
# (the probe patch replaces the macOS-only proc_pid_rusage footprint with /proc).
set -eu
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."   # repo root

echo "== machine state: $(cat /proc/loadavg) ; $(grep MemAvailable /proc/meminfo)"

echo "== patch"
if ! git diff --quiet -- crates/universe/examples/nladder.rs 2>/dev/null || [ -n "$(git diff --name-only -- crates/universe/examples/nladder.rs 2>/dev/null)" ]; then
  echo "nladder.rs already modified; assuming the probe patch is applied"
else
  git apply "$RUN/work/patch.diff"
fi

echo "== build"
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
ls -la "$BIN"

echo "== flights (A1/A2: 400-member 470f scene quiet/loaded — the VOID arm; B1/B2: ladder 1e5 quiet/7-way loaded; C/C1: K=1000 crowd loaded/quiet)"
"$RUN/run_flights.sh" "$BIN" "$RUN/flights" A1 A2 B1 B2 C C1

echo "== analysis (every number in dossier.md's table)"
python3 "$RUN/analyze.py" "$RUN/flights"
