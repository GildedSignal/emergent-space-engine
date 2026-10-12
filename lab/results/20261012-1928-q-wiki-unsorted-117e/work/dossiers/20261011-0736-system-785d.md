# Dossier — run 20261011-0736-system-785d (lens: the whole system)

## Claim

The resonance gate is not a classifier with a width constant: **one certificate —
excursion(δ) = min(2·ṗ_coh/|θ̇(δ)|, c_H·μ^(1/3)), every term already computed by the
engine** (compiled frequencies, the kick quadrature, the masses) — predicts where and at
what quantum the orbit-averaged law fails, and derives B17's detuning convention
W = 2.5·μ^(2/3) as the crossing of its two terms instead of a frozen number.

## Bottleneck

Board focus line 1–2 (fewer kicks; the changeover near a secondary, reversible and
integer) and the law's resonance gate ("averaging only away from resonance", law.md).
The gate is today a detection step ("p·Ω₁ − q·Ω₂ ≈ 0") plus a scan convention (B17's
W). If the gate is one certificate in the same arithmetic as the kick cadence, the jet
re-anchor (√(floor/C)) and the slack queue, the engine deletes a mechanism (principle 1)
and gains a computed changeover: switch to the rotating binary doll exactly when
excursion crosses the quantum. Expected gain: not a speed factor but a deletion — one
expiry rule where there was a classifier, a width table and a special case; and the
cadence/revalidation schedule near every resonance comes out of the same numbers.

## Evidence (all commands ≤ 25 s wall each, Linux x86, 8 vCPU shared, float64 — orders of
magnitude only)

