# Reproduction (each <= 60 s):
# 1. Fetch and cache the Readwise export (READWISE_TOKEN must be set):
#    python3 fetch_readwise.py          # writes readwise-export.json, highlights-flat.txt
# 2. Verbatim-check the six quotes against the parsed export:
#    python3 quotes-check.py            # prints VERBATIM + source per quote
# 3. Shock-asymmetry probe (lesson 2's instrument, toy calibration):
#    python3 shock_probe.py             # ~25 s, prints A(tau) table
import json, os, urllib.request

def fetch(out="readwise-export.json"):
    tok = os.environ["READWISE_TOKEN"].strip()
    cursor, books, n = None, [], 0
    while True:
        url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor not in (None, "") else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
        n += 1
        books += d.get("results", [])
        cursor = d.get("nextPageCursor")
        if cursor in (None, "", "null") or n > 40:
            break
    json.dump(books, open(out, "w"))
    flat = []
    for b in books:
        for h in b.get("highlights", []):
            flat.append(f"### {b.get('title')} | {b.get('author')}\n" + (h.get("text") or ""))
    open("highlights-flat.txt", "w").write("\n\n".join(flat))
    return f"pages {n}, books {len(books)}, highlights {len(flat)}"

if __name__ == "__main__":
    print(fetch())
