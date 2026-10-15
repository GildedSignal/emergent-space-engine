topic: handoff
status: open
closed-by:
valid-while:
updated: 20261015-1747-redteam-de98

# Handoffs between dolls and the doll boundary

## Current best

**The boundary in time stands; the boundary in space does not.** The doll boundary has
three measured parts: the surface where a body changes doll, the key that orders events
across dolls, and the payload (the tide) that crosses with the member. One of the three
is adoptable now, one is refuted as built, one has its certificate.

**Keys: each event's image on the root clock (adoptable, silver).** The canonical key is
the doll tick plus the doll chain's integer simultaneity shear `sinh(η)·x̂_axis`, frozen
per entity and refreshed in `apply` (ae29; ~150 lines). P6: a 0.5 c doll's 1,000 members'
keys spread −8,314..+6,002 root ticks, worst miss 0.500 tick against an independent float
recompute, one history under 1/4/8 threads; the old-identity-key control fails exactly
(−110.52 ticks; a tie at 16,384); the plane's own Moon moves −25 ticks; B13's detail line
bit-identical, B8 suite green. The high-β hole is closed: where the centre's readout
leaves its word, 52/200 members were silently keyed at the unsheared tick — now a loud
per-entity `key_fault` and the entity stands unscheduled (4e9c, checker-rebuilt from
spec: 148/52 faults, 943/928 events, β 0.5 bit-identical). Not on `main` (12 October);
ae29's shipped `work/patch.diff` is 0 bytes, so adoption starts by re-emitting it.

