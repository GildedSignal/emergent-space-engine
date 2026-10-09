# Predictions — run 20261009-0208-redteam-e369

Written before the decisive experiment (no run of it has happened yet; the
first draft's with-planet cases were dropped as out of scope and disclosed in
the dossier).

Premise under attack (`docs/representation.md` §1): "A dense region with no
central mass (a battle, a fleet) is also a doll: the free-fall frame of its
centre of mass. Inside it, tides are linear to first order, with the
Clohessy–Wiltshire closed form (1960). … so members re-anchor to the frame at
events or carry the quadratic term."

The CW closed form is exact only for a circular reference orbit. The doc's
hedge ("carry the quadratic term") is sized for the second-order tide error,
not for a first-order-in-e parent eccentricity. Belts and fleets in this game
live on Rayleigh-e orbits (e ~ 0.1–0.5 is the norm, per the belt gates), so
the eccentric parent is the player's normal case, not an extreme.

Setup: truth = exact star-only two-body motion of the member (RK4, converged
under step halving), parent = analytic Keplerian marker (massless, e_p ∈
{0, 0.1, 0.3, 0.7}, R = 1). Member starts at pericenter on CW initial
conditions (closed form used with the mean motion n), offset a/R = 0.01, two
IC families: the CW ellipse (ẏ₀ = −2na) and at-rest (all relative velocities
0). Error(t) = |CW closed form − truth| in the parent's rotating frame,
sampled at k parent periods, k ≤ 100. These cases are not tuned on.

Held-out predictions:

- **P1 (circular control — the premise survives where it was measured).**
  At e_p = 0, error after 100 periods < 10⁻²·a (I expect ~10⁻⁴·a, growth
  ≈ linear in t with slope ~ (a/R)²). H0203's one-period number was the
  member's own CW excursion (7x₀ oscillation + 6nx₀ drift), not model error.
- **P2 (eccentric — the uncovered case).** At e_p = 0.3 the error reaches
  ≥ a within ≤ 10 parent periods; at e_p = 0.7 within ≤ 3; growth is secular
  (no saturation) and first order in e_p.
- **P3 (re-anchor cadence).** Holding error < 1% of a: circular needs a
  re-anchor at most every ~500+ periods (cheap enough to ignore); e_p = 0.3
  needs one every ~≤ 1 period for the closed form — one full true-state
  evaluation per member per orbit, which is the integration cost the doll
  existed to delete.
- **P4 (instrument).** e_p = 0 error ≪ 10⁻³·a; step halving changes the
  error by < 10⁻⁶·a; the CW closed form reproduces a numerical CW
  integration to machine precision.
- **P5 (kill shape).** If the eccentric error instead stays bounded below
  ~0.1·a at e_p = 0.3 over 100 periods, the premise survives everywhere I
  probed and I report survival.

What would make me wrong: on an eccentric parent the leading relative-motion
error could be oscillatory (periodic at the parent's period) rather than
secular; then re-anchoring at events might still suffice and only the
amplitude ~e·a matters. The honest read is the envelope of error(t).
