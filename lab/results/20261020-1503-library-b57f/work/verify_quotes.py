#!/usr/bin/env python3
"""Verify the five lesson quotes byte-identically against the Readwise export.

Usage: verify_quotes.py [readwise.json]  (default: work/readwise.json beside this file)
Prints one line per quote: PASS/FAIL, book title, author, match length.
Exit 0 iff 5/5 PASS.
"""
import json, sys, os

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "readwise.json")

QUOTES = [
    # (book title contains, author contains, exact byte fragment as used in lessons.md)
    ("Sherlock Holmes", "Conan Doyle",
     "Now the skilful workman is very careful indeed as to what he takes into his brain-attic. "
     "He will have nothing but the tools which may help him in doing his work, but of these he has "
     "a large assortment, and all in the most perfect order."),
    ("The Third Door", "Banayan",
     "Sure, there may be billions of frogs, but sometimes I\u2019ll notice there are only ten different "
     "kinds of frogs. So that\u2019s a good second tip: you should kiss one of these, one of those\u2014but "
     "don\u2019t try to kiss every possible frog."),
    ("The Art of Learning", "Waitzkin",
     "chunking relates to the mind\u2019s ability to take lots of information, find a harmonizing/logically "
     "consistent strain, and put it together into one mental file that can be accessed as if it were a "
     "single piece of information."),
    ("The Caves of Steel", "Asimov",
     "Efficiency had been forced on Earth with increasing population. Two billion people, three billion, "
     "even five billion could be supported by the planet by progressive lowering of the standard of living. "
     "When the population reaches eight billion, however, semistarvation becomes too much like the real thing."),
    ("The Great Mental Models", "Parrish",
     "Most geniuses\u2014especially those who lead others\u2014prosper not by deconstructing intricate "
     "complexities but by exploiting unrecognized simplicities."),
]

def main(path):
    pages = json.load(open(path))
    books = [b for p in pages for b in p["results"]]
    ok = 0
    for i, (title, author, frag) in enumerate(QUOTES, 1):
        hits = [b for b in books
                if title.lower() in b.get("title", "").lower()
                and author.lower() in b.get("author", "").lower()
                and any(frag in h.get("text", "") for h in b.get("highlights", []))]
        status = "PASS" if hits else "FAIL"
        ok += bool(hits)
        print(f"{status} q{i} [{title} | {author}] fragment {len(frag)} chars, books matched: {len(hits)}")
    print(f"{ok}/5 byte-identical")
    sys.exit(0 if ok == 5 else 1)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
