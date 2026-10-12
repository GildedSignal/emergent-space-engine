# Dossier — 20261012-1227-second-20261012-1117-redteam-4808-d617 (second author)

**Claim.** The checker's named experiment is done and it closes the loop: the
multiply-add kick layer's one-signed phase error fails both frozen budgets on
every orbit within margin μ = p − p_crit(e) ≤ 0.3 of the plunge separatrix
(drift 1.5e−2–6.9e−2 rad per 10³ kicks at δL/L = 10⁻⁴, all e tested), the band
is **fed** — 30–40% of captures from deep near-capture passages (r_p ∈ [4, 4.5]M)
land in it, at e ≥ 0.92 — and captured bodies **linger** there a median
~4×10⁴ kicks, accruing player-visible apsidal drift while the law's shipped
re-anchor rule (law.md "Not adopted" entry) never fires. The multiply-add needs
its domain rule; the prior run's claim, held out by the checker's experiment,
holds.

**Bottleneck.** Board focus lines 2/4 (motion law v2 / the changeover) and the
law's error model ("one error budget", representation.md §2). This closes the
premise red-team 20261012-1117's silver: its measured divergence is real AND
its domain is populated, so the hole is live, not dormant.

## What ran (all from shipped scripts, ≤ 60 s each except linger ~10 min)

- `check_instrument.py` — an instrument independent of the prior run's ODE:
  Δφ from the cubic roots of R(u) = E² − (1−2u)(1+L²u²) and a Gauss–Legendre
  quadrature on the root-factored integral (no ODE). Agrees with the prior
  run's `falsifier2.py` ODE (copied verbatim into `cycle.py`) to 7 digits at
  7 orbits, reproduces the checker's independent values (10.0552 at (10, 0.5);
  8.6969; 14.7651; 16.5960), the near-circular epicyclic limit
  Δφ/2π → 1/√(1−6/r₀) to 5 digits, and the separatrix root-merge at p_crit.
  This also closes the prior record's minor gap (its Evidence named an RK4
  cross-check that was not shipped).
- `kickgate.py` (E1) — the frozen rung **B-sep** (predictions.md): kick trains
  of 10³ kicks, δL/L = 10⁻⁴, alternating and random signs, on the shipped jet
  (exact offset plus stored derivatives, re-anchored at 730 quanta).
- `scatter.py` (E2) — the checker's toy: parabolic bodies (E = 1), r_p uniform
  in a window, one impulsive encounter at periapsis (k·v_p, v_p = √(2/r_p)
  exact), direction uniform; fates from the allowed region containing the body.
- `linger.py` (E3) — residents' walk: zero-mean kicks δL/L = 10⁻⁴, absorbed at
  plunge (region lost) or unbind (E ≥ 1); drift = jet error vs exact, accrued
  per kick, with the shipped re-anchor rule active.

## E1 — the frozen gate: the multiply-add fails at μ ≤ 0.3, at every e

| e | μ | gain | resid/kick (both signs) | A: ≤1e−6·Δφ | B: ≤5e−3 rad/10³ | verdict |
|---|---|------|------------------------|-------------|------------------|---------|
| 0.50 | 2.0 | 2.9 | +2.78e−6 | PASS | PASS (2.8e−3) | SAFE |
| 0.50 | 1.0 | 5.1 | +9.25e−6 | PASS | **FAIL** (9.3e−3) | UNSAFE |
| 0.50 | 0.3 | 12.7 | +6.88e−5 | **FAIL** | **FAIL** (6.9e−2) | UNSAFE |
| 0.50 | 0.03 | 75.2 | +4.90e−3 | **FAIL** | **FAIL** (4.9) | UNSAFE |
| 0.90 | 1.0 | 2.9 | +2.87e−6 | PASS | PASS | SAFE |
| 0.90 | 0.3 | 6.6 | +1.84e−5 | **FAIL** | **FAIL** (1.8e−2) | UNSAFE |
| 0.99 | 0.3 | 5.9 | +1.47e−5 | PASS (4%) | **FAIL** (1.5e−2) | UNSAFE |
| 0.99 | 0.03 | 36.3 | +1.07e−3 | **FAIL** | **FAIL** (1.07) | UNSAFE |

