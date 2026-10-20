#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# ~2-3 min on a quiet 8-vCPU box (build ~1 min warm, runs ~70 s total). Never edits main's history:
# the patch is applied to the working tree only (run.sh's harness restores it).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"
if git apply --check --reverse "$HERE/work/patch.diff" 2>/dev/null; then
  echo "work/patch.diff already applied (harness pre-applies it); skipping git apply"
elif git apply --check "$HERE/work/patch.diff" 2>/dev/null; then
  git apply "$HERE/work/patch.diff"
else
  echo "work/patch.diff neither applies nor is already applied to this tree" >&2
  exit 1
fi
cargo build --release -p emergent-universe --example nladder
cargo build --release -p xtask
T="${CARGO_TARGET_DIR:-target}/release"
OUT="$HERE"
run_belt () {  # $1 = N, $2 = tag
  ES_SCAFFOLD_AUDIT=1 timeout 90 "$T/examples/nladder" "$1" coast 60 1800 > "$OUT/belt$2-audit.txt" 2>&1
  timeout 90 "$T/examples/nladder" "$1" coast 20 1800 > "$OUT/belt$2-off.txt" 2>&1
  ES_SCAFFOLD_AUDIT=1 timeout 90 "$T/examples/nladder" "$1" coast 20 1800 > "$OUT/belt$2-on.txt" 2>&1
}
run_belt 30000 30000
run_belt 10000 10000
ES_SCAFFOLD_AUDIT=1 timeout 90 "$T/xtask" universe --kick-bench --seed 1 --rtf 100 --seconds 30 > "$OUT/bench-seed1-audit.txt" 2>&1
timeout 90 "$T/xtask" universe --kick-bench --seed 1 --rtf 100 --seconds 30 > "$OUT/bench-seed1-off.txt" 2>&1
echo "== identity (P6): digests audit vs off =="
grep -E '"digest"|"replay_digest"' "$OUT/bench-seed1-audit.txt" "$OUT/bench-seed1-off.txt"
echo "== nladder counters audit vs off (must match: kicks/events/refusals/dead) =="
grep "^ladder:" "$OUT"/belt10000-off.txt "$OUT"/belt10000-on.txt | sed 's/.*kicks_per_body_gs/kicks_per_body_gs/'
echo "== the bill (dossier table) =="
grep -A14 "scaffold audit" "$OUT"/belt30000-audit.txt "$OUT"/belt10000-audit.txt "$OUT"/bench-seed1-audit.txt
