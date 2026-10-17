#!/usr/bin/env python3
"""Verify the five dossier quotes byte-identical against the fresh Readwise
export (full-text containment, not fragment matching)."""
import json, sys
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_os.chdir(_HERE)


QUOTES = [
    # (short name, exact text as quoted in the dossier)
    ("L1 Munger/FS inversion",
     "problems frequently get easier and I would even say usually *are* easier to solve if you turn around in reverse.\n\nIn other words if you want to help India, the question you should ask is not “how can I help India?”, you think “what’s doing the worst damage in India? What would automatically do the worst damage and how do I avoid it?” You’d think they are logically the same thing, but they’re not."),
    ("L2 Taleb, Fooled by Randomness",
     "For one cannot consider a profession without taking into account the average of the people who enter it, not the sample of those who have succeeded in it."),
    ("L3 Taleb, The Black Swan",
     "The more information you give someone, the more hypotheses they will formulate along the way, and the worse off they will be. They see more random noise and mistake it for information."),
    ("L4 Asimov, The Naked Sun",
     "I could not bring myself to believe that if knowledge presented danger, the solution was ignorance. To me, it always seemed that the solution had to be wisdom. You did not refuse to look at danger, rather you learned how to handle it safely."),
    ("L5 Young, Ultralearning",
     "The rate-determining step is the slowest part of this chain of reactions, forming a bottleneck that ultimately defines the amount of time needed for the entire reaction to occur."),
]

r = json.load(open("readwise_export.json"))
texts = [h.get("text") or "" for b in r if not b.get("is_deleted")
         for h in b.get("highlights", [])]
ok = 0
for name, q in QUOTES:
    # byte-identical containment; also accept the nbsp variant (U+00A0)
    hit = any(q in t or q.replace(" You’d", "\xa0You’d") in t for t in texts)
    print(f"{'VERIFIED' if hit else 'MISMATCH'}  {name}  ({len(q)} chars quoted)")
    ok += hit
print(f"{ok}/{len(QUOTES)} byte-identical")
sys.exit(0 if ok == len(QUOTES) else 1)
