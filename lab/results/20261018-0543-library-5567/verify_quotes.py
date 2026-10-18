#!/usr/bin/env python3
"""Verify the dossier's five quotes are byte-identical fragments of the cached Readwise export."""
import sys
from pathlib import Path

hl = Path(__file__).with_name("work") / "hl.tsv"
rows = [
    (r.split("\t")[0], r.split("\t")[1], r.split("\t", 2)[2])
    for r in hl.read_text().splitlines()
]
quotes = [
    ("L1", "\u201cStep one should be to question the requirements,\u201d he says. \u201cMake them less wrong and dumb, because all requirements are somewhat wrong and dumb. And then delete, delete, delete.\u201d", "Elon Musk", "Walter Isaacson"),
    ("L2", "\u201cIt\u2019s not the product that leads to success. It\u2019s the ability to make the product efficiently. It\u2019s about building the machine that builds the machine. In other words, how do you design the factory?\u201d", "Elon Musk", "Walter Isaacson"),
    ("L3", "to a man with a hammer, every problem looks like a nail.", "Five Simple Notions that Solve Problems", "Farnam Street"),
    ("L4", "increasing engagement with existing key features is more impactful than launching new features", "How to Accelerate Growth by Focusing on the Features You Already Have", "Lenny\u2019s Newsletter"),
    ("L5", "the behavior of the system differs from the simple addition of its parts. This characteristic is called emergent behavior.", "Power Laws: How Nonlinear Relationships Shape the World", "Farnam Street"),
]
ok = 0
for tag, q, book, author in quotes:
    hits = [(b, a) for (b, a, t) in rows if q in t]
    good = bool(hits) and any(b.startswith(book[:25]) for b, a in hits)
    print(f"{tag}: {'BYTE-IDENTICAL' if good else 'MISS'} in {hits[:1]}")
    ok += good
print(f"{ok}/5 verified against {len(rows)} cached highlights")
sys.exit(0 if ok == 5 else 1)
