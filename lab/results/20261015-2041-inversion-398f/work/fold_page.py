#!/usr/bin/env python3
"""Fold this run's result into the nladder page copy (wiki/nladder.md), additively."""
import io, sys

P = "wiki/nladder.md"
txt = open(P).read()

entry = """**The depth axis is the page's blind one: every memory win above was measured at <= 20k game-s cuts (at most one settle wave), and the one per-body term that grows with play — the causal history stack (`PlainBodies.history`, one 336-B `Segment` per retired binding, each pinning its full compiled arc under ctl) — is now measured per class, with the mechanism named (20261015-2041-inversion-398f, inversion; 8b89's patch + a 15-line `Universe::history_census` at the canonical cut). The belt saturates flat: 1.04 segments/body at 32k/48k/96k, arm-independent (ctl and all read identical counts — the prune governs the stack, not the seam), bpb 974-1,004, and digest identity ctl==all holds at 96k (`e75c90f2…`, 4x the deepest prior cut). The infalling comet class grows LINEARLY with play: 46.5 -> 479.9 segments/body from 3k to 32k (exponent +0.99; max 2,770 on one body; bpb 165,751, still under-booked by the 4,096-B Live-passage placeholder; rss 2,816 MB on a 171-body scene, against the 10,000-body belt's 62 MB), and the prune cannot stop it: a segment leaves only past `until + 2*light_distance(body->observer) + 2^26` ticks (`universe.rs:572,1273,1299`), and at the comets' ~10^4 AU that keep-behind is ~10^7 game-s — inert at any playable depth. The retention is the light cone itself (PRINCIPLES 23: nothing past c), not a bug: a reader inside the cone may still ask for every retired binding. `ES_LAZY_ALL` shrinks each retired segment ~75x (the slot vs the pinned ~25 kB arc) and bounds nothing — on any body that keeps crossing dolls, retained history grows ~linearly with distance travelled (~15 segments per 1k game-s on this class). Consequence for the adoption: both 8b89 checkers' named gold experiment (compose ALL + `ES_RETAIN_HOT`, fly 10^5 coast + burn, close it in one flight) flies 20k cuts and cannot see this term; the memory sentence needs a depth clause (>= 2 settle waves) and a far class aboard before it closes.**

"""

refuted = '- **"Digest identity plus a census at one cut certifies the memory claim" (the adoption\'s implicit certificate): the census is depth-dependent by class — the belt reads flat to 96k while a +1.0-exponent linear stack grows on the far class over the same cuts, on shipped code (20261015-2041-inversion-398f).**\n'

opendir = """6. **The adoption flight must fly depth and a far class (398f):** ALL+retention at >= 48k on the belt AND one infalling class, with the history census aboard. The stack to price at 10^9: segments/crossing x 336 B (ALL) or x the pinned arc (shipped), crossings ~ distance travelled, retention horizon 2*r/c per body — the light cone's memory bill, charged to whatever population commutes between dolls. The representation question under it: a retired segment holds a full `Binding`; if it held only its generator (key + interval, re-mintable on read like ALL's slots), the retained past would ride at the key's size — but re-derivation inside the cone must then be priced against retention (the belt's own floor is already 1.04 segments/body).
"""

runs = "- 20261015-2041-inversion-398f (this run, awaiting grade): the history stack's growth law measured per class — the belt flat (1.04 seg/body at every cut, arm-independent), the infalling comet class linear (+0.99 exponent, 46.5->480 by 32k, rss 2.8 GB on 171 bodies); keep-behind = 2*light_distance makes the term causal; single-cut adoption flights are blind to it.\n"

lines = txt.split("\n")
out = []
for i, l in enumerate(lines):
    if l.startswith("updated:"):
        out.append("updated: 20261015-2041-inversion-398f")
    elif l == "## Current best":
        out.append(l)
        out.append("")
        out.append(entry.rstrip("\n"))
    elif l == "## Refuted":
        out.append(refuted.rstrip("\n"))
        out.append(l)
    elif l == "## Open directions":
        out.append(l)
        out.append("")
        out.append(opendir.rstrip("\n"))
    elif l == "## Runs":
        out.append(l)
        out.append(runs.rstrip("\n"))
    else:
        out.append(l)

open(P, "w").write("\n".join(out))
print("folded")
