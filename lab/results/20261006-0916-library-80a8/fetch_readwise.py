import json, os, time, urllib.request

tok = os.environ.get("READWISE_TOKEN", "")
assert tok, "READWISE_TOKEN unset"

def get(url):
    req = urllib.request.Request(url, headers={"Authorization": "Token " + tok})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())

# sanity: what does the first page look like?
d0 = get("https://readwise.io/api/v2/export/")
print("first-page keys:", sorted(d0.keys()), "n_results:", len(d0.get("results", [])), "cursor:", repr(d0.get("nextPageCursor")))

cur = d0.get("nextPageCursor")
out = list(d0.get("results", []))
pages = 1
while cur:
    d = get("https://readwise.io/api/v2/export/?pageCursor=" + urllib.parse.quote(str(cur)))
    out.extend(d.get("results", []))
    pages += 1
    cur = d.get("nextPageCursor")
    time.sleep(0.7)

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "readwise.json"), "w"))
print("pages", pages, "docs", len(out))
