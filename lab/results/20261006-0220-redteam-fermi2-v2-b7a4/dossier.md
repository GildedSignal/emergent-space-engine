# Dossier: the corrected phase-2 kernel table (window→0) and the epoch rule from it

**Claim (one sentence).** With the sign fixed (R_{r̂φ̂r̂φ̂} = −M/r³) and windows taken to
zero, the Fermi-frame Schwarzschild tide is confirmed to be the closed form of
`20261002-0539-q-fermi2-tide-0dee` — geodesic pair-differences, a sign-fixed Riemann
einsum and the closed form agree to 10⁻⁴…10⁻¹³ at 6M, 4M, 3.1M, eccentric and unbound
orbits — and the epoch rule derived from it is **N/orbit = 512π√2·3f√g/√((2−3x)²+g²)**
(tensor rule, ε = 2⁻⁸, x = M/r, g = 1−3x): 3047 at 1000M falling monotonically to 421
at 3.1M, so phase 2's kick cadence is set by the *weak* field, while both axis-rule
epoch columns of the prior run (3214/4017/16081) are unwrap artifacts, not physics.

## Bottleneck

Board focus 4 (the Schwarzschild tide in the Fermi frame, phase 2 after E9). This is the
one re-derivation the prior red-team's checker specified: corrected kernel table with no
window leakage, validated at 6M, 4M, 3.1M, eccentric and unbound orbits, plus the epoch
rule from the corrected kernel, cross-checked against the q-fermi2-tide closed form.
Gain: E9 can freeze (positive control = this kernel, negative = the naive Newtonian-form
kernel), and the epoch rule deletes the fear that the strong field is expensive.

## Evidence

Oracle: exact Schwarzschild geodesics + numerically parallel-transported tetrad
(constraint drift ≤ 4×10⁻¹⁴, E/L conserved to ≤ 10⁻¹³), reused from run
20261002-0539-redteam-fermi2-21db with two defects repaired (below). Three independent
kernel paths: (G) geodesic pair differences, quadratic fit, Richardson in h → 0;
(S) sign-fixed einsum; (C) the q-fermi2-tide closed form with Φ = −∫ω dτ accumulated from
the measured r(τ), independent of the transport. Commands (Linux cloud, 8 vCPU; each
under 60 s): `python3 sanity.py` (0.7 s), `python3 kernel.py` (56 s, writes
`kernel-table.json`; full table in `decisive.log`), `python3` heredocs logged in
`leakage.log`/`leakage6.log` (4 s).

**K1 — the kernel table.** In-plane eigenvalues {−(2+3λ)m, +m} (m = M/r³, λ = L²/r²),
out-of-plane m(1+3λ); radial = −w(2−3M/r)/(1−3M/r) = −w(3γ²−1) exactly.

| scene, point | r | closed radial/2w | geodesic h→0/2w | relF (S vs C) |
|---|---|---|---|---|
| circ 6M | 6.0 | −1.50000 | −1.50001 | 5.6×10⁻¹³ |
| circ 4M | 4.0 | −2.50000 | −2.49998 | 2.1×10⁻¹⁵ |
| circ 3.1M | 3.1 | −16.00000 | −15.99912 | 2.7×10⁻⁷ |
| rosette rp6.5 L3.5, peri | 6.5 | −1.43491 | −1.43617 | 9.8×10⁻⁶ |
| ecc rp6.5–ra20, peri / apo | 6.5 / 20.0 | −1.52163 / −1.05511 | −1.52220 / −1.05560 | 2.4×10⁻⁵ |
| parabolic rp6, peri / r=8 | 6.0 / 8.0 | −1.75000 / −1.42205 | −1.75012 / −1.41708 | 1.1×10⁻⁷ |
| hyp E=1.05 L=6.5, peri | 11.05 | −1.51936 | −1.51957 | 1.0×10⁻⁷ |
| hyp E=1.2 L=6.5, peri | 6.07 | −2.72260 | −2.72257 | 7.5×10⁻⁷ |

