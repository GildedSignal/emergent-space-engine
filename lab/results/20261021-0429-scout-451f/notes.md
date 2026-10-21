# Scout run 20261021-0429-scout-451f — topic: fleet-doll-speed (od 5)

## The question (board families row, fleets half)
"How long a member's certificate lasts against its separation" in the plane's fleet doll,
at the game's speeds. 4c79 closed the *coefficient* half (linear tide exact, kinematic
amplification, no M/r term). What the page lacks (od 5): the **second order in ξ** — the
member congruence was naive (θ-offsets are not geodesics; constant-(E,L) members carry
ξ̇ ≠ 0), so the measured −0.136% → −0.298% growth is polluted by an IC floor. The named
next experiment: **exponential-map member ICs**, judged against the built deviation ODE.

## Requirements as numbers (PRINCIPLES ties)
- Fleet doll interior law = geodesic deviation with contracted E(u) (4c79 gold).
- Member certificate: the interval over which linear-in-ξ reproduces the member's true
  geodesic to the game's quantum. c₂(τ,β,r) := err/(ξ₀/r_p)² is the law to measure.
- Speeds: B15's fleet stream at β 0.9; legality cap c/4; weak-field cap r=18M nR=c/4.
- Dimensions: error type over size (P2); certificate as interval (P5 of board);
  dimensionless numbers pick the regime (P4).

## Prior art (to rank, verify at source where possible)
1. Fermi normal coordinates / generalized Fermi (Manasse & Misner 1963; Marck 1983):
   the metric expansion around a worldline, second order known in closed form.
2. Geodesic-deviation perturbation approach in EMRI data analysis (Drasco & Hughes 2004;
   second-order deviation eqn used for LISA): skin in the game = 10⁵ orbits of validity.
3. LIGO "flexible expansion" (Estabrook 1969; extended by Ni & Zimmermann).
4. Spacecraft formation flying mean elements (Schaub & Alfriend) — Newtonian regime.

## Design
- Equatorial Schwarzschild, units M=1. Reference geodesic (circular + hyperbolic at
  periapsis β_p). Parallel-transported tetrad by RK4 Fermi transport (geodesic a=0).
- Member ICs by the exponential map: x_m = exp_{x0}(ξ n̂), u_m = u - Γ(u, ξn̂) + O(ξ²)
  (comoving congruence IC: initial Fermi velocity exactly 0).
- Truth: integrate member geodesics. Prediction: deviation ODE d²ξ/dτ² = -E(u)ξ with the
  analytically contracted E(u) in the transported frame.
- Measure c₂ = |ξ_true - ξ_ODE|/|ξ_true| / (ξ₀/r_p)² at exit/along path; sweep β_p,
  r_p, offset angle α (radial / along-motion / oblique 45° / out-of-plane).
