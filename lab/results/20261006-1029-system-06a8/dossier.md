# Dossier — run 20261006-1029-system-06a8 (lens: the whole system)

## Claim

Kills the configuration "kicks as conjunction-scheduled pair events with a zero-kick secular kernel between" (the tempting reading of representation.md §"one kick per conjunction" extended to the whole cadence): in a Jupiter-belt float replica it never reaches the behaviour bar at any evaluation count tried, while fixed-cadence kicks pass at 8/orbit — so the kick layer's remaining lever is not event-shaping the cadence, and q-cadence already has its answer: the floor in this regime is ≈ 8 kicks/orbit.

## Bottleneck

Board focus item 1: "fewer kicks per orbit at the same behaviour (kicks dominate the engine's cost)". The candidate simplification was structural: principle 14 ("no ticks") read against law.md's "kicks … at a fixed step in the drift's own phase" (a tick), with the encounter crate's conjunction finder (continued-fraction recursion, law.md) proposed as the one schedule serving both layers. Expected gain if it had held: 2–10× fewer kick evaluations per orbit plus deletion of the cadence parameter and of the skin/kick window duplication. Measured gain: none; the configuration is killed.

## Evidence

Scene: heliocentric 2D restricted three-body, Sun + circular Jupiter (μ = 1e-3, a_p = 5.2 AU), 72 test ships (48 non-resonant a ∈ [2.3, 4.4] e₀ ∈ [0.02, 0.3]; 16 at 2:1 ± {0…0.08} AU, e₀ = 0.02, two phases; 8 edge a ∈ [4.45, 4.6]), 40 yr. Truth: RK4 h = 2.5e-4 yr (vectorised, full solar + Jovian acceleration; elements ↔ state round-trip exact to 1e-15). Candidates share the exact-Kepler drift and second-order DKD kick; they differ only in kick timing: A_n (law's current shape) equally spaced n ∈ {4,8,16,32} per orbit; B_m kicks only inside ±30° synodic windows at each conjunction (m ∈ {4,8} sub-kicks) with a Laplace–Lagrange quadrupole secular precession between events; B0 = B with events removed; Bn = post-hoc narrow window (±3°, m = 2), declared post-hoc. Every disturbing-acceleration evaluation is counted.

Band bar: ≥ 90% of seeds within |Δa|/a ≤ 0.005, |Δe| ≤ 0.05, |Δϖ − Δϖ_truth| ≤ max(0.1 rad, 10%).

| config | non-res pass | res pass | edge pass | evals/orbit |
|---|---|---|---|---|
| A4 | 0.792 | 0.812 | 0.000 | 4.1 |
| **A8** | **0.938** | **1.000** | 0.125 | **8.1** |
| A16 / A32 | 0.938 | 1.000 | 0.625 | 16.2 / 32.3 |
| B4 / B8 | 0.688 | 0.000 | 0.000 | 3.3 / 5.4 |
| Bn (post-hoc) | 0.625 | 0.000 | 0.000 | 2.2 |
| B0 (negative) | 0.625 | 0.000 | 0.000 | 0.14 |

Pump ratios at 2:1 (e₄₀/e₄₀(truth), band [0.8, 1.25]): A4 1.051, A8 1.008, A16 1.001, B4/B8 0.667, B0 in-band 0.38.

Why B fails (measured, not asserted): (i) the conjunction window's duration is set by the synodic phase rate (Δt = 2W/ψ̇), not by the interaction's strength — at 2:1, ψ̇ is small, so a ±30° window is 2.1 yr long and its m = 8 sub-steps (0.26 yr) are coarser than the A4 cadence it replaces (0.078 yr); the tide is delocalised over the synodic period, so windowed impulses systematically under-pump (0.667). (ii) Away from resonance the binding failure is the between-events kernel: of B8's 15 non-resonant failures, 12 fail the apsidal term ('w') — the quadrupole secular precession is off by more than 10% for a third of the band (α ≈ 0.69 here; truncation, not cadence). A8's only 3 failures are the three Jupiter-crossing seeds (a ≈ 4.31–4.37, real encounters) — the bar itself, not the integrator.

Controls: positive (A32 non-resonant 0.938 ≥ 0.90) passes; negative (B0 at 2:1: 0.38 pump in-band vs 1.00 for A) fails as required — it also reproduces, inside this harness, the lab's q-secular-v2 kill of secular-only phasors.

Reproduce: `cd lab/results/20261006-1029-system-06a8 && python3 probe.py` (22 s; `--quick` 15 s). Raw per-seed records: `raw.json`.

## Predictions (pre-registered in predictions.md before the decisive run)

- Held: #1 positive control passes; #2 negative control fails at resonance (0.38 in-band); #4 the edge band breaks B — and A too (best 0.625): the edge belongs to the doll changeover, not to any cadence.
- Failed: #3 (the claim's core) — no B configuration passes any band; the kill criterion ("loosest passing A ≤ 2× evals of loosest passing B") triggered in the strongest form. #5 resolved negatively: conjunction windows cannot carry the resonant phase (pump 0.667), so resonance keeps its own phase-feedback representation exactly as law.md line 68 legislates — my extension of "one kick per conjunction" beyond resonance is what died. #6 not supported: Bn's pass rate rises slightly with e₀ (0.579 → 0.655) but the gap to A8 does not close.

## What would make it wrong

The between-events kernel here is quadrupole Laplace–Lagrange only (circular coplanar perturber, numerical b_{3/2}^{(1)}). A full orbit-averaged kernel (all orders in α, inclined/eccentric perturbers) would remove failure (ii) and could let B or even B0 pass the non-resonant band at 0.14–5 evals/orbit — a bounded 2–8× win could then reappear. That experiment (better kernel, same schedule) is the one named follow-up. It cannot rescue the resonance band: failure (i) is structural (window width ∝ 1/ψ̇). Float replica, single perturber, coplanar, 40 yr, no belt-belt pairs; the design's real kernel is compiled and exact-integer, not this truncation.

## Cost of adoption / what it deletes

Nothing to adopt: the configuration is killed. What the run hands the integrator for free: q-cadence's belt-regime answer (fixed-cadence floor ≈ 8/orbit at probe tolerances; A4 already fails), a second independent kill of secular-only (with B12's redesign pending, this supports "averaging binds"), and a warning that the encounter crate's conjunction times cannot double as the kick schedule near resonance.

PRINCIPLES fit: "A failed expectation is not automatically a failed method" (H0183) — the method (event-driven everything, principle 14 "no ticks") is not impeached; this configuration of it is. "Write the kill criterion before the run" — done, and it fired.

## The lens

The system lens pushed toward the elegant unification (one schedule for kicks and encounters) and this run is the hard special case it told me to name: the resonant regime, where the synodic rate collapses and the "event" swallows the whole period. The lens may also over-weight structure: the plane's real kick cost (29 µs, 15 in rebinding) may fall to the jet/re-anchor work already adopted regardless of cadence shape; this probe could not see that.
