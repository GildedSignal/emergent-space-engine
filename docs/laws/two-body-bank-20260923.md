# Frozen two-body behavior bank — 23 September 2026

Declared before candidate runs. This tests finite weak-field orbital arcs of
`es-linearized-retarded-gem-response-v0`, not full-orbit stability or strong-field
physics. No result promotes canonical engine gravity.

Twelve resolved ICs: six base cases, each at compactness G M/(a c²) = 1/512
and 1/2048. Base index b=0..5 sets a=4+2(b mod 3), eccentricity
[0,0.3,0.6][floor(b/2)], mass ratio [0.01,0.2,1][b mod 3], and orientation
b*pi/7. Total mass follows the declared compactness; barycentric positions and
velocities come from the analytic Newtonian ellipse. Seed is the case index,
not a label on an unchanged IC. Genesis is -4a/c; observation window is
[0, 0.75 sqrt(a³/(G M))], sampled at 33 endpoint-inclusive times. This is
0.119 Newtonian periods, explicitly not evidence of a complete bound orbit.

Independent physical anchor: solve E-e sin(E)=n t by bounded bisection and
use x=a(cos E-e), y=a sqrt(1-e²) sin E, with their analytic derivatives.
These standard Kepler formulas are documented by
[NASA/JPL](https://ssd.jpl.nasa.gov/planets/approx_pos.html#formulae).
Only the formulas are used, not fitted Solar System elements or ephemerides.
The candidate retains its causal genesis/switch-on; its difference from a
Newtonian initialized ellipse remains measured, not silently tuned away.

Frozen diagnostic acceptance: maximum relative position error / a <= 0.05;
maximum Newtonian relative-energy drift / |E_genesis| <= 0.05; maximum relative
angular-momentum drift / |L_genesis| <= 0.05. These finite weak-limit tolerances
are screening criteria, not rigorous post-Newtonian remainder certificates.
Every case retains its outcome, including FAIL or unsupported compiler domain.

Separate same-equation numerical audit: slow Euler reference from the same IC
at dt=(horizon-genesis)/512 and /1024; finest reference versus compiled position
error / a <= 0.02; reference step-halving difference / a <= 0.01. Euler shares
the force evaluator and does not supply independent physical-law validation.
All reference/compile charges and wall time stay visible.

Negative control: ballistic relative motion from the identical genesis must
violate the 0.05 physical position band on every case. Analytical anchor tests
check period closure, energy and angular momentum across eccentricities without
using the candidate's force, retarded query, or trajectory helpers. No golden
trajectory or frozen operation-count assertion is used.

## Follow-up diagnostics (declared after first bank, before their measurement)

The first bank has four retained failures. Add observation-start position and
velocity offsets, energy/angular momentum at t=0, subsequent invariant changes
relative to that actual state, and GEM relative acceleration versus independent
Newtonian -GM r/|r|³ along the actual candidate path. These diagnose switch-on
versus continuing dynamics; they do not replace the frozen acceptance above.
Charge field evaluations separately. Logical audit-query counts do not represent
all arithmetic; failed compiler/reference APIs do not return partial ledgers,
so those counts are unavailable rather than zero work (wall time remains counted).