Full table in `run.log` (15 cells). The frozen verdict rule ("B-sep FAILS the
multiply-add if budgets fail at μ ≤ 0.3 for any e") fires. The residual is
identical for + and − kick signs at every cell — one-signed, hence compounding;
its rate scales as δL² exactly (train drift at μ=0.3, e=0.9: 1.85e−4 / 1.84e−2 /
1.84e0 rad per 10³ kicks at δL/L = 10⁻⁵/10⁻⁴/10⁻³), so smaller kicks only slow
it. **The e = 0.5 column is the worst at fixed margin** (its UNSAFE boundary is
μ ≈ 1, not 0.3): the prior dossier's high-e framing understated the domain, as
the checker suspected.

**The shipped rule does not catch it.** With random-sign kicks (10³ kicks at
μ = 0.3): drift −6.07 / −3.19 / −3.81 rad (e = 0.5/0.9/0.99) with **zero
re-anchors** — the accumulated offset reaches only 2.0–3.8e−3 of L against the
7.3e−2 trigger (law.md: "Not adopted" entry), and a recompile would not reset
the accrued phase anyway (it recomputes Δφ, not the body's already-advanced
angle). The trigger watches the wrong quantity for this error.

## E2 — the band is fed: by deep near-capture passages, and by nothing else

Fractions of 10⁵ bodies per cell (full grids in `run.log`):

| r_p window | k | plunge | band | band\|captured | band e-range |
|---|---|---|---|---|---|
| [4, 8] | 1e−3 | 0.001 | 0.019 | 0.037 | [0.992, 1.0] |
| [4, 4.5] | 1e−4 | 0.001 | 0.150 | **0.30** | [0.999, 1.0] |
| [4, 4.5] | 1e−2 | 0.078 | 0.128 | **0.31** | [0.92, 1.0] |
| [4, 4.5] | 3e−2 | 0.244 | 0.098 | **0.39** | [0.76, 1.0] |
| [5, 8] | ≤ 3e−2 | 0.000 | 0.000 | 0.000 | — |

The geometry the predictions froze is what the exact map shows: a tangential
retro kick at periapsis preserves r_p, so a capture is born at margin
≈ L²(1−2/r_p) − 4 ≈ 2r_p − 8: **every capture at r_p ∈ [4, 4.15]M is born in
the band**, and the band's fed width grows with kick strength (band captures up
to r_p ≈ 4.4 at k = 3e−2). Wider periapses ([5, 8]) essentially never feed the
band at k ≤ 3e−2; bound-bound scatters (second channel, parents at μ = 1) reach
it only at k = 0.1 (16% of captures). So the band's feed rate is the rate of
deep passages (r_p within ~0.5M of the plunge boundary) — near-capture
encounters and any percent-level thrust there (thrust is a kick too:
"decisions are the only kinks").

## E3 — bodies linger, and the drift runs away (not merely visible)

4096 residents each, seeded as captures put them there (μ₀ ∈ (0.05, 0.3]),
zero-mean kicks δL/L = 10⁻⁴, absorbed at plunge or unbind:

| e | plunge / unbind | residence (median, p90) | accrued drift (median, p90) | > budget B | re-anchors |
|---|---|---|---|---|---|
| 0.9  | 68% / 32% | 4.1e4, 1.4e5 | **−2.1e4 rad**, −3.3e3 | 100% | 0 |
| 0.99 | 45% / 55% | 1.7e4, 5.9e4 | **−5.7e3 rad**, −77.6 | 100% | 0 |

Nobody survives to the 2×10⁶ cap. The runaway is dominated not by the per-kick
truncation (−10⁻⁵ rad/kick) but by the jet's quadratic error over the
random-walk excursion (∝ Δφ″·(accumulated offset)²), so it grows ~N²: −3 to
−6 rad at N = 10³ (E1) → −2×10⁴ rad at N = 4×10⁴ (E3) — thousands of full
apsidal turns wrong, while the shipped offset trigger (7.3e−2) never fires
(max offset ≈ 0.03). Entry from above (μ₀ ∈ (0.3, 0.6]): 18% of e = 0.9
walkers transit the whole band into plunge before unbinding — the band is not
only fed at birth; diffusive entry from just above is at the ~1/5 level.
(e = 0.99's entry row is degenerate: its family's bound branch ends at
μ = 0.53, so most seeds sit at the unbinding edge and leave immediately — 0.5%.)

## Predictions (scorecard; all frozen before the runs)

