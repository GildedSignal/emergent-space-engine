import json, re, sys
books = json.load(open('readwise-books.json'))
hl = [json.loads(l) for l in open('readwise-highlights.jsonl')]
pat = re.compile(sys.argv[1], re.I)
for h in hl:
    if pat.search(h['t']):
        b = books[str(h["b"])]
        print(f"[{b['author']} — {b['title'][:45]}]")
        print(f"  {h['t'][:600]}")
        print()
