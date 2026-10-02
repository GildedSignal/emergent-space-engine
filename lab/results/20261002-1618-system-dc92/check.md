Grade: silver

**Abstract.** Claim: the cells' β rule is β = −∇χ with |∇χ|² = −2Φ, the eikonal of the additive potential; three of the contract's four requirements become theorems. Reproduced: every stage bit-identical except table build wall-times. Verified beyond the author's regime: the contract's law is exact Painlevé–Gullstrand geodesic motion (mass shell), so one-mass exactness holds at p/M = 15 (+2.5×10⁻⁴ vs exact, where 1PN errs −31%); curl 1.7×10⁻¹⁷ one-mass; Newtonian-exact composition to 2×10⁻⁵. Not decided: the two-mass 1PN requirement — the decisive ratio 1.26 carries ±30% noise and the ν-scaling prediction was never run. Gain: deletes the β-rule design space and curl enforcement. Adoption: a law-text edit, then rung 2.

**Reasons.**

1. **Reproduction.** `run.py ctl` bit-identical; `run.py main` identical except `table_s` (26.9→27.4 s, 22.4→25.0 s); `decisive.py` (92 s) and `analyze_final.py` bit-identical. No patch to apply. Commands as given.
2. **Predictions.** `predictions.md` (43 min before `results-decisive.json`) pre-registers held-out cases. (1) pipeline = analytic: held. (2) eikonal identity 7×10⁻⁷: held. (3) |S| < 0.5×6πM/p: nominally held (S = 0.038 = 0.27×) but inside the ±0.05 rad slope noise — the author says so. (5) negative control: held (plunges to r ≈ 1.4, advance −0.48). (4) the ν-scaling probe was **not run** — a pre-registered held-out case left undelivered, disclosed.
3. **Adversarial, beyond the author's cases.**
   - *Mass shell (new):* H = √(1+|p|²)+β·p satisfies g^{μν}p_μp_ν = −1 for the PG metric exactly (numeric inverse, random states). So the contract's equations are exact geodesic motion in PG coordinates for *any* exact flow — the "not a truncation" claim is structural, and gravity-law.md's equations are independently validated.
   - *Strong field:* one-mass eccentric orbits, apoapsis-tracked: p/M = 15, e = 0.25 → law 1.83353 vs exact 1.83307 (+2.5×10⁻⁴) while 1PN sits −31%; p/M = 31.5 → +3.8×10⁻⁴ vs −15%. The claim survives a field 10× stronger than tested.
   - *Control B re-derived:* realized turning points (3.600, 5.479) (the stored `rmax` is pericenter scatter); law vs exact +4.2×10⁻⁵, 1PN −3.1%. Dossier's one-mass numbers check out.
   - *Newtonian-exact theorem:* p ≡ 0 is invariant (dp/dT = −(∇β)ᵀp), and −H·β = −∇Φ pointwise to 2.4×10⁻⁷ over 72 points (relative ~2×10⁻⁵, pipeline accuracy).
   - *Curl:* 1.7×10⁻¹⁷ one-mass (the dossier's number is real); two-mass 2.9×10⁻⁹ at r = 4.5, 3.8×10⁻⁵ at r = 1.2.
   - *Caustics (the named blind spot, now located):* the θ→angle map has zero folds at r = 4.5 and 1.2, but 138 backward steps at r = 0.6 (218/1024 rays never reach) — β is multi-valued there. The tested orbit (rmin = 3.52) is safely outside.
4. **Novelty.** No eikonal/Maupertuis/Jacobi-action composition in docs/HISTORY.md, docs/, git log or other lab results. It answers gravity-law.md's open question (line 41) at premise level; the ray-bundle field record extends rule 11's idea. Not previously tried.
5. **Goal fit.** Board bottleneck 1, premise level, as the dossier says: the β-rule design space and curl-free enforcement collapse into one scalar identity — PRINCIPLES #7 ("Multipoles are the mechanism"), #32 ("under the right representation many symmetries appear"). Floats explore; no integer decision claimed.

**Why silver, not gold.** The contract's fourth requirement — the two-mass 1PN behaviour, rung 2's actual judgment — is undecided: the decisive correction 0.186 rad/orbit vs monopole 0.148 carries ±0.05 rad slope noise (the Newtonian peri-vs-apo spread alone is 0.05) and a flagged 7.5% L-drift from ray-selection outliers, which I confirm are real (cold-start queries land on wrong rays, β spreads up to ~1.0). Gold requires the composed rule to be *judged*, not plausibly ordered.

**The one experiment.** Run the frozen 1PN/EIH oracle (H0178 protocol) on these same scenes, plus the already-predicted ν-scaling probe (M₁M₂ at fixed M_tot), with the ray-selection outliers fixed (verify query branch/convergence, or densify the table near the fold). That decides whether S = 0.038 is a real cross term; everything else is already proven.

**What the author missed.**
- The strongest support went unstated: the law is exact PG geodesic motion (mass shell), making one-mass exactness structural — and the one-mass control should have run at p/M ~ 15, where 1PN fails by 31% and the control actually discriminates, instead of p/M ≈ 132 where 1PN is already within 3%.
- The ~10⁻¹⁷ curl quote is a one-mass number placed in a two-mass claim; two-mass is 10⁻⁹ at the orbit radius (still negligible) and 4×10⁻⁵ at r = 1.2, near the fold boundary. The rule's domain needs a stated inner boundary: folds begin near r ≈ 0.4× the mass separation from a source.
- No null test of the composed flow (light deflection/capture, contract B4); exact for one mass by the mass-shell argument, untested for two.
- `results-ctl.json`'s `rmax` fields are pericenter scatter (the `advance()` quirk the author knew from `analyze_final.py`) — misleading to any later reader; apoapsis should have been recorded.
- The rest-release theorem is about acceleration: a river body at u = 0 moves at β while a Newtonian body at rest does not, so position comparisons need the β-drift removed.
- Adoption cost beyond the doc edit is unstated: the pipeline is a float probe (~10⁴ queries per 20 orbits, 27 s table build); "(moments, ray bundle)" as a cell field record is a sketch, not measured.
