Working...
Check complete. `check.md` written to the run folder: **Grade: silver**.

**What I did:**
- **Reproduced** in a clean tree: `fermi_budget` regenerates bit-for-bit (all sinks, knot counts, memo collapse, cycle bytes; timings ±3%); `jet_anchor` digests, stream caches, and every deterministic table row identical, timings ±10% load noise.
- **Timeline verified**: `predictions.md` 15:12:48 precedes bench1 15:31:15 by 18.5 min; the prediction failures themselves (P5 off 25–50×) rule out tuning.
- **Four adversarial cases**: different spans (rates stable, jet rtf 168–233), seed 2 (hauler ρ 0.007 vs 0.001 — conclusion holds, jet rtf 191–229), escaped-tail recompute (rtf ≈ 13 at 10⁹ — the debris tail genuinely doesn't close), and a full arithmetic audit of the identity (every row recomputes; the "rtf 133" hand-calc is ~150 at its stated inputs — direction unchanged).
- **Novelty/goal fit**: no prior measurement of re-anchor rate, per-class cadence, `crossing_state` on plane entries, or the cold-store floor; moves board #3/#5.

**Why silver, not gold:** the decision-level claim (jet closes rtf 100 at 10⁹ with ~2× margin, refuting the original's "1.6× short" favorably) is reproduced and robust across span, seed, and the whole ρ band — but three of eight held-out predictions failed (P1, P2, P5), and lab precedent bars gold on failed held-out predictions. P5's band even contradicted the red-team's 730-kick bound the author itself cites. The named gold experiment: measure the re-anchor rate by law.md's own drift-floor criterion (√(floor/C)), not the stickier quantized-cell proxy — the run's own numbers show the two disagree at the factor-2 level (0.0005–0.001/kick measured vs ≥0.0014/kick bound).
