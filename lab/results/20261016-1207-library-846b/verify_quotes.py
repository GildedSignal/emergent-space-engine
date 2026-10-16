#!/usr/bin/env python3
"""Verify every verbatim quote used by the dossier against the cached export.

Each entry is a distinctive ASCII-safe substring of the stored highlight.
Prints PASS/FAIL per quote with book/author, and the library's census numbers.
Exit 1 if any quote fails (so the checker can rely on it).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JL = os.path.join(HERE, "cache", "highlights.jsonl")

QUOTES = {
    "musk-question-delete": (
        "Make them less wrong and dumb, because all requirements are somewhat "
        "wrong and dumb. And then delete, delete, delete."
    ),
    "musk-10pct-addback": (
        "if you do not end up adding back at least 10% of them, then you didn"
    ),
    "musk-automation-last": (
        "Always wait until the end of designing a process"
    ),
    "feynman-box-of-tools": (
        "my box of tools was different from everybody else"
    ),
    "naval-marginal-cost": (
        "Fortunes require leverage. Business leverage comes from capital, "
        "people, and products with no marginal cost of replication (code and media)."
    ),
    "waitzkin-chunking": (
        "ability to assimilate large amounts of information into a cluster that "
        "is bound together by certain patterns or principles particular to a given discipline."
    ),
    "taleb-size-stress": (
        "size hurts you at times of stress; it is not a good idea to be large "
        "during difficult times."
    ),
}


def main():
    rows = [json.loads(l) for l in open(JL)]
    print(f"census: {len(rows)} highlights, {len(set((r['title'], r['author']) for r in rows))} books")
    import re
    sync = sum(1 for r in rows if re.search(
        r"synchron|simultaneous|jitter|phase lock|traffic jam|convoy", r["text"], re.I))
    cache = sum(1 for r in rows if re.search(r"\bcache|caching", r["text"], re.I))
    print(f"absent-practitioner-themes: synchronization={sync} hits, cache={cache} hits")
    ok = True
    for qid, sub in QUOTES.items():
        hit = next((r for r in rows if sub in r["text"]), None)
        if hit is None:
            print(f"FAIL {qid}")
            ok = False
        else:
            print(f"PASS {qid}  [{hit['author'][:24]} | {hit['title'][:40]}]")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
