#!/usr/bin/env bash
# Regen: every dossier number, from a fresh Readwise export + the cited constants.
# No tree edits were made for this run (work/patch.diff is absent/empty by design:
# every number composes from shipped artifacts and published page constants).
set -euo pipefail
cd "$(dirname "$0")"

echo "== fetching Readwise export (fresh) =="
python3 - <<'EOF'
import json, urllib.request, os
tok = os.environ["READWISE_TOKEN"]
cur = ""; out = []
while True:
    req = urllib.request.Request("https://readwise.io/api/v2/export/?pageCursor=" + cur,
                                 headers={"Authorization": f"Token {tok}"})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    out.extend(d.get("results", []))
    cur = str(d.get("nextPageCursor") or "")
    if cur in ("", "None"): break
json.dump(out, open("work/readwise.json", "w"))
print(len(out), "books;", sum(len(b.get("highlights", [])) for b in out), "highlights")
EOF

echo "== quote verification (dossier's 5 lessons, 7 fragments) =="
python3 quote_check.py work/readwise.json

echo "== the 10^7 rung composition (dossier table) =="
python3 compose_rung.py | tail -14
echo "== full JSON with every constant's citation =="
python3 compose_rung.py | sed -n '1,80p' | head -5
echo "(full constants+citations in work/compose_out.txt)"
python3 compose_rung.py > work/compose_out.txt
