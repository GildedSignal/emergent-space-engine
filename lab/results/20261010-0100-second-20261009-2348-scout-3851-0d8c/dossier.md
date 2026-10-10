# Dossier — second-author run 20261010-0100-second-20261009-2348-scout-3851-0d8c

## Claim

The second checker's gold experiment, done: on the **full 2×2 coupled member
tide** (both in-plane channels, their shear, and the parallel-transport
precession ω), the Floquet certificate survives end to end — the cheap chart
closed forms match the exact-transport truth on **144/144 bands** (centers
≤ 0.03 grid steps), quantizing the coefficient tables to fixed-point Q = 2^12
shifts band edges by **≤ 0.03 grid steps** (bound stated below), while the
orbit-averaged law misses **127/144** truth bands and overstates ruin speed
1.8–3.6×, and the scout's frozen scalar certificate misses **142/144** — so
the coupled monodromy chart, not any averaged or scalar reading, is the
certificate the engine can adopt.

## Bottleneck

Board item 4 ("the Schwarzschild tide in the Fermi frame, phase 2"), fencing
H0190's 114× averaging lever. What this adds to the scout run: the exact
coupled structure the engine will actually meet — the tide in the orbital
frame is a full symmetric 2×2 with shear Λ₁₃ = −w·3γu_φu_r/N² (zero only at
turning points), and the doll's Fermi axes precess at
ω = −γu_φu(f−u)/(N²√f) (circular: Δψ = −2π√(1−3u), the geodetic value,
reproduced to 8×10⁻⁵). Gain: the certificate's adoptable form is now fixed —
one 4-column table per (E, L) tube (Λ₁₁, Λ₃₃, Λ₁₃, ω), all closed functions
of quantities the tube already compiles, quantized, and one 4×4 monodromy per
member. What it deletes: any per-member kick scheduling or averaging decision
inside dolls, and the scalar-chart pretence that channels decouple.

## Evidence (all from `sh run-all.sh`, every command < 60 s; `run.log` is the run)

Model: doll on an eccentric equatorial Schwarzschild geodesic (Darwin, M=1);
member in the Fermi frame obeys x″ + Ω_m²x = Λ(τ)x with Λ = −E (electric
Weyl). In the periodic orbital frame (f₁ = (e_r+u_r u)/N, f₃ =
(u_φe_t+γe_φ)/N, N² = 1+u_r²):

```
Λ₁₁ = w(2+3u_φ²/N²)   Λ₃₃ = w(3u_r²u_φ²/N² − 1)
Λ₁₃ = −w·3γu_φu_r/N²  Λ₂₂ = −w(1+3u_φ²)      (w = u³, out-of-plane decoupled)
ω   = −γu_φu(f−u)/(N²√f)                     (precession of Fermi axes)
member ODE:  x″ + 2ωJx′ + [ω′J − ω²I + Ω²I − Λ(τ)]x = 0
```

Turning-point limit: diag(w(3γ²−1), −w) — the frozen phase-2 kernel; the
frozen λ = u³(3γ²−1) used along the whole orbit is its O(u_r²) approximation.

**Validation (independent paths).** Truth: tide by direct wedge contraction
of the coordinate Riemann (sympy-verified against the repo's frozen signs
R_t̂r̂t̂r̂ = −2w, R_θ̂φ̂θ̂φ̂ = +2w, R_r̂φ̂r̂φ̂ = −w; Kretschmann 48M²/r⁶) plus
ψ, ω from exact tetrad transport (DOP853, coordinate Christoffels, rtol
10⁻¹²). Chart: the closed forms above (sympy S-matrix path). Cross-checks:
dΛ/w_max ≤ 2.7×10⁻¹⁵ on every channel and every case (rp 10…10⁶, e 0…0.6);
|ω_transport − ω_closed| ≤ 4.2×10⁻⁶; |∫ω − Δψ| ≤ 4.2×10⁻⁴; circular Δψ =
−5.960256 vs −2π√(1−3u) = −5.960753. Integrator: circular cases reproduce
the autonomous expm monodromy to 1.2×10⁻¹⁴; growth at band peaks matches an
independent solve_ivp integration to 10⁻⁶; sub-doubling conv ≤ 2×10⁻⁶ worst.

**Results (12 cases: rp ∈ {10, 30, 100, 10⁴, 10⁶} × e ∈ {0, 0.3, 0.6};
Ω_m ∈ [0.02,16]×Ω_r, 601 log points; threshold 0.02/orbit; 144 truth bands).**

1. **Chart = coupled truth (P1 held).** 144/144 bands matched, 0 missed, 0
   extra; worst center shift 0.026 grid steps; worst peak error 3×10⁻⁴.
