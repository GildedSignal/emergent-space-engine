# predictions.md — 20261020-1815-redteam-38e2

Written BEFORE the decisive run (`python3 kerr_wedge.py` main). Only the
controls (C1–C3: quadrature cross-checks, Simpson convergence, one RK orbit)
ran first; everything below the line is unmeasured by me at writing time.

Attack: representation.md L67 ("a kick updates the cycle by a multiply-add")
in the zoom-whirl separatrix wedge, on Schwarzschild and Kerr dolls; B19's
256 uniform seeds as the putative (and, I predict, blind) rung guard.

## Predicted, in order of confidence

- **P1 (survivor).** Kerr equatorial cycles repeat: the RK-integrated orbit's
  per-cycle phi spacings are equal to ~1e-8 (repeat-ratio 1 ± 1e-8) and match
  the quadrature Dphi to < 1e-7 relative. The register's "in the plane, Kerr
  keeps rotational symmetry, so its orbits still repeat" holds exactly.
- **P2 (log divergence).** Dphi grows logarithmically in 1/delta: fit slope
  ~ 5–15 rad per decade at the spins measured; at a = 0.998 prograde,
  Dphi > 60 rad (> ~10 whirls) somewhere inside delta = 1e-6.
- **P3 (the kill contour).** The multiply-add's apsidal misprediction crosses
  B19's own 1% bar at delta* ≈ (10–100)x the kick size dE: so a 1e-3-class
  kick (Peters endgame; any strong tide near the rim) is out of bar already
  at delta ~ 1e-2..1e-1 (a fat slice of the bound space), while one-quantum
  kicks (2^-48) are out of bar only inside delta ≲ 1e-11.
- **P4 (compounding).** A chained inspiral of 1e-5-sized kicks entering the
  wedge accumulates > 2pi of phase error (a full cycle wrong) before the
  20-kick stop rule ends the walk, with the error growing superlinearly as
  delta shrinks (the stored derivative is the frozen one).
- **P5 (blind spot).** Uniform (L, E) seeds: fraction with delta < 1e-6 is
  < 1e-3 at both a = 0.9 and 0.998; B19's 256 seeds cannot see the wedge
  (expected hits ~ 0). Dynamics still visits it: every inspiral and every
  near-rim slingshot crosses into delta < 1e-6 by construction.
- **P6 (quantum-floor magnitude).** At the closest representable key (one q48
  from the separatrix), Dphi reaches ~ 150–400 rad (25–60 whirls) at
  a = 0.998 prograde — the stored dDphi/dE there is ~ 1e15-1e16 rad per unit E.

What would refute MY attack: if P3's contour sits at delta* < dE for all
physical kick sizes (multiply-add always in-bar), or if P2's slope is ~ 0
(no whirl growth), then L67 survives everywhere the player goes and the
premise stands; I would report the survivor with the measured envelope.
