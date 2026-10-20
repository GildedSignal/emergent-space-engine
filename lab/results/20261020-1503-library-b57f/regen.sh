#!/usr/bin/env sh
# Regen: every dossier number, from the Readwise export, the scripts and the
# shipped tree. Run from anywhere; ~15 s cached export, +~11 s fresh fetch.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$HERE/work"
cd "$HERE/../../.."   # repo root (the tree the run ran in)

# The run's tree patch (empty: read-only run). Apply if present and non-empty.
if [ -s "$WORK/patch.diff" ]; then git apply "$WORK/patch.diff"; echo "patch applied"; else echo "patch empty (read-only run)"; fi

# Fresh export if the token is set; else reuse the cached readwise.json.
if [ -n "$READWISE_TOKEN" ] && command -v python3 >/dev/null; then
  python3 - "$WORK/readwise.json" <<'EOF'
import json, os, sys, time, urllib.parse, urllib.request
out, cursor = [], None
while True:
    url = 'https://readwise.io/api/v2/export/'
    if cursor is not None:
        url += '?pageCursor=' + urllib.parse.quote(str(cursor))
    req = urllib.request.Request(url, headers={'Authorization': 'Token ' + os.environ['READWISE_TOKEN']})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    out.append(d); cursor = d.get('nextPageCursor')
    if cursor is None: break
    time.sleep(0.4)
json.dump(out, open(sys.argv[1], 'w'))
print('fetched', sum(len(p['results']) for p in out), 'books,',
      sum(len(b.get('highlights', [])) for p in out for b in p['results']), 'highlights')
EOF
else
  echo "READWISE_TOKEN unset or no python3: using cached export"
fi

echo; echo "== quotes =="
python3 "$WORK/verify_quotes.py" "$WORK/readwise.json"
echo; echo "== composition =="
python3 "$WORK/compose.py"
echo; echo "== anchors =="
sh "$WORK/anchors.sh"
echo; echo "REGEN OK"
