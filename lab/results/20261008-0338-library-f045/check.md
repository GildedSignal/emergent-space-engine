# check.md — 20261008-0338-library-f045

Grade: silver

**Abstract (for the integrator).** Library-lens dossier: five Readwise lessons — all six quotes verbatim in the cached 770-book/4,580-highlight export, sources and corpus counts exact — re-order the kick-cadence decisions: a deletion ladder for kick classes, tail-hitch cost criteria for q-cadence, an empirical push-the-doll-deeper boundary for b-handoff-surface, and a worst-seed boundedness line for B12v2 (top of queue; today's B12 judges the median seed only). Adoption cost near zero. But the one measurement — A(τ) crossing 1 at 0.17–0.25 Hill radii, "on top of r9's τ₀" — is fragile: the crossing vanishes under consistent secondary-phase shifts (A16 = 0.73, 0.89 at τ = 0.25), moves to τ ≈ 0.10 at μ = 10⁻², and inverts at 150 orbits. Also wrong: B15 already judges p99; method.md already has the deletion pass.

## Reproduction (clean tree, author's own commands)

- `python3 quotes-check.py`: 6/6 VERBATIM, sources match the dossier's attributions (Isaacson ×2, *Antifragile* ×2, *Surely You're Joking*, *Almanack of Naval Ravikant*). I re-grepped the 4.2 MB export independently (my own script, not the author's): single unique hits, correct books; Musk's 10%-re-add sentence matches character for character. Corpus: 770 books / 4,580 highlights; "315 Personal MBA highlights" — all exact.
- `python3 shock_probe.py` (26 s): reproduces digit for digit — A(1/16) = 0.45, 0.80, 0.75, 1.68 at τ = 0.05, 0.10, 0.17, 0.25; 0.35/0.50 non-monotone, as the dossier says.
- Doc-state claims verified: `lab/queue.txt` has q-b12-design first, b-handoff-surface and q-cadence queued; `lab/rungs/` has no cadence rung; law.md B12 is median-seed today; B14 (r9's judge, 0.2–0.9 Hill radii, apsidal precession) exists as proposed; law.md line 38 confirms r3 v3's handoff criterion failed against a 10⁻¹¹ chaotic reference; plane.md 29–31 carries the tail dashboard (p99.9, hitches > 16.7/33/50 ms, worst hitch) — as a dashboard, not a frozen gate.

## Predictions

`predictions.md` predates the decisive run on mtime order (predictions 4 min before the dossier; `shock_probe.py` last written 3 min before; `run.log` is empty, 0 B, so mtime plus the honestly-disclosed direction failure is the only pre-registration evidence — it is consistent but not proof). Held-out outcomes: quote checks held (6/6 for kept quotes; the predicted Waitzkin/Chouinard/Dignan quotes were never verbatim-checked — dropped, per the pre-stated rule); decision-openness is scored "held" but two sub-claims failed as written (below); the probe prediction failed in direction and was reported — good.

## Attack (five adversarial cases; all ≤ 2 GB, /tmp/adv, author's code exec'd unmodified)

1. **Truth convergence** (4,000/8,000/16,000 RK4 steps per orbit, τ = 0.10/0.17/0.25): dω_truth and A16 identical to three digits at every resolution. The reported numbers are numerically solid, not under-resolved.
2. **Secondary phase seed** (φ = π/2, π, applied consistently to truth *and* kicked runs — the physically correct seed variation): **the crossing disappears.** φ = π/2: A16 = 0.85, 0.94, 0.90, 0.73; φ = π: 0.10, 1.01, 0.36, 0.89. No value exceeds 1 at τ = 0.25. The φ = 0 row reproduces the author's table exactly (harness faithful). (A fifth case where I shifted only the kicks against a φ = 0 truth was harness-inconsistent; discounted.)
3. **Mass ratio** (μ = 10⁻⁴, 10⁻², 300 orbits): μ = 10⁻² crosses already at τ ≈ 0.10 (A16 = 1.52, 5.87 at 0.10/0.17); μ = 10⁻⁴ never crosses in 0.05–0.35 (max 0.97). τ* is a function of (τ, μ), not of τ alone. μ = 10⁻³ does match B14/r9's Jupiter-like scene, so the agreement is one calibrated point, not a law.
4. **Horizon halved** (150 orbits, μ = 10⁻³, φ = 0, n_orb passed explicitly): A16 = 5.16, 5.66, 0.69, 0.87 — the deep-τ asymmetry flips sign versus 300 orbits.

Conclusion of 2–4: "the crossover sits at 0.17 < τ* < 0.25, on top of r9's τ₀" is one cell of a surface fragile in phase, mass and horizon. As run, the toy violates principle 20 (behaviours over many seeds) and its own kill criterion's spirit. The dossier's wrong-if list names the integer law but not this.

## Factual errors in the dossier

- **"B15 today judges medians only" is false.** Frozen B15: "PASS iff the gravity run's CPU seconds are ≤ 2× the flat run's at every rung, **median and p99 alike**" (taste log, 1 October: "B15 medians (p99 added)"). Lesson 3's substance survives — B15 judges CPU-seconds percentiles, not per-frame hitch tails or kick-count tails, and no gate judges cadence by the frame tail — but the stated premise is wrong.
- **Prediction 2's "the taste log is the only record" of the memo kill is false**: law.md line 35 records the kill (principle 13, random walk) with the redteam-df81 measurement. The dossier half-corrects this inline yet still scores decision-openness "held".
- **Lesson 1 novelty gap**: docs/method.md (draft awaiting Julien) already encodes Musk's delete order, a deletion pass for every Flying component, and the re-add calibration ("if nothing deleted ever comes back, too little was deleted"), and plans "Generators and deletion become lab lenses". Not cited. The increment — a kick-class deletion ladder for q-cadence with the 10% number and B gates arbitrating — is real (no rung file exists) but narrower than presented.

## Novelty

Library mining itself is established here (H0162's allocator principles; the H0065–69 Readwise waves; the 30 September library-lens lead). The A(τ) shock-asymmetry trigger is new; the B12 boundedness line is new and correctly separates boundedness from the growth exponent, so it does not collide with the r2 lesson (never judge a *noisy exponent* on the worst seed). The tail-cost and boundary-sweep criteria are new increments on open queue entries.

## Goal fit

On-focus (board item 1, cadence). Adoption cost near zero: three criteria lines and experiment order, no code. PRINCIPLES quotes are accurate and applied (1, 4, 12, 13, 26). Not gold: no bottleneck moves 10× by a measured result, and the one measurement does not survive adversarial variation.

## The one experiment that would make it gold

Re-derive A as a seed-robust statistic — median A16 over ≥ 6 secondary phases at fixed μ, per principle 20 — and report whether the τ-crossing survives in the toy; if it does, measure the same statistic on the real engine by doubling kick size across r9's Hill ladder with B14 as judge (the dossier's own "test on the real engine"). A crossing that survives phase-averaging in both toy and engine is a gold-grade regime trigger; if it does not survive, that kill is also a result the cadence rung needs before it freezes criteria.

## What the author missed

The strongest falsifier (seed/mass/horizon fragility) was minutes away and is the one thing the lens's own Taleb lessons preach; B15's frozen text (p99); method.md's deletion pass; law.md's memo-kill record; an empty run.log left no execution trail.
