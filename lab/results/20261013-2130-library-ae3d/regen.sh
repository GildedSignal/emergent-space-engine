#!/usr/bin/env bash
# Regenerates every number in dossier.md: the ladder/measure probe rows and the
# verbatim-quote verification against the cached Readwise export.
# Run from anywhere; the repo root is three levels above this script.
set -euo pipefail
ID=20261013-2130-library-ae3d
HERE="$(cd "$(dirname "$0")" && pwd)"          # lab/results/$ID
ROOT="$(cd "$HERE/../../.." && pwd)"           # repo root
cd "$ROOT"

echo "== build (warm cache ~10 s, cold a few minutes)"
cargo build -p emergent-shipmem --release --example ladder --example measure
T="$(cargo metadata --no-deps --format-version 1 | python3 -c 'import json,sys;print(json.load(sys.stdin)["target_directory"])')/release/examples"

echo "== probe rows"
mkdir -p "$HERE/probe"
for args in "1e-3 64 20000 20000 row-n2e4" "1e-3 64 200000 20000 row-n2e5" "1e-4 64 20000 20000 row-trickle" "3e-1 64 20000 20000 row-storm"; do
    set -- $args
    "$T/ladder" "$1" "$2" "$3" "$4" "$HERE/probe/$5.jsonl" > "$HERE/probe/$5.out" 2> "$HERE/probe/$5.err"
done
"$T/measure" convoy 1000000 20000 128 "$HERE/probe/spikes-convoy.jsonl" > "$HERE/probe/spikes-convoy.out" 2> "$HERE/probe/spikes-convoy.err"

python3 - "$HERE" <<'EOF'
import json, sys, glob, os
here = sys.argv[1]
print("row            members   rung   b_update_ns b_compact bits/member inferred mismatches")
for f in sorted(glob.glob(f"{here}/probe/row-*.jsonl")):
    d = json.loads(open(f).read().strip().splitlines()[-1])
    print(f"{os.path.basename(f)[4:-6]:14} {d['n']:>9} {d['rung']:>6} "
          f"{d['b_update_ns']:>11} {d['b_compact_ns_per_update']:>9} "
          f"{d['b_bits']:>10} {str(d['inferred']):>8} {d['mismatches']:>10}")
d = json.loads(open(f"{here}/probe/spikes-convoy.jsonl").read().strip().splitlines()[-1])
print(f"convoy spikes : n={d['n']} hot p50/p99/max={d['hot_ns_p50']}/{d['hot_ns_p99']}/{d['hot_ns_max']} ns "
      f"compact/update={d['compact_ns_per_update']} ns max_step={d['compact_max_step_ns']} ns "
      f"repacks={d['repacks']} roundtrip={d['updates_roundtrip']}")
print("dossier table check: b_update_ns 6/7/6/7, bits/member 12.35/12.33/12.17/48.38, hot 34/1271/9217, max_step 1264859 (orders of magnitude on this runner)")
EOF

echo "== corpus and verbatim quotes"
if [ ! -s "$HERE/readwise/corpus.jsonl" ]; then
    if [ -z "${READWISE_TOKEN:-}" ] && [ ! -d "$HERE/readwise/page-1.json" ] && [ ! -f "$HERE/readwise/page-1.json" ]; then
        echo "no cached corpus and no READWISE_TOKEN; cannot verify quotes" >&2; exit 1
    fi
    if [ ! -f "$HERE/readwise/page-1.json" ]; then
        echo "READWISE_TOKEN unset but corpus missing; expected the cached pages or corpus.jsonl" >&2; exit 1
    fi
    python3 - "$HERE" <<'EOF'
import json, sys, glob
here = sys.argv[1]
rows = []
for f in sorted(glob.glob(f"{here}/readwise/page-*.json")):
    for b in json.load(open(f)).get('results', []):
        for h in b.get('highlights', []):
            rows.append({'book': b.get('title',''), 'author': b.get('author',''),
                         'category': b.get('category',''), 'text': h.get('text','')})
with open(f"{here}/readwise/corpus.jsonl", 'w') as out:
    for r in rows: out.write(json.dumps(r, ensure_ascii=False) + '\n')
EOF
fi
python3 - "$HERE" <<'EOF'
import json, sys
here = sys.argv[1]
texts = [json.loads(l)['text'] for l in open(f"{here}/readwise/corpus.jsonl")]
ok = True
for q in [l.rstrip('\n') for l in open(f"{here}/quotes.txt") if l.strip()]:
    hit = any(q in t for t in texts)
    ok &= hit
    print(('VERBATIM  ' if hit else 'MISSING   ') + q[:70])
print('all quotes verbatim' if ok else 'QUOTE VERIFICATION FAILED')
sys.exit(0 if ok else 1)
EOF
echo "== done"