**Keys' additive composition is falsified at depth 2 with relativistic links — the re-emit
must compose boosts, not sum shears (20261014-1631-redteam-e8f7).** The sum-of-per-link-shears
form is exact at depth 1 (P6) and at moon-speed depth 2 (the old ±0.49), but the exact map
for a chain is a product of Lorentz boosts, and products are not sums: a float oracle (exact
2+1 matrices, validated against the pre-registered analytic law to 5.3e-12 over a 108-cell
grid) pins the missed cross terms exactly — chain-tracking form err = (γ₁−1)·sinhη₂·(v̂₂·x),
frozen form adds sinhη₁·(γ₂−1)cosθ·(v̂₂·x). Numbers (offsets in light-ticks): player-group
scale (β₁ 0.3, β₂ 0.3, 90°, d 10³) 15.2 ticks both forms; inspiral-scale binary doll
(0.5, 0.5, collinear, 2·10³) 179/357; high-γ grandchild (0.9, 0.1, 10³) 130/140; worst
grid cell 4,070/5,067; 79/108 cells ≥ 1 tick. Third channel: the doll tick carries the *composed*
map's time factor, not a per-link product — γ₁γ₂(1+β₁β₂) = 1.667 collinear (an unscaled tick
misses 66.7 %; 6,667 ticks on a 10⁴-tick child tick) and γ₁γ₂ = 1.333 only perpendicular
(checker's correction: the run's own "γ₁γ₂ = 1.3333, 33 %" line contradicted its 6,667). Depth
compounds (β 0.3/link, d 10³): 15 → 78 → 227 at depths 2/3/4 (checker: 512/995/2,921 at 5/6/8;
the law holds to ≤ 1e-12 at β₂ 0.5–0.9 and θ 45–60°, outside the swept grid). Controls: depth 1 = 0
exactly; moon-speed depth 2 = 3.1e-3 ticks. The perpendicular-offset arm reads 0.0 (only the
along-velocity offset shears) while the Wigner axis error is real (−2.7°/−8.2° at the
named rows) — second-order for the key, owned by the spatial turn machinery if anyone's.
No rung, gate or engine test sees any of it (P6/B8/B13 key depth-1 dolls; the one depth-2
probe ran at moon speed; `step.rs` flags the open question itself: "a boost also maps an
event's time"). The machinery is in the tree, the fix is not written: `lorentz.rs` composes
boosts on four-velocities only and its header says of event times "nothing here answers it";
the re-emit must compose the chain's boosts as products of the crate's integer shears on the
event map — one matrix per doll refreshed at re-anchor, where ae29 already refreshes the
frozen shear (checker's integer probe of that form, coefficients at 2^-100 and events at
ae29's 2^-64 tick: 1.1e-11 ticks on the worst collinear arm).

**Surfaces: the hysteresis-free single predicate is refuted as built (lead).** One
predicate (planetocentric `E_p < 0` and `r < R_H/2`, both directions), the event boosted
through R3's nine shears, the child's clock sheared by the exact offset `−w·x′∥` (18d2).
What holds: the out-and-back map is the identity to 4,000/4,000 at β 0.01/0.3/0.9
(checker; the author's 0.9 row was 3,999/4,000 with one 6.3e−7 deviant), B13 bit-identical,
B17 after-side exact (before-side corroborated, not measured), a moon born in the planet's doll never leaves (0 handoffs, 100 periods,
0.3 R_H; 0.9 R_H released at its first s-boundary). What kills it: the checker's
completed six-case table fails catastrophically where the author's window ran out —
0.5-retro 20.0 with 21,403 handoffs, 0.9-pro 4,455, 0.9-retro 104.5 (Jacobi decade
ratio) — and the surface chatters near the boundary (retrograde 0.49 R_H: 210 handoffs
per 20 periods); the dossier's own 2.18 "failure" at 0.3-pro was an unsorted-median
artifact (sorted: 0.998, bounded). `main` still ships the changeover levels
(`soi.scale(1 − LEVELS)`); the single surface is design text (law.md step 3), not code.

**Payload: the member's tide is Hill's equation, and its certificate is the coupled
Floquet chart (gold, twice).** Orbit-averaged tides (H0190's 114× lever) are blind to
100% of the member tide's parametric pumping bands; the monodromy over one compiled
radial cycle — shared per (E, L) key, one 2×2 product per member, zero steady-state
cost — is the exact certificate (3851: 0/24 bands caught by averaging vs 12 truth-banded
cases; kick32 erases a 0.646/orbit Hill loss at e = 0; e = 0.9 pumps 12.8/orbit). On the
full 2×2 coupled Fermi frame (both channels, shear Λ₁₃, geodetic precession) the
closed-form chart matches 144/144 truth bands to ≤ 0.026 grid steps and Q = 2¹²
quantization shifts edges ≤ 0.026 steps, while orbit averaging misses 127/144 and
overstates ruin speed 2–4×, and the scalar (trace-only) certificate misses 142/144
(0d8c) — the coupled chart is the adoptable form: one 4-column quantized table per
(E, L) tube plus 4×4/2×2 monodromies, one build step.

**The two-body doll's ν-blindness is uncertifiable at strong field — the oracle, not the
doll, is what breaks (20261015-1747-redteam-de98).** Instrument: doll = exact
Schwarzschild geodesic at the design's own map inverted (E_eff = 1 + ĥ + (ν/2)ĥ² from
r3's E_real/μ = (1/ν)√(1+2ν(E_eff−1)), same L), reference = the reduced ADM 2PN
Hamiltonian (DJS, Schäfer–Jaranowski review Eq. 6.7–6.9; ADM/isotropic r), both at
matched real invariants (ĥ, j); radial quadratures only; doll quadrature validated
against independent RK to 6.5e-12–9.3e-11 (regenerable). The ADM side's shipped RK
control is dead code (prints "?"): checker-validated instead by a φ-parametrized RK of
the ADM Hamilton equations (2e-12 at four labels) and H_adm(ν=0) against the exact
isotropic test Hamiltonian E² = α²(1+p²/ψ⁴) (2PN shrinks the gap 5–26× at r 12–50).
The dossier's Newtonian-closure and weak-field controls are not regenerated by
regen.sh, and the weak-field match is 3 digits (0.031075 vs series 0.031350), not 4.
**At ν→0 — where the doll is definitionally exact — the
2PN reference sits +5.2% (p̄=30M, e=0.6) to +16.2% (p̄=20M, e=0.6) away from the
geodesic at matched invariants: the strong-field advance's PN series is barely convergent
exactly where the ν-effects live.** ecfd's single measured point (+0.36% at ν=0.25,
p̄=20M, e=0.6) does not reproduce at matched invariants (this run: +13.1% raw,
baseline-dominated); the two numbers disagree by 36× on the same named quantity and no
third oracle at that field strength can adjudicate. Where the reference is clean the
ν-blindness error is 0.4–0.9% at ν=0.25 (0.01–0.04% at ν=0.01), e-flat, crossing 1%
inside p̄ ≈ 40M — a projection no available oracle can test. (Checker: measured
baselines are +1.1–2.2% at p̄=50M and <0.8% only at p̄≥80M — the author's "baseline
<1.5% at p̄≥50M" is wrong at e=0.9, and at p̄ 50–80 the corrected signal is only
0.5–1× the baseline; what vouches for the correction is ν-linearity at fixed p̄ —
which the dossier never invokes — confirmed off-grid at ν=0.05/0.2 (ratio 5.4 vs
5.0 linear), with absolute error ~ν/p̄² into p̄=400M, exponents 1.90–1.96.)
Withdrawn by the author: the plunge-separatrix/ISCO arm and the
3PN bracket (the circular-Ω scan degenerates; the fabricated-plunge census fires
identically at ν=1e-6, i.e. a ν=0 coordinate artifact). This is the fifth member of the
oracle-domain defect family (B11, B12, B13, B17): r3 v3's sampler (p̄ ≥ 20M) plus its
truncation rule τ = 8M/p (tolerance 0.01+2τ → 81% at p̄=20M) certify the premise only
where it is trivially safe. The ν-through-energy-map premise itself survives everywhere
it can actually be judged.

**The dolls the boundary schedules across.** The two-body doll's premise — exact
Schwarzschild geodesic + 1PN energy map, ν only through the map — survives its first 2PN
measurement: worst +0.36% periastron at ν = 0.25, p̄ = 20M, e = 0.6 (c₂ gap 0.058, apsidal
drift 0.0044 rad/orbit at the hardest seed) (ecfd). Kerr's spin χ is compiled —
`crates/space/src/kerr.rs`, equatorial, bound/plunging/unbound/photons through one phase
on `Scalar` integers — and gate B19 passes all six criteria (cycles 256/256, advance
2.0e−13; fates 1680/1680; frame dragging 379/379, rates 1.4e−14; Penrose 85/73/27; light
4.4e−13; χ = 0 digest `59d54de0f9ead66f`), edges re-verified against an independent
r-space truth (fa4b, gold twice; `isco(1,pro)` = 6.0 vs the wrong 1.0, the separatrix a
true double root). It reached `main` through an unreviewed autopilot commit (cd57fd7a,
"not reviewed, not merged"); fa4b's 19-line guard — refusing the whirl cap's silent band
k ≥ 44 and the negative-a `isco` slide (6.0/9.0 vs 7.5546/4.2330) — is **not** on `main`.
The galaxy doll is the same compiled-cycle law one scale up: in the smooth 2D field
every orbit is the integrable (E, L) rosette the compiler already owns — ≤ 16 panels to
1e−6, per-cycle error 4.1e−12 rad, re-key 2.4e7 cycles; the disc turns ≤ 5.1e−3 orbits
per 100-h session even at rtf 1e8; the GR seam lies inside the nucleus's Newtonian SOI
at every horizon (5e−4–0.13 of r_SOI) (6765, gold first check, no second check yet).
Its regime gate is measured dead: the (E, L)→cycle compile works at galaxy scale
(~690× cheaper than DOP853 per 60 periods, readout ~1e−3 bounded and non-compounding,
precession carried exactly) but a static resonance flag from initial-cycle frequencies
cannot gate the regime — bar-driven churn takes 13.9% of a disc at ε = 0.03 and 55.5% at
ε = 0.10, best recall 13.2% at fpr 14.4% (aac1); sustained churn switches on between
eps_eff = ε·A(r_CR) ≈ 0.008 (0–0.5%) and ≈ 0.025 (27–35%), walkers migrate for real
(median ΔL 53%), and 60-period censuses err in both directions (P1 under-reads ~2×, P2
over-reads 9.1%→0.0%) (2da8, gold). So (E, L) drift is owned by the kick layer with
re-anchoring, and the quiet/churned boundary follows the pattern speed in space.

**Domain.** Keys: one 0.5 c doll, 1,000 members, the plane; no depth-2 doll in the shipped
scenes (the checker's probe composed one and it held to ±0.49 tick at moon speed; a fast
grandchild, where the O(β²) Galilean carry binds, untested). Surface: six (f, sense) cases
at 0.3–0.9 R_H, β ≤ 0.9; P4's remaining cases and the player's own handoff unmeasured.
Tide certificate: eccentric equatorial geodesics r_p/M = 10–10⁶, e ≤ 0.6, moons at 10⁻³
mass ratio; not inclinated, not the belt's conjunction regime. Kerr: equatorial
only; inclined Kerr untested anywhere. Galaxy: a *given* smooth Φ(r) — how the multipole
cells produce that program, and bar/arm lumps as kicks, is the unmeasured half; a disc
that turns needs rtf ≳ 2e10 (disclosed); near-radial orbits (r_p 1e−4, r_a 11) converge
only algebraically, the plane's own `NoBoundOrbit` boundary inherited. Keys, depth-2
composition: float-exact matrix math only (e8f7), not measured on integer words by the author
— the checker's composed three-shear integer probe (collinear arm, 2^-100 coefficients,
2^-64-tick events) holds to 1.1e-11 ticks; 2+1 planar, collinear and one perpendicular
geometry swept (checker: the law verified at β₂ 0.5–0.9 and θ 45–60°, depth 8); key
*staleness* under thrust between re-anchors unprobed. ν-blindness: clean only at
p̄ ≥ 80M in fact (baselines +1.1–2.2% at 50M), ν ∈ {0.01, 0.1, 0.25} (checker: 0.05
and 0.2 linear, p̄ to 400M), e ≤ 0.9 — the doll's turning-point search caps at
r = 2000M, so e ≳ 0.94 is silently flagged PLUNGE (checker, cap lifted: p̄=50M,
e=0.99 is bound, corrected +0.23%) — label-matched per ν (de98); below p̄ ≈ 30M no
PN oracle vouches for anything (baseline ≥ signal). All numbers
Linux/x86 shared runners, orders of magnitude only.

## Refuted

- **"r3's family certifies the two-body doll at strong field":** the sampler never opens
  p̄ < 20M, and inside its own range the truncation rule (τ = 8M/p) loosens the
  precession bar to 81% at p̄ = 20M — the rule excludes exactly the seeds where the
  premise could fail (20261015-1747-redteam-de98; the fifth oracle-domain defect after
  B11, B12, B13, B17).
- **ecfd's +0.36% at (ν=0.25, p̄=20M, e=0.6) as a reproducible periastron error:** at
  matched invariants the same configuration reads +13.1% against DJS-2PN, and the ν→0
  baseline alone is +16.2% — the number is oracle-convention-dependent, not a property
  of the doll (same run; ecfd's 2PN claim of B11's oracle defect stands — this extends
  it to the doll's own strong field).
- **"The two-body doll's premise — exact Schwarzschild geodesic + 1PN energy map, ν
  only through the map — survives its first 2PN measurement" (ecfd, as a certified
  strong-field statement):** survives only at p̄ ≥ 50M (0.4–0.9% at ν = 0.25,
  ν-linear, e-flat); below that it is uncertifiable with PN oracles, not confirmed
  (de98).
- **"The root-clock key is a sum of per-link shears" (ae29's form) at depth ≥ 2 with
  relativistic links**: the exact map is a product of boosts; missed cross terms
  (γ₁−1)·sinhη₂·x (chain form) and +sinhη₁(γ₂−1)cosθ·x (frozen form) give 15–5,067 ticks
  on the 108-cell relativistic grid, 79/108 ≥ 1 tick, and the doll tick carries the composed
  map's time factor (1.667 collinear: an unscaled tick misses 66.7 %; γ₁γ₂ = 1.333 perpendicular
  only); exact at depth 1 and moon speed, both controls 0 / 3.1e-3 ticks
  (20261014-1631-redteam-e8f7, float oracle validated to 5.3e-12).
- The hysteresis-free single surface at `r < R_H/2` as built: Jacobi decade ratios 20.0 /
  4,455 / 104.5 on the un-run cases and 210 handoffs per 20 periods of chatter at 0.49
  R_H retrograde (18d2, checker's completed table).
- "One tick is the same physical time in every doll": the identity-key control fails by
  −110.52 ticks and ties events 16,384 ticks apart (ae29).
- The silent high-β key fallback — 52/200 members keyed unsheared when the centre's
  readout leaves its word; replaced by `key_fault` (4e9c).
- A static resonance flag from initial-cycle frequencies as the galaxy doll's regime
  gate: recall 13.2% at fpr 14.4% (aac1); censuses at 60 periods err both directions
  (2da8).
- Orbit-averaged member tides as a default: blind to all parametric pumping bands; on
  the coupled frame misses 127/144 and overstates ruin speed 2–4× (3851; 0d8c).
- The scalar (trace-only) Floquet certificate: misses 142/144 bands on the coupled frame
  (0d8c).
- B11's precession leg as a GR certificate: its 1PN oracle sits 34–718× farther from the
  shipped law than GR is and it passes a sign-flipped-2PN law at every seed (margins
  ≥ 3.6×) — the fourth member of the oracle-domain defect family (B12, B13, B17) (ecfd).

## Open directions

1. **Adopt the root-clock keys** (silver → one step): re-emit ae29's patch with 4e9c's
   `key_fault` guard — **composing the chain's boosts (products of the crate's integer
   shears), never a sum of shears, and carrying the composed map's time factor on the child
   tick (γ₁γ₂(1+β₁β₂) collinear, γ₁γ₂ perpendicular)** (20261014-1631-redteam-e8f7) — run a
   graded run. Deletes a wrong convention that every
   relativistic doll inherits; no compute gain claimed (ae29, 4e9c). Freeze-ready P6 arm:
   depth 2 at β₁·β₂ ≥ 0.09, negative control the additive key (must miss ≥ 10 ticks),
   positive control the composed-boost key (must hold ≤ 1 tick).
2. **Rebuild the surface rule.** The fixed predicate's failure cases are the test set:
   a chatter-free condition (hysteresis or rate-based) at r_c, judged on the checker's
   six-case table plus P5 and the moon test. The clock side (shears, simultaneity
   offset) already passes and is reused as-is (18d2).
3. **Wire the coupled Floquet chart** (gold, one build step): one 4-column quantized
   table per (E, L) tube plus 4×4/2×2 monodromies; fences H0190's 114× averaging exactly
   where it is safe and flags pumping members (3851, 0d8c).
4. **Freeze r3 v4 with a real oracle at strong field, or state the doll's certified
   domain (de98).** Either add a p̄ ∈ [8, 50] leg judged against a numerical-GR two-body
   oracle (a 1.5 s class reference, as ecfd prescribed for B11), or freeze the premise's
   domain as p̄ ≥ 50M in representation.md §1. The one-line reason: every PN-truncated
   oracle is ≥ 5% from the doll's own resummed geodesic at ν→0 inside p̄ ≲ 30M, so no
   r3-family criterion is passable-in-principle there — the integrator's own r2/r3/r8
   lesson, repeated before it is frozen, not after.
5. **The galaxy doll's unmeasured half:** how the multipole cells produce the smooth
   Φ(r) program at galactic scale, and the kick-layer re-anchoring that owns bar churn —
   eps_eff ≈ 0.008–0.025 is the measured switch-on to design against (6765's checker;
   aac1; 2da8).
6. **Land the Kerr guard** (19 lines, gate-neutral, verified): `main` carries the
   compiler without it, so the whirl cap's silent band (k ≥ 44, errors to 1.1e−2) and the
   negative-a `isco` slide ship unfixed (fa4b; 6586).
7. **Fix B11's precession oracle to 2PN** before the motion law v2's binaries are judged
   — a 1.5 s reference closes it (ecfd).
8. **Inclined Kerr** — the one named hole in the doll inventory; nothing tests it
   (fa4b's domain).

## Contradictions

- **ecfd's +0.36% vs de98's +13.1%/+16.2% baseline at the same named configuration
  (ν=0.25, p̄=20M, e=0.6).** Both cannot be the doll's periastron error. Recorded as
  unresolved: the two runs match orbits differently (ecfd's comparison form is not
  reproducible at matched invariants from de98's instrument), and at that field strength
  no third oracle can adjudicate — the resolution is r3 v4's numerical-GR oracle
  (open direction 4), not re-running either instrument.
- **"The galaxy doll is a frozen program" (6765) versus "14–55% of the disc churns"
  (aac1, 2da8).** Composed, not contradicted: 6765's claim is scoped to the smooth field
  and playable rtf (the disc never turns), and its own checker names the perturbation
  half as unmeasured; aac1/2da8 measure exactly that half. Recorded so the next galaxy
  run measures both on one sample instead of citing either alone.
- 18d2's P4 line: the dossier reports 0.3-pro failing at 2.18; its checker shows that
  number is an unsorted-median artifact (sorted 0.998, bounded) while other cases fail
  catastrophically. Resolved in the checker's favour; the surface is refuted either way
  (chatter), but the 0.3-pro case itself is not a failure.
- fa4b's grade: the branch commit says "silver (second checker disagreed)" but the
  second checker's own record shows gold — the silver was a missing `Grade:` line that
  `run.sh:99` greps for (6586). Bookkeeping, not physics; the page stands on gold+gold.

## Runs
- 20261006-1738-b-handoff-surface-18d2 (lead): single-surface handoff built; P5 exact, moon never leaves; P4 table fails elsewhere, surface chatters.
- 20261006-1738-b-kerr-compiler-fa4b (gold): Kerr χ compiled on Scalar integers; B19 all six criteria; χ = 0 bit-identical.
- 20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586 (gold): adjudicates fa4b gold (missing Grade: line); edges hold vs independent truth; 19-line guard.
- 20261006-2240-b-root-keys-ae29 (silver): root-clock event keys with integer simultaneity shear; Moon −25 ticks; identity control fails.
- 20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c (silver): silent high-β key fallback made a loud key_fault; patch 0 bytes, rebuilt achieves claim.
- 20261008-0041-redteam-ecfd (silver): ν-through-energy-map survives 2PN (+0.36% worst); B11 precession certifies nothing GR-shaped.
- 20261009-2348-scout-3851 (gold): member tide is Hill's equation; Floquet monodromy the exact certificate; averaging blind to pumping.
- 20261010-0100-second-20261009-2348-scout-3851-0d8c (gold): coupled 2×2 Floquet chart 144/144 bands; scalar certificate misses 142/144; averaging overstates ruin.
- 20261011-1729-scout-6765 (silver): galaxy doll is the compiled rosette program one scale up; GR seam inside the SOI; gold first check, second pending.
- 20261012-0036-scout-aac1 (silver): (E, L) compile 690× at galaxy scale; static resonance gate dead (14%/55% churn under bars).
- 20261012-0138-second-20261012-0036-scout-aac1-2da8 (gold): churn switches on between eps_eff 0.008 and 0.025; walkers migrate for real; 60-period censuses err.
- 20261014-1631-redteam-e8f7 (silver): the additive-shear key falsified at depth-2 relativistic links — error law (γ₁−1)·sinhη₂·x plus the cosθ term, 15–5,067 ticks, doll tick carries the composed time factor; fix = composed boosts (lorentz.rs machinery).
- 20261015-1747-redteam-de98 (awaiting grade): the two-body doll's ν-blindness uncertifiable below p̄≈30M — the DJS-2PN oracle is 5–16% from the doll's own geodesic at ν→0; clean rows (p̄≥50M) put the ν-error at 0.4–0.9% (ν-linear); ecfd's +0.36% not reproducible at matched invariants; r3 v4 needs a numerical-GR oracle or a stated p̄≥50M domain.
