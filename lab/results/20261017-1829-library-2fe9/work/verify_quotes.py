import json, os, urllib.request, sys
# The five quotes, chosen BEFORE this script ran (predictions.md P4):
KEYS = {
 "feynman_integrals": "So I got a great reputation for doing integrals, only because my box of tools was different",
 "taleb_provinces": "Mediocristan is where we must endure the tyranny of the collective",
 "feynman_spoil": "made mistakes in my physics by thinking the theory isn",
 "naval_replication": "products with no marginal cost of replication",
 "wal_bottleneck": "the technology had just moved the bottleneck",
}
# 1) locate ids in the cached fetch
cache = json.load(open("readwise_books.json"))
id_map = {}
for bid, b in cache.items():
    for h in b["highlights"]:
        for name, frag in KEYS.items():
            if frag in h["text"] and name not in id_map:
                id_map[name] = {"id": h["id"], "title": b["title"], "author": b["author"], "loc": h["loc"]}
# 2) independent re-fetch, byte-compare by id
tok = os.environ["READWISE_TOKEN"]
cursor = ""; fresh = {}
while True:
    url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    for b in data.get("results", []):
        for h in b.get("highlights", []):
            fresh[h["id"]] = h["text"]
    cursor = data.get("nextPageCursor")
    if not cursor:
        break
ok = 0
for name, meta in id_map.items():
    t_fresh = fresh.get(meta["id"])
    t_cache = None
    for bid, b in cache.items():
        for h in b["highlights"]:
            if h["id"] == meta["id"]:
                t_cache = h["text"]
    byte_ok = (t_fresh is not None and t_fresh == t_cache)
    ok += byte_ok
    print(f"{name}: id={meta['id']} byte-identical(cache==fresh)={byte_ok} [{meta['author']} — {meta['title']} @{meta['loc']}]")
    print(f"   VERBATIM: {t_cache[:260]}")
print(f"{ok}/{len(id_map)} byte-identical")
json.dump(id_map, open("quote_ids.json", "w"), indent=1)
