# G2 physical-law laboratory

This is an executable, bounded experiment, not a promoted gravity engine. The frozen gate manifest is `scenarios/law-gates.json`; it was written before either candidate map. `emergent_law_lab::qualify()` executes both maps, emits all measured values and gate failures, and selects no production law unless every required gate passes. The checked-in example prints the full serializable report:

```sh
cargo run --release -p emergent-law-lab --example qualify
```

The root orchestrator owns builds and execution on the M1 with 8 GB. The experiment allocates only small state arrays and source fixtures. It has no GPU, network, filesystem mutation, stochastic seed or dependency on wall-clock time.

## Two separate finite maps

`stationary-verlet-q-v1` uses the planar restriction of the 3D Newtonian potential `V=-mu/r`. One step computes `p_half=p+dt*a(x)/2`, `x'=x+dt*p_half`, `p'=p_half+dt*a(x')/2`, then projects position and momentum to the chosen quantum using nearest-even rounding. The unprojected velocity-Verlet map is a discrete variational integrator. The added projection is a law change and generally destroys exact symplecticity and exact time reversal. Those properties are not claimed for this candidate. The fixed step, quantum and projection boundary define this experiment; a diagnostic read never inserts a projection.

`stationary-shell-lapse-q-v1` defines annular constant-lapse patches of width `h=1/128` with `alpha_k²=1-2mu/(c²(k+1/2)h)`, using `c=64` and Euclidean spatial geometry. The map is explicitly limited to `1/16 <= r < 8`. Inside a patch, the Hamiltonian `H=alpha_k c² sqrt(1+p²/c²)` gives constant momentum and coordinate velocity `alpha_k p/sqrt(1+p²/c²)`. A circle-intersection calculation advances to the next shell boundary. At that boundary the map preserves the Hamiltonian and tangential momentum, solving for the radial momentum in the next patch. A negative radial-momentum square produces specular reflection in the old patch. It then continues through the remaining fixed step and projects position and momentum once. Shell selection after projection is part of this experimental finite map and can change the energy; the suite measures that effect.

The shell map permits at most 64 crossings per fixed step. Exceeding the limit produces an explicit error and a failed execution gate. It never accepts an unresolved result. This is finite failure handling, **not** proof of a terminating exact branch solver. The circle roots and all physical calculations use `f64`. Neither map is claimed bitwise portable across math libraries or hardware.

These are distinct candidate universes. They are never switched according to distance, speed or the optimizer. A future FMM or analytic propagator must evaluate the selected production law; it cannot become an alternate force law.

## Frozen numerical experiments

The suite executes 18 orbit scenarios per candidate: two eccentricities (`0` and `0.6`), three quanta (`2^-22`, `2^-23`, `2^-24`) and three rotations (`0`, `pi/8`, `pi/4`). It runs eight regular or four eccentric Kepler periods, using fixed steps `1/512` and `1/1024` respectively. Initial velocities and reference periods come from independent vis-viva and Kepler formulas. The lapse initial momentum is chosen to match the same coordinate velocity. The discrete candidates are compared against those physical diagnostics, not declared identical to continuum Kepler flow.

Every run reports maximum relative energy and angular momentum drift, extrema of the radial envelope compared with the expected periapsis/apoapsis, and every completed revolution's period error. Orientation tests compare final radius and energy drift. Quantum tests compare radial envelopes and drift across each adjacent pair of quanta. Thresholds are in the manifest; no threshold is fitted after looking at a candidate. Results preserve all failing rotations and resolutions. Clock tests compare each candidate's stationary `d_tau/d_t` with `sqrt(1-2mu/(c²r))` at four radii. Newtonian time is explicitly `1` and can fail that test. Clock agreement by the lapse candidate does not establish Schwarzschild spatial geometry or general relativity.

The report also performs 12 direct-source versus bounded-quadtree queries, using compact rings, extreme mass ratios and irregular spatial distributions, with near and far targets. For a positive-mass node of total mass `M`, support radius `a` around its center of mass and target distance `d>a`, the field derivative bound gives

`|a_direct-a_monopole| <= 2 M a / (d-a)^3`.

This follows from the operator norm `2/r³` of the Jacobian of `x/r³` and the mean-value bound for each source. The implementation opens nodes until `a/d<0.2` or evaluates a small leaf directly. It is a **monopole quadtree, not FMM**. The analytic truncation bound is sound in real arithmetic; the small floating padding is diagnostic and has not been formally justified with directed rounding. Passing these comparisons therefore does not supply a production numerical certificate.

A direct backreaction fixture compares the acceleration of a massive source due to one ship versus 64 ships and checks the two-way total force balance. Every ship contributes positive source mass. This independently exercises source accounting. Neither stationary orbit map dynamically couples the star and fleet, so passing this fixture does not grant dynamic-source capability to either candidate.

## Concrete failures and promotion

The causality fixture changes a source's gravitational parameter from 1 to 2 and queries radius 4 at a quarter of its light-travel time. The Newtonian acceleration and stationary lapse respond immediately. That measured nonzero response fails the zero pre-lightcone-response gate. Neither candidate includes retarded source histories or a coupled causal field update.

The exterior fixture adds a unit source at radius 16 and measures its nonzero effect at radius 1. No infinite source measure, background field, initial field history or certified omitted tail exists here. Ignoring that source cannot be certified. A finite authoritative massive root with explicit source history is the allowed next model; unbounded coordinates do not by themselves define infinite gravitating content.

Both candidates fail compact-field certification and terminating exact branches. Newtonian inverse-distance gravity has no relativistic capture/deflection law. The shell lapse's finite weak-field domain does not reach the compact radius, and its flat spatial metric is not Schwarzschild or Kerr. Floating roots and an iteration cap are not exact certificates. These reasons remain machine-readable alongside the actual numerical results, so the report cannot become a false positive because an orbit looks stable.

Production promotion requires **all** numerical measurements and **all** required gates. Until then `production_law` is `null`, candidate status is `FAIL`, and the root engine's exact inertial/causal laboratory remains a separate capability. No billion-year gravitational qualification or integrated billion-ship claim follows from these bounded experiments.

## Verification

Unit tests compare inverse-square acceleration against an independent 3-4-5 geometry, zero-force propagation against a binary-exact straight line, a circular orbit against analytic radius/period, shell free flight against the Hamiltonian velocity, and circle crossings against known entry/exit times that lie between coarse samples. They also check an asymmetric direct-source bound and the explicit instantaneous-source counterexample. The gate manifest is checked for the complete quantum ladder and zero permitted pre-lightcone response.

The root should retain the full JSON report with its embedded BLAKE3 gate-manifest digest. Do not report only passing numerical gates or replace the frozen manifest to obtain a passing candidate.
