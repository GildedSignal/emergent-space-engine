import json, os, urllib.request, sys
tok = os.environ["READWISE_TOKEN"]
cursor = ""
books = {}
hl_count = 0
pages = 0
while True:
    url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    pages += 1
    for b in data.get("results", []):
        bid = b.get("user_book_id")
        books[bid] = {"title": (b.get("title") or "").strip(), "author": (b.get("author") or "").strip(),
                      "category": b.get("category"), "highlights": []}
        for h in b.get("highlights", []):
            t = (h.get("text") or "").strip()
            if t:
                books[bid]["highlights"].append({"id": h.get("id"), "text": t,
                                                 "loc": h.get("location"), "note": (h.get("note") or "").strip()})
                hl_count += 1
    cursor = data.get("nextPageCursor")
    if not cursor:
        break
with open("readwise_books.json", "w") as f:
    json.dump(books, f)
print(json.dumps({"pages": pages, "books": len(books), "highlights": hl_count}))
