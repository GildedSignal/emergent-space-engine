#!/usr/bin/env python3
"""Verify the five dossier quotes byte-identically against a fresh Readwise export
(cached at work/readwise.json by fetch_readwise.py / regen.sh). Full-substring match."""
import json, sys

QUOTES = [
 ("Timothy Ferriss", "The 4-Hour Body",
  "The minimum effective dose (MED) is defined simply: the smallest dose that will produce a desired outcome."),
 ("Timothy Ferriss", "The 4-Hour Body",
  "Anything beyond the MED is wasteful. To boil water, the MED is 100\u00b0C (212\u00b0F) at standard air pressure. Boiled is boiled."),
 ("Nassim Nicholas Taleb", "Incerto 5-Book Bundle",
  "Knowledge is subtractive, not additive\u2014what we subtract (reduction by what does not work, what not to do), not what we add (what to do)."),
 ("Orson Scott Card", "Ender's Game",
  "Humanity does not ask us to be happy. It merely asks us to be brilliant on its behalf. Survival first, then happiness as we can manage it."),
 ("Scott Young", "Ultralearning",
  "Directness is the practice of learning by directly doing the thing you want to learn."),
 ("Scott Young", "Ultralearning",
  "Passive learning creates knowledge. Active practice creates skill."),
 ("Walter Isaacson", "Elon Musk",
  "Separating the design of a product from its engineering was a recipe for dysfunction. Designers had to feel the immediate pain if something they devised was hard to engineer."),
]

books = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "work/readwise.json"))
n_h = sum(len(b.get("highlights", [])) for b in books)
ok = True
for author, title, frag in QUOTES:
    hit = any(frag in (h.get("text") or "")
              for b in books if (b.get("author") or "").startswith(author) and b.get("title") == title
              for h in b.get("highlights", []))
    print(f"{'OK ' if hit else 'FAIL'}  [{author} | {title}]  {frag[:72]}...")
    ok = ok and hit
print(f"\n{len(QUOTES)} quote fragments checked against {n_h} highlights in {len(books)} books")
sys.exit(0 if ok else 1)
