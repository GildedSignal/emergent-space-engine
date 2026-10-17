# Predictions (written before the decisive run)

Attack: docs/representation.md §2 "Observables are emergent" (L53–59) enumerates the
view's physics — clock, colour (−p·u), aberration, lensing crossings from a memoized
deflection(b), blackbody beaming, aggregates, "Nothing bounces" — and omits opacity
entirely. The shipped gather (`crates/universe/src/view.rs`) is straight light ("no
lensing yet"), so nothing blocks anything: no black-hole shadow (capture), no eclipse
(no opaque worldtube test). The falsifier measures the size of what the player would
see wrong. Cases below are NOT tuned on: the numeric integrator is an independent
control for the analytic Synge boundary, and the near-rim behaviour is predicted from
theory before integration.

- **P1 (instrument validity, both sides).** Backward null-geodesic integration
  (d²u/dφ² = −u + 3u², M = 1, RK4) classifies r1's own photon-capture cases exactly:
  b/b_c ∈ {0.9, 0.97} capture (u reaches 1/2), {1.03, 1.1} escape after a turn.
- **P2 (the shadow boundary).** The exact Synge boundary α_sh = asin(√27·√(1−2/r_o)/r_o)
  agrees with the numerically bisected capture boundary to better than 1% of α_sh at
  r_o ∈ {100, 20, 6, 3.2} M (the wiki's own view-test radii, 6eae).
- **P3 (sky fraction; 2-D sky, fraction = α_sh/π).** r_o = 100 M: ~1.6%; 20 M: ~7.9%;
  6 M: exactly 25% (α_sh = 45°); 3.2 M: ~47%. With 10⁴ uniform sky emitters the
  straight gather fabricates rows inside the shadow arc accordingly (P4).
- **P4 (fabricated rows).** At N = 10⁴ emitters: >150 rows at 100 M, >700 at 20 M,
  ~2,500 at 6 M, >4,500 at 3.2 M — every one a star drawn where exact GR shows no
  arrival direction exists.
- **P5 (rim deflection diverges).** Total deflection at b = 1.01·b_c exceeds 3 rad
  (logarithmic divergence at the photon sphere); the weak-field series
  (4M/b + 15π/4·(M/b)²) misses it by more than an order of magnitude there — the
  doc's "memoized deflection(b)" readout is a perturbation whose domain ends at the
  shadow rim, and the letter is silent on rows whose straight b < b_c: keep-straight
  → fabricated in-shadow rows; drop-on-None (the shipped `deflection` returns None
  for captured b) → the emitter vanishes, though exact GR shows its images outside
  the rim at 100% of azimuths (6eae). Either wiring fails eclipse parity.
- **P6 (planet occlusion, flat geometry).** An opaque disk of radius R at distance d
  blocks an arc α = asin(R/d): at d = 10R, ~3.2% of the sky (~320 of 10⁴ emitters);
  at d = 2R (close approach), ~17% (~1,700) — stars visible through the planet.
- **P7 (the gap is total).** No file in `lab/rungs/`, no criterion in the frozen r6,
  and no line in `docs/representation.md` or `docs/law.md` gates the view's arrival
  set against opacity; r6's presence criterion requires the rows occlusion must
  remove (it counts their absence as a failure). Verified by search, not by tuning.

What would falsify the attack: α_sh matching but the fabricated fraction small
(<0.1% at game-relevant radii), or an existing opacity gate found in the tree.
