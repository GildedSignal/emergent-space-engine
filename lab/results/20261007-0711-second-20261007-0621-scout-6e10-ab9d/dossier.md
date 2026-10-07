# Dossier — run 20261007-0711-second-20261007-0621-scout-6e10-ab9d (second author on 20261007-0621-scout-6e10)

## Claim

The checker's named experiment is done, and its answer **refutes the original run's
smooth pole for the belt's real churn**: real Jupiter-flyby kicks on B18b's belt scene
(integrated under the plane's own force model, `force.rs`: differential pull + origin
fall, 700 steps/orbit, one 10-orbit epoch) are entropy-typed **chaotic for every
bounded event program tried** — the original's 12-term birth basis recaptures **0.0
bits** of the kick's 41.4 bits at q24 (its A1 objection, measured: worse than the
checker's adversarial 29/39-bit examples), the pre-registered 80-feature synodic basis
3.5%, post-hoc 2-D Fourier programs up to 840 features 4.8%, per-band fits 3–5% —
while the true-Laplace–Lagrange secular program recaptures ~0.1% (conjunctions, not
secular drift, are the whole kick at these windows). Real kick σ is 0.0148/component
(2× the original's invented 0.0075), rising ×12 from the inner to the outer belt, and
**every belt body is kicked every epoch** (conjunctions are universal, not 1%/epoch),
so the belt's scar stock sits at the materialization asymptote from the first epoch:
≈ 41 bits/body = **5.2 GB per 10⁹ at q24, 3.0 GB at q16** (matching the original's own
q16 asymptote 2.7 GB), plus its carry line (0.56 GB, untouched). The original's
"≤ 0.6 GB + 37 MB/epoch" belt line is optimistic ≈8×; the stock-vs-flow core of the
claim stands, the smooth pole does not exist for planet flybys.

## Bottleneck

The same one the original attacked (board: 10⁹ in 8 GB "decided by distinctions
created per game-second"; HANDOFF: H_live "not measured yet"), one rung further: the
original measured the two poles on invented distributions (a coin flip
`is_chaot = rng < 0.5`, σ chosen); the checker held gold for exactly this ("the mix
is not measured") and its A1 (the smooth pole is program-relative). Expected gain:
the allocator's belt budget line now prices the real workload — the per-population
scar quantum (q16) is not an option but a requirement (a 10⁹ belt at q24 does not fit
8 GB with anything else in the machine), and the store-vs-replay fork is now a
measured design decision.

## Evidence (deterministic, seeded; every command from this folder)

```
python3 real_kick_ledger.py control     # 8 s   -> ctrl.npz  (Jupiter off)
python3 real_kick_ledger.py integrate   # 58 s  -> int.npz   (the real run)
python3 real_kick_ledger.py measure     # 28 s  -> real_kick_ledger.json + run_log.txt
python3 diag_bands.py                   # 0.4 s -> diag_bands.json (per-band, post-hoc)
```

Scene: the original's/B18b's (a ∈ [2.0, 3.6] uniform, e Rayleigh 0.1, angles uniform;
Jupiter a 5.2, e 0.05, μ 10⁻³), N = 2¹⁵ bodies, velocity-Verlet at 700 steps/orbit
(the plane's own cadence regime), 10 of each body's own orbits. Entropy convention:
the original's (differential entropy per component at the quantum, sum of both).

| Quantity | Measured |
|---|---|
| Control: Jupiter off, max \|Δz\| (integrator noise floor) | 1.2×10⁻³ (12× below kick σ; its σ is far lower) |
| Total Δz over one epoch, no program | 41.45 bits at q24; σ 0.0149/component |
| True-LL secular program (g = nμαb₃/₂⁽¹⁾/4, scale scanned 0.7–1.3) | 41.41 bits — recaptures 0.1%: conjunctions dominate |
| **Original's 12-term basis on the real kick (A1)** | **41.41 bits, recaptured 0.000** |
| Pre-registered synodic basis (80 features, predictions.md) | 39.96 bits, recaptured 3.5% (65% of variance: σ 0.0148→0.0088) |
| Post-hoc 2-D Fourier (conjunction longitude × perihelion × a), 200/400/840 features | 39.86/39.57/39.40 bits — 3.7/4.4/4.8% |
| Per-band fits (diag_bands.py): inner/middle/outer third | 34.24/36.16/41.50 bits vs kick 35.84/37.31/42.99 — 3–5% |
| Low-e subset (e < 0.07, the cleanest geometry) | 37.57 vs 40.95 bits — 8.2% |
| σ by a-third | 0.0021 / 0.0036 / 0.0256 (×12 across the belt) |
| Heavy tail (the checker's A2 direction) | excess kurtosis 20.7, p99 \|Δz\| 0.073, 2 Jupiter crossers to \|Δz\| 0.46 — the Gaussian dh is an upper bound |
| Belt stock, real mix (everyone kicked, pole-priced) | 41.4 bits ≈ 5.2 GB per 10⁹ at q24; 24.0 bits ≈ 3.0 GB at q16 |

The physics cross-checks: per-conjunction Δe from the impulse approximation
(Δv = 2Gm_J/(bU)) is ~0.005 inner to ~0.018 outer; √(4–8 conjunctions) random walk
gives 0.01–0.04 — the measured 0.0021–0.0256 (partial coherence included) matches in
order; the secular precession over 10 orbits is gT ≈ 0.01 rad, so LL *must* be tiny.

## Predictions

`predictions.md` was written before the run. Scorecard:
- **P1 ✓** σ 0.0148 ∈ [2×10⁻³, 5×10⁻²], ×12 across the belt, 41.4 bits ∈ [33, 48].
- **P2 ✓** (stronger than predicted): the true-LL program recaptures 0.1%, not just <50%.
- **P3 ✓** (decisive): the original's basis recaptures 0.0% — A1 confirmed on the
  engine's own physics, beyond the checker's invented cases.
- **P4 ✗ — my own kill criterion fired**: the synodic basis recaptured 3.5% < 60%;
  per its pre-registered branch, real flybys are effectively chaotic for any bounded
  program and the belt prices at the full pole with P1's σ. I tried to break this
  kill post-hoc (richer Fourier ladders to 840 features, per-band, low-e): all ≤ 5%;
  the kill survives everything cheap I could throw at it.
- **P5 ✓** in direction: real stock 5.0–5.2 GB q24 (top of my predicted 1.5–5 GB
  range), the original's belt line optimistic ≈8×; at q16, 3.0 GB ≈ its own 2.7 GB
  asymptote (independent consistency check).

## What would make it wrong

- The replica is still Newtonian 2-D one-perturber. Resonant structure (Kirkwood
  gaps) is *in* the measurement (the σ ×12 gradient is partly resonance-fed), but a
  second perturber or 3-D inclinations could change σ by factors, not the typing:
  the typing follows from the conjunction phase's steep dependence on birth a
  (~57 rad drift across the belt per window), which more planets only worsen.
- dh is Gaussian-fit entropy on a heavy-tailed sample (kurtosis 21): true scar
  entropy is *lower* (the checker's A2), so the pole is an upper bound — the
  conclusion (no smooth pole, belt materialized) is tail-robust.
- Windows of one orbit instead of ten sparsify conjunctions (~0.4–0.8 per body per
  orbit), but scars are a stock: within a few orbits every body is kicked once and
  the belt sits at the same asymptote. The stock framing, not the churn rate,
  decides — which is the original's own thesis, now applied to its churn line.
- The engine can avoid the whole bill by **deriving belt states on read** (replay
  the shared kick cadence: Jupiter is analytic, the body's tube is computable, cost
  O(#conjunctions) per read). My run prices the *store* path (B18b's regime); the
  replay path is unpriced and is where `b-h-live` (still queued) should look.

## Cost of adoption, fit with PRINCIPLES

Adoption: rewrite the original's proposed allocator line a second time — not
"+62/kick, −60/reabsorption" (flow, killed by the original) and not "smooth churn
costs membership only" (killed here): *the belt's real churn is pole-priced and
universal; a 10⁹ belt needs the per-population scar quantum (q16: 3.0 GB) or
derive-on-read replay, or it does not fit 8 GB* (PRINCIPLES 24, "the memory floor
is information"; 3, "compute only surprises" — the surprise here is not
compressible, it must be either stored or recomputed; 19, two wrong representations
of the same line have now been killed by measurement, which is the process working).
Fits the board's belt row (B18b's churn cases should be typed pole, not smooth).

## The lens

The second-author lens trusts the original's scripts and attacks only the named gap;
what it may have missed: I priced one scene at one epoch length with one perturber
(the belt the board actually runs), and the store path only — the replay/recompute
path, GPU-side scar reads, and the battle workload (no real encounters exist in the
plane to measure; its kicks are contact-driven, the original already typed them
chaotic) are untouched. The `b-h-live` dashboard build remains the right next step,
now with a typed expectation to measure against.
