topic: fleet-doll-speed
status: open
closed-by:
valid-while:
updated: 20261021-0429-scout-451f

# The fleet doll's interior tide law at the game's own speeds

## Current best

**NEW (451f, scout, checker-corrected — od 5 half-measured): the exponential-map instrument is
validated (periapsis eigenvalues = 4c79's certified forms <1e-9 at 7 grid points). z-channel law
(rp 18M, one flyby): **err = c₂(ξ/rp)² + an O(h) instrument floor, c₂ = 78/129/239 at β 0.5/0.9/0.95**
(resolution-robust, asymptote 80/134/250; the 0.9→0.95 step scales ~γ²). Certificate: the linear
interior law holds 1% over a flyby only for ξ/rp ≲ 1e-2 at β 0.9; 12–23% at ξ/rp = 3e-2 by β 0.95.
Checker corrections (451f's two headline readings fall): the flat "desync floor" (2e-3–1e-2) is the
deviation-ODE's O(h) E-freezing error — z err at 1e-4 halves with every halving of h (6.7→3.4→1.7e-3
at β 0.9) — so 288f's −0.136% and 451f's 0.2–1.3% small-ξ residuals are both instrument artefacts
(physical ~c₂·1e-8); the in-plane O(ξ) channel is the member-IC transport sign (u0 + Γ(u0,w),
anti-parallel): flipping it drops in-plane exit error ×70 at 3e-2 (β 0.95: 147→2.0), makes member
u·u O(ξ²), and leaves a real sign-fixed in-plane excess (~9× z at 3e-2) unexplained; c₂'s M/r
independence untested.**

**Standing (4c79, gold): the linear coefficients are exact at every compactness and speed — radial
γ²(2+β²)/2 × Newtonian, along-motion 1×, out-of-plane γ²(1+2β²), cross-terms 0; purely kinematic
(no M/r term ≤ 7e-15, 6M–300M), so the legality rule gates on compactness alone.**

## Refuted

- **"The second-order-in-ξ term is unreachable without the exponential map" (288f's reading of
  its own −0.136%): half-refuted (451f, checker-corrected): with the map, the z channel is
  cleanly quadratic at exit — but the small-ξ "floor" both runs read (−0.136%; 0.2–1.3%) is
  instrument, not law: 288f's IC floor, 451f's O(ξ) IC-sign channel and O(h) E-freezing error.**
- [unchanged from 4c79/288f: the letter's Newtonian tensor refuted transverse; the
  diagonal boost-only cure wrong along-motion; the O((nR/c)²) budget a category error;
  the rival γ²|1−2β²| excluded.]

## Open directions

1. **The two one-line fixes, then the full grid (451f checker): parallel-transport the member
   IC (u0 − Γ(u0,w), kills the O(ξ) channel) and sample E inside the step (or halve h and
   Richardson-extrapolate, kills the O(h) floor); rerun angles × β × rp {18,100}M plus the
   τ-growth shapes with a resolution control. The sign-fixed in-plane excess (~9× z at 3e-2)
   is the real second-order signal left to read.**
2. **c₂'s M/r independence (P4 at second order):** rerun the flyby grid's rp = 100M arm
   (lost in 451f to a grid edit).
3. **The circular/secular arm (the certificate's duration, not its extent):** the 400-orbit
   run never produced valid data in 451f's window; the prediction (linear in orbit count,
   C ≈ 2π·15/8 per orbit) is untested.
4. [previous: the integrator's build (integer coefficients in frame.rs) remains the
   integrator's; B15 still judges no doll interior at player speed.]

## Contradictions

- None open. 451f's in-plane VOID is an instrument gap (the IC sign), not a conflict with
  4c79's certified linear forms (which 451f's controls reproduce).

## Runs
- 20261020-1002-redteam-288f (this run, awaiting grade): the fleet doll's Newtonian
- 20261020-1729-scout-4c79 (awaiting grade): the cure certified exact by a separation-free
- 20261020-1002-redteam-288f (silver): the letter's interior law refuted on the transverse channel.
- 20261020-1729-scout-4c79 (gold): the cure certified exact by a separation-free instrument.
- 20261021-0429-scout-451f (awaiting grade): od 5's instrument built and validated; z-channel c₂ measured (78/129/239 at β 0.5/0.9/0.95); in-plane VOID, desync diagnosed.
