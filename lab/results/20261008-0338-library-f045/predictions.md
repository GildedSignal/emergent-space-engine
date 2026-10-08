# predictions.md — 20261008-0338-library-f045

Question: the board's top measured bottleneck is "fewer kicks per orbit at the same
behaviour — kicks dominate the engine's cost" (board.md Focus list, item 1). Which
lessons from Julien's library (Readwise, 770 books, 4,580 highlights, cached in this
folder) change a decision on that bottleneck or the live questions it gates?

Held-out cases (written before reading docs/law.md, docs/plane.md and the queue;
the quotes were found by grep in the cached export, not by memory):

1. Quotes. Each lesson's quote will be extractable verbatim from
   `readwise-export.json` by an exact substring match (Musk's delete algorithm
   incl. the 10% re-add rule; Waitzkin's sandals; Feynman's "the theory isn't as
   good as it really is"; Taleb's fragile/cumulative-shocks asymmetry; Chouinard's
   "replace complex technology with knowledge"; Dignan's proxy warning).
2. Decisions. Each lesson must name a decision that is currently open, and the
   docs will show it open:
   - the cadence question is phrased as a *mean* ("kicks per orbit"), and no
     frozen gate judges cadence by the per-frame tail (p99.9 kick count or worst
     hitch) — prediction: true in law.md/plane.md;
   - the quantized-cell memo is treated as disqualified because it "changes
     orbits (a law change)" — prediction: the taste log is the only record, and
     no B-gate evaluation of that variant exists;
   - the changeover's placement near a secondary is not decided by a behaviour
     gate on the doll alone pushed deeper into the encounter regime;
   - cell quanta/packet sizes are set from a global worst case (the 2.3e-14 m
     position quantum), not derived per cell from gate-required distinctions;
   - no delete-first protocol (with a re-add budget) orders the kick-path work.
3. Cheap tests. Every lesson's test is runnable as a ≤60 s behave/run or a
   bisection on an existing harness; none requires new infrastructure.
4. Lens bias check. This lens over-samples management books; I predict ≥3 of the
   5 kept lessons will come from practitioner narratives (Musk, Feynman,
   Chouinard, Waitzkin, Taleb-as-trader) rather than from productivity guides,
   and any productivity-guide lesson will be dropped unless it changes a named
   decision. (Prediction: the Dignan proxy quote is the weakest — dropped or
   folded as mechanism, not kept as a lesson.)

If (2) fails for a lesson (the decision is already made as the lesson suggests),
that lesson is deleted, per the lens brief: keep only lessons that change a decision.

## Probe prediction (added before running the toy, after the quote/doc checks)

Lesson 2's instrument A(τ) = err(one batched kick per orbit) / err(16 kicks per orbit),
same total impulse, apsidal-advance observable, Hill-regime toy (parent + circular
secondary, exact Kepler drift + tidal impulses, float — exploring, not canonical):

- A(τ) > 1 (batching hurts) for moons below about 0.17 Hill radii (r9's τ₀),
- A(τ) < 1 (batching wins) above it, and
- A is monotone falling in τ.
Kill for the instrument: if A(τ) never crosses 1 in 0.05–0.5 Hill radii, or crosses
without monotone shape, the asymmetry is not a usable regime trigger as claimed.
