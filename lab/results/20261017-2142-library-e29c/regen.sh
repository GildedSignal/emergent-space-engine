#!/bin/sh
# Regenerates every number in the dossier from shipped code constants and the cached
# Readwise export. Fast (seconds). Never touches main, the crates or the docs.
cd "$(dirname "$0")"
if [ ! -f work/page_1.json ]; then
  echo "cache missing; refetching Readwise export"
  mkdir -p work && cd work
  cursor=""; page=1
  while [ "$cursor" != "null" ] && [ $page -le 30 ]; do
    if [ $page -eq 1 ]; then url="https://readwise.io/api/v2/export/"; else url="https://readwise.io/api/v2/export/?pageCursor=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$cursor")"; fi
    curl -s -m 60 -H "Authorization: Token $READWISE_TOKEN" "$url" > page_$page.json
    cursor=$(python3 -c "import json;print(json.load(open('page_$page.json')).get('nextPageCursor') or 'null')")
    page=$((page+1))
  done
  cd ..
fi
python3 bars.py > bars.regen.out && diff bars.out bars.regen.out && echo "bars: identical"
python3 verify_quotes.py
