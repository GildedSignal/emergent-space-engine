# Dossier — 20261010-1816-dynamics-3a4c (lens: dynamics and attractors)

## Claim

In a belt on the engine's own drift-kick split, kick cadence is governed by
the rate at which behaviour unfolds within the certification horizon, not by
resonance proximity: where e-motion is slow or absent, 4 kicks per perturber
orbit reproduce every body's e-statistics (even mu x3, resonance-proximal,
at 5x the horizon), and per-body scheduling buys at most 2x; only the
fast-unfolding belt (near-perturber, high e0, pumping and ejections within
120 orbits) spreads sufficient cadence 32x and would save 6.8x under
scheduling — and there the demand is NOT rankable by any single
Chirikov-style resonance scalar from birth elements (sign-unstable across
belts), so q-cadence must schedule from measured unfolding (the kicks' own
effect on E,L), not from a predicted per-body frequency oracle.

## Bottleneck

Board focus line 1 ("fewer kicks per orbit at the same behaviour; kicks
dominate the engine's cost") and the taste-log lever "the lever is cadence
(q-cadence queued)". Expected gain where it applies: ~7x on belt kick work;
the negative part (cadence is horizon-governed, not resonance-governed, in
quiet regions) redirects q-cadence away from a per-body frequency oracle.

## Evidence (all commands from lab/results/20261010-1816-dynamics-3a4c/, Linux x86, 8 vCPU shared, load 1.4-2.1)

Scene: Sun + circular Jupiter (a=5.204 AU, mu_J=9.5459e-4) + massless planar
belt; exact Kepler drift (universal variables, conserved e,h to 1e-15) +
full Jupiter tide as one impulse per kick (the plane's split, law.md
"Perturbed motion: the compiled drift plus kicks"). Cadence K = kicks per
Jupiter orbit, powers of two (block steps). Behaviour of a body = mean/std/max
of e(t) over the horizon. K* = min K reproducing truth (top cadence) within
max(10-15% rel, absolute floors). Truth convergence: 512 vs 1024 kicks/orbit
differ by <= 1.2e-5 of tolerance (out_conv.npz).

- Belt A (a 2.0-3.6, e Rayleigh 0.05, 1024 bodies, 120 Jupiter orbits):
  median K* = 4, p90 = 4, never-sufficient 0%; e_std p50 = 4e-5 (nothing
  unfolds); uniform(p99)/scheduled = 2.0x.
  `python3 cadence.py A 120 4,8,16,32,64,128,256,512` then `python3 analysis.py`
- Belt B (a 3.6-4.6, e Rayleigh 0.12, 1536 bodies, 120 orbits; pumping and
  ejections unfold, e_std up to 0.2, e>1 for a few): K* histogram
  8:1235, 16:64, 32:28, 64:24, 128:23, 256:162 (spread 32x);
  uniform(256)/scheduled = 6.8x; K*-strata resonance-proximity medians fall
  monotonically 2.3 -> 1.0 (calibrated units); but Spearman rho(log K*,
  log zeta) = +0.49 — sign-unstable against belt A's structure — so the
  single scalar does not rank individual bodies.
  `python3 cadence.py B 120 8,16,32,64,128,256`
- Belt C (belt A's range, mu_J x3): K* = 8 for 1526/1536 — cadence demand
  rises with mu but stays near-degenerate; the earlier rho=0.98 was rank
  noise on a constant, discarded.
  `python3 cadence.py C 120 8,16,32,64,128,256,512`
- Experiment 2 (600 orbits, mu x3, NEAR = 250 smallest birth-element zeta vs
  FAR = 250 largest, pre-registered in predictions.md addendum):
  NEAR excitation unfolds as predicted (e_std median 0.0019, p90 0.0089,
  vs belt A's 4e-5 — 48x; some bodies pump mean e from 0.06 to 0.19), but
  cadence barely bites: K* histogram 4:182, 16:67, 64:1, never-sufficient 0.
  P8 FAILED (median K*(NEAR) = 4, not >= 16) -> the pre-registered kill
  branch fires: at mu x3, resonance-proximal, 5x horizon, kick cadence is a
  non-lever below 64/orbit for e-statistics behaviour; the tide's orbit
  average is already right at 4/orbit (H0190's premise, re-confirmed at the
  cadence level). FAR control: e_std median 2e-5 (dead flat — P7's second
  clause holds; NEAR/FAR excitation ratio 95x), K* 4:242, 16:8. P9 read 89%
  but is near-tautological by construction. Honest pooled savings vs
  uniform(p99 = 16): 4.4x (85% of bodies at the floor 4); the 43x in
  exp2_analyze.py compares against the ladder top (256) that nothing needed.
  Full table: `python3 exp2_analyze.py` (out_exp2_far.npz landed after
  write time; the run finished clean).
- FTLE (shadow renormalized every half perturber orbit): uniform ~7e-3/yr
  baseline across the whole belt = ln(1+s*6yr)/6yr with synodic shear s, i.e.
  the instrument measures phase shear, not chaos, at this horizon; resonant
  excess only ~10%, concentrated at the 4:1 (top-lambda bodies a 2.03-2.11).
  Measured: median lambda 6.86e-3/yr (A) vs 6.88e-3/yr (C, mu x3) — ratio
  1.00, exactly the shear-baseline prediction (P4's instrument reading).

Machine state: Linux 6.8.0, 8 vCPU shared with the window's other runs
(load 1.4-2.1 during the decisive runs), every process < 100 MB.

## Predictions

predictions.md was written before the ladder runs; the addendum before exp2.
What happened: P1, P2 failed (K* bottoms at the ladder floor where nothing
unfolds; the zeta ranker is sign-unstable). P3's factor-2 transfer held only
vacuously (belt C's K* constant). P4's lambda ratio reads ~1 for an
identified instrument reason (shear-dominated FTLE). P5 had no cliff to test
(no never-sufficient bodies at these horizons — unlike r4's resonant normal
form cases, my belts do not hit the phase-feedback regime within 120-600
orbits). Exp2: P7 half-held (NEAR excitation 48x belt A, FAR table in
out_exp2_far.npz), P8 failed and fired the kill branch (median K*(NEAR) = 4),
P9 moot. The refined reading: belt B (K* spread 32x) and exp2 NEAR (spread
4-16x) differ by unfolding RATE — B reaches e_std ~0.01-0.02 in 120 orbits
with ejections, NEAR reaches similar magnitudes only over 600, so cadence
demand tracks how much e-motion accrues per perturber orbit, not proximity
to resonance.

## What would make it wrong

- A behaviour metric coarser than the engine's certificates: if the plane's
  gates (B5/B17-style) are sensitive to quantities my mean/std/max e misses
  (apsidal phase, resonant angle), K* could be underestimated. The
  convergence control (512 vs 1024) only bounds self-consistency.
- The belt is planar and massless (no self-gravity, no mutual encounters);
  cadence demand at the same unfolding rate could differ with the real
  kick layer (orbit-averaged tides, H0190) — my kicks are the full tide.
- 600 orbits is still short vs the 10^4-10^5 yr secular timescales; the
  horizon story could invert at very long horizons (everything eventually
  unfolds). That is consistent with the claim: the bill follows the horizon
  the engine actually certifies.

## Cost of adopting

None as code: the deliverable is a redirection for q-cadence (schedule by
certificate horizon, not by a predicted per-body frequency) plus a measured
7x ceiling for per-body scheduling in belts where behaviour unfolds. The
FTLE-shear instrument warning is free to keep.

## Fit with PRINCIPLES

- "Compute only surprises" (3): cadence work should track unfolding
  behaviour, and the measurement says the surprise rate, not the resonance
  rank, is the observable — the horizon IS the scheduler's clock.
- "No work for no reason" (14) and "the simulation decides; heuristics
  schedule" (22): the ladder floor result says quiet belts owe ~4 kicks per
  perturber orbit and no more, at B5-level tolerances.
- "A failed expectation is not automatically a failed method" (H0183): the
  pre-registered zeta ranker failed; the diagnosis (horizon-governed demand,
  shear-dominated FTLE) is the payload.
- Via negativa: the negative result deletes the temptation to build a
  Chirikov-scalar cadence oracle into the compiler.

## The lens

The dynamics lens pushed me to Lyapunov/entropy framing; what the data
rewarded instead was an unfolding-rate framing (transients within a
certification window — the lens's own blind-spot warning: "long-run
behaviour can hide a transient that ruins a frame" cuts both ways: here the
transients are absent, and that absence is the result). The run may miss that
the engine's real certificate horizon per body is set by handoffs and
encounters, not by my fixed 120/600-orbit windows; the next run should
measure K* against the plane's own event cadence.
