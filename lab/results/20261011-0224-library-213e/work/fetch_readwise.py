import json, os, urllib.request, urllib.parse, sys
tok = os.environ["READWISE_TOKEN"]
cursor = ""
pages = []
while True:
    url = "https://readwise.io/api/v2/export/?" + urllib.parse.urlencode({"pageCursor": cursor})
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    pages.append(data)
    nc = data.get("nextPageCursor")
    if isinstance(nc, (bytes, bytearray)):
        nc = nc.decode()
    if not nc:
        break
    cursor = nc
books = [b for p in pages for b in p.get("results", [])]
with open("readwise-cache.jsonl", "w") as f:
    n = 0
    for b in books:
        title, author, cat = b.get("title") or "", b.get("author") or "", b.get("category") or ""
        for h in b.get("highlights", []):
            t = (h.get("text") or "").strip().replace("\n", " ")
            f.write(json.dumps({"t": title, "a": author, "c": cat, "h": t}) + "\n")
            n += 1
print(f"pages={len(pages)} books={len(books)} highlights={n}", file=sys.stderr)
