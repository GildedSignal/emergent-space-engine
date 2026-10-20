#!/usr/bin/env python3
"""Verify the 5 lesson quotes are byte-identical substrings of the Readwise export.
Merges cache/page-*.json (fresh fetch by regen.sh when the token is available).
Prints PASS/FAIL per lesson with book + author. Exit 1 on any FAIL."""
import json, sys, pathlib

RUN = pathlib.Path(__file__).resolve().parent

QUOTES = {
    "L1 Ries (Lean Startup), larger batches feel efficient":
        "by working in larger batches and passing work between departments",
    "L2 Hoffmann (World Atlas of Coffee), even bed / do no more":
        "The goal is simply to produce an even coffee bed, and do no more.",
    "L3 Kahneman (Thinking, Fast and Slow), attention when needed":
        "it is also the ability to find relevant material in memory and to deploy attention when needed",
    "L4 Farnam Street (Power Laws), declining exponent":
        "Quadrupling our training mileage from 16 to 64 miles is unlikely to double our endurance again",
    "L5 Darwin via Farnam Street (How Darwin Thought), memorandum at once":
        "to make a memorandum of it without fail and at once",
}

results = []
for f in sorted((RUN / "cache").glob("page-*.json")):
    results.extend(json.loads(f.read_text())["results"])

corpus = []  # (title, author, text)
for book in results:
    for h in book.get("highlights") or []:
        corpus.append((book.get("title", "?"), book.get("author", "?"), h.get("text", "")))

print(f"export: {len(results)} books, {len(corpus)} highlights")

fails = 0
for label, q in QUOTES.items():
    hits = [(t, a) for (t, a, txt) in corpus if q in txt]
    if hits:
        t, a = hits[0]
        print(f"PASS  {label}\n      [{t} — {a}] ({len(hits)} hit(s))")
    else:
        fails += 1
        print(f"FAIL  {label}\n      quote not found byte-identical")
sys.exit(1 if fails else 0)