2. **Quantization is free (P4 held, stronger than predicted).** All four
   tables as fixed-point shares of their max: Q = 2^16 shifts edges by 0.000
   steps; **Q = 2^12 by ≤ 0.026 steps, peak error ≤ 0.3%**. Bound: edge
   shift ≤ 3×10⁻² grid steps at Q = 2^12, scaling ∝ 1/Q — four orders of
   magnitude coarser than the law's 32-bit packets already saturates the
   grid, so the tide table can ride the law's grid untouched.
3. **Averaging is blind and alarmist (P2 held).** The law.md avg (constant
   decoupled channels) finds only the Hill region in every case: misses
   127/144 truth bands (12–22 per eccentric case) and reports ruin peaks
   8–15/orbit where the coupled truth pumps at 3.5–7/orbit (1.8–3.6×
   overstatement of ruin speed).
4. **avg+kinematics is a third wrong answer (P3 held).** Keeping exact ω(τ)
   and averaging only the tide: misses 124/144 bands, 67/87 of its own bands
   have no truth partner, peak errors to 93%.
5. **The scout's frozen certificate does not ship (P5 held).** λ =
   u³(3γ²−1), decoupled, no precession: misses 142/144 truth bands; where
   its centers coincide its peak error still reaches 73%. The O(u_r²)
   channel corrections + shear + Coriolis coupling are not perturbations:
   at e = 0.6 the truth has 18–23 bands against frozen's 9–14 (P7 held, 4/4
   radii), and even circular strong-field dolls (rp = 10, e = 0) carry 9
   Coriolis-driven bands the scalar sees none of (expm-verified).
6. **Out-of-plane channel (P6 partially failed).** At e = 0.3 it is clean
   (1 band, ≤ 0.041/orbit — the scout's α = −1 finding holds); at e = 0.6 it
   develops 5–7 real bands with peaks to 0.253/orbit — 15–40× weaker than
   the in-plane channels but not negligible: the certificate must carry the
   scalar Λ₂₂ channel too (same machinery, one more 2×2 monodromy).
7. **P8 failed as worded.** No stable rotation-confined gaps exist below
   k = 1 (0/12 cases); the low-Ω Hill region merges into the parametric
   structure everywhere. The calibration-case "gap" was one band layout,
   not a phenomenon. The real overstatement is in ruin speed (item 3).

## Predictions

In `predictions.md`, written before the sweeps (mtimes: predictions 02:05
sweeps 02:0x). Tuned-on: rp=100/e=0.3 (machinery calibration, disclosed).
Held: P1, P2, P3, P4 (stronger), P5, P7. Failed: P6 at e = 0.6 (channel 2
bands up to 0.25/orbit, predicted ≤ 0.1), P8 (no gaps; wrong mechanism
guessed for the avg's overstated ruin).

## What would make it wrong, adoption cost, fit

Wrong if: the exact transport or the closed forms share a systematic error —
they do not share code paths (coordinate Riemann wedge vs sympy orthonormal
S-matrix vs DOP853 tetrad transport vs scipy expm), and every pair agrees at
its own noise floor (10⁻¹⁵…10⁻⁶); if the member model's linear binding or
the neglect of the doll's own multipoles matters inside the Hill sphere —
outside this certificate's scope, unchanged from the scout run (finite
amplitude saturates the linear pumping at order a/R_H: from birth amplitude
a₀ ≈ 10⁻³R_H and ruin speed 2–7/orbit, saturation takes ~3–7 orbits, so
detection stands and ruin-time is bounded by the Hill-fill time). Adoption
cost: one 4-column quantized table per (E, L) tube key (Λ₁₁, Λ₃₃, Λ₁₃, ω)
replacing the 1-column λ table — all closed functions of (u, γ, L) the tube
already holds — plus one 4×4 (and one 2×2) monodromy per member per element
change; the averaging lever survives only outside band charts, exactly as
the scout run concluded. Fit: "Errors never compound" (#13) — every averaged
reading ships compounding or wildly mis-sized errors (127/144 blind, ruin
speed 1.8–3.6× wrong); "Regimes are chosen by dimensionless numbers" (#4) —
band membership is read from the tube's compiled (Λ, ω) tables;
"Compute only surprises" (#3) — the chart is computed once per tube key, not
per body. Stolen with skin in the game: Courant–Snyder/machine-orbit
formalism (the rotating-frame member ODE is exactly their rotating-frame structure), and
the geodetic −2π√(1−3u) per orbit anchors the precession channel.

## The lens (what the second-author lens may have missed)

I inherited the scout's Darwin parametrization and Ω grid (comparability
with its record), so any defect shared with the original run — e.g. the
mirrored half-orbit table seam — is common to truth and chart and would not
show in my deltas; the expm/scipy cross-checks bound the effect at 10⁻⁶ on
circular and spot cases only. The Ω grid ceiling (16×Ω_r) still never
reaches the innermost moons (the second checker's own note); pumping there
is extrapolated, not measured. Quantization was tested as amplitude
fixed-point on the tables; the law's eventual integer time-grid (cadence)
is a different quantization this experiment does not touch.
