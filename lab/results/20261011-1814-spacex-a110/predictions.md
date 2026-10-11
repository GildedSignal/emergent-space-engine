# Predictions (held out before the decisive sweep)

Written 2026-10-11 after smoke tests on two configs only
(smoke-convoy: n=1024, slots, σ_a=1e-4, T=64, b=3e-3 → enc 150, d0_med 5,
d0_max 418, d0≤4 = 0.47; smoke-belt: n=512, ring, σ_a=3e-2, σ_e=0.15, T=4 →
enc 21). All other configurations below are untuned; these are commitments.

Notation: d0 = encounter partner's rank in the longitude order at certificate
epoch t=0 (1 = immediate neighbour); d0≤4 = fraction of encounters whose
partner was within rank 4 at t=0 (the gold taleb-09b5's certificate);
swaps/enc = conjunctions (= phase-order transpositions) per real encounter
(the phase tier's steady churn cost); cone/enc = Binet-cone candidate pairs
× 1.1 element changes per body-orbit, per encounter (the window tier's cost).

1. **Fresh convoy control (σ_a=1e-6, slots, T=256):** d0≤4 ≥ 0.9 — the gold's
   rank-4 reproduces on a fresh convoy; cone/enc > 1e4 (the window tier is
   dead in the co-orbital regime, as the gold found at 135×); swaps/enc ≤ 20.

2. **Convoy aging (σ_a = 3e-5 → 1e-3, same fleet older):** d0≤4 falls below
   0.5 already at σ_a=1e-4 and below 0.1 at σ_a=1e-3; d0_max > 100 at
   σ_a ≥ 1e-4. The rank-4 certificate is a fresh-formation statement; it is
   not a structure statement, and an aged fleet breaks it.

3. **Churn cost stays O(1) per encounter in σ_a:** swaps/enc stays between
   ~5 and ~100 across the whole ring sweep (σ_a=1e-4 → 1e-2, b=3e-3) and the
   convoy sweep; it does not blow up with spread (no quadratic hole between
   the two tiers — the phase tier covers the co-orbital middle at a churn
   cost set by geometry). At fixed σ_a it does not grow from n=512 to n=2048
   (nscale configs).

## Post-mortem (appended after the decisive run; the commitments above were
## written before it)

- The decisive sweep ran (results.json, probe.py). Its event engine was then
  FALSIFIED by direct integration: on ring n=256, σ_a=1e-3, σ_e=0.03, T=2
  it reports 0 encounters where integration finds 57; a pair verified by
  integration to close to 1.7e-4 has no event at all. Root cause (verified,
  mechanism + numbers): the engine enumerates conjunctions by mean-longitude
  (synodic) crossings, but with e-spread the relative TRUE longitude
  oscillates ±2√(e_i²+e_j²) each orbit, so pairs inside that band align
  twice per orbit — the epicyclic channel — which the synodic enumeration
  cannot see (it would place their first meeting ~1/|Δn| orbits away).
  Every table column derived from that engine (enc, swaps/enc, cone/enc,
  d0, dH in probe.py's sweep) is RETRACTED. The analytic cone-pair count
  stands (co-orbital swarms: cone pairs ≈ all pairs).
- Prediction 1 therefore neither held nor failed: it was tested with a broken
  instrument. Predictions 2–6: untested by the retracted run; the brute-force
  rerun (probe2.py) tests the e-noise axis of prediction 2 and CONFIRMS its
  direction: rank-4-at-epoch decays with spread (frac≤4: 1.00 → 0.98 →
  0.84 → 0.56 as σ_e goes 0 → 0.003 → 0.01 → 0.03 on the same convoy).

4. **Both tiers' per-encounter cost scales ∝ 1/b** (b-sweep, b = 1e-4 → 1e-2,
   factor 100): swaps/enc and cone/enc each grow ~100× from b=1e-2 to b=1e-4;
   encounter rate itself scales ∝ b. At ship scale (b=1e-4, ~15 km at 1 AU,
   still 100× a ship) swaps/enc > 300 — the wall both adopted tiers share.

5. **Two-fleet engagement pass:** cross-fleet encounters have d0 of order
   n/4 (≈ 256 of 1024; the certificate at build time cannot see an
   engagement that has not started); during the pass (dH at T/2) the
   cross-encounter partner rank is small (< 10). Engagements are invisible
   at build time and cheap during the pass: the certificate must rebuild on
   the arrival of concentration, which is what the trigger must detect.

6. **Belt control (σ_a=3e-2, σ_e=0.15):** cone/enc lands in 1e3–1e5 — the
   window tier's home ground, same order as r8 v2's measured 786 work per
   encounter for element-sort at its belt parameters (cross-check of the
   harness against a frozen result, orders of magnitude only).

**Kill criteria pre-registered.** The gold's certificate design is falsified
at the edges if (a) the fresh-convoy control gives d0≤4 < 0.9 (rank-4 does
not even reproduce on its own case), or (b) swaps/enc grows with n at fixed
density (a quadratic leak the two adopted tiers cannot cover). The "hole"
hypothesis (neither tier tracks real encounters in the co-orbital middle) is
killed if swaps/enc < 50 everywhere in the σ_a sweep at b=3e-3.

**What would make me distrust the harness:** encounter counts below ~30 in a
config (Poisson noise dominates the rank fractions there — such a config is
reported but decides nothing), or the belt control's cone/enc below 100
(would mean my cone proxy miscounts the window tier's candidates).
