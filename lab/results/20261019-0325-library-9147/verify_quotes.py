#!/usr/bin/env python3
"""P1: the five dossier quotes reproduce byte-identically in a FRESH Readwise export."""
import json, os, sys, urllib.request, urllib.parse

QUOTES = [  # (book title substring, exact fragment as shipped in lessons.md)
    ("Elon Musk",        "“Step one should be to question the requirements,” he says. “Make them less wrong and dumb, because all requirements are somewhat wrong and dumb. And then delete, delete, delete.”"),
    ("Second-Order Thin","**First-order thinking is fast and easy.** It happens when we look for something that only solves the immediate problem without considering the consequences. For example, you can think of this as I’m hungry so let’s eat a chocolate bar."),
    ("The Art of Learnin","To walk a thorny road, we may cover its every inch with leather or we can make sandals."),
    ("Thinking, Fast and","Intelligence is not only the ability to reason; it is also the ability to find relevant material in memory and to deploy attention when needed."),
    ("Gather and Synthes","In the short term, you are as good as your intensity. In the long term, you are only as good as your consistency."),
]

def fetch(out):
    tok = os.environ.get("READWISE_TOKEN")
    if not tok:
        print("READWISE_TOKEN unset: cannot fetch fresh; using the cached export"); return False
    books, cursor, pages = [], "", 0
    while True:
        url = "https://readwise.io/api/v2/export/" + (("?pageCursor=" + urllib.parse.quote(str(cursor), safe="")) if cursor else "")
        req = urllib.request.Request(url, headers={"Authorization": "Token " + tok})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        books += d.get("results", []); pages += 1
        cursor = d.get("nextPageCursor") or ""
        if not cursor: break
    json.dump(books, open(out, "w"))
    print("fresh export: %d pages, %d books, %d highlights" % (pages, len(books), sum(len(b.get("highlights",[])) for b in books)))
    return True

fresh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work", "readwise_fresh.json")
ok_fetch = fetch(fresh)
books = json.load(open(fresh if ok_fetch else os.path.join(os.path.dirname(os.path.abspath(__file__)), "work", "readwise.json")))
n_ok = 0
for i, (tkey, frag) in enumerate(QUOTES, 1):
    hits = [b for b in books if tkey.lower() in (b.get("title") or "").lower()
            and any(h.get("text") == frag or frag in h.get("text", "") for h in b.get("highlights", []))]
    exact = [b for b in books if tkey.lower() in (b.get("title") or "").lower()
             and any(h.get("text") == frag for h in b.get("highlights", []))]
    status = "BYTE-IDENTICAL" if exact else ("fragment-found" if hits else "MISSING")
    if exact: n_ok += 1
    print("Q%d %-16s %s" % (i, status, (hits[0].get("title") + " | " + (hits[0].get("author") or "")) if hits else tkey))
print("quotes verified: %d/%d %s" % (n_ok, len(QUOTES), "(fresh fetch)" if ok_fetch else "(CACHED - token unset)"))
sys.exit(0 if n_ok == len(QUOTES) else 1)
