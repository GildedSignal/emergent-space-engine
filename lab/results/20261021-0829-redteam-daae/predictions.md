# Predictions (written before the decisive run)

Question: does the view's past-light-cone gather, as specified (a `delay(b)` column
memoized per doll, keyed by b alone — the cure column named by 5977/9f4a/fb64, with
8be2's finding that the *deflection* key needs (sense, b)), read the wrong arrival
time at rotating dolls? Oracle: exact Kerr equatorial null geodesics, quadrature of
dt/dr from the Carter constants (M = 1, E = 1, L = b_signed, Q = 0), emitter r_e = 6,
observer r_o = 100. Error of the χ-blind gather := t_exact(χ, b, sense) −
t_static(|b|), the delay the letter's column would return.

Cases I have NOT tuned on (held out):

- **P1.** At χ = 0.9, b = 8, prograde, the χ-blind error exceeds 10% of the
  Schwarzschild delay Δt_Schw(b) itself. (Mechanism: the frame-dragging time term is
  order a × the same log that carries the static delay.)
- **P2.** The prograde−retrograde arrival-time difference at the SAME |b| (χ = 0.998,
  b = 8.5) exceeds the whole static delay Δt_Schw(8.5): |Δ_sense| > Δt_Schw. If true,
  no b-keyed column (even sense-averaged) can serve both senses at any useful width.
- **P3.** The error is linear in a at fixed sense: [t(χ=0.5) − t(0)] / [t(χ=0.25) −
  t(0)] = 2.00 ± 0.05 at b = 10 (a perturbative-in-a leading term, so the cure can be
  one closed correction, not a second memo table).
- **P4.** Player-visibility (0b45's channel, emitter on a circular orbit at r_e = 6):
  the emission-time error renders the emitter out of phase by > 30° somewhere on
  χ ∈ {0.9, 0.998} × b ∈ {8, 8.5, 12} prograde. (0b45's flat-light-time worst case
  was 86°; the χ-blind delay is the next order of the same channel and should be
  comparable, not negligible.)
- **P5 (the memo's domain edge).** At b = 20, χ = 0.5, the error is below 1% of
  Δt_Schw — the χ-blind column decays toward weak field like a/b, so the kill is a
  strong-field rotating-doll kill, not a global one.

Controls that must pass before any case counts (both sides):

- **C+ (positive).** Instrument: at a = 0 an independent RK4 integration of the same
  orbit (the λ-equations, not the quadrature) reproduces the quadrature's t to
  < 1e−6 M at every b flown. Physics: the Shapiro log coefficient fitted at
  b ∈ {12, 20, 40} (where the 1PM term dominates) is c = 2.00 ± 0.02; at b = 6 the
  higher-PM terms shift the naive fit (reported, not judged).
- **C− (instrument).** Sense symmetry: t(a = 0.9, b retrograde) = t(a = −0.9, |b|
  prograde) to the quadrature's convergence (< 1e−9 M); and step-halving changes the
  answer < 1e−9 M. A quadrature that cannot hold these has no standing on P1–P5.

Kill criterion for the premise: if P1 and P2 both fail (χ-blind error < 10% of the
static delay everywhere AND |Δ_sense| < Δt_Schw at χ = 0.998), the b-keyed delay
column survives as specified and I report the premise as standing with these numbers.
