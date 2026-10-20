import json, sys
docs = json.load(open("readwise.json"))
needle = sys.argv[1].lower(); frag = sys.argv[2].lower() if len(sys.argv) > 2 else None
for d in docs:
    if needle not in (d.get("title","") + " " + d.get("author","")).lower(): continue
    for h in d.get("highlights", []):
        t = h["text"].replace("\n", " ")
        if frag is None or frag in t.lower():
            print(f"[{h['id']}] {d.get('title')} — {d.get('author')}")
            print("   ", t[:380])
