Working...
Check complete. Summary:

**Grade: gold** (`check2.md` written).

**Reproduction** — `regen.sh` exit 0 in my own run; grade roster re-extracted independently (different tooling): 5 gold / 20 silver / 3 missing, exact match; all 22 run ids resolve to branches.

**Attack beyond the author's regen strings** — ~30 sampled numbers read directly from the runs' own branches: every gold headline (ace6's 2–176°/ISCO 98°/135°, 8be2's checker-corrected 3.32×, 9f4a's ≤0.084% windings and Σμ deficit, 94dc's 0-drop kinked tubes), twelve silvers, both ungraded leads, and efb2's pre-flyby refinement — all trace.

**Two defects found, corrected in place** (page only, per mandate):
1. "1.06–1.19 readouts/emitter" — the 1.19 endpoint traces to nothing; 70b0's real figure is ≈1.0 (the 1.1958 in its JSON is a **ms** p99). Corrected to 1.0–1.1; true values flatter the claim, no weighing changed.
2. 0fe0's "3.00 iterations for every β" lacked its own checker's warm-start condition (cold seeds leave the bracket at β ≥ 0.9). Qualifier added, in body and run line.

`regen.sh` still exit 0 after the edits. efb2's missing run line is **correct as a pointer** — its run lines live on the high-gamma page with "→ view" handoffs.

**Unfalsifiable caveat recorded**: predictions.md's final mtime postdates the page, exactly as its disclosed fill-after workflow predicts, but priority can't be proven from mtimes; the P6 content is branch-verifiable regardless and holds.

**Closure: no** — five golds agree on the diagnosis, but the converged memo is unbuilt, so `valid-while` can't be pinned; topic stays open with the honest open-directions list.
