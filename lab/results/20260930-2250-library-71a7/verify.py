#!/usr/bin/env python3
# Decisive checks for run 20260930-2250-library-71a7.
# P1: verbatim match of the 5 shipped quotes against the cached export
#     (whitespace- and quote-glyph-insensitive: curly/straight quotes are typography).
# P2: crossover arithmetic for the encounters setup cost vs kick cadence.
# P4: concentration number. Assumptions inline; every number traced to
#     board.md / HANDOFF.md / the taste log (r8 v2).
import json, re

def norm(s):
    s = re.sub(r"[\u2018\u2019\u201a\u201b\u2032'`\u201c\u201d\u201e\u201f\"]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()

hay = []
with open("readwise.jsonl") as f:
    for line in f:
        d = json.loads(line)
        for h in d.get("highlights", []):
            hay.append((d.get("title",""), d.get("author",""), norm(h.get("text",""))))

quotes = [
 ("L1 Simons", "James Simons (full length interview) - Numberphile", "it wasabstract algebra and then in a week everything came together for me iunderstood i was no longer puzzled iunderstood why they did everything"),
 ("L2 We Are Legion", "We Are Legion", "In fact, the technology had just moved the bottleneck."),
 ("L3 Feynman", "Surely You're Joking", "So I got a great reputation for doing integrals, only because my box of tools was different from everybody else's"),
 ("L4 Zipf", "Power Laws", "In all known languages, a small percentage of words make up the majority of usage. This is known as Zipf's law"),
 ("L5 Asimov", "All Models Are Wrong", "The basic trouble, you see, is that people think that \u201cright\u201d and \u201cwrong\u201d are absolute; that everything that isn't perfectly and completely right is totally and equally wrong."),
]

print("== P1 verbatim ==")
ok = 0
for tag, book, q in quotes:
    hits = [(t,a) for (t,a,x) in hay if norm(q) in x and norm(book) in norm(t)]
    print(f"{tag}: {'PASS' if hits else 'FAIL'} ({len(hits)} hit) {hits[:1]}")
    ok += bool(hits)
print(f"P1 total: {ok}/5")

print("== P2 crossover ==")
N_cand   = 1.7e6      # candidate pairs, belt 0 (taste log r8 v2)
W_enc    = 786        # element-sort work per encounter (taste log r8 v2)
E_orbit  = 427/20     # encounters per orbit, belt 0 (taste log r8 v2)
enc_work = W_enc * E_orbit
# Unit assumption: 1 work-unit ~= 1 us (both are per-event costs on the same cloud
# box). Reported with a 100x sensitivity swing on that assumption.
for s_us, label in [(2.5,"setup low"), (24.0,"setup high")]:
    for scale in [1.0, 100.0]:
        K_star = enc_work * scale / (N_cand * s_us)   # kicks/orbit at crossover
        print(f"{label} s={s_us}us work={scale}us: crossover K*={K_star:.2e}/orbit "
              f"(element lifetime t*={1/K_star:,.0f} orbits); "
              f"setup/encounter ratio at K=0.3..32/orbit: {N_cand*0.3*s_us/(enc_work*scale):.0f}x..{N_cand*32*s_us/(enc_work*scale):.0f}x")

print("== P4 concentration ==")
print(f"encounters/candidates per 20 orbits = {427/1.7e6:.1e} (uniform would make every pair meet); "
      f"bodies n~{int((2*1.7e6)**0.5)}")

print("== P3 anchored control ==")
print("committee quote -> 'commutative-monoid' already a recorded lead (HANDOFF line 78); Korzybski -> minimap already OC#30 (PRINCIPLES line 19)")
