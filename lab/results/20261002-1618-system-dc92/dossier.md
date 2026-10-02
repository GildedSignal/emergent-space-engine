# Dossier — 20261002-1618-system-dc92 (system lens: the whole system)

## Claim

The gravity law's first open design question — "what the cells add", the rule
from a cell's multipole potential to the local flow β (moments add, the flow
does not, β ∝ √M) — dissolves if the flow is the gradient of the Jacobi
(Maupertuis) action of the additive potential:

    β = −∇χ,   |∇χ|² = −2Φ,   Φ = Σᵢ −Mᵢ/rᵢ,

because three of the contract's four requirements become theorems of the
representation instead of gates: **exactly Doran for one mass** (χ = 2√(2Mr)
is the Schwarzschild river), **curl-free for static sources** (β is a
gradient; measured antisymmetric part of ∇β: ~10⁻¹⁷), and **Newtonian-exact
for N sources** (a body released at rest obeys d²X/dT² = −∇Φ exactly —
½|β|² = −Φ and the antisymmetric parts cancel). The flow's characteristics
are free-fall orbits, so the field record is a ray bundle — the same
compiled-orbit machinery the engine owns — and the transport laws are local:
rays obey Newtonian fall, and ∇β is recovered from the congruence Jacobian.

## Bottleneck

gravity-law.md "Open, the first design question" / board bottleneck 1.
Expected gain: deletes the β-rule design space and any curl-free enforcement;
one scalar PDE on the quantity cells already store; the cell field record
becomes (moments, ray bundle) — engine.md rule 11's open "multipoles as the
mechanism for causality regions" in miniature, since a ray bundle's expiry
("moments changed by more than ε") is a certificate.

## Evidence (cloud Linux/x86, orders of magnitude only; G = c = 1)

Scene: two static masses 0.015 + 0.015 at (±0.75, 0); test body, circumbinary
orbit (realized a = 4.03, e = 0.126); river law dX/dT = u + β, dp/dT = Hp,
u = p/√(1+p²); β from the ray congruence (fall from rest at R = 10⁵, DOP853
rtol 1e-10, cache circle r = 8), H = −∇β from the congruence Jacobian.

- **One-mass, all PN orders:** analytic Doran advance 0.1343466 vs exact
  Schwarzschild (quadrature from the orbit's own turning points) 0.1343422 —
  **3.3×10⁻⁵ relative** (the 1PN formula 6πM/p = 0.13018 sits 3% below both:
  the river is exact Schwarzschild, not a truncation).
- **Ray pipeline validated:** one-mass pipeline advance 0.134351 vs analytic
  0.134347; β and H match the analytic Doran fields to ~6×10⁻⁷ per query;
  antisymmetric part of ∇β ~10⁻¹⁷ (curl-free in machine zero).
- **Eikonal identity on the fly:** max |β|² + 2Φ ≈ 7×10⁻⁷.
- **Kepler control:** Newtonian advance 2.6×10⁻⁸ rad/orbit.
- **Newtonian cleanliness of composition:** the two-mass river orbit's shape
  matches the Newtonian two-mass orbit to 0.06% (r_min) and 1.1% (r_max).
- **Decisive (two-mass GR correction):** river − Newtonian = 0.186 rad/orbit
  vs exact-Schwarzschild monopole 0.148 for the realized orbit — ratio 1.26,
  excess +0.038 (= 0.26 of the monopole term). Noise: pericenter-vs-apoapsis
  slope fits spread ±0.05 (quadrupole harmonic wobble), and a flagged 7.5%
  L-drift from occasional ray-selection outliers (E conserved to 2×10⁻⁴).
  So: the composed correction is of the right order and no Newtonian-scale
  corruption appears, but this run cannot decide 1PN correctness to better
  than ~±30%.
- **Negative control (χ additive, β = −Σβᵢ):** its potential −½|Σβᵢ|² carries
  cross terms ~√(Φ₁Φ₂); the orbit plunges from r ≈ 3.6 to r ≈ 1.4 with
  advance −0.48 — grossly wrong, as it must be. The probe can see composition
  errors.

Commands (from this folder; the decisive stage is minutes, not ≤ 60 s):

    pip install -q numpy scipy
    python3 run.py ctl          # controls B, E: seconds
    python3 run.py main         # A (eikonal), C (pipeline), F (additive): ~5 min
    python3 decisive.py         # apoapsis + E/L diagnostics for A: ~3 min
    python3 analyze_final.py    # assembles the numbers above

## Predictions

`predictions.md` was written before any measurement. Outcome: (1) pipeline =
analytic to 4×10⁻⁶ — held, better than the 3×10⁻⁴ bound; (2) eikonal identity
7×10⁻⁷ — held; (3) |S| < 0.5×6πM_tot/p — held (S ≈ 0.26×, though with ±0.05
rad noise this is an order-of-magnitude confirmation only); (5) additive rule
fails grossly — held; (4) the ν-scaling probe (M₁M₂ at fixed M_tot) was
**not run** for time; (6) no kill condition fired, but the L-drift flag means
the machinery, not the rule, is the accuracy limiter today.

## What would make it wrong

- The 1PN verdict itself: the +26% excess over the monopole term could be a
  real cross term (kill) or noise + real 2PN-scale structure (pass) — the EIH
  oracle on these scenes decides; that is the named next experiment, plus the
  ν-scaling probe that this run did not reach.
- Moving sources: rays from infinity are a static-source concept; the
  contract's retarded-moment reading has no eikonal form yet.
- Caustics of the congruence between close masses (β stays single-valued but
  loses differentiability; merged-horizon pairs untested) — the lens's named
  blind spot.
- Everything here is continuum floats: a premise probe feeding the law text's
  "implementer writes" list (κ, P, the β rule), like probes 1 and 2 — not a
  law, not a gate. The integer/discrete side is untouched.

## Cost of adopting

The β rule enters gravity-law.md as the answer to its open question; cell
field records become (moments, ray bundle); no new component. Judged next by
the contract's rung 2 (two masses vs the 1PN/EIH oracle) — one step.

## Fit with PRINCIPLES

- #7 "Gravity is compiled into geometry held by cells… Multipoles are the
  mechanism" — the eikonal is the compile step from moments to geometry.
- #32 "under the right representation many symmetries can appear" — in χ,
  composition is additive and curl-freeness is a symmetry of the
  representation, not a constraint to enforce or gate.
- #35 "the simplest form that does the most" — one scalar PDE replaces the
  β-rule design space; #2/#21: floats explored, only an integer law decides.

## The lens

The whole-system lens pushed the β composition, the cells' field records and
the compiled orbits into one structure (rays). What it may have made me miss:
the integer side entirely, and the board's current top bottlenecks (kick
count, changeover, encounters) are addressed only at the premise level — the
plane's measured costs do not move because of this run. One engineering
lesson is banked for the law's implementer: the tempting transport dH/dT =
Hess Φ + H² is exact but numerically vicious (positive-eigenvalue runaway
over long falls); recover ∇β from the congruence Jacobian instead.
