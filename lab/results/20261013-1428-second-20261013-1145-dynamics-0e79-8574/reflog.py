#!/usr/bin/env python3
"""Decompose the off-axis refusal storms: bucket the G-logged refusal changes by phase.

Reads the probe's stderr trace (traces.txt), lines of the form
    G t=<s> phase=<n> dref=<k> tot=<n> doll=<name> g_d=<x>
Phase codes: 0 coast, 1 pump-up, 2 turn, 3+ hold/burn, 5 raise, 6 coast-out.
Also reports the first-refusal tick and the doll at each change for the two flights.
The G lines carry no flight name; the probe emits them only for the two C off-axis rows,
off45 first then off90, and each flight's trace starts at t=82.6 s — split on the reset
of `tot` to a smaller value (a new flight's first change).
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "traces.txt"
name_re = re.compile(r"^(C: held L15 g3 off45|C: held L15 g3 off90)")
rows = []
flight = None
flights = []

# Flight boundaries from the stdout grid order: off45 comes before off90 in the list.
gline = re.compile(r"G t=([\d.]+)s phase=(\d+) dref=(\d+) tot=(\d+) doll=(\S+) g_d=([\d.]+)")
cur = {"lines": [], "tot": 0}
order = ["off45", "off90"]
for line in open(path):
    m = gline.match(line)
    if not m:
        continue
    t, phase, dref, tot, doll, gd = (float(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5], float(m[6]))
    if tot < cur["tot"]:  # new flight
        flights.append(cur)
        cur = {"lines": [], "tot": 0}
    cur["lines"].append((t, phase, dref, tot, doll, gd))
    cur["tot"] = tot
flights.append(cur)
flights = [f for f in flights if f["lines"]]

for i, f in enumerate(flights):
    tag = order[i] if i < len(order) else f"flight{i}"
    print(f"== {tag}: {len(f['lines'])} refusal-change checks, total {sum(l[2] for l in f['lines'])}")
    by_phase = {}
    by_doll_change = {"same-doll": 0, "doll-change": 0}
    prev_doll = None
    first = None
    for (t, phase, dref, tot, doll, gd) in f["lines"]:
        by_phase[phase] = by_phase.get(phase, 0) + dref
        if first is None:
            first = (t, phase, gd)
        if prev_doll is not None and doll != prev_doll:
            by_doll_change["doll-change"] += dref
        else:
            by_doll_change["same-doll"] += dref
        prev_doll = doll
    total = sum(by_phase.values())
    print(f"   first refusal at t={first[0]:.0f}s (phase {first[1]}, g_d={first[2]:.3f})")
    for ph in sorted(by_phase):
        label = {0: "coast", 1: "pump-up", 2: "turn", 3: "hold"}.get(ph, f"phase{ph}")
        print(f"   {label:<8} {by_phase[ph]:>7}  ({100.0*by_phase[ph]/total:.1f}%)")
    for k, v in by_doll_change.items():
        print(f"   {k:<11} {v:>7}  ({100.0*v/total:.1f}%)")
    # the g_d band where refusals fire
    gds = [l[5] for l in f["lines"]]
    print(f"   g_d at refusal checks: min {min(gds):.3f} max {max(gds):.3f}")
