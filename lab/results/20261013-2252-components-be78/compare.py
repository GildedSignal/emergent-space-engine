#!/usr/bin/env python3
"""The dossier's table: for each scene, the shipped arm (`off`) against `ES_WORD_FIRST=1`
(`on`). Digests must be equal; retries (FIT2, main thread) must go to zero; the hand-out's
per-item cost is the bind term (H_BIND) and the whole item (HANDOUT). `off2`, when present,
is the shipped arm run twice (the collapse regime's wall wobble control)."""
import json, sys, glob, os

d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "work")
HO = "hand-out (a member made a body)"
HB = "  hand-out: bind (the member as a tube)"
F2 = "  fit again: the coarser word (bind_surface)"

def load(name):
    with open(os.path.join(d, name + ".json")) as f:
        return json.load(f)

def prof(j):
    return {p["stage"]: p for p in j["prof"]}

def us(j, stage):
    p = prof(j).get(stage)
    return p["ms"] * 1000 / p["calls"] if p and p["calls"] else 0.0

scenes = ["m1500-s1-rtf1", "m1500-s3-rtf1", "m1500-s5-rtf1", "m1500-s7-rtf1",
          "m4000-s3-rtf1", "m8000-s3-rtf1", "m400-s1-rtf100"]
print(f"{'scene':>15} | {'digest':>3} | handouts | retry off->on | hand-out us off->on (d%) | bind us off->on (d%)")
tot_ho = [0, 0]
for s in scenes:
    o, n = load(s + "-off"), load(s + "-on")
    po, pn = prof(o), prof(n)
    ho = po.get(HO, {"calls": 0, "ms": 0})["calls"]
    r0 = po.get(F2, {"calls": 0})["calls"]
    r1 = pn.get(F2, {"calls": 0})["calls"]
    h0, h1 = us(o, HO), us(n, HO)
    b0, b1 = us(o, HB), us(n, HB)
    tot_ho[0] += h0 * ho; tot_ho[1] += h1 * ho
    print(f"{s:>15} | {'=' if o['digest'] == n['digest'] else 'DIFF':>3} | {ho:8d} | {r0:6d}->{r1:<6d} "
          f"| {h0:6.0f}->{h1:<6.0f} ({100*(h1-h0)/h0:+.0f}%) | {b0:6.0f}->{b1:<6.0f} ({100*(b1-b0)/b0:+.0f}%)")
    if os.path.exists(os.path.join(d, s + "-off2.json")):
        w = load(s + "-off2")
        print(f"{'(wobble ctl)':>15} | {'=' if w['digest'] == o['digest'] else 'DIFF':>3} | shipped twice: presented "
              f"{o['presented_tick_at_end']} vs {w['presented_tick_at_end']}, lost {len(o['lost_bodies'])} vs "
              f"{len(w['lost_bodies'])}, overflow {o['rtf']['overflow_frames']} vs {w['rtf']['overflow_frames']}")
# P7: the plain (no-prof) build, the exact shipped feature set.
p, q = load("plain-m1500-s3-off"), load("plain-m1500-s3-on")
r = load("m1500-s3-rtf1-off")
print(f"{'plain m1500-s3':>15} | {'=' if p['digest'] == q['digest'] else 'DIFF':>3} | plain off == plain on == prof-on: "
      f"{p['digest'] == q['digest'] == r['digest']}")
n = sum(1 for s in scenes for _ in [0])
print(f"hand-out aggregate across scenes: {tot_ho[0]/sum(prof(load(s+'-off')).get(HO, {'calls':0})['calls'] for s in scenes):.0f}"
      f" -> {tot_ho[1]/sum(prof(load(s+'-off')).get(HO, {'calls':0})['calls'] for s in scenes):.0f} us per hand-out (weighted)")
