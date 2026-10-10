Working...
Check complete. `check.md` written with **Grade: gold**.

**What I did (30 min budget):**

1. **Reproduced exactly.** Applied `work/patch.diff` to the pristine tree, rebuilt offline, reran all three scenes. Every dossier number regenerates — and CTRL matches the crate's published frozen evidence bit for bit (enc 2093, pairs 44850, steps 15,948,922, fine 180,897 = `verify.jsonl` line 16; spec+seed confirmed as `main.rs`'s `coorbital`, s+9=20261010).

2. **Validated the new instrument.** RETRO's mirrored march is author-written code, so I re-derived 37 sampled pairs (102 events) with an independent numpy Kepler solver + two-stage scan: all 102 reproduced, zero spurious minima. Dup=0, distinct events confirmed.

3. **Ran three adversarial cases of my own:**
   - **Seed 20261013**: cross 44.1%, ≤17.0% coverage at W=1–10, 99% needs 537 certs/enc — structural, not seed luck.
   - **warm1 — single warm fleet, one group**: 22.2% at W=1, 99.4% only at 428 certs/enc. This isolates the e-spread layer from cross-group effects and closes the "just scope per-group" escape: the e-gate is load-bearing even inside one group. The author missed this isolation; it makes the finding *stronger*.
   - **pro12** (retro unmirrored): 4564 vs 71,923 enc = 15.76×, matching the claimed 15.5× head-on density.

4. **Predictions**: file times consistent with pre-registration; kill criterion pre-registered and decisively met (≤26 certs/enc buys ≤17.6% coverage). The one material miss (cross ≥95% predicted, 43.7% measured) is disclosed and actually strengthened the finding via the intra e-crossing layer.

5. **Novelty/goal fit**: no prior H entry covers multi-population, retrograde, or e-spread rank stability; the attacked build is queued, so this is the required pre-freeze red-team. Premise shown wrong with the crate's own truth; fix (cold-group scoping + e-gate + envelope tier + two gate scenes) adoptable in one step.

Tree restored to pristine (`git status`: only untracked `lab/results/`); nothing else in the run folder touched. Minor dings noted in check.md: the 10⁶ extrapolation constant is ~4× off (6.3e-6, not 1.5e-6), and retro's "200×" is extrapolated rather than measured at that window.
