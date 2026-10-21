import gzip, json, os, urllib.request
tok = os.environ["READWISE_TOKEN"].strip()
cursor = ""; books = []
while True:
    url = f"https://readwise.io/api/v2/export/?pageCursor={cursor}" if cursor else "https://readwise.io/api/v2/export/"
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    books.extend(d.get("results", []))
    cursor = d.get("nextPageCursor")
    if not cursor: break
hl = [{"id": h.get("id"), "text": h.get("text"),
       "_book": {"title": b.get("title"), "author": b.get("author")}}
      for b in books for h in (b.get("highlights") or [])]
with gzip.open("readwise_cache.json.gz", "wt") as f:
    json.dump({"highlights": hl}, f)
print(f"{len(hl)} highlights, {len(books)} books -> readwise_cache.json.gz")