Scene: r4 v3's cases (interior (j+1):j resonance, circular perturber, e₀ = 0.02, 8 phase
seeds, 200 synodic periods, leapfrog at P₂/600; μ ∈ {3×10⁻⁴, 10⁻³, 3×10⁻³}; j = 1 (2:1)
and j = 2 (3:2); Δa/a grid 0…±0.032). Truth: barycentric leapfrog, energy drift ≤
3×10⁻¹²; μ = 0 control: e bounded with exactly the (n₁dt)²/2 ringing, zero drift.
Cheap side (no truth): θ̇ = (j+1)n₂ − j·n₁ − ϖ̇_sec from Kepler frequencies plus a
double-averaged precession; ṗ_coh = the slow-phase amplitude of de/dt from a λ₁-quadrature
at fixed resonant angle (the same orbit-average the engine's kick layer computes).
Instrument: e's running mean over one synodic period; "band" = its peak-to-peak;
failure = leaving [e₀ − q_e, e₀ + q_e].

1. **ṗ_coh is exactly μ-linear** (7.31e-4 / 2.44e-3 / 7.31e-3 at 2:1) — one quadrature,
   no per-μ work.
2. **Capped excursion law** (predictions P1–P2, capped form): over 327 circulating
   systems (5 cases), band / min(2ṗ/|θ̇|, c_H·μ^(1/3)) has median 0.88, p10 0.43,
   p90 1.14; **99.4% within [0.3, 3]**; per case 97–100%.
3. **The cap is the Hill scale**: c_H = 1.112 (2:1) and 0.935 (3:2), each constant in μ
   to ±1% across 10× in μ — the saturated excursion is c_H·μ^(1/3), independent of δ.
4. **Never under-predicts** (P4a): across the full (δ, q_e) grid — 15 quanta × 15
   detunings × 8 seeds × 5 cases — **zero** failures of the averaged law where the
   certificate's excursion < q_e/2. A certificate that never under-predicts is a guard
   (principle 34).
5. **The convention derived**: the crossing 2ṗ/|θ̇| = c_H·μ^(1/3) gives, in period-ratio
   units, W = 0.0100 / 0.0230 (2:1, μ = 3×10⁻⁴ / 10⁻³) against B17's 2.5μ^(2/3) =
   0.0112 / 0.0250 — **8–12%**, with the μ^(2/3) scaling produced, not assumed.
6. **Regime boundary** (librate/circulate, measured at circ-fraction 0.5): predicted
   within 20% and 4% for 2:1 (μ = 3×10⁻⁴, 10⁻³); μ = 3×10⁻³ predicted beyond the grid
   and measured at the grid edge (consistent); **3:2 overpredicted ~2× — the named hard
   case** (closer conjunctions; see the lens section).
7. **The time model failed** (P3): time-to-failure at exact resonance = κ·q_e/ṗ_coh with
   κ = 2.98 / 3.48 / 6.40 / 5.62 / 11.13 (prediction [1, 4]): 2 of 4 held-out cases
   pass; κ falls as q_e grows (κ ∝ q_e^(-0.35…-0.68)) — the coherent-linear pump
   over-estimates the rate, the phase feedback r4 measured as "2×" is q- and μ-dependent
   in time. The certificate is an amplitude guard, not a clock inside the zone.

Commands (from this folder): `python3 probe.py selftest`, `... quad`, `... calib`,
`... scan 1 0.001` (and 1 0.0003, 1 0.003, 2 0.0003, 2 0.001), `python3 analyze.py`.
Data: `quad.json` (cheap-side certificate inputs), `scan-j*-mu*.npy`, `metrics.json`,
`final.json` (verification numbers above). Wall times: scans 11–22 s each.

## Predictions

`predictions.md` was written after calibration on ONE case (2:1, μ = 10⁻³) and the
controls, before the four held-out scans. Outcome: P1 **failed as written** (the
uncapped 1/|θ̇| law: 165 violations — the excursion saturates), **passed in the capped
form** (99.4%, above) — the cap is the diagnosis; P2 passed for 2:1 (0.93–1.02) and 3:2
μ=10⁻³ (0.96), marginal for the two smaller cases (0.49–0.64); P3 failed at 3 of 4
held-out cases (κ up to 11); P4a passed (0 violations); P4c held wherever the predicted
boundary was inside the grid (2:1); P5 untested (matched detuning pairs sit inside the
saturated zone, where the cap is symmetric by construction).

## What would make it wrong

- c_H is empirical: circular coplanar perturber, e₀ = 0.02, single perturber, j ∈ {1,2}.
  Eccentric or inclined secondaries, other j, or resonance overlap (μ ≥ 3×10⁻³ smears
  the boundary; circ-fraction transitions are 0.25–0.88, not sharp) could move it.
- The 3:2 boundary miss (2×) suggests the slow-phase quadrature over-counts when
  conjunctions are close — if the same factor appears at 4:3 or for eccentric
  perturbers, the crossing-derived W is not general and the gate needs the quadrature
  re-run per geometry (still cheap, but a table by stealth).
- Float probe on a cloud x86 box; the engine's integer law must re-derive c_H on its own
  grid (the lab rules: floats explore, integers decide).
- If the engine ever needs the time-to-failure inside the zone (not just the switch),
  this certificate does not provide it (item 7).

## Cost of adoption

Small: θ̇ comes from frequencies the compiler already emits; ṗ_coh is the existing
orbit-average evaluated at fixed slow phase (one more quadrature per (doll, resonance
class), memoizable); c_H is one constant per resonance family, or re-derived per
geometry. Deletes: the resonance detection step and its threshold, B17's width constant
as an input (it becomes an output), and any width table. The changeover to the rotating
binary doll becomes certificate-driven, in the same shape as the JANUS integer
changeover direction.

## Fit with PRINCIPLES

- "No central control and no categories: regimes are chosen by dimensionless numbers"
  (4): the gate stops being a class ("resonant") and becomes a number against a quantum.
- "The cheapest compute is compute not done. Delete before optimizing" (1): a mechanism
  (the classifier + width) is deleted, not tuned.
- "Compute only surprises… error type over error size" (2, 3): the certificate expires
  exactly when a surprise can reach the quantum; inside the zone the error type is
  bounded-by-construction (switch), not accumulated.
- "A game is an illusion spectacle; the oracles are guards, not shepherds" (34): the
  certificate rejects the averaged description where the player would see a wrong e; it
  does not model the zone — the binary doll does.
- The lens brief: "two mechanisms that are secretly one" — the certificate's expiry and
  the kick amplitude are the same quadrature; the resonance gate, the kick cadence
  (quantum ÷ rate), the jet re-anchor (time for accumulated drift to reach √(floor/C))
  and the slack queue are one arithmetic, with the light cone (distance ÷ c) as its pure
  member. What it unifies: every "when to look again" in the engine. What it deletes:
  the resonance classifier. Cheapest experiment that shows it keeps the behaviours: this
  probe (25 s per case, reproduced numbers above).

## The lens (what it may have made me miss)

A whole-system lens hunts unifications and can over-claim one constant where there are
two regimes. The hard special case is visible in the data: 3:2 (the closer resonance)
breaks the boundary prediction by 2× — the elegant crossing is least reliable exactly
where encounters are strongest, which is also where the co-orbital certificate
(20261006-0346-taleb-09b5) found its own failure. Second miss: I did not test eccentric
or inclined perturbers, and did not test the certificate's boundary against a second
independent truth (a different integrator or the plane itself) — the truth here is one
leapfrog at one step size (energy drift 3×10⁻¹², but the r4 v2 checker's lesson about
convergence ladders stands). Third: the saturated-zone time behaviour (κ) is reported as
a failure of my prediction, not explored — the binary doll's own clock may predict it,
which would extend the unification rather than break it.
