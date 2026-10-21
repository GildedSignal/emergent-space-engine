#!/usr/bin/env python3
"""Verify the five lesson quotes byte-identical against readwise_cache.json (P6).

Each lesson quotes a contiguous span of one highlight; a span is checked byte-exactly
(same bytes, in order, no edits). L1/L2/L5 quote the whole highlight.
"""
import json, sys
import gzip; d = json.load(gzip.open("readwise_cache.json.gz"))
by_id = {h.get("id"): h for h in d["highlights"]}

QUOTES = {
  1002498309: ("L1 minority rule",
    "Let us conjecture that the formation of moral values in society doesn\u2019t come from "
    "the evolution of the consensus. No, it is the most intolerant person who imposes "
    "virtue on others precisely because of that intolerance. The same can apply to civil rights."),
  533417933: ("L2 sampling frequency vs noise",
    "The more frequently you look at data, the more noise you are disproportionally likely "
    "to get (rather than the valuable part called the signal); hence the higher the noise to "
    "signal ratio. And there is a confusion, that is not psychological at all, but inherent "
    "in the data itself."),
  1001552690: ("L3 distributional information",
    "The prevalent tendency to underweight or ignore distributional information is perhaps "
    "the major source of error in forecasting. Planners should therefore make every effort to "
    "frame the forecasting problem so as to facilitate utilizing all the distributional "
    "information that is available."),
  568257797: ("L4 local vs system productivity (batch)",
    "They will ask to go back to the old way of working, in which they had the opportunity "
    "to \u201cstay efficient\u201d by working in larger batches and passing work between departments. "
    "It\u2019s safe to predict this result, and not just because I have seen it many times in the "
    "companies I work with."),
  1006185304: ("L5 redundancy and the unusual",
    "Redundancy is ambiguous because it seems like a waste if nothing unusual happens. "
    "Except that something unusual happens\u2014usually."),
}
ok = 0
for hid, (name, span) in QUOTES.items():
    h = by_id.get(hid)
    src = (h or {}).get("text") or ""
    same = span in src
    whole = (src == span)
    ok += same
    b = (h or {}).get("_book", {})
    print(f"{name}: {'BYTE-IDENTICAL' if same else 'MISMATCH'}"
          f"{' (full highlight)' if whole else ' (contiguous span)'} "
          f"[{b.get('title')} \u2014 {b.get('author')}]")
print(f"{ok}/5 byte-identical; total highlights in cache: {len(d['highlights'])}")
sys.exit(0 if ok == 5 else 1)
