import json, re, sys
books = json.load(open("readwise_books.json"))
noise = re.compile(r"episode|podcast|chronicle|moonshot|founders —|george mack|ferriss|beau of the fifth|_thread|twitter|thread", re.I)
ranked = sorted(books.values(), key=lambda b: -len(b["highlights"]))
print("== top books by highlights (non-noise) ==")
n = 0
for b in ranked:
    if noise.search(b["title"]) or b["category"] == "tweets":
        continue
    n += 1
    if n <= 45:
        print(f"{len(b['highlights']):4d}  {b['author'][:28]:28s} {b['title'][:70]}")
print()
q = re.compile(sys.argv[1], re.I)
print(f"== matches for /{sys.argv[1]}/i ==")
for b in books.values():
    for h in b["highlights"]:
        if q.search(h["text"]):
            print(f"--[{b['author'][:30]} — {b['title'][:60]} @{h['loc']}]\n{h['text'][:900]}\n")
