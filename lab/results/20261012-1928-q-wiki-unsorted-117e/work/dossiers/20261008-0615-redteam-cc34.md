# Dossier — redteam-cc34: the resonance gate is an untested state switch

## Claim

The design's resonance gate (averaged kicks outside, exact/normal-form inside a fixed frequency tolerance, `law.md` #29) is the same structure the project already killed at the sphere of influence (events3): a state-selected switch; a 60-s float probe shows the true resonant reach is ≈1.9× the tolerance at e = 0.005 and ≈1.0× at e = 0.2, so no fixed width fits, and one chirp across the 2:1 at moderate e ends with an irreversible 33–69% eccentricity error against the truth — while no rung or gate ever crosses the boundary.

## Bottleneck

Not a compute bottleneck: a correctness seam under "kicks and cycle derivatives absorb perturbations" (premise 3 of the lens). It decides whether belt- and moon-scale history (resonant families, Kirkwood structure — principle 29, "history being made") can be produced by the cheap path, and it is also a p99 risk: under-triggering sends bodies into the dense order (350–700 steps/orbit) where one kick per orbit would do.

## Evidence

`python3 probe.py` (12 s, 1 core, ~30 MB; planar circular restricted 3-body, interior 2:1, μ = 3×10⁻⁴ — r4's range; truth = unaveraged RK4, convergence-checked at half step: labels stable, e_final 0.2248 vs 0.2251; "switched" = secular-averaged elements outside tolerance, exact integration inside — the design's best case). Tolerance W = 2.5·μ^(2/3) (r4 v3's half-width), i.e. ±1.0 W in a at the gate; slow drag chirps the particle across.

| case | truth reach (first e response) | gate at | e_final truth / switched |
|---|---|---|---|
| e₀=0.005, fast, λ_p 0/π | 1.83 W / 2.11 W | 1.14 W | 0.069/0.077, 0.084/0.076 (±11%) |
| e₀=0.05, fast, λ_p 0/π | 1.82 W / 1.92 W | 1.14 W | **0.060/0.102 (+69%)**, 0.105/0.099 |
| e₀=0.2, fast, λ_p 0/π | 0.94 W / 1.12 W | 1.14 W | 0.225/0.252, 0.246/0.241 (±12%) |
| e₀=0.05, slow (4×) | 1.90 W | 1.14 W | 0.116/0.132 (+14%), a_final −0.3 W |
| e₀=0.2, slow (4×) | 1.13 W | 1.14 W | **0.265/0.179 (−33%)**, a_final +3.2 W |

Labels (capture/pass) matched in all 8 cases — no capture occurred at these chirp rates, so the capture question stays open; the demonstrated damage is quantitative and irreversible (eccentricity is the belt's observable). The pre-registered kill criterion (labels and e_final within 25% everywhere → premise survives) is violated twice: fast e₀=0.05 (+69%) and slow e₀=0.2 (−33%). Full numbers in `probe-out.json`; method in `probe.py`.

## Predictions

`predictions.md` was written before the run. Held: outcome divergence >25% at held-out e₀=0.05 (69%, one of two phases); label agreement at e₀=0.005. Missed: my width prediction (island ∝ √e, ratio 0.5→3) — the measured *behavioural reach* is nearly flat in e (≈1.9 W at low e, ≈1.0 W at high), i.e. it tracks Wisdom's μ^(2/3) chaotic-zone scale, which a fixed tolerance *can* match with the right constant; the constant is then wrong by ~2× at the ends, which is what the outcome errors show. Reported as held-missed.

## Ranked attacks (ranked by player-visibility of the failure)

1. **The resonance gate (above).** Catcher: **none**. r4 v1–v3 and B17 sit at fixed detunings (inside ±W/3, or at 5.0/2.55/2.15 period ratios); nothing ever crosses a boundary, no metric reads the gate width or the crossing outcome. Propose r4 v4: chirp across 2:1 and 3:2 at e₀ ∈ {0.005, 0.05, 0.2}, two chirp rates, two phases; metrics: outcome-label match, e_final ratio, and reach/gate-width ratio; negative control: a fixed ±W gate with the reach measured per (E, L).
2. **`representation.md` is stale against the law** (premise 2's letter). Its "primary in-cell solution" (Minsky's in-band map, line 32) was killed on 30 September — "band-centre tangents carried a first-order slope error in every cell holding a turning point" (`law.md` #20) — and replaced by `space-darwin16-v1`, which the design doc never mentions; §7 promises r5/r6 rungs that do not exist; and `law.md` itself carries the contradiction (#29: average away from resonance, normal form near it; #30: "resonances need no special case, because the split keeps the resonant angle"). A fresh builder reading the design rebuilds the killed map. Catcher: none — a doc gate cannot exist; the fix is the rewrite the doc's own status line already owes (its falsifiers have run). Principle 11: one home per kind of truth; right now the two homes disagree.
3. **Two of the six lens premises have no frozen kill criteria.** r5 (dense/sparse bit-identity) and r6 (view gather) are named in `representation.md` §7 and `law.md` #88 as GLM's open rungs; no files exist in `lab/rungs/`. Both guard load-bearing claims with live evidence of stress: the tie-rule run (5 Oct) found order-one differences between two orders of one same-epoch batch, and the gather measured 83% of a light frame. Catcher: none, by definition — freeze the rungs.
4. **"Cost ≈ 0 for undisturbed bodies" (premise 6)** survives per-body (tube drift is zero work; B9/B10/B15 gate it), but the undisturbed body's *regime selection* is not free: candidate-pair setup at 2.5–24 µs per pair per element change with candidates per body growing ~linearly in N at fixed density (870 at 10⁴, 8,598 at 10⁵ — known, q-candidate-degree), and (from attack 1) a mis-tuned gate parks bodies in the dense order at ~10²× the kick cost. Catcher: B9/B10 measure per-orbit work but nothing measures *wrong-regime* cost.
5. **Premises that survive (worth reporting).** (a) Two-body EOB at 1PN, ν only in the energy map: a theorem at 1PN, confirmed by r3 v3 (1024/1024 precession, 632/632 periods, assists 64/64) and B11; the 2PN ν-potential terms that break it live in the comparable-mass strong field, oracle territory, not the plane's regime. (b) View uniqueness: arrival time is monotone in emission time (d t_arr/d t_em = 1 − β cos ψ > 0), so each visible tube crosses the past light cone once and Newton-from-the-frame tracks the primary image; multi-image lensing is deferred to deflection(b), gated for moving lenses by B16. Open sub-risk for r6: images are born/died in pairs at caustics, which per-image Newton roots cannot discover — one sentence in that rung when written. (c) Binet cells in their law form (Darwin-compiled cycles): m16/m32 pass every r1 criterion at ~38 crossings per cycle, with period and precession errors identical each cycle (≈10⁻⁶ at m16) — a calibration, not a walk; the right error type.

## What would make it wrong

The gate's width is not written in `law.md` ("p·Ω₁ − q·Ω₂ ≈ 0"), so my ±W reading is an assumption: with a ±2W gate the low-e under-trigger closes and only the cost side (over-trigger at high e) remains. But the reach measurements (1.9/1.85/1.0 W across e at fixed μ) are gate-independent: any *fixed* width is ~2× wrong at one end. Second: no captures occurred at my chirp rates, so if the game's crossings are all fast-and-low-e the labels may never diverge — the e_final errors stand regardless. Third: all of this is float and single-resonance; overlapping resonances or an eccentric perturber (forced e ≠ 0 in the averaged branch) could be better or worse; the integer law's own behaviour is unmeasured here.

## Cost of adopting

No new component: give the gate its e-dependence (the compiled frequencies already carry e; the reach or island width is one more memo field per cycle, set from the same measurement), or use the smooth-changeover machinery already adopted for SyMBA (law.md #30). Freeze it with r4 v4. Estimated cost: one rung plus a field in the cycle memo.

## Fit with PRINCIPLES

Principle 13 ("basically we don't want errors that can compound that's the goal"): an irreversible outcome difference produced by representation *selection*, not by the law, is the compounding type. Principle 22 ("the simulation tells us what's next not us, subtle but deadly"): a threshold heuristic is choosing a physics regime, not scheduling work. And the project's own precedent: events3 killed exactly this structure at the sphere of influence because "a state-selected switch … is not [symplectic]" — the resonance gate got the exemption without ever being crossed by a test.

## The lens

A red-team overweights exotic cases; I stayed inside the plane's own regime (μ = 3×10⁻⁴, circular, coplanar), but 60 s of float on one resonance cannot speak for the integer law, for eccentric/inclined perturbers, or for overlap chaos — and the dense-order fallback may simply be correct there, at a cost the allocator may or may not absorb. The doc-staleness attack (2) is the one with the largest expected value per hour spent, and it needed no compute at all.
