#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff:
#   1. applies the probe patch (Update.kick + Universe.kick_log + example kick_tail),
#      and proves it digest-neutral (frame_digest's reverse-L15 flight, base vs patched);
#   2. runs the four shipped scenes (scenario::plane) and analyzes the per-body kick
#      distribution (rule 2's falsifier);
#   3. reruns the store baseline rows the claim builds on (shipmem ladder/measure).
# Run from anywhere; the repo root is three levels above this script. ~3 min warm.
set -euo pipefail
ID=20261013-2252-second-20261013-2130-library-ae3d-7497
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"

echo "== probe neutrality: is the patch already applied?"
if ! grep -q "pub kick_log" crates/universe/src/universe.rs; then
    git apply "$HERE/work/patch.diff"
    APPLIED=1
else
    APPLIED=0
fi
trap '[ "${APPLIED:-0}" = 1 ] && git apply -R "$HERE/work/patch.diff" || true' EXIT

echo "== build"
cargo build -p emergent-universe --release --example kick_tail --example frame_digest
cargo build -p emergent-shipmem --release --example ladder --example measure
T="$(cargo metadata --no-deps --format-version 1 | python3 -c 'import json,sys;print(json.load(sys.stdin)["target_directory"])')/release/examples"

echo "== digest neutrality of the probe (the strongest check: a burn flight, base vs patched)"
"$T/frame_digest" 8 L15 2>&1 | grep "reverse L15" | cut -d'|' -f1-4 | sed -E 's/ *\[[0-9.]+ s\] *$//' > "$HERE/probe/neutral-patched.txt"
git stash -q
cargo build -p emergent-universe --release --example frame_digest 2>&1 | grep -E "^error" || true
"$T/frame_digest" 8 L15 2>&1 | grep "reverse L15" | cut -d'|' -f1-4 | sed -E 's/ *\[[0-9.]+ s\] *$//' > "$HERE/probe/neutral-base.txt"
git stash pop -q
cargo build -p emergent-universe --release --example frame_digest --example kick_tail
if diff "$HERE/probe/neutral-base.txt" "$HERE/probe/neutral-patched.txt" > /dev/null; then
    echo "DIGEST IDENTICAL: $(cat "$HERE/probe/neutral-patched.txt")"
else
    echo "PROBE IS NOT DIGEST-NEUTRAL"; exit 1
fi

echo "== the four scenes (rule 2's falsifier)"
mkdir -p "$HERE/probe"
"$T/kick_tail" idle 40000 1 48    > "$HERE/probe/idle-s1-m48.jsonl"
"$T/kick_tail" idle 40000 7 48    > "$HERE/probe/idle-s7-m48.jsonl"
"$T/kick_tail" burn 1000 1 48 1 12 1 > "$HERE/probe/burn-s1-m48.jsonl"
"$T/kick_tail" idle 3600 1 4000   > "$HERE/probe/idle-s1-m4000.jsonl"
python3 "$HERE/analyze.py" "$HERE"/probe/idle-s1-m48.jsonl "$HERE"/probe/idle-s7-m48.jsonl \
    "$HERE"/probe/burn-s1-m48.jsonl "$HERE"/probe/idle-s1-m4000.jsonl

echo "== store baseline (shipmem: the run this one completes)"
mkdir -p "$HERE/probe-store"
"$T/ladder" 1e-3 64 20000 20000 "$HERE/probe-store/row-n2e4.jsonl" > /dev/null 2>&1
"$T/ladder" 1e-3 64 200000 20000 "$HERE/probe-store/row-n2e5.jsonl" > /dev/null 2>&1
"$T/ladder" 1e-4 64 20000 20000 "$HERE/probe-store/row-trickle.jsonl" > /dev/null 2>&1
"$T/ladder" 3e-1 64 20000 20000 "$HERE/probe-store/row-storm.jsonl" > /dev/null 2>&1
"$T/measure" convoy 1000000 20000 128 "$HERE/probe-store/spikes-convoy.jsonl" > /dev/null 2>&1
python3 - "$HERE" <<'EOF'
import json, sys, glob, os
here = sys.argv[1]
for f in sorted(glob.glob(f"{here}/probe-store/row-*.jsonl")):
    d = json.loads(open(f).read().strip().splitlines()[-1])
    print(os.path.basename(f), {k: d[k] for k in ("n", "b_update_ns", "b_bits", "inferred", "mismatches")})
d = json.loads(open(f"{here}/probe-store/spikes-convoy.jsonl").read().strip().splitlines()[-1])
print("spikes-convoy.jsonl", {k: d[k] for k in ("n", "hot_ns_p50", "hot_ns_p99", "hot_ns_max", "compact_max_step_ns", "repacks")})
EOF
echo "== done"
