#!/usr/bin/env python3
"""Verify the dossier's five quotes verbatim against the cached Readwise export.

If work/readwise_raw.json is missing and READWISE_TOKEN is set, refetch first.
Exit 1 if any quote cannot be found verbatim.
"""
import json, os, sys, urllib.request, urllib.parse, time

RAW = os.path.join(os.path.dirname(__file__), "readwise_raw.json")

if not os.path.exists(RAW):
    tok = os.environ["READWISE_TOKEN"]
    cursor, out = None, []
    while True:
        url = "https://readwise.io/api/v2/export/"
        if cursor:
            url += "?pageCursor=" + urllib.parse.quote(str(cursor))
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Token " + tok}), timeout=60) as r:
            data = json.loads(r.read())
        out.append(data)
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
        time.sleep(0.7)
    json.dump(out, open(RAW, "w"))

books = [b for p in json.load(open(RAW)) for b in p["results"] if not b.get("is_deleted")]

QUOTES = [
    ("Feynman, Surely You're Joking, Mr. Feynman!",
     "They had wasted all their time memorizing stuff like that, when it could be looked up in fifteen minutes."),
    ("Waitzkin, The Art of Learning",
     "Chunking relates to the mind\u2019s ability to assimilate large amounts of information into a cluster that is bound together by certain patterns or principles particular to a given discipline."),
    ("Taleb, Fooled by Randomness",
     "By a law of probability called distribution of the maximum of random variables, the maximum of an average is necessarily less volatile than the average maximum."),
    ("Taleb, Antifragile",
     "Redundancy is ambiguous because it seems like a waste if nothing unusual happens. Except that something unusual happens\u2014usually."),
    ("Kahneman, Thinking, Fast and Slow",
     "The gorilla study illustrates two important facts about our minds: we can be blind to the obvious, and we are also blind to our blindness."),
]

ok = True
for label, q in QUOTES:
    hit = any(q in h.get("text", "") for b in books for h in b.get("highlights", []))
    print(("VERBATIM  " if hit else "MISSING   ") + label + ": " + q[:70] + "...")
    ok &= hit
sys.exit(0 if ok else 1)
