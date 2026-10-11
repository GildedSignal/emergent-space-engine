Working...
Check complete. **Grade: silver**, written to `lab/results/20261011-0324-constraint-986f/check.md`; the tree is restored (only `lab/results/` untracked, as found).

**What I did:**

1. **Reproduced everything load-bearing** on a clean tree with `work/patch.diff` applied: the rtf-100 bench gives an identical digest with view_gather 70.1% vs the stored 68.9% (p50 3.44 vs 3.42 ms); the probe matches within 1% at every point (per-member 5.93/7.85/10.20 vs 5.90/7.87/10.12 µs; 163 vs 162 ms at 16,000 members); kick-bench memo rates are bit-exact (0% / 94.49%); the m480 bench and the 400-member clamp (`mod.rs:32`) reproduce, and the stored m480/m4800 JSONs are provably identical — the clamp in the data.

2. **Adversarial cases:** (a) 400 members at rtf 1 — the case the author skipped — view 0.81 ms vs engine 0.083 ms per frame, so the claim holds at the speed the player actually flies, not just the 100× stress mode; (b) the readout split re-measured at 4.40 µs/call ≈ 100% of the per-emitter floor, so the "~89%" is understated but the "3.7 µs" is unsaved; (c) the gates claim verified against code — no view-vs-N gate exists, but the author's "B15" citation actually points at the view unit test, not gate B15.

3. **Novelty:** H0210 already recorded "the view gather is 83% of a light frame" and plane.md foundation 7 already names the gather as something that must not take an unbounded claim on the frame. What's genuinely new: the floor decomposition, the 2.8× bound-body premium, the superlinear fleet-loop scaling to 16k, the saturation estimate, and both instrument gaps.

**Why silver, not gold:** the held-out magnitude P4 missed (2.8× vs ≥10×); nothing is moved or deleted — the fix was already promised by the design, so the run quantifies a known, designed-against violation rather than overturning a premise; plus two erroneous load-bearing sentences (the B15 label, "the only O(N) term"). The one experiment to gold: the event-driven fleet-loop gather behind display quanta, showing per-frame cost stops tracking N on the same 400/4k/16k sweep, guarded by a view-vs-N gate seeded from these numbers.
