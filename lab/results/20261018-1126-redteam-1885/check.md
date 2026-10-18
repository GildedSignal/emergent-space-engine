Grade: gold

**Abstract (integrator).** Premise refuted, reproduced bit-identically: representation.md
L58/L59/L116 ("Aggregates are one sample each… a type × log k table gives the sprite") is
wrong wherever anything relativistic flies. At β 0.9/σ_β 0.03 the one-sample sprite errs
40% median (p90 86%) and strobes ×1.79/frame; at β 0.99/σ_β 0.01 the top 1% of members
carry 37.2% of seen flux (17k samples for a 1σ 5% bar); the player's own β_O 0.5 suffices
on a zero-dispersion crowd. Closed forms in s = γ²σ_β; boundary σ_β* = 0.005/γ²; belt
regime (B18) safe. My attacks strengthen it: velocity-Gaussian fleets are worse (top-1% →
98–100%), and at γ 22–71 the boundary falls to 10⁻⁵–10⁻⁶ c. Gain: stops a wrong readout law
being frozen (principle 20 made physical). Cost: doc edit + one float rung; no engine code.

## Reasons

1. **Reproduction.** Clean-tree copy, `python3 falsifier.py`, 3.4 s: table and
   `results.json` bit-identical to the author's (md5 eab63ede…); `regen.sh` exit 0.
   Every dossier number I spot-checked (p90s, strobe linear factors ×1.79/×5.65, tail
   0.1% = 13.6%, n@5% 196/799/16,788, Newtonian 628×, belt zeros) is in the artifacts.
2. **The letter, not a strawman.** L58/L59/L116 verified verbatim at base a63c446, in
   context (§2 observables, §6 cost table). Both natural readings of "which k does the
   aggregate carry" are instrumented and fail (one sampled member; one shared log-word =
   geometric mean, per-arm asserted against e^{−8s²}−1, 12/12 within 0.02). The
   derive-from-the-program reading is addressed honestly: it is the design's own cure for
   smooth programs and cannot carry real fleets (member velocities are individual states;
   k is observer-dependent).
3. **Physics sound.** k = 1/(γ(1−β·n̂)); ln k = φ exactly for approach (γ(1−β) = e^{−φ});
   k⁴ bolometric (I_ν/ν³ invariant); T_obs = kT. My independent receding arm matches the
   closed forms to 0.001 (logword −0.425 vs −0.426; CV 1.41 vs 1.43); σ_φ = γ²σ_β
   confirmed on LOS+transverse draws (s 0.0538 vs 0.0526 predicted).
4. **Predictions.** `predictions.md` (11:33) predates the decisive artifacts
   (falsifier 11:40, dossier 11:42); run.log is empty so strict log-order is unprovable,
   but the priors are analytic, 9/10 held, and the one miss is reported and conservative
   (predicted 90% one-sample median at s 0.263, measured 63%). One loose scorecard
   mapping: "observer 12% predicted vs 12.3% measured" compares the strobe prediction
   with the one-sample median; the measured strobe there is 16.4% vs 12% predicted —
   same conclusion either way.
5. **Adversarial cases (mine, incl. outside the swept range).**
   - γ beyond the grid (β 0.999, 0.9999; direct truncated-β draws): failure persists and
     the boundary collapses — σ_β* = 1.0×10⁻⁵ c at γ 22.4, 1.0×10⁻⁶ c at γ 70.7; a mere
     0.03% c dispersion at β 0.999 already gives s 0.18 (strobe ~70%/frame).
   - Parameterization: a Gaussian-in-β fleet is **not** lognormal in ln k (artanh
     curvature): measured s runs 17–40% above γ²σ_β, CV(k⁴) reaches 165–609 where the
     closed form gives 0.9–2.3, top-1% share 98–100% at the author's own flagship
     σ_β. The author's rapidity-Gaussian (additive, unbounded — my naive β-Gaussian even
     drew members past c) is the defensible and *conservative* choice; the headline
     numbers are lower bounds.
   - Geometry: receding arm symmetric exactly (above); transverse-only σ 0.05 at β 0.9
     gives s 0.0139 — "second order" as the dossier's caveat says, but still ~3× the
     2% visibility boundary: even the second-order channel strobes at battle dispersion.
   - Sample-bar semantics: n = (CV/0.05)² is a 1σ scale — at n = 817 (s 0.263), 31% of
     600 trials still exceed ±5% (p99 |err| 14%); the author's own p99-within-5%
     criterion needs ≈ ×6.6 (5,422). The sampling fix costs more than the table says;
     the premise dies harder.
6. **Novelty.** No prior run measures the aggregate readout: the census's §2 attack
   (e59e) was opacity; view.md (47 runs) holds nothing on sampling or beaming moments;
   2fa4's "no gate judges a seen value" concerned member colour (cited honestly, extended
   with magnitudes); HISTORY.md has no entry. L58/L59's readout law was unowned.
7. **Page.** Faithful — every new line matches the reproduced instrument; the Refuted
   entry and direction 6 (freeze-ready criterion) are exactly the evidence. I added one
   checker paragraph (parameterization robustness, boundary collapse, 1σ-vs-p99, ln-vs-
   linear strobe convention); nothing reworded. Note for the integrator: the NEW block
   sits above the "## Current best" heading (schema wants sections in order) — a
   placement matter for the publish step, not content.
8. **Goal fit.** Shows a design-doc premise is wrong in the goal's flagship regime, with
   controls on both sides and closed forms — principle 20 ("averages crush data
   especially tail events", made physical: 1% of members = 37% of what the player sees),
   principle 12 (smoothness: per-frame jumps to ×5.7), principle 2 (error *type*: a
   point k cannot express a k⁴-moment), principle 19 (the moment/rapidity integral is
   the water for this fish). Standalone float is the lab's established pattern where
   shipped code cannot express the regime (gravity-news.md L239 records the same wall;
   view.rs draws members individually — no aggregate path is wired, so adoption is a doc
   amendment plus one rung, before the letter freezes).

Gold clause met: "shows that a premise is wrong," reproduced, held-out predictions held,
adoptable within one step.

## What the author missed

- "Fleet model exact, not a toy" overstates: exact *in the rapidity parameterization*;
  the σ_β → γ²σ_β labeling is first-order, and the β-Gaussian fleet at the same σ_β is
  worse in every metric (my attack 5b). The claim survives strengthened; the wording
  should say "conservative lower bounds."
- Convention mix in the strobe column: median |Δ ln F| printed as "%" in the text
  ("58%/frame" is ×1.79 linear) while other rows give linear multiples ("2.6×", "5.7×").
  All conservative-direction.
- The "samples for 5%/2%" columns are 1σ scales; the proposed criterion is p99 —
  inconsistent by ×6.6.
- Transverse-only battle dispersion (σ 0.05) still crosses their own 2% visibility bar
  (s 0.014 > 0.005): the "second order" caveat is not a safe harbour either.
- The moment-tracking cure (incremental Σkᵖ per aggregate vs observer state) is named
  but unpriced — the author flags this; it is the one buildable follow-up and may be
  cheaper than any sampling count.
