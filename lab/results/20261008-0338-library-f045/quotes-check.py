import json

books = json.loads(open("readwise-export.json").read())
QUOTES = [
    "Delete any part or process you can. You may have to add them back later. In fact, if you do not end up adding back at least 10% of them, then you didn",
    "Step one should be to question the requirements",
    "For the fragile, the cumulative effect of small shocks is smaller than the single effect of an equivalent single large shock.",
    "the benefits are small and visible, and the side effects potentially severe and invisible",
    "I’ve very often made mistakes in my physics by thinking the theory isn’t as good as it really is",
    "The one thing you have to avoid is the risk of ruin.",
]
for sub in QUOTES:
    src = "NOT FOUND"
    for b in books:
        for h in b.get("highlights", []):
            t = h.get("text") or ""
            if sub in t or sub.replace("\u2019", "'") in t.replace("\u2019", "'"):
                src = f"{b.get('author')} — {b.get('title')}"
                break
        if src != "NOT FOUND":
            break
    print(("VERBATIM " if src != "NOT FOUND" else "MISSING  "), src[:75])
