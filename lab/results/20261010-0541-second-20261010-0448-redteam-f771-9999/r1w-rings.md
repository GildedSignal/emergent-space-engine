# Rung r1w: orbits in rings around one mass — the widened re-freeze (DRAFT)

Draft for the integrator by the second author of run
20261010-0541-second-20261010-0448-redteam-f771-9999. r1 is DISPUTED pending a
clean re-run; this is that re-run's spec, measured end-to-end in
[r1w-output.txt](r1w-output.txt) + [metrics.json](metrics.json) (Python float64
port; the integrator re-runs the rung in the shipped harness). Base text:
[r1-rings.md](../../rungs/r1-rings.md). Changes are marked **[w]**; everything
else is r1's frozen text carried unchanged.

**Question.** Unchanged: around one static Schwarzschild mass (G = c = M = 1,
equatorial plane, float64), are orbits and light correct in a cell model where
motion inside a cell is that cell's exact local solution, the cells follow the
rotational symmetry, and one radial cycle repeats exactly?

**Configurations.** Unchanged: `binet-m8`, `binet-m16`, `binet-m32` (+
`binet-m64` measured analysis-only for the m⁻² law), `river-m16`, `river-m32`,
`square` (negative), `tiltonly` (negative). The in-band law is unchanged,
including the hyperbolic branch of r1 line 10 — **[w]** which must now be
implemented (the original probe asserted on it; the widened domain and r1's own
capture cases need it: `u = u* + A·e^{λφ} + B·e^{−λφ}`, `λ = √(6u_k−1)`,
events closed-form as the quadratic `A·x² − (edge−u*)·x + B = 0` in `x = e^{λφ}`,
turning points at `x = √(B/A)`).