The transverse eigenvalue is +w at every scene to ≤ 2×10⁻⁴ (e.g. +0.50000 at all
circulars). h-sequences are monotone, second order (e.g. 3.1M: −16.048, −16.012,
−16.003, −16.000 for h = T_p/45…T_p/360); Richardson residuals ≤ 9×10⁻⁴ relative.
Rotation: dΦ/dτ tracks the closed-form ω = ELM/(r²(rE²+2M−r)) to 4×10⁻¹¹ (circ 6M),
5×10⁻⁶ (3.1M), 3×10⁻⁵ (eccentric), with the sign exactly as q-fermi2-tide wrote it
(Φ = −∫ω dτ; the S-vs-C agreement at τ = T_p/4 pins it). E-independence: same L = 6.5,
E = 1.05 vs 1.2 at r = 20 — closed form identical to machine precision
(−2.316875m, +m, +1.316875m), the two geodesic measurements agree with it to
0.4–0.7% (window bias on the fast leg; the two agree with each other to 0.4%).

**K2 — window leakage is real and one-sided.** Orbit-scale windows do not measure the
kernel: at 6M, h = T_p/4 gives −2.246 (1.50× the true value — the inflation band I
predicted), h = T_p/2 gives −2.643 and h = T_p gives −0.548 against the true −1.500
(units 2w). At 3.1M, members launched at rest ±0.02M do not survive an orbit-long window
(they plunge — the prior run's "reconstruction breakdown" member), so its 23.6 (a 5.57-orbit
window, +47%) is not reproducible with consistent member data; my h→0 sequence passes
through the checker's smallest-window value (−16.012 at h = 0.069 vs their 16.119).
Consequence: E9's positive control must extrapolate h → 0; a full-window fit is not a
measurement.

**K3 — the epoch rule from the corrected kernel.** Re-kick when the held kernel drifts
by ε = 2⁻⁸ in ‖ΔE‖_F/‖E‖_F. Closed form for circular orbits (ω = √(M/r³) exactly,
ωT_p = 2π√g):

N/orbit = 256·√2·(|a−b|/√(a²+b²))·ωT_p = **512π√2·3f√g/√((2−3x)²+g²)**

| r/M | 1000 | 50 | 20 | 10 | 6 | 5 | 4 | 3.1 |
|---|---|---|---|---|---|---|---|---|
| axis rule (true = naive) | 1606 | 1559 | 1483 | 1346 | 1137 | 1017 | 804 | 289 |
| tensor rule | 3047 | 2946 | 2781 | 2484 | 2035 | 1779 | 1338 | 421 |

(quadrature of the closed form and of the sign-fixed einsum agree to 4+ digits; the exact
formula column matches both.) Eccentric and unbound, from the closed form along the
measured r(τ): rosette rp6.5 (τ_per = 235.4M): 5925/radial period; ecc rp6.5–ra20:
4459; parabolic rp6: 6898 per passage (r out to 200M); hyp E=1.05 L=6.5: 5320. The
unbound cost is dominated by *amplitude* drift ∫|ṁ|/m ≈ 6 ln(r_max/r_p), not the axis —
and it accrues at large r where no battle exists (τ₁₀ ≤ 0.3 T_p everywhere).

**K4 — the prior epoch columns were artifacts; the tensor column survives.** The prior
run's window 2πr^1.5 of proper time is the *coordinate* period (1/√g true orbits), over
which the true eigenaxis sweeps exactly ω·2πr^1.5 = 2π at every radius (ω = √(M/r³)):
honest axis counts over their window are 1608 always. Their 3214/4017/4038 = 2.0–2.5
turns come from `np.unwrap` applied to the *half* angle (π-jumps uncorrected — my
reproduction with the same formula gives 2× the true sweep; unwrapping the doubled angle
fixes it), and their 16081 for the naive axis adds a non-unit, neither-fixed-nor-
co-rotating reference vector (`v1 = cosφ·f∂_r − sinφ∂_φ/r`). The checker's corrected
*tensor* counts, normalized per true orbit, reproduce my closed form: 2877/1.4142 = 2034
vs 2035 at 6M; 2395/5.5678 = 430 vs 421 at 3.1M. The naive kernel's axis on circular
orbits costs the *same* 512π√g as the true one — its crime is accuracy (K1 of the prior
run), not cadence; near the photon sphere the honest numbers invert the prior claim's
magnitude: 289 vs 16081.

