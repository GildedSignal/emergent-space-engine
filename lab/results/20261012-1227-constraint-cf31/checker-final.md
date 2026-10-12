Working...
Check complete. `check.md` written to `lab/results/20261012-1227-constraint-cf31/`; tree restored clean for the second blind checker.

**Grade: silver.**

What I did and found:

**Reproduced (from scratch):** applied `work/patch.diff`, rebuilt, reran intact and probe at rtf 100 — engine digest bit-identical across all three (`6ce636fa…`), matching the author's saved JSONs exactly. Adversarial **held-out seed 2**: digest identity holds there too (`c9794984…`). The core constraint claim is robust: gather = 0.65–0.75 of frame CPU in *every* run, theirs and mine. Gates match HANDOFF (space G1/G2/G5 PASS; plane G-failures are adapter non-answers; B13 60/64; B14 60.1 s timeout). Predictions predate the probe (file-time order verified); №5 held, №1–3 failed and were honestly disclosed.

**Deflated the headline:** the "2–3.5× frame cut from deleting the search" is load-confounded — the author's *own* intact rerun (diag4: gather 0.85 ms, 13.8 µs/body) already sits at the probe floor, and my back-to-back pairs measure 1.6× (seed 1) and **no gain** (seed 2, 0.83→0.99 ms). The stable fact is the author's own refinement: the per-body re-derivation floor (~14–22 µs/body), not the Newton search.

**Discrepancies:** the fleet-member 2.6 µs is extrapolated, not measured — their own traces give 5–9 µs/member (so "6–20× cheaper" is really ~2.5–7×); prediction №6 scored "held at the top edge" though 18–22 µs is outside the predicted 3–15.

**Novelty:** not cited against H0210's Limitations ("the view gather is 83% of a light frame", 1 October) or `representation.md` rung r6 ("Newton iterations and samples per frame for the gather"). Genuinely new: the digest-identity proof that the view is a pure read (cadence free), and that iterations (~1.1 readouts/seen after redteam-4570's memo) are no longer the lever.

**Gold path:** build the cadence + surprise-gate policy in `gather_with` and measure back-to-back with digest identity — the fix is proposed, not built.
