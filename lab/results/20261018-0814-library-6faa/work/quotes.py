#!/usr/bin/env python3
"""Verify the five dossier quotes byte-identical against the fresh Readwise export.
Cache: work/readwise.json (built from work/readwise_raw.json, the API's own bytes).
A quote passes iff its full text appears in the export as an exact substring of one
highlight (whitespace normalized exactly as the cache stores it: none)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
QUOTES = [
    ("L1 Feynman, Surely You're Joking (box of tools)",
     "So I got a great reputation for doing integrals, only because my box of tools was different from everybody else’s, and they had tried all their tools on it before giving the problem to me."),
    ("L2 Naval, The Almanack of Naval Ravikant (inputs vs outputs)",
     "Tools and leverage create this disconnection between inputs and outputs."),
    ("L3 Musk via Isaacson, Elon Musk (the machine that builds the machine)",
     "It’s not the product that leads to success. It’s the ability to make the product efficiently. It’s about building the machine that builds the machine."),
    ("L4 Confucius via Bevelin, Seeking Wisdom (uncorrected mistake)",
     "A man who has committed a mistake and doesn't correct it, is committing another mistake."),
    ("L5 Asimov, Foundation's Edge (appearance vs essence)",
     "We abandoned the appearance of power to preserve the essence of it."),
]

def main():
    books = json.load(open(os.path.join(HERE, 'readwise.json')))
    corpus = [h for b in books for h in b['highlights']]
    ok = 0
    for name, q in QUOTES:
        hits = [(b['title'], b['author']) for b in books for h in b['highlights'] if q in h]
        status = 'PASS' if hits else 'FAIL'
        ok += bool(hits)
        print(f"[{status}] {name}")
        if hits:
            print(f"       byte-identical in: {hits[0][0][:60]} | {hits[0][1][:30]}")
    print(f"{ok}/{len(QUOTES)} byte-identical")
    sys.exit(0 if ok == len(QUOTES) else 1)

if __name__ == '__main__':
    main()
