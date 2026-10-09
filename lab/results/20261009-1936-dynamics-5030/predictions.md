# Predictions — run 20261009-1936-dynamics-5030 (dynamics lens)

Written before the decisive sweep. Nothing below is tuned on the held-out slice.

## The question

The law's cheap path is drift on compiled tubes plus **orbit-averaged kicks at a fixed step in the drift's phase** (docs/law.md). Cadence ("fewer kicks per orbit at the same behaviour") is the #1 live engine question; `q-cadence` is queued and unmeasured. Dynamics view: the averaged-kick layer is a **discretization of the secular flow**. As the kick interval h (orbits per kick) grows, where does *behaviour* (error type: libration vs circulation class, e_max, boundedness) break, and what single dimensionless number sets the floor?

Model (H0190 K2's family: first-order quadrupole averaging, circular outer perturber): double-averaged quadrupole Kozai–Lidov tide, canonical pair (j = sqrt(1-e^2), omega), j_z conserved, tide strength eps scales the secular rate. Truth = RK4 on the same flow (the averaging-vs-GR error is r9's axis, not mine; this isolates the cadence axis). Map = kicks at interval h in the two orders the law could apply them: shear (kick in j, then advance omega — the WH-like order) and naive explicit Euler.

## Pre-registered predictions

Cases: C1 deep Kozai (j_z=0.3, e0=0.1), C2 near the libration centre, C3 near the Kozai separatrix (j_z=0.74), C4 prograde circulator, C5 retrograde circulator, C6 **held out** (j_z=0.2, e0=0.9). eps in {0.3, 0.1, 0.03, 0.01} (held out: 0.01 slice). Cadence h in orbits per kick, geometric sweep. N_lib = T_lib/h = kicks per secular (libration or precession) period.

- **P1 (collapse).** For the shear order, the type-break (class flip, or Lyapunov growth lambda*T_lib > 0.5, or e_max error > 10%) across all cases and eps collapses onto one boundary in **N_lib**, within a factor of 4. It does NOT collapse in kicks-per-orbit h. The lambda>0 onset sits near N_lib = pi (linear stability bound of the discretized libration centre: h*omega_lib = 2).
- **P2 (order is load-bearing).** Naive explicit Euler has no floor: no bifurcation, but a systematic compounding drift at every cadence — e_max error > 5% still at N_lib ~ 300, secular-energy error growing ~linearly (exponent ~1 against B12's 0.2). The shear order is bounded (exponent <= 0.2) at N_lib >= 20.
- **P3 (plateau).** Shear order, N_lib >= 20: class exact, e_max within 1% of truth, libration/precession period within 0.1%, lambda*T_lib < 0.2. Between pi and 20: distortion (period error grows ~ N_lib^-2, second order).
- **P4 (separatrix held out).** C3 (near-separatrix) breaks at N_lib a factor ~3–10 higher than C1/C2.
- **P5 (sub-pi).** Below N_lib = pi the shear map destabilizes outright (class flip or e_max error > 30% on most cases).
- **P6 (cost).** If P1/P3 hold, the cadence certificate is h_i = T_sec,i / 20 read off the compiled frequencies (already computed for resonance detection). For belt-scale tides (T_sec/T_orbit ~ 10^3) that is ~50 orbits between kicks, ~150x below H0190's 0.3 kicks/orbit operating point, with behaviour intact; near the Kozai threshold or resonance T_sec collapses and averaging must be abandoned (r9's Clairaut bound, r4's resonance kill), not just re-timed.

## What would make it wrong

- No collapse in N_lib (breaks scatter > factor 4 across cases/eps): then cadence is set per-case by something else (per-kick element change), and the certificate must carry more than the compiled secular frequency.
- Shear order breaking below N_lib ~ 10 on the plateau cases: floor is tighter than the linear-stability estimate, certificate needs the quadratic term.
- Euler order passing at N_lib ~ 10: order is not load-bearing; the naive kick layer is already safe.
