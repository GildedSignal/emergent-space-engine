import json, os, time, urllib.parse, urllib.request
tok = os.environ["READWISE_TOKEN"]
cur = ""
results = []
pages = 0
while True:
    url = "https://readwise.io/api/v2/export/?pageCursor=" + urllib.parse.quote(str(cur))
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read())
            break
        except Exception:
            if attempt == 4: raise
            time.sleep(3 * (attempt + 1))
    results.extend(d.get("results", []))
    pages += 1
    cur = d.get("nextPageCursor")
    print(f"page {pages}: next={cur!r} items={len(d.get('results', []))}", flush=True)
    if not cur:
        break
with open("readwise_export.json", "w") as f:
    json.dump(results, f)
bk = [r for r in results if not r.get("is_deleted")]
hl = sum(len(b.get("highlights", [])) for b in bk)
with open("readwise_export.json", "w") as f:
    json.dump(results, f)
print(f"DONE pages={pages} books={len(bk)} highlights={hl}")