- **P1** mostly right, one cell wrong and one direction worse than predicted:
  Budget A holds at μ ≥ 1 (all e) ✓, fails at μ ≤ 0.3 for e ∈ {0.5, 0.9} ✓ but
  passes (by 4%) at (e=0.99, μ=0.3) ✗; Budget B fails at μ ≤ 0.3 for all e ✓
  and *also* at (e=0.5, μ=1), which I did not predict. Re-anchor: never fires ✓,
  but my "gap ≥ 10²" was wrong (the offset random-walks to 20–38 quanta; gap
  19–36×) — I ignored the √N walk when freezing.
- **P2** half right: the deep-window structure held (30–40% on [4, 4.5],
  e ≥ 0.8 ✓, plunge < 1% at k = 1e−4 ✓), but the letter of my "≥ 5% at
  r_p ∈ [4, 8]" is wrong (3.7–3.8%), and "> 30% plunge at k ≥ 0.1" holds only
  on the deep windows (12% on [4, 8]). By the frozen classification the band is
  "commonly populated" (≥ 5% over contiguous k ∈ [1e−4, 1e−2] on [4, 6] and
  [4, 4.5]) and is not dormant anywhere.
- **P3** right, conservatively: residence ≥ 10³ kicks ✓ (median 1.7e4–4.1e4,
  17–40× the frozen floor), drift ≥ 5e−3 rad ✓ (measured 10⁶–10⁷× that), and
  the walk is not biased out fast ✓. What I under-predicted: the drift is not
  linear-in-N (~10⁻⁵/kick) but ~N² via the excursion term — even the E1 trains
  at safe margins would eventually cross any budget if the walk persists.

## What would make it wrong

The feed rate is conditional on deep passages: if a universe never puts bodies
within r_p ≈ 4–4.5M of a hole (no battles there, no capture cascades), the
band stays empty and the hole is dormant — the gate still fails on its own
terms, but nothing hits it. The toy's encounter is one impulsive kick at
periapsis; a sustained interaction (many small kicks during the passage) would
concentrate captures toward the band's top edge the same way the k-sweep shows
(k larger → wider fed width, more plunge). Residence is measured under
zero-mean kicks: a systematically retro kick stream (inspiral) crosses the
band faster, but each crossing still accrues the one-signed drift at the
band's rate.

## Cost of adoption

One domain rule in the law: below μ = 0.3, the multiply-add does not update
the cycle. The exact fallback is already shipped (the darwin16 compile,
law.md:2), and the record bounds the cost: a drift-counter trigger (recompile
when accrued |drift| > floor, ~10⁻⁵ rad/kick ⇒ one compile per ~100 kicks per
band resident) costs ≈ 0.01 compiles/kick for residents and ≈ 0 for the
population at large — cheaper than the shipped offset trigger's own 0.05
compiles/kick. No new component; B-sep is the rung that guards it.

## PRINCIPLES fit

"basically we don't want errors that can compound that's the goal" (P13): the
residual is one-signed per kick at every tested (e, μ) and its rate scales as
δL², so it compounds at any kick size. "what really matters is navigation…
need to be perfect" (P30): the accrued drift is apsidal, near a black hole,
reaching radians. "A failed expectation is not automatically a failed method"
(H0183): the multiply-add is not killed; μ ≤ 0.3 is its domain boundary.

## The lens (second author)

Second-authoring rewards reproduction over novelty, and this run inherited the
first author's instrument debt: my independent quadrature initially carried a
2× weight bug and an eigval root-solver that silently mis-stated the region
structure below the unstable-circular angular momentum (a body at fixed r_p
below L_c is on the plunge branch even though the sorted roots spell a bound
orbit). The region-aware classifier (allowed region containing the body) is
what makes the scatter fates trustworthy; the frozen predictions were written
before it existed, which is the right order. What this lens may miss: the toy
is one hole, one kick, 2D equatorial — Kerr and repeated-passage structure
(the whirl itself storing phase) are untouched.

## Grade suggestion

Gold: the checker's named experiment ran, against criteria frozen before it,
and both branches resolved — the gate fails at μ ≤ 0.3 (every e), the band is
fed by the deep-capture channel (30–40% of [4, 4.5] captures), bodies linger
a median 1.7–4.1×10⁴ kicks accruing −5.7×10³ to −2.1×10⁴ rad of apsidal drift
(100% of residents past the budget), and the shipped re-anchor rule never
fires while it runs away. Every number regenerates from the shipped scripts in this folder
(`run.log` is the tee of each run).
