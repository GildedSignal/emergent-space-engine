#!/usr/bin/env python3
"""Verify the dossier's five lesson quotes byte-identical against the fresh fetch."""
import json, sys

doc = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "readwise.json"))
by_book = {}
for h in doc["highlights"]:
    by_book.setdefault(h["book_id"], []).append(h["text"])

QUOTES = [
    ("L1 clean slate", 36375189, "What characterizes real speculators like Soros from the rest is that their activities are devoid of path dependence. They are totally free from their past actions. Every day is a clean slate."),
    ("L2 maximum law", 36375189, "By a law of probability called distribution of the maximum of random variables, the maximum of an average is necessarily less volatile than the average maximum."),
    ("L3 invisible accumulation", 41533337, "“Just because results are not visible doesn’t mean they are not accumulating.”"),
    ("L4 moved bottleneck", 37017531, "In fact, the technology had just moved the bottleneck."),
    ("L5 parade retention", 28092592, "Once a few people decide to stand on their tip-toes, everyone has to stand on their tip-toes. No one can see any better, but they’re all worse off."),
]
ok = 0
for name, bid, frag in QUOTES:
    hit = any(frag in t for t in by_book.get(bid, []))
    print(f"{'OK ' if hit else 'FAIL'} {name} (book {bid})")
    ok += hit
print(f"{ok}/{len(QUOTES)} byte-identical")
sys.exit(0 if ok == len(QUOTES) else 1)
