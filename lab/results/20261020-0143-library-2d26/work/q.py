import json, re, sys
docs = json.load(open("readwise.json"))
pats = sys.argv[1:]
rx = re.compile("|".join(pats), re.I)
for d in docs:
    for h in d.get("highlights", []):
        t = h.get("text", "")
        if rx.search(t):
            print(f"[{h['id']}] {d.get('title','?')} — {d.get('author','?')}")
            print("   ", t.replace("\n", " ")[:400])