**Implementation invariants learned the hard way** (all violated by the shipped
probe's own code at the widened domain; each one measured in this run):
1. **Absorb/capture edges must sit off the dyadic band grid.** `u = 0.5` (r = 2)
   is exactly `2^{−16/16}` — a band edge for every m that divides 16. A stop
   placed there never fires (the band-edge event fires first and its nudge
   carries the orbit *past* the horizon); plunging orbits then propagate into
   nonsense interior bands. Place absorb edges at `0.5·(1−ε)`. Measured: all 6
   capture cases misbehave without it, all 6 correct with it.
2. **The event landing point carries reconstruction error ~R·ε (R = in-band
   amplitude), not ~u·ε.** A landing nudge proportional to u (the shipped
   `u·(1±1e-12)`) loses when R/u ≫ 1 — always true in a light ray's far tail
   (R ≈ 1/b against u → 0): the state stays in the old band, the oscillator
   escapes the band at full amplitude, and the inbound leg becomes a straight
   line (measured: 50% of the deflection gone; photon capture misclassified at
   ±3% of b_crit). The nudge must scale as `(u+R)·1e-13`. With it, deflection
   errors are 6.7e-5 at m32 and photon capture classifies all 4 cases at both
   m16 and m32.
3. **Near-circular seeds (e ≲ 0.02) can spend a whole radial cycle inside one
   band.** The event set must include extremum-to-extremum segments inside a
   band (half a rotation); the shipped event search returns nothing there.
   These seeds are exactly the low-e strong-field axis where m16 fails.

**Cases** (sampler: Python `random.Random(20261010)`, drawn in this order).
- **[w] Bound seeds:** 256, with p log-uniform in [10, 1000] then e log-uniform
  in [0.01, 0.99] per attempt (was: e uniform in [0, 0.7]). Reject and redraw
  the pair unless p ≥ 6.5 + 2e and the exact orbit is bound (E² < 1, real
  turning points). The e floor 0.01 keeps the radial amplitude above the
  in-band circular degeneracy; the e cap 0.99 is load-bearing — at e ≳ 0.999
  the period error passes 5% and grows ~5× per 0.004 of e (measured wall:
  9.6e-3 at 0.995, 4.9e-2 at 0.999, 7.7e-1 at 0.9999, all still bound at m32).
- **[w] Low-e strong-field grid** (the second envelope hole, explicit): r_p ∈
  {10.9, 12.0, 13.4} × e ∈ {0.01, 0.02}, judged per-point against the same
  bands. m16 fails all 6 (up to 3.7e-3 period, 1.5e-2 precession on the axis);
  m32 passes all 6 (worst 9.9e-4, marginal); m64 passes with ≥ 9× margin.
- Light seeds: unchanged (64, b log-uniform [10, 1000]) — **[w]** swept from
  and to r = 10⁸ with each side's own exact tail integral
  ∫₀^{u₀} du/√(q−u²+2u³) (residual tail-modeling difference measured 1.2e-11
  relative; the flat 4/b oracle control and the 4/b scaling are in the output).
- Capture, photon capture, ISCO, long runs: unchanged cases, **[w]** with
  invariant 1 applied (absorb edge off-grid) and the long runs' repeat
  criterion anchored: every later cycle's Δφ and Δt equal cycle 1's to 1e-12
  relative, and the band-crossing sequence of cycle 2 equals cycle 1's
  (measured at m32: fraction 1.0000, max first-cycle deviation 6.8e-16; the
  shipped probe's 1.17e-11 at (8, 0.95) reproduces exactly).

**Oracle.** Unchanged ports (periapsis_elliptic, bound_period_quad,
deflection_quadrature). This run's independent oracle: vectorized RK4 exact
Binet, h=1e-4, Richardson 1.1e-12 (Δφ) / 5.2e-13 (period); precession → 6π/p
at +3.1% (2PN scale); ties to the shipped scalar oracle with dphi exact.

**Metrics.** Unchanged names and thresholds. Measured verdicts at the widened
envelope (this run): `binet-m16` FAILS `prec` (0.9883; worst 1.54e-2 — the
low-e axis) and `period` (0.9766; 6 fails, both axes) → KILLED by the widened
envelope, two criteria; `binet-m32` passes every criterion (prec 1.0 / prog
1.0 / period 1.0, worst 5.97e-4 / defl 1.0, worst 6.7e-5 / capture 0 wrong /
isco 1 / shape 1.0 / repeat 1.0 / crossings median 18, worst 312);
`binet-m64` passes but costs median 38 and worst 624 crossings/cycle — over
the 512 budget per-seed at the top e, so m = 32 is the unique m satisfying
both the physics bands and the cost budget.

**Per-e period-band decision (measured, for the integrator).** The error is a
fixed non-compounding bias per (E, L) (retrace-verified) scaling as m⁻²
(slopes −1.97 to −2.02 across the fixed cases; faster, −2.7 to −3.7, on the
low-e axis). At m = 32 the largest e with per-seed period error ≤ 0.1% is
e* ≈ 0.95 at r_p ≤ 8 M, 0.97 at 10 M, 0.98 at 15 M, 0.99 at r_p ≥ 30 M. Per-seed
0.1% at e = 0.99, r_p = 7 needs m ≈ 70 ⇒ ~1100 crossings/cycle, outside the
512 budget: unreachable by m alone. Expected per-seed failures of the 0.1%
band under the widened sampler ≈ 0.5 of 256 (Fermi over the e* table), against
the 2.56 the fraction criterion allows — m32's pass is not draw-luck. So: keep
0.1% as the fraction criterion (≥ 0.99), freeze the domain at e ≤ 0.99, and
record err₃₂(e, r_p) as a calibratable arrival-time bias (navigation may
calibrate; the integrator decides whether a per-e band table is worth the
hiding).

```configs
binet-m8 candidate
binet-m16 candidate
binet-m32 candidate
river-m16 candidate
river-m32 candidate
square negative
tiltonly negative
```

```criteria
prec behaviour precession_pass_fraction >= 0.99
prog type prograde_fraction >= 1.0
period behaviour period_pass_fraction >= 0.99
defl behaviour deflection_pass_fraction >= 0.99
capture behaviour capture_misclassified <= 0
isco behaviour isco_correct >= 1
shape type shape_kept_fraction >= 0.99
repeat type cycle_repeat_fraction >= 0.99
cost cost crossings_per_cycle <= 512
```
