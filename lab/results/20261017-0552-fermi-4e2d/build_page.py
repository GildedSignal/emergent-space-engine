#!/usr/bin/env python3
"""Fold this run's result into the kick-cadence page (three-way base = the page as it stands)."""
import re

SRC = "lab/wiki/kick-cadence.md"
DST = "lab/results/20261017-0552-fermi-4e2d/wiki/kick-cadence.md"
RUN = "20261017-0552-fermi-4e2d"

page = open(SRC).read()
page = re.sub(r"^updated: .*$", f"updated: {RUN}", page, count=1, flags=re.M)

para = (
    f"The 10\u2079 ledger is recomposed on the two-comb and on 1a46's own belt count, and both "
    "corrections point the same way: at flown legality the composed bottom line is **10.3 M1 cores "
    "(2.6\u00d7 over the 4-core budget)**, not e7ef's 5.1\u20138.65 \u2014 that row survives neither the boundary "
    "comb (+25%, 8ffc) nor the belt's measured delete (274/712 deleted \u21d2 survival 0.615, not 0.39: "
    "1a46's scene ledger \u221270% is the locals' delete, and the belt is everything at 10\u2079). Anchors "
    "regenerate on shipped code: belt first item p50 14,071 game-s = interval/2 to the digit "
    "(`belt_first 10000`); one comb window at 10\u2074 flies kicks \u224873.8k \u2248 boundaries \u224871.6k (count "
    "parity, the two-comb; per-flight counts) at 42\u201350 \u00b5s/event this box (record 50\u201352); memory steps 2,461 B/B "
    "\u2192 ~5.6 kB/B through the crest (the plateau minting in flight). The other terms close: encounters "
    "0.03\u20130.6 cores (f0a2, adjudicated \u2014 `Key::new` stores E absolutely in Q48 on scale 1, "
    "source-verified here), promotion CPU free (cbc5: the mint IS the kick's compile), H_live 21 bits/s "
    "(4b55), genesis one-time 7.8 h (program births delete it). The wiring's memory is a dwell identity: "
    "live = mint\u00d7dwell\u00d74.95 kB plateau, so at split 8 the dwell window is **[~100, ~115] game-s "
    "(razor, 1.15\u00d7)**; the CPU-closing split (S* = 20.7\u00d7 at today's \u0108) widens it to [~100, ~300], "
    "the record diet to ~570. So one dial \u2014 the belt's metronome split \u2265 21\u00d7, or mixed \u0108 \u2264 14.6 \u00b5s "
    "M1 at split 8 \u2014 closes CPU and memory together: kick cost and cadence are redundant for CPU alone "
    "(e7ef) but NOT for the composed budget, because only cadence relieves the dwell window "
    f"({RUN}, fermi; shipped code + page constants; x86 shares, orders of magnitude).**\n\n"
)

page = page.replace("## Current best\n\n", "## Current best\n" + para, 1)

refuted = (
    "- **e7ef's composed 10\u2079 row as stated (\"today's 104\u2013178-core stream falls to 5.1\u20138.65 cores\" on "
    "\"the measured 61% belt delete\")**: the belt's own measured delete is 274/712 = 38.5% (survival "
    "0.615 \u2014 1a46's own belt count; the \u221270% is the scene ledger, dominated by the locals), and the "
    "stream is two combs (+25%, 8ffc): recomposed 10.3 M1 / 17.7 x86 cores at split 8 and frozen "
    "legality \u2014 1.6\u00d7 deeper over budget, required split S* = 20.7\u00d7 (20261017-0552-fermi-4e2d). The "
    "cadence-vs-kick-cost redundancy for CPU alone stands; the composed budget breaks it (dwell).\n"
)
page = page.replace("## Refuted\n", "## Refuted\n" + refuted, 1)

runs = (
    f"- {RUN} (fermi, this run): the 10\u2079 ledger recomposed \u2014 10.3 M1 cores at flown legality "
    "(2.6\u00d7 over), encounters closed on the adjudicated anchor (source-verified), dwell window "
    "[~100, ~115] gs at split 8 (razor); one dial (split \u2265 21\u00d7) closes CPU and memory together.\n"
)
page = page.rstrip("\n") + "\n" + runs

import os
os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, "w").write(page)
print(f"wrote {DST} ({len(page)} chars)")
