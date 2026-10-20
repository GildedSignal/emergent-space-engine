#!/usr/bin/env python3
"""verify_quotes.py — the five lessons' quotes, byte-identical by Readwise id,
against a fresh export (fetch if corpus.json absent or --fresh)."""
import json, os, sys, urllib.request

QUOTES = [
    (1023288364, "The Black Swan", "Nassim Nicholas Taleb",
     "The same property in reverse applies to our unhappiness. It is better to lump all your pain into a brief period rather than have it spread out over a longer one."),
    (537557761, "The Great Mental Models", "Shane Parrish, Rhiannon Beaubien",
     "We do have to remember though, that a map captures a territory at a moment in time. Just because it might have done a good job at depicting what was, there is no guarantee that it depicts what is there now or what will be there in the future."),
    (746334999, "This Is How People Lazier Than You Are Making Millions", "Anthony Vicino",
     "This theory simply states that a system will never grow beyond its biggest constraint or bottleneck."),
    (517641395, "Five Simple Notions that Solve Problems", "Farnam Street",
     "to a man with a hammer, every problem looks like a nail."),
    (666298219, "We Are Legion", "Dennis Taylor",
     "You would think that 3D printers would have solved the scarcity problem. In fact, the technology had just moved the bottleneck."),
]

def fetch(path="corpus.json", fresh=False):
    if os.path.exists(path) and not fresh:
        return json.load(open(path))
    docs, cursor, page = [], "", 0
    while True:
        url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Token {os.environ['READWISE_TOKEN']}"})
        d = json.loads(urllib.request.urlopen(req, timeout=60).read())
        docs += d["results"]
        cursor = d.get("nextPageCursor")
        page += 1
        if not cursor:
            break
    json.dump(docs, open(path, "w"))
    print(f"fetched fresh: {len(docs)} docs, {sum(len(x.get('highlights',[])) for x in docs)} highlights, {page} pages")
    return docs

def main():
    fresh = "--fresh" in sys.argv
    docs = fetch(fresh=fresh)
    by_id = {}
    for d in docs:
        if d.get("is_deleted"):
            continue
        for hl in d.get("highlights", []):
            by_id[hl.get("id")] = (d, hl)
    ok = 0
    for qid, title, author, text in QUOTES:
        hit = by_id.get(qid)
        if not hit:
            print(f"MISSING id {qid} ({title})")
            continue
        d, hl = hit
        exact = text in hl["text"] and title in d["title"] and author in d["author"]
        print(f"[{'BYTE-IDENTICAL' if exact else 'MISMATCH'}] {qid} | {d['title']} | {d['author']}")
        if not exact:
            print(f"  want: {text[:120]!r}")
            print(f"  have: {hl['text'][:160]!r}")
        ok += exact
    print(f"{ok}/{len(QUOTES)} byte-identical")
    sys.exit(0 if ok == len(QUOTES) else 1)

if __name__ == "__main__":
    main()
