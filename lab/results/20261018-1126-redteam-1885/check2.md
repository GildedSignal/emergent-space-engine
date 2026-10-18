Grade: gold

**Abstract (for the integrator).** Premise refuted, reproduced bit-exact: representation.md's aggregate view law ("aggregates are one sample each" L59, "≤ 1 sample per pixel" L116, "type × log k table" L58) is wrong wherever anything relativistic flies. At β 0.9/σ_β 0.03 one-sample sprites err 40% median (p90 86%), strobe 58%/frame, 196 samples per aggregate for a 5% bar; at β 0.99/σ_β 0.01 the top 1% of members carry 37% of seen flux and the bar needs 1.7×10⁴ samples. The failure is a closed form in s = γ²σ_β, boundary σ_β* = 0.005/γ². My arms confirm at γ 22.4, receding, bounded and bimodal dispersions; belt regime safe (B18's blind side). Adoption: amend L58/59/116 + one seen-flux rung; no engine code. One domain note: the observer arm reads one aggregate per crowd.

## Reasons

**Reproduction.** `sh regen.sh` exit 0, 3.6 s; every number in the dossier's table matches `results.json` (bit-identical file after regen: controls −0.0772/−0.5123 vs closed forms −0.0769/−0.5132, Newtonian 628×, belt zeros, all fleet/observer rows, p90s 86/121/100%, tail 37.2%/13.6%, n@5% 19/196/799/16 788). Quotes of L58/L59/L116 are verbatim in the tree; the sentence is original to the coherent design (cd912a46), not a stray line.

**Physics, verified independently.** k = 1/(γ(1−β·n̂)) = e^φ for LOS approach is exact (γ(1−β) = e^−φ); dφ/dβ = γ²; E[k⁴] = e^{4μ+8s²}, CV(k⁴) = √(e^{16s²}−1), log-word miss = e^{8s²} — recomputed, all match; k⁴ bolometric beaming and k·T colour are standard; d ln k/dθ = β sinθ/(1−β cosθ) checked against the θ=0 row. The rapidity-Gaussian fleet is the physically natural model (a comoving Gaussian stays Gaussian in φ under boosts).

**Predictions.** predictions.md predates falsifier.py and results.json (mtimes 23/16/13 min; runner log order agrees); the scorecard reports one conservative miss (90% predicted vs 63% measured at s 0.263) — post-hoc fitting does not look like this.

**My five adversarial arms** (`/tmp/check2-adv.py`, 2 s):
1. **Outside the swept range (γ 22.4, β 0.999):** s = γ²σ_β holds to the digit — σ_β 10⁻⁴ c → s 0.050 → 13.6% one-sample; 3×10⁻⁴ → s 0.15 → 38.4%; closed forms exact at s ≤ 0.15, 10% at s 0.5 (as the dossier itself states). At γ 22 the boundary is σ_β* = 10⁻⁵ c.
2. **Receding** mirrors approach (40.3% vs 40.0% at s 0.158): the approach-only sweep is not a loophole.
3. **Bounded uniform rapidity** at s 0.263: one-sample 72.5%, strobe 1.07 — worse than Gaussian. Shape-robust.
4. **Bimodal formation** (two squadrons at β 0.85/0.90, zero internal dispersion): 41% median error, 2.37× square-wave flips. Even a two-value crowd breaks the readout. (Instrument nuance: median |Δln F| reads 0 for bimodal crowds — the >2%-visible fraction is the right statistic there; the author's unimodal arms are unaffected.)
5. **Velocity-Gaussian (β-space) dispersion:** far worse (s +17–29% over γ²σ_β, top-1% flux share 96–100%, sampling unrecoverable) — confirms the first checker's page block in direction; the author's parameterization is the premise's *most favourable* case, so the table is a lower bound.

**Novelty.** No HISTORY entry or wiki page measures the aggregate seen-flux readout; the view topic's runs are per-emitter cost; 2fa4's "no gate judges a seen value" is per-emitter expressibility — the dossier cites it correctly and extends it to aggregates with magnitudes. The occlusion-sprite work on this page is a different sprite. lab/rungs has no seen-value gate.

**Goal fit.** Principle 20 ("averages crush data especially tail events") made physical: 37% of what the player sees rides on 1% of members, drawn 1% of frames. Principle 12 (smoothness): 5.7×/frame brightness jumps. Principle 2 (error type over size): a point k cannot express a crowd's k⁴-moment. The regime where it breaks is the goal's own sentence ("feel what living at high c would feel like"), and the run prevents freezing a readout law that is guaranteed-wrong there — "gates are frozen before the first run and never weakened after."

**Gold path:** a design premise of record is shown wrong, with closed forms, controls on both sides, reproduction bit-exact, held-out predictions held, and adoption within one step (doc amendment + the freeze-ready seen-flux criterion; no engine code — the aggregate path is not wired above β ≈ 0 today, which is why this is cheap now and expensive after a freeze).

## What the author missed

1. **The observer arm's domain.** Its σ_θ = 0.05 rad is the whole crowd's span in one sample — the letter's own reading ("aggregates are one sample each"), but if aggregates were re-clipped per pixel, σ_θ per aggregate is bounded by the pixel FOV (~1.5 mrad) and the pure-angular observer arm falls to 0.4–0.7% at β_O 0.9 (measured). The LOS-dispersion fleet arms are untouched by clipping (velocity dispersion survives pixel subdivision), so the refutation stands on them; the claim's "the player's own motion alone" sentence should carry this domain note. Recorded on the page.
2. **Sticky sampling.** The strobe assumes the sample is re-drawn per frame; a per-aggregate sticky sample would trade the strobe for a persistent 40–92% error (still refuting) plus staleness under membership churn. Unpriced.
3. **Prose slips:** the boundary at β 0.5 is 0.4% of c, not 0.7% (conservative direction); "closed forms verified ≤4%" overstates the strobe form (6–10% at s ≥ 0.25; exact coefficient 3.82s, not 4s — corrected on the page); the scorecard line "observer arm 12% predicted vs 12.3% measured" matches prediction 8's *strobe* number against the measured *one-sample* number (measured strobe is 16%); the dossier's rung sentence is truncated mid-line ("and its frame-to-("), complete on the page.
4. The cure it names (tracked observer-dependent k-moments) is unpriced — the natural next run, and the design's own "compute only surprises" answer.
