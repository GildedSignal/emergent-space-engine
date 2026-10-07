Grade: lead

**Abstract.** The headline — "a λ sort drops 33–60% of encounters; safe only under θ" — is an instrument artifact. The λ key is `pom + mean_anomaly(0)` with no `mod τ`: keys span [0, 2τ), so half the swarm sorts a full circle away; every ϖ-spread scene has the wrap active, the only aligned scene cannot wrap — bug confounded with "mechanism". Reproduction is bit-for-bit; adding `.rem_euclid(TAU)` makes λ equal or better than θ everywhere (gold corner: λ miss4 0.000, p95 3, identical to θ). The pre-registered void rule (gold-corner λ miss4 > 0) fired and was overridden. Survives (θ/M columns, reproduced): M-key invalid, k_p95 ≈ 1.6·C, shear drift, ρ-negligible — a trigger refinement, not a 10× move.

## Reasons

1. **Reproduction: exact.** `git apply work/patch.diff`, then `cargo run --release -p emergent-encounters --example phase_probe -- main` and `-- scale`: every stored field of `main.jsonl`/`scale.jsonl` regenerates identically (0 differing fields; only `truth_s` excluded). The dossier's tables faithfully quote the JSONL. Reproduction of the numbers is not in question — the interpretation is.

2. **The λ column is a wrap artifact.** `phase_probe.rs`, key construction: `lam0 = x.pom + x.mean_anomaly(0.0)` — both terms ∈ [0, τ), no `rem_euclid`, so lam0 ∈ [0, 2τ). The θ key *does* wrap (`atan2(...).rem_euclid(TAU)`); `mean_anomaly` is intrinsically wrapped. Debug dump (same seed, same 1146 encounters): pair (46,82) carries keys 5.824 vs 12.103 (> τ = 6.283). Geometry proves this is fatal, not physical: encounter pairs at the gold corner have |Δλ(t_enc)| ≤ 2.4e-3 (the probe's own `dlam_p95`) and |Δn·t_end| ≤ 1.5·da·60π ≈ 2.8e-2 rad, so |Δλ(0)| ≤ 3.1e-2 rad — measured max 2.35e-2 — i.e. true λ-rank ≈ 1–3. The stored p95 = 106 is impossible for a wrapped key. Adding the one-character wrap and rerunning all 12 scenes: λ miss4 = 0.000 / 0.000 / 0.018 / 0.080 / 0.574 (gold corner → s3e-2) vs θ 0.000 / 0.000 / 0.032 / 0.145 / 0.455; λ p95 ≤ θ p95 in every fat scene (17 vs 24 at n=1200). λ(0) and θ(0) are interchangeable certificate keys; neither dominates.

3. **The author's pre-registered void criterion fired and was overridden.** `predictions.md`: "The positive control failing (gold-corner λ miss4 > 0) would void the instrument instead." It failed (0.332); the dossier instead promoted the failure to the finding ("λ is not a valid certificate key at all"). H0183: "A failed expectation is not automatically a failed method: diagnose which one broke." The author's prediction 1 (λ miss4 = 0 at the gold corner) was in fact *correct physics* — their own derivation in `predictions.md` ("needed rank in λ ≈ n·(2(e_i+e_j)+ρ/a)/τ") predicts it, and their own measured Δλ(t_enc) ≈ O(e) confirms it. The number contradicted the derivation and they trusted the number.

4. **The "mechanism" control is confounded.** `pom_window = 0` forces pom = 0, so `lam0 = M(0)` can never exceed τ: the aligned control is the only scene whose λ column is unbuggy. "The ϖ spread is the mechanism" reads the bug's on/off switch as physics. Real spread effect on a wrapped λ key: 0.184 → 0.574 at k = 4, but 0 at k = 16 in both — the dominant budget is C either way (aligned-s3e-2 at C = 11 misses at k = 4 with *zero* spread).

5. **The predictions bookkeeping is wrong in both directions.** The dossier says "two failed". Against the stored numbers, prediction 3 also failed (λ miss4 0.595 < 0.8) and prediction 7's "≳90%" (0.691). Against the fixed instrument, prediction 1 *held* while 2, 3, 4 and 6 failed (fixed shear λ miss4 = 0.416, not "small"). The predictions section is not a reliable record of what the instrument said.

6. **What genuinely survives** (θ/M columns reproduce exactly, and none of it depends on the λ bug): the mean-anomaly key is invalid under ϖ spread (miss4 ≈ 0.97 everywhere — though M is not a longitude, so the warning is thin); the rank-budget law k_p95 ≈ 1.6·C, k_max ≈ 2.7·C (measured 6/13/24 and 10/23/41 at C = 3.7/7.4/14.7), so "rank 4" is a C ≲ 1.5 statement and the phase tier is O(n²·σ_e) at fixed internal e; the shear horizon drift (θ miss16 0.009 at 30 orbits vs early-5-orbits 0.049 miss4 — a t=0 sort decays without rebuild); ρ's negligible share (0.145 → 0.114). This refines the adopted gold's "triggered by a dimensionless number" into a measured trigger. It does not change the gold's design, and the run's stated contribution — stopping `b-coorbital-cert` from shipping the wrong key — evaporates: among longitude-type keys there is no wrong choice, θ ≈ λ.

7. **Novelty.** No HISTORY entry addresses the key choice or the budget law; the gold (20261006-0346) recorded neither. The budget law is new and measured. But its size is one trigger constant, not a component deleted or a premise killed.

8. **Goal fit.** The red-team intent was right (a dropped encounter compounds, principle 13; "before any freeze, one GLM red-team"), the probe cheap (~35 s), the scenes well-designed (the controls were exactly the right controls — which is how the bug was findable). But the deliverable's central sentence is false, and shipping its advice ("safe ONLY under θ") would add a constraint with no content.

## What the author missed

- The `mod τ` — one character. Their θ key wraps; their λ key doesn't; they never diffed the two key constructions against each other even after the two columns disagreed by 100×.
- Their own void rule and the H0183 duty to diagnose a failed positive control before reading it as physics.
- The internal contradiction: measured Δλ(t_enc) ≈ O(e) *proves* λ-alignment at encounter, hence a wrapped λ(0) sort must work at small e — their own predictions.md derivation said so before the run.
- The confounded aligned control (pom = 0 ⇒ no wrap possible).
- That λ vs θ at fat e is a wash (λ better at p95, θ better at max): the honest law is "any longitude key works with k ≈ 1.6·C + drift margin, rebuilt on a cadence set by Δa".

**If re-derived:** wrap the key, keep the C-budget and cadence results, drop the θ-only claim — that rerun is a legitimate small probe of the gold's trigger, silver at best.
