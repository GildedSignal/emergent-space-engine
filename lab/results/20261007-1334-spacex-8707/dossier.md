# Dossier — H_live for a plane-like belt: measured, and it is not the memory bottleneck

## Claim

For a plane-like belt (30k bodies, Jupiter-analogue perturber, 1000 yr, 3 seeds), the live-distinction rate after one global secular refit is ~10⁻³ scars per body per year at quantum q = 10⁻³ — at 10⁹ bodies that is ~0.03 scars per game-second (~0.5 B/s at 16 B per scar; ~50 B per real second at rtf 100) — so planetary secular dynamics cannot force the 8 GB ceiling at session scale; scars saturate only on a ~5–7 yr sim-time scale (≈ weeks of continuous play at rtf 100), which sets the program-refit cadence, and the saturation tail is dominated by the 2:1 resonance zone at the belt's outer edge.

## Bottleneck

Board risk #2, "distinctions created per game-second (H_live): not measured yet" (docs/plane.md readout, docs/HANDOFF.md risks). The naive fear: 10⁹ bodies × per-body deviations from the population program overflow 8 GB. Measured answer: the belt's secular H_live is 4–5 orders of magnitude below any memory pressure at game timescales; the memory question at session scale is decided by encounters and the player, not by planetary dynamics. This deletes the worry, not a component: no new store, no new gate is needed for the secular path; the number goes into B18's "reported at 10⁹" line.

## Evidence

All commands from `lab/results/20261007-1334-spacex-8707/`. Machine: shared Linux runner, 8 vCPU, load 2.6–3.0 during runs, 13 GB available.

- Harness: `hlive.py` — the plane's own architecture, not an integrator: bodies coast on exact Kepler generators; the planet's field is applied as midpoint-sampled kicks; elements updated by exact impulse conversion. Null control (m_p = 0, same code path): max |Δa|/a = 4.4e-12, |Δe| = 1.5e-13 over 1000 yr (`python3 hlive.py --scene null --N 30000 --years 1000 --dt 0.1 --seed 7 --out null_1000.json`, ~45 s).
- Convergence: dt 0.05 vs 0.1 (N=4000, 300 yr) agree to ≤ 1.3e-5 relative on all reported statistics (`conv_dt05.json`, `conv_dt10.json`, 15 s).
- Decisive runs: `python3 hlive.py --scene belt --N 30000 --years 1000 --dt 0.1 --seed {7,8,9} --keep-sub 6000 --out belt_s{7,8,9}.json` (3 in parallel, 184 s wall; single-seed serial ~150 s — over the 60 s guide, disclosed).
- Aggregate (`python3 aggregate.py` → `aggregate.json`): reabsorbed e-residual RMS grows as t^0.573 (median over seeds; 0.5–0.7 band). Crossing rates (out-of-sample): q=1e-3 → 1.0e-3/body/yr long-run; early-time (first 20 yr) ~3.7e-2/body/yr from the residual curve (rms 2.9e-3 at 20 yr). Median first-cross at q=1e-3: 6.2 yr; at q=3e-3: 21.7 yr. In-sample vs out-of-sample rates differ by 0.4% → fit noise is not driving the crossings.
- Resonance fingerprint (median |Δv| by a): inner belt 1.4e-3; 3:1 zone (2.45–2.55) 3.3e-3 (1.8× local); outer edge (3.25–3.30, the 2:1) 3.5e-2 — 19× the inner belt, p99 |Δv|/v = 7.8%: the 2:1 zone is being actively sculpted and dominates the churn tail.
- Coherence of the cumulative kick field: cell means over 0.1 AU × 10° cells (351 cells, 81% of bodies) leave residual RMS = 0.55 of the field (70% of variance captured). Finer cells do not resolve at N=30k.

Memory verdict at 10⁹ bodies (16 B per scar, 4 GB budget): even at the early-time peak rate, +21 B per game-second; 4 GB fills in ~200 game-years without any refit. With a secular program refit every ~5 yr of sim time the scar fraction stays ≤ 25% (≈ 4 GB at 10⁹).

## Predictions

`predictions.md`, written before the decisive runs. Outcome: 4 of 7 held (null control 1e-12; growth exponent 0.573 ∈ [0.5, 0.7]; in/out-sample within 0.4%; session-scale lag < 5% crossed in 2 game-years). Two failed honestly: (a) near/far crossing-rate ratio at q=3e-3 was 1.33, not ≥ 2 — the ±0.05 AU windows dilute; the resonance structure is real but shows in the |Δv| profile (3:1 bump, 2:1 edge), not in that ratio; (b) coherence at the finest usable cell captured 70% of variance, not ≥ 80% — each body's own conjunction phase randomizes the response more than I estimated. One missed low: T*(frac ≤ 25%) ≈ 5–7 yr, below my predicted 10–300 yr bracket — scars arrive faster than predicted, which strengthens, not weakens, the refit-cadence conclusion.

## What would make it wrong, cost, fit

Wrong if: the plane's actual belt sampler (B18b: banded p) concentrates bodies where my uniform-in-a scene diffuses them — resonance-zone fraction could be much higher; a second giant or self-gravity of the belt would raise the floor; and the null control only bounds the harness, not the fit (the 0.4% in/out-sample gap bounds the fit). Adoption cost: none — no engine change proposed; one number and one cadence for B18's belt wiring and the `b-h-live` dashboard build (which still needs to measure the plane's live scenes: encounters, player scars, rebinding remainders — that is where H_live actually lives). PRINCIPLES: "Store the generator, not the generated" (#6 — the secular part of the generator is two smooth fields, F(a) and g(a), plus a refit clock); "Compute only surprises" (#3 — the coherent 70% never becomes per-body state); "Measure before claiming" (board risk #2 was a fear, now a number).

## The lens

The SpaceX lens pushed to a single-number verdict fast; what it may have missed: the tail is the story, not the median (the 2:1 zone is 4% of the belt and most of the churn — a refactor of that zone into resonant-normal-form programs, not scars, is the real follow-up, and r4 v3's KILL says that representation is not yet available); and this measured the cheap path the design already chose (kick map), so it inherits the design's blind spot: near-resonant kick statistics are exactly where the map's error type matters (r9's lesson).
