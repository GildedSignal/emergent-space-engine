#!/usr/bin/env python3
"""Band summary: panels and time ratios, ladder vs a candidate arm, plus passages."""
import sys

rows = {}
for f, arm in [("grid_ladder.csv", "ladder"), ("heldout_ladder.csv", "ladder"),
               ("grid_c_4.csv", "c:4"), ("heldout_c_4.csv", "c:4")]:
    for line in open(f):
        t = line.strip().split(",")
        if t[0] == "ROW" and t[4] != "ERR":
            rows.setdefault((t[1], t[2]), {})[arm] = (int(t[4]), int(t[9]))
        elif t[0] == "PASSAGE" and t[5] != "ERR":
            print("PASSAGE", t[1], t[2], t[3], (t[4] or "ladder"), "panels", t[5], "ns", t[6])
band = lambda e: "e>=0.9" if float(e) >= 0.9 else ("0.3<=e<0.9" if float(e) >= 0.3 else "e<0.3")
import statistics as st
for b in ["e>=0.9", "0.3<=e<0.9", "e<0.3"]:
    pr, tr = [], []
    for (p, e), arms in rows.items():
        if band(e) == b and "ladder" in arms and "c:4" in arms:
            pr.append(arms["ladder"][0] / arms["c:4"][0])
            tr.append(arms["ladder"][1] / arms["c:4"][1])
    if pr:
        print(f"{b}: n={len(pr)} panels ladder/c4 median {st.median(pr):.2f} "
              f"min {min(pr):.2f} max {max(pr):.2f} | time median {st.median(tr):.2f} "
              f"min {min(tr):.2f} max {max(tr):.2f}")
for k in [("8", "0.99999"), ("20", "0.99"), ("50", "0.9999"), ("200", "0.999"),
          ("100000", "0.99999")]:
    if k in rows:
        print(k, "ladder", rows[k]["ladder"], "c:4", rows[k]["c:4"])
