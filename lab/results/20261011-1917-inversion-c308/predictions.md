# Predictions (written before the run)

Run: 20261011-1917-inversion-c308. Lens: inversion. Target: gold `20261006-0346-taleb-09b5`
("every real encounter lies within partner rank 4 along the orbit"), now being built as
`b-coorbital-cert` (O(n·k), k~4, triggered by a dimensionless concentration number).

## The model behind the predictions

In-plane Kepler, circular unless noted. Conjunction distance for a co-orbital pair is exactly
|Δa|, so encounter-capable pairs have Δa ≤ ρ (circular). Mean-longitude gaps close at 1.5·Δa
rev/orbit, so a pair sits inside rank k of its partner for t_k = k/(1.5·Δa·n) orbits before
conjunction. A certificate derived at cadence H (per-orbit is the most favorable reading of
"O(n·k) per evaluation"; q-candidate-degree's goal is lazier still) catches an encounter only
if some derivation lands inside that window, giving:

    k_required ≈ 1.5 · n · H · reach,   reach = ρ (circular), min(W, 2·e·a)/a (ϖ-spread eccentric)

and miss-fraction at window k, pooling over encounter events (event weight ∝ Δa):

    miss(k) ≈ (1 − k/k*)²  for k ≤ k* = 1.5·n·H·reach, else 0.

If the certificate is instead maintained continuously, it misses nothing but pays one update
per conjunction: work per real encounter ≈ 0.67·(W/reach)² (circular), n-independent at fixed
distribution.

## Scenes (all: a ~ U(1−W/2, 1+W/2), λ₀ uniform, one shared plane; H = certificate cadence in orbits)

- S0  control (gold-like tight formation): n=10⁴, ρ=1e-4, W=2e-4, e=0, H=1, window 100 orbits
- S1  ladder, fixed scene ρ=3e-4, W=1e-3, e=0, H=1: n ∈ {3×10³, 10⁴, 3×10⁴, 10⁵}, windows 300/100/30/10
- S2  cadence, same scene at n=3×10⁴: H ∈ {0.25, 4}
- S3  eccentric pair at n=10⁴, ρ=3e-4, W=1e-3, H=1, window 30: e=0 (twin) vs e=0.05 with ϖ uniform
- every scene also scored at cadence H/20 (the "near-tautology" row)

## Held-out predictions

- **P1 (control, reproduces the gold):** S0 miss(k=4) = 0 at per-orbit cadence (k* = 1.5).
- **P2 (the scaling kill):** S1 miss(4) rises along the ladder as (1−4/k*)² with k* = 1.5nHρ:
  n=3×10³ → 0%; n=10⁴ → ~1%; n=3×10⁴ → ~49%; n=10⁵ → ~83%. The 99th percentile of partner
  rank at last eval grows ∝ n¹·⁰±⁰·¹ (k* = 1.35 → 45 across the ladder).
- **P3 (cadence):** at n=3×10⁴, required k scales ∝ H: k* = 3.4 (H=0.25, miss(4)=0) and 54
  (H=4, miss(4)≈87%).
- **P4 (eccentricity extends the reach, the genuinely uncertain one):** at identical n, W, ρ, H,
  the eccentric twin (e=0.05, ϖ spread) inflates the encounter-capable Δa range from ρ to ≈ W,
  so miss(4) jumps from ~1% (circular twin) into the 45–75% band, and the rank p99 lands near
  1.5·n·H·W ≈ 15. If the crossing-arc probability turns out to suppress high-Δa pairs, miss(4)
  could fall below 45% — that would bound the e-effect; if ranks exceed ~30, my arc model is
  wrong in the other direction.
- **P5 (not rigged / tautology row):** at cadence H/20, miss(4) < 3% in every scene, including
  S1d and S3-ecc — rank-4 is true close enough to the encounter; what fails at per-orbit
  cadence is scale × cadence, not the rank concept. (This is also what a rank measured *at*
  encounter time would show, which certifies nothing.)
- **P6 (continuous-maintenance cost):** conjunctions per real encounter ≈ 0.67·(W/reach)²,
  n-independent: ~7 in S1 (W/ρ = 3.3), ~2.7 in S0, and ≥ 100 in S3-ecc. Any of these above
  ~1.5 falsifies "work tracks real encounters" for the continuous variant (r8 v4's
  checks_per_encounter gate is ≤ 1.5).

## Kill criteria for my own run

- If S1c/S1d show miss(4) < 10%, the drift-residence model is wrong and the gold's rank-4 is
  more robust than I derived — that is a result too, and I will report it as such.
- If the H/20 rows miss, my harness is broken (rank lookups wrong), and nothing else counts.
- All conjunction events are distinct by construction (same-pair conjunctions ≥ 1/(1.5·W) ≈ 667
  orbits apart, windows ≤ 300 orbits) — the memo-artifact lesson is checked by design.
