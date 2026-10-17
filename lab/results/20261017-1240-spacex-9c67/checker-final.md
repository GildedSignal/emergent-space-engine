Working...
Check complete. **Grade: silver** — written to `lab/results/20261017-1240-spacex-9c67/check.md`, with the author's wiki page corrected in place.

**What reproduced:**
- Probe `(35275, 39, 17643)`, coverage 99.89% — bit-identical on the runner's regen and my own clean rebuild of `work/patch.diff`.
- Digest + replay identity pristine vs patched: seeds 1, 7 (runner) plus my held-out **seed 42** and a **4× horizon (1,200 frames)**.
- Predictions pre-registered before the decisive artifacts; the POS_MISMATCH kill criterion fired and was honored.

**What fell:**
- **Timing:** my 6 interleaved pairs give −3.4% mean (5/6 negative); the dossier's −5.1…−6.0% doesn't survive (runner's own regen: −5.9/−0.4/+4.3). Also the author's seed-7 control moved +40% and went unreported.
- **The mechanism, inverted by my per-kind probe** (the decisive attack): mismatches are boundaries 17,442/17,442 (100%) and opens 108/162, **kicks only 89/17,667 (0.5%)** — the opposite of "rebinding kicks; opens/boundaries match". Magnitudes reach **677,571 root light-ticks**, not sub-quantum bits. Cause: `apply` walks at `event_time` (last binding anchor) while the resolver reads at the **item tick** — half a step apart on boundaries. The residual round-trip is exact by construction (`bind_in`: residual = exact − turn(decoded); `readout` re-adds), so the "fix the residual word → mismatch → 0" falsifier and open direction 6 were unfounded; I replaced them on the page. What survives is stronger than claimed: the pristine cache was anchor-stale by up to ~7×10⁵ light-ticks on 35% of events, and outcomes are blind even to that.

**Silver, not gold:** real deletion, honest kill of its own premise, but the run's claimed value (the exactness diagnosis) was wrong in mechanism, magnitude, attribution and falsifier until decomposed, and the gain is unmeasured on the belt scene 5ade priced (−13%). The one gold experiment: belt-wave measurement + folding the corrected mechanism in.

Tree restored pristine; the author's patch reapplies cleanly.
