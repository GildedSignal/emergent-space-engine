# Predictions (written before the decisive run)

Run: 20261011-0324-inversion-0981, inversion lens. Target: lab gold `20261006-0346-taleb-09b5`
("every real encounter lies within partner rank 4 along the orbit") and the queued build
`b-coorbital-cert`, which hard-codes that lesson. Inverted question: **what is "rank 4" a
function of?** Held-out cases (not tuned on):

## Scenes

- S1(n): near-circular co-orbital fleet. a = 1 ± 1e-3, e ~ Rayleigh(5e-4), ϖ uniform,
  λ clustered in a window w = 0.1 rad, ρ = 2e-3, T = 10 orbits, n ∈ {125, 250, 500, 1000, 2000}.
  Fixed spreads and ρ; only n grows (the fleet gets denser — the game's scaling).
- S3-ring: eccentric co-orbital ring. a = 1 ± 1e-3, e = 0.7 fixed, ϖ ~ U(−0.3, 0.3),
  λ uniform, n = 200, ρ = 2e-3, T = 20 orbits.
- S3-form: eccentric formation. Same but ϖ ~ U(−0.15, 0.15), λ clustered at apoapsis (π ± 0.05).

Truth: the crate's `truth_pair` (conservative advancement, Halley states — no shared solver
path with any certificate logic). Metrics per true encounter: partner's mean-longitude rank and
true-longitude rank at the dip, the ρ-window population, and the time the pair spends inside
the rank-4 / ρ-window neighbourhood before the dip (catchable duration), from which exact
missed fractions at refresh cadences follow.

## Predictions

- P1 (S1, density artifact): the λ-window population (bodies within angular distance ρ) grows
  ~linearly with n, ≈ 2ρn/w (predicted ≈ 5, 10, 20, 40, 80 across the series). The rank-4
  catchable duration shrinks ≈ 1/n; the ρ-window catchable duration is ≈ n-invariant
  (set by ρ/|δn|, a few × 0.1 orbits). Consequently the rank-4 missed fraction at a fixed
  cadence (≥ 4/orbit) rises from ~0 at n = 125 to > 50% at n = 2000, while the ρ-window
  missed fraction stays ~0 at ≥ 4/orbit at every n. Prediction: k=4 is one point of the law
  k_honest(n) ≈ 2ρn/w; at a 10⁶-ship fleet (w = 0.1, ρ = 2e-3) k_honest ≈ 4×10⁴.
- P2 (S1, rank at dip): because random ϖ × small e leaves an e·δϖ-scale λ-offset at the dip,
  the λ-rank at the dip has p99 growing ~linearly with n, exceeding 4 somewhere in
  n ∈ {500, 1000, 2000}.
- P3 (S3, wrong longitude at high e): for co-orbital bodies with ϖ-spread at e = 0.7,
  λ-separation is nearly constant in time (equal periods) and equals ~0.6·δϖ at the dip
  (amplified by the true-to-mean compression at the crossing), so the partner sits at
  λ-rank ~ n/16 permanently: the λ-rank certificate misses those encounters at ANY k below
  ~n/10 and ANY cadence (permanent miss), while the true-longitude rank at the dip is ~0–3.
  Predicted λ-rank p99 in S3-ring > 10 at n = 200; φ-rank p99 ≤ 4.
- P4 (S3, no sampling certificate catches eccentric crossings): the dip duration (time inside
  the ρ-tube) at e = 0.7 crossings is ≪ 1/64 orbit (predicted ~10⁻⁴–10⁻³ orbits), so catching
  them requires the predictive timing layer (crossing longitudes + conjunction times), not any
  sampled neighbourhood watch.

If P1 fails (window population flat, or rank-4 duration not shrinking), the gold's k = 4 is
robust in n and my attack dies. If P3 fails (λ-rank at dip ≤ 4 in S3), mean longitude is safe
at high e and only the density axis matters.
