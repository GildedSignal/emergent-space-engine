Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-2312-system-9eeb/check.md`, with the author's page corrected in place.

**Reproduction (patch self-applied, clean rebuild 3m21s):** every dossier number matched exactly — 58 builds / 1,764 rebinds (3.3%), FIT 129→46 ms (−64%), period max 6.786e-4 inside B2's 1e-3, advance 75× inside B1, knots 0, exact-key recurrence 0.000, hash `0x7f43b75a59fff0f3` stable, off-arm bit-identical with the served memo untouched. The disclosed memo.rs on-arm guard trip verified at 0.898 — which regen.sh's "both arms" echo never actually runs; only the off-arm executes there.

**Adversarial arms (one beyond the author's range):** held-out seed 3 (build 2.67%, 71 cells, all bands hold), 3× horizon at 2,700 frames (cells 85→90→92 — **saturating, not linear**; build rate falls to 2.09%), 4× bodies at 192 (162 cells < 192 bodies — sublinear, the memory direction strengthens with scale). Nothing broke.

**Why silver, not gold:**
- **Novelty lineage uncited.** The direction is kick-jet gold 6c47's named prize ("the realizable prize is the QuantizedMemo, ~70×, a law change"), and read-stream 0355 (18 October, one day earlier) already benched the carried form — `from_shape(exact key, class shape)`, ~85% of compile deletable at 0.40 µs/hit, error p50 1.9e-6 via a 61×-finer class key. Genuinely new here: the **live** wiring, the feedback measurement (served stream explores 2× cells; live recurrence 0.898 vs census 0.947), FIT measured, off-arm inertness, saturation.
- **Under the 10× bar where it counts:** 30× on compile calls but 2.8× on the kick itself; and adoption is a law decision (B12/B13/B17 un-re-judged, eviction, memo.rs guard recalibration) — not one step.

**The gold rung:** fly the served law through the plane gates plus the belt cell census, pricing this 11+11 cell against 0355's class memo in the same run.
