#!/usr/bin/env bash
# Regenerates every number in dossier.md. Total runtime < 2 min (cache present)
# or ~1 min + fetch (cache absent, needs READWISE_TOKEN).
set -euo pipefail
cd "$(dirname "$0")"
RUN=$(pwd)
ROOT=$(cd ../../.. && pwd)
cd "$ROOT"

# work/patch.diff (this run edits no shipped code; applied by the runner if present)
W="$RUN/work"
mkdir -p "$W"

# 1. The corpus: use the cache; refetch only if absent.
if [ ! -s "$W/highlights.ndjson" ]; then
  test -n "${READWISE_TOKEN:-}" || { echo "no cache and no READWISE_TOKEN"; exit 1; }
  cursor=""; : > "$W/highlights.ndjson"
  for i in $(seq 1 40); do
    resp=$(curl -s --max-time 40 -H "Authorization: Token $READWISE_TOKEN" \
      "https://readwise.io/api/v2/export/?pageCursor=$cursor")
    echo "$resp" | python3 -c "
import sys,json
d=json.load(sys.stdin)
out=open('$W/highlights.ndjson','a')
for r in d.get('results',[]):
    for h in r.get('highlights') or []:
        out.write(json.dumps({'t':r.get('title'),'a':r.get('author'),'x':h.get('text')})+'\n')
sys.stderr.write('NEXT:'+str(d.get('nextPageCursor'))+'\n')" 2> "$W/cursor.log"
    nc=$(tail -1 "$W/cursor.log" | sed 's/NEXT://')
    [ "$nc" = "None" ] && break
    cursor=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$nc")
  done
fi

# 2. Every dossier number: the audit (corpus stats, verbatim anchors, kill/add-back
#    ledger, automation-debt sites, lookup budget).
python3 "$W/audit.py"
