# Predictions (written before the decisive run)

Run 20261019-0628-redteam-638b. Attack: the composed strong-field view —
`docs/representation.md` L57 ("Each visible tube crosses the observer's past
light cone once; Newton's method finds the crossing ... Lensing adds crossings,
from each doll's memoized deflection(b)") and the measured occlusion cure
(22d1's per-row worldtube test, the r11 absence half) in the field of a black
hole. Oracle: exact Schwarzschild null geodesics, 2D plane (the game's sky is
S¹), M = 1, static observer at r_o, sources on the celestial circle at
infinity plus one static beacon at r_s = 4 M.

Not tuned on: everything below is derived from GR textbook structure, not from
a pilot run of the instrument. Written 2026-10-19 before `sky.py` ran once.

- **P1 (shadow law).** The exact shadow arc is 2·arcsin(min(1, b_c·√(1−2/r_o)/r_o))
  with b_c = 3√3: 90° (= 25.0% of the sky, e59e's number) at r_o = 6 M, ≥ 150°
  at r_o = 3.5 M, 180° at the photon sphere. The worldtube test (occluder =
  the 2 M horizon tube) reads an arc b_c/2 = 2.598× smaller at large r_o; I
  predict the ratio exact/tube stays inside [2.3, 2.8] at every r_o
  (scale-free), and the fabricated-visible fraction (inside the true shadow,
  not occluded by the tube) is ≥ 15% of the whole sky at r_o = 6 M.
- **P2 (multiplicity, starfield at infinity).** Every celestial source whose
  direct image is outside the shadow has ≥ 2 images (1D lensing: the map folds
  once). The secondary's flux ratio to the primary (1D magnification
  |dc/dα| per image) exceeds 5% for sources within ~30° of the anti-hole
  direction at r_o = 6 M, and → 1 at the fold (the rim). ≥ 15% of the
  celestial circle carries a >5% ghost. A scalar deflection(b) memo returns
  one image per ray, so the base gather + memo shows exactly 1.
- **P3 (beacon at r_s = 4 M).** Some beacon longitudes have ≥ 3 images
  (primary, secondary, one relativistic image); the ghost carries > 5% of the
  primary's flux over ≥ half of the beacon's longitudes; the retarded time
  along the secondary's geodesic exceeds the flat-row time by ≥ 30% near the
  rim (Shapiro), while the flat crossing solve carries error 0 by
  construction — an error of type (wrong emission event), not size.
- **P4 (Newton-seed stability).** The image magnification |dc/dα| drops below
  0.1 (the image moves ≥ 10× the source) over a band ≥ 1° wide adjacent to
  the shadow rim at r_o = 6 M: the previous-frame seed's tangent is wrong by
  ≥ 10× there, so the letter's Newton iteration must re-converge from a bad
  seed every frame (branch-hopping flicker at the rim).
- **P5 (instrument controls).** My integrator's total deflection at b = 100 M
  matches the series 4/b + 15π/(4b²) to < 0.5% relative; light at b = 5.0 M
  is captured and at b = 5.5 M escapes (b_c = 5.196 M, the shipped oracle's
  own boundary pair); the exact shadow fraction at r_o = 6 M reproduces
  e59e's 25%.
- **P6 (the one-line cure and its limit).** Occluding with the hole's capture
  cross-section (an arc built from b_c) instead of its 2 M tube reproduces the
  exact shadow arc to < 1° at every r_o (the shadow is derivable — principle
  3), and cures none of P2–P4 (still one image per ray, still the flat
  retarded time).

Kill criterion for the attack: if the fabricated-visible fraction at r_o = 6 M
is < 5% of the sky, or no source ever carries a >5% ghost, the strong-field
view premise survives this falsifier and I report that.
