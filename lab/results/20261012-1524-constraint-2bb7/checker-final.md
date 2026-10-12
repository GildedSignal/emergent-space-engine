Working...
Check complete. **Grade: gold**, written to `lab/results/20261012-1524-constraint-2bb7/check.md`; tree restored to clean, nothing committed.

**What I did:**

1. **Reproduced** from a clean tree with `work/patch.diff` applied: the decisive m2000/rtf100/seed-1 rerun returned the **identical digest** (`a3216476…`), view share 78.0% vs the author's 72%, engine budget-capped at 5.3 ms, gather 7.6 µs/emitter — my absolutes ~1.5× theirs from box load, exactly the regime their "shares, not absolutes" caveat covers. All six dossier table rows match the saved JSONs; predictions.md (15:26:55) predates every decisive run (15:27:04+).

2. **Three adversarial cases, all supporting the claim:**
   - Fresh held-out **seed 4**: 86.2% below display quantum (above their 75–78% band).
   - **10× tighter quantum** (1e-5 rad / 1e-4 shift, my own instrumentation edit, digest still identical): 74.6% — their named "wrong if" does not bite.
   - **m480 mid-scale**: 50.3% below quantum, view share 70% — freeze fraction is scene-dependent, but the constraint *ranking* holds at every scale.

3. **Novelty/goal fit:** no HISTORY entry measures the view's frame share; the board's queue (`b-readout-cost`) rests on the premise this run falsifies, and the measured gather is a live violation of plane.md §7's own "no unbounded synchronous claim on the frame… or a gather".

**Misses recorded for the integrator:** the ~4× cadence saving is inferred (below-quantum counts), never demonstrated with a built cadence; the "same scene" 15% rtf-1 figure is actually members-400; the engine's ≳1.7k saturation point is load-sensitive (wall-clock budget) though the ranking is structural in the code; and the counter-intuitive rise of the freeze fraction with rtf (15→41% at fixed members) is unexplained — a cadence gate must not lean on a late-battle phase artifact.
