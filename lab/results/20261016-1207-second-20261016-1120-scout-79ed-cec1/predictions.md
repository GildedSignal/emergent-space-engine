# Predictions — r1v2 execution (written before the decisive run)

Pre-registered against the freeze `r1v2-rings-band-constant.md` (sha256 recorded in
dossier.md). The instrument is rebuilt from 20261016-1120-scout-79ed's script: band_of
dyadic-edge fix, exact hyperbolic segment solver, escape detection, light/capture/ISCO/
long-run channels added. Cases not tuned on: everything except the handful of debug rows
already shown in the scout run and its check (frozen circle errors at three radii, the
sampler medians).

- **P1 (circles, the decisive channel).** centre arm: worst relative advance error
  ≥ 1.5e-2 at m=16 (fails the 1% bar on near-edge rows; fe85's first-order family,
  2π(1/√(1−6u_k)−1) at worst offset). refit arm: worst ≤ 1e-8 at every m (the refit's
  fixed point puts u_k at the circle's own u0; the band ODE's circular solution then
  coincides with the GR circle). Both arms' circle period errors track the same pattern
  (centre worst ~1e-2..1e-1 at small r, refit ~1e-14).
- **P2 (strong-field rows).** Both arms pass advance (1%) and period (0.1%) at m=16 and
  m=32 on all six rows — the hyperbolic periapsis band's Taylor error is second order in
  the band width. m=8: the deepest row (8.5, 0.9) may fail the period bar (width 4×).
  If both arms fail a row at m=16, that is a model limit, not a rule difference; I will
  report it as such and the freeze fails every candidate there.
- **P3 (capture + photon capture).** 0 misclassified for both arms at m=16 and m=32
  (rows are ≥3% from the threshold; the model's barrier error is ~1e-3 relative at
  m=16). m=8 centre: possibly 1 misclassification on the photon 0.97/1.03 rows
  (barrier error ~4× the m=16 one, still likely inside 3%). refit ≡ centre on absorbed
  rows (no turning band visited) and differs only in the turning band on escaped rows.
- **P4 (ISCO).** r=7, L=1.01·L_c stays bound (100 cycles, and by exact per-band
  reversibility the first cycle decides); r=5.5, L=0.99·L_c plunges within 50 cycles —
  both arms, m=16 and m=32. The r=5.5 row starts inside hyperbolic-band territory
  (u=0.182 > 1/6): it exercises the fixed solver.
- **P5 (light).** 64/64 within 1% for both arms at m=16/m=32 (deflection error is
  second order in band width; b ≥ 10 never enters a hyperbolic band). The refit moves
  deflection by ≲ 1e-3 relative (turning-band constant shifts by ≤ band width; effect
  on the integral second order). m=8: expect ≥ 63/64.
- **P6 (long runs, 32 seeds × 10⁴ cycles).** shape 32/32 both arms (drift is rounding-
  scale). repeat to 1e-12: uncertain. Per-cycle rounding drift in the returned apoapsis
  is ~1e-16 relative; if it walks randomly over 10⁴ cycles the cycle-Δφ spread reaches
  ~1e-14..1e-12 — I predict ≥ 0.99 of seeds hold 1e-12 in both arms (arm-independent),
  but a few seeds may sit at the bar. This is the first execution of the letter's 10⁴-
  cycle repeat bar by anyone (H0205 was never graded).
- **P7 (sampler, letter-pinned draw).** centre m=16: prec 250–256/256, median advance
  error 1.7–2.1e-4 (the draw changes from the scout run's, which had a dead RNG line;
  the scout's 1.83e-4 median calibrates the neighbourhood). refit m=16/m=32: prec
  256/256, period ≥ 255/256. refit m=8: prec ≥ 255/256 but period 0.975–0.985 (< 0.99,
  m=8 stays unlicensed — consistent with two prior draws). prograde 1.0 in every arm.
- **P8 (crossings).** Median crossings identical between arms at the same m (the refit
  never adds or removes a crossing): m8 ≈ 18, m16 ≈ 34, m32 ≈ 68, all ≤ 512.

**Kill bar (pre-registered).** If `binet-m16-refit` or `binet-m32-refit` fails any of
prec/prog/period/defl/capture/isco/shape/repeat/cost/nearcirc/strongf, the one-law refit
is killed for the primary in-cell law and only a contained-only variant remains live.
If both refit configs pass everything while the centre configs fail only nearcirc (and
m8-centre fails prec as the negative control), the freeze discriminates and the refit
wins: gold stands. A both-arms failure on a shared criterion (e.g. repeat at 10⁴ cycles,
or a deep strong-field row) is a certificate finding about the case set, not an arm
verdict; it goes to the integrator as such.

**Cheapest decisive part.** If time forces cuts: the long-run channel at m=32 first
(halve its seeds to 16), never the circles, the capture/ISCO set, or the m=16 pair.
