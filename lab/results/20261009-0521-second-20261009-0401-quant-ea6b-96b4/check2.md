# check2 — 20261009-0521-second-20261009-0401-quant-ea6b-96b4

Grade: silver

**Abstract.** Claim: with timers on the sampled path, a real kick is 84.6% rebind (not 59.3%), mean 79.4 µs (not 52.6), cadence 1.32×10⁻² kicks/active ship/game-s (not 1.5×10⁻³), capacity ≈9.5×10³ ships/core at rtf 100 (not 1.3×10⁵; gap to 10⁹ ~5 orders/core). I reproduced everything from a clean tree at a838a28: digests bit-identical (m2000 `ca74ff5a…`, memo q-hit 0.970988618611917, 260/8962, ships_mean 231.7017, cadence 0.0132239, refused 0), shares within 0.3 points (84.5–84.8% bench and engine phase), units audit exact, cold/warm 1.39× with rebind 1.20×. My clean-binary m2000 digest control proves the patch inert at the decisive workload. Not gold: prediction 4 (mean band 40–60 µs) failed, and the patch hides an undisclosed 9-line engine change. Cost to adopt: board pricing only.

**Reproduction** (my runs, load 0.96–1.66 vs author 0.3–0.9; timings shift ≤2%, all deterministic fields bit-identical):
- Clean default bench: `dac49af387662466` == patched default (23 samples = 11 legacy + 12 clock, as predictions.md states).
- Clean m2000: replay digest `ca74ff5a7b71f200` AND plane digest `f4876d97…` identical to patched — **my control, stronger than the author's**, who compared clean vs patched only at default args.
- Patched warm/repeat/cold/rtf1 (exact dossier commands): legacy rebind 84.5/84.6% (bench), engine phase 84.8/84.7%, clock path 59.0/58.2/59.5%, gather 8.8%, readout 4.9–5.0%, forces 1.4%, other 0.3%, no-fire 0.04%; made 35.5–35.8 µs, leavers 70.1–70.2 µs, mean 79.8–80.7 µs, median 67.1–67.3, p99 384–388.
- Units audit from the author's own record: 9180 × 79.30 µs = 727.99 ms = legacy_total_ns; 9213 × 76.17 µs = 701.75 ms; capacity 1/(79.30 µs × 1.3224×10⁻² × 100) = 9.54×10³/core, 3.8×10⁴ on 4 cores. Exact.
- Cold/warm paired: 93.70/67.25 = 1.39× (author 1.40×); per stage rebind 1.20×, gather 1.37×, readout 2.82×, forces 3.24× (author 1.20/1.34/2.78/3.14).
- The rtf-1 "first-handout, median 384 µs, n=3" regenerates: author's kick-warm-m2000.json `kick_us_leavers` = {median 384.018, n: 3}.
- Bit-identity with the prior run's saved JSONs holds for every shared deterministic field (digest, memo, samples, refused); only new patch fields and machine noise differ.

**Predictions.** File times corroborate the claimed order (clean-baseline 05:25 → patched-baseline 05:30 → predictions 05:31 → decisive runs 05:36+), and the content knows only the default-args split. 6 of 7 held (population 99.87%, rebind >75%, ordering, no-fire, cold/warm band, clock 55–65%). Prediction 4 failed (mean 79.4 vs 40–60 band) — honestly reported, and the failure itself diagnoses the prior run's wrong-path mean. By the letter, gold requires the held-out predictions to hold.

**Adversarial cases.**
1. Clean binary at m2000 (above): the patch, including its hidden hunk, is inert on the decisive scene.
2. `--members 500` is bit-identical to m2000 (same digest, 9192 samples, ships_mean 231.7): the scene is handout-rate-bound; "members" above the rate is a no-op knob, so "2000-target, 232-active" under-describes what sets 232.
3. Early fill (`--seconds 10`): rebind 86.3%, cadence 2.10×10⁻², mean 89.5 µs.
4. Late fill (`--seconds 45`): rebind 83.8%, cadence 1.08×10⁻², mean 75.1 µs. The portable claim (rebind ≈84–86%) survives; cadence is fill-phase-dependent and still drifting at window end, so 9.5×10³ is a mid-fill figure inside a ≈5×10³–1.2×10⁴ band (the dossier discloses the fill caveat).

**Novelty.** No HISTORY entry carries these numbers. Closest: H0212/H0213 (the memo hit-rate artifact — frequency, not time share), the 6 Oct gold components-4643 (encounter-setup share, a different tier), and the board's "recompiles an orbit on ~99% of kicks". The 85% share confirms a probe the prior run's checker already had (per predictions.md); the new load-bearing results are the cadence/capacity correction (13×, premise of the prior claim shown wrong) and the per-stage cold/warm split (rebind compute-bound, the small stages memory-bound).

**Goal fit.** Board focus line 1 (kicks dominate the engine's cost) and the top-scaling framing; PRINCIPLES 10 ("measure before claiming") is the run's own thesis, PRINCIPLES 1 the lever it re-prices. Timings are honestly caveated as cloud x86, orders of magnitude; digests and counts carry the canonical content.

**Why not gold.** (a) Prediction 4 failed — the clause is explicit. (b) `work/patch.diff` contains an undisclosed 9-line **behaviour change** in `kick_clock`: crash scheduling at the next periapsis (`What::Crash` at `tp`) replaced by immediate death (`alive = false; Resolved::Lost`). The dossier calls the patch "instrumentation only … digest-proven inert" — inert on every scene run (my clean-binary m2000 control covers the decisive workload; a taken branch would break digest identity), so no number is contaminated, but a law-adjacent edit must be disclosed, and it must be stripped before anyone reuses this instrumentation.

**The experiment that would make it gold.** Re-run with a timers-only patch: (i) cadence/capacity measured on a filled fleet at steady state (not mid-fill — my s45 shows it still drifting), (ii) a law-v2 clock-body bench with its own sampler (12 accidental samples today), predictions written beforehand. If shares and the capacity band hold there, every gold clause is met.

**What the author missed.** The hidden hunk (above); `--members` is a no-op above the handout rate, so the population driver is misnamed; the capacity is a band across fill phases, not the point 9.5×10³; and the bench comment says "the replay digest covers warm calls" while the code digests the cold call `upd` (the purity proof still holds — cold replay ≡ single replay — but the comment misdescribes the record).
