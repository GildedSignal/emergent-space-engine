# Predictions — panel-grid floor of `Orbit::compile` (written before the oracle run)

Component: the compiled cycle's panel grid (`OrbitShape::bound`, crates/space/src/orbit.rs).
Question: how many panels does the 4-point Gauss walk actually need to hold the law's
~2^-30 total certificate, versus the shipped fixed EDGE ladder (2^(-j/16) band edges,
~16 panels per octave of x, CAP = pi/4 chunks, dyadic cut doubling near the layer)?

Cases I have NOT tuned on (the oracle decides them; the grid is chosen blind from the
record's key ranges, not from my results):

- P1 (ladder vs floor on the belt band): at p >= 8, e in [0.9, 0.9999] the shipped
  ladder is >= 8x above the bisection floor N* (the integrands are smooth in psi; only
  the 1/x^2 amplitude spread and, near the separatrix, the 1/sqrt(1-q a) layer force
  refinement). Expected ratio band: 8–25x.
- P2 (scaling): N* grows only weakly (log-like) as e -> 1 at fixed p (x_apo = 2k-1
  shrinks but 1/x^2 stays smooth in psi), while the ladder grows 16 per octave — so the
  ratio is roughly flat or rising in e, not falling.
- P3 (low-e collapse): at e <= 0.1 the ladder is already near its CAP-minimal ~4–8
  panels, so the ratio collapses to ~1–2x.
- P4 (separatrix): keys pushed toward the refusal edge (small delta = 1 - q(4k+2))
  must show the ratio falling toward a small constant (<= 4x): the peak layer width
  ~sqrt(delta/(q(1-k))) genuinely forces a geometric grid, and dyadic doubling is
  near-optimal for a square-root endpoint layer.
- P5 (Carlson-table pricing): at N* knots, a Carlson-built table priced at de99's
  6.5–30 us per 3-channel incomplete evaluation costs more than a thinned walk at
  N* panels (~1.3 us/panel node work) at every key in the grid — i.e. the table
  rebuild (closed-form-kernel open direction 2) is not the cheap compile lever; a
  thinned integer grid is.
- P6 (oracle sanity, a control not a prediction): the float oracle's total integrals
  must match the shipped increments (advance/period/proper_period decoded) to <= 1e-9
  relative on every key, and the shipped ladder's own summed panel error must sit at
  or below 2^-30 — otherwise my integrand transcription is wrong and everything above
  is void.

Kill criterion for the run: if P6 fails on any key, the run is VOID regardless of P1–P5.
