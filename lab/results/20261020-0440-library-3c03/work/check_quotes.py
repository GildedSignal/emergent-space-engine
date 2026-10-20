#!/usr/bin/env python3
"""Verify the five dossier quotes byte-exactly against the fresh Readwise export."""
import json, sys
rows = json.load(open(__file__.replace("check_quotes.py", "highlights_flat.json")))
FRAGS = [
    ("L1", "Farnam Street", "You can tell where a decision lies on this spectrum by asking how much it would cost to undo. The higher the cost to undo, the more irreversible it is."),
    ("L2", "Taleb", "For antifragility is the combination aggressiveness plus paranoia\u2014clip your downside, protect yourself from extreme harm, and let the upside, the positive Black Swans, take care of itself."),
    ("L3", "All Models Are Wrong", "A map is not the territory it represents, but, if correct, it has a similar structure to the territory, which accounts for its usefulness."),
    ("L4", "Feynman", "The first principle is that you must not fool yourself\u2014and you are the easiest person to fool."),
    ("L5", "Taleb", "There is no such thing as END, Evidence of No Disease."),
]
ok = True
for tag, src, frag in FRAGS:
    hit = [r for r in rows if frag in r["text"]]
    good = bool(hit) and any(src.lower() in (r["author"] + r["book"]).lower() for r in hit)
    ok &= good
    print(f"{tag}: {'OK' if good else 'MISS'} ({len(hit)} hits) — {hit[0]['book'] if hit else src}")
sys.exit(0 if ok else 1)
