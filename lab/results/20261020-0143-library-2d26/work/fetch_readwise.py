import json, os, sys, urllib.request
tok = os.environ["READWISE_TOKEN"]
cur = None; docs = []; out = sys.argv[1]
while True:
    url = "https://readwise.io/api/v2/export/" + (("?pageCursor=" + str(cur)) if cur else "" if cur else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    docs.extend(data.get("results", []))
    cur = data.get("nextPageCursor")
    if not cur: break
json.dump(docs, open(out, "w"))
print("docs", len(docs), "highlights", sum(len(d.get("highlights", [])) for d in docs))