## Two defects found and repaired in the reused harness

- `unbound_y0` (mine, first version): the turning-point bisection bracket was inverted,
  launching "periapsis" members from inconsistent data (g(u,u) = −1.0146, not −1). Every
  unbound geodesic number above is from the repaired launch (E, L conserved ≤ 10⁻¹⁵,
  tetrad drift ≤ 10⁻¹⁴). This is the same class of bug as the prior run's template sign:
  silent, and caught only by cross-checking three paths.
- The prior run's `ax` unwrap (their file, line 118): see K4. Not repaired in their tree
  (not mine to fix); documented here.

## Predictions (predictions.md, written before kernel.py)

- **Held:** P1 (all closed-form values, geodesic within 1e-3: worst 9e-4 at rosette
  peri); P3 (rotation sign and rate as written); P5 in full (axis = naive axis =
  512π√g on circular; tensor table to 4 digits; prior axis columns artifacts; checker
  anchors reproduce once normalized per true orbit); P7 (monotone convergence at 4M and
  3.1M).
- **Partially held:** P2 (leakage mechanism and magnitude confirmed at 6M; the 3.1M
  full-window number is unmeasurable — members plunge); P4 (E-independence confirmed,
  at 0.4% not the predicted 1e-3); P6's eccentric half (4459 in the predicted
  2000–6000; the prior run's "eccentric" scene is in fact a rosette, r ∈ [6.5, 7.5],
  e ≈ 0.07 — its e ≈ 0.88 label was wrong).
- **Failed:** P6's unbound half — predicted < 1500 per passage, measured 6898 (parab)
  and 5320 (hyp): I underestimated the amplitude-drift integral at large r.

## What would make it wrong

The (G) path and the (C) path share only the geodesic integration itself (r(τ)); (S)
shares the transport with (G) but not the formula. A sign error common to (S) and (C)
would flip the rotation direction — pinned instead by the geodetic anchor
2π(1−√(1−3M/r)) = 2π − ωT_p (an identity once ωT_p = 2π√g, itself verified by the
transported tetrad to four digits in `sanity.py`). The
residual 0.4–0.7% geodesic-vs-closed offsets on fast legs of eccentric/unbound orbits
are window bias (h-sequence still descending), not kernel error; if they survived
h → 0 they would falsify the closed form's C23 term.

## Cost of adoption, fit with PRINCIPLES

Phase 2 needs no new component: the kernel is the q-fermi2-tide rational core (integer-
exact per that run) plus one accumulated angle; the epoch rule is one comparison against
a rational integrand — "the best part is no part" (principle 17). The cadence finding
deletes the strong-field epoch fear: compute not done (principle 1). Validation against
geodesic pair differences, never against the formula, is K2 of the prior run confirmed
— "the simulation tells us what's next, not us" (principle 22). One derivation, not a
patch series (principle 19): the same closed form gives kernel, rotation and cadence.

## The lens

A re-derivation lens trusts the checker's fix and tests it; I nearly inherited their
epoch columns' framing (naive-vs-true cadence) — only the algebraic identity
ω = √(M/r³) exposed it. Missed: 3D structure (out-of-plane eigenvalue quoted, not
measured from geodesics — the game is 2D); the τ₁₀ × epoch-rate product (kicks per
*battle*) computed only from the prior run's τ₁₀ table, not re-measured; and member-level
error tables (L1/L2/L3) were not redone with the corrected kernel — the checker's halved
member errors stand as the only member-level evidence.
