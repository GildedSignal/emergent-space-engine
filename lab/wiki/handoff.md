topic: handoff
status: open
closed-by:
valid-while:
updated: 20261015-1926-second-20261015-1747-redteam-de98-97b0

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

**The two-body doll's ν-blindness is now measured at strong field — the ecfd-vs-de98
contradiction is adjudicated and both prior instruments were wrong
(20261015-1926-second-…-de98-97b0).** The oracle de98 lacked: a 3PN EOB from primary
sources (Damour arXiv:1212.3169: A = 1−2u+2νu³+a₄νu⁴, D = 1−6νu²+2(3ν−26)νu³, tortoise
P_{R*} = (A/B)^{1/2}P_R so the canonical p_r² coefficient is A²/D, Q = z₃u²p_{r*}⁴;
4PN-fit bracket a₅c = 23.5, a₅log = 64/5 from Damour–Nagar 1406.6913), whose energy
map is *identically* the design's map, so at matched real invariants doll and oracle
share (E, j) and no baseline subtraction exists. Validated: ν→0 exact (no truncation
floor), quadrature vs its own RK 7.7e−9–1.4e−8 at strong labels, and the decisive
structure test at p̄ = 400M — per-unit-ν advance effect: DJS −0.5037%, A²/D −0.5139%
(gap 2% = 3PN residual), **ecfd's F = A²·D̄ +0.0052% (≈ zero: the sign of their 6νu²
term cancels the ν-effect)**. **Verdicts: ecfd's +0.36% at (0.25, 20M, 0.6) is a
wrong-coefficient artifact** (their own convention, correct coefficient: +3.2% 2PN /
+5.9% 3PN), **and de98's DJS-corrected contour undershoots 1.5–13× with the wrong sign
at p̄ ≤ 30M** (at 30M: +0.24% vs +3.10% [+2.04, +3.07]; at 20M: −3.1% vs +6.03%; converges
only at p̄ ≳ 80M). **The measured contour (3PN ≈ 4PN everywhere,
2PN↔3PN the honest bracket): at ν = 0.25 the doll's error is +1.4–1.8% at 50M, +2.8–3.9%
at 30M, +5.6–9.9% at 20M, crossing 1% between 50M and 80M, ≈65–70M (e ≤ 0.6;
≈79M at e = 0.9 — checker2, measured directly at p̄ 65/80) (≈35M at ν = 0.1, ≈10M at ν = 0.01)
— roughly twice de98's ≈40M projection — ν-linear (25.5 ratio), e-mild within ~2× at
p̄ ≥ 20M, period error same order opposite sign (−1.7% at 20M). Below p̄ ≈ 12M the
2PN↔3PN bracket opens past 8 points: no analytic oracle vouches there — but the
resummed family (itself PN-truncated) certifies down to p̄ ≈ 12M, refuting "uncertifiable
by any PN-truncated oracle" (the checker's caution, now measured). **Fabricated plunge,
adjudicated: at ν = 0.25 all 21 labels in p̄∈[6.5,8.5]M (e = 0.3) are doll-plunge vs
oracle-bound — the band is ≥ 2M wide; at ν = 0.01, 0/21** (de98's ν = 0-artifact
withdrawal confirmed; the real effect at comparable mass is large). The premise's
certified domain moves out to p̄ ≳ 65M at ν ≤ 0.25; r3 v4's strong-field leg points at
this oracle (8 s, self-validating). Also corrected in the record: 1/√(1−6/j²)−1, used
as "the closed form" by ecfd and quoted by de98, is not exact (its j²-expansion has
27/2j⁴ where the true series has 45/2j⁴); de98's three non-regenerated controls now
regenerate (weak field 3 digits, not 4 — the residual is the 3PN term; iso→areal map
11.75→12.77/48.99→50.00; Newtonian closure 6e−14); the EOB→ADM instrument switch after
predictions.md is disclosed.

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
*staleness* under thrust between re-anchors unprobed. ν-blindness: measured (97b0) on
p̄ ∈ [8,50]M at ν ∈ {0.01, 0.1, 0.25}, e ≤ 0.9, both label conventions (same sign
everywhere; agree within ~1.3× at p̄ ≥ 30M but up to ~4× at 15–20M when e ≤ 0.3 —
checker, off the author's claim of ~1.3× from 15M; checker2 off-grid: ν=0.05 linear,
ratio 5.09 vs 5.0 at 30M/0.6; error +0.86% at 80M / +0.41% at 150M; plunge census at
e=0.6 46/46 at ν=0.25 and 1/46 at ν=0.01, a p̄=9.7 edge label), 3PN≈4PN-fit
bracket; the 2PN↔3PN
spread is the honest systematic (2.6 points at 20M, > 8 below 12M); no numerical-GR
anchor anywhere in the chain (an NR-calibrated EOB would refine the contour's last
digit); the plunge census trusts the EOB separatrix, qualitative near p̄ ≈ 7M;
e ≳ 0.94 rows carry the inherited r ≤ 2000M false-PLUNGE cap, and the inherited doll
quadrature is noisy only in the near-circular weak corner (e ≲ 3·10⁻³ at p̄ ≳ 300M;
no shipped row inside — checker). All numbers Linux/x86 shared runners,
orders of magnitude only.

## Refuted

- **ecfd's +0.36% periastron error at (ν = 0.25, p̄ = 20M, e = 0.6), and its
  "premise survives its first 2PN measurement" as a strong-field statement:** the
  number is an artifact of the wrong p_r² coefficient (F = A²·D̄ instead of A²/D); at
  p̄ = 400M that structure carries +0.005%/ν against DJS's −0.504%/ν, and under
  ecfd's own turning-point convention the correct coefficient gives +3.2% (2PN) /
  +5.9% (3PN) (97b0). ecfd's B11 finding (1PN oracle certifies nothing) is untouched.
- **de98's DJS-corrected ν-blindness contour below p̄ ≈ 80M:** subtracting the ν→0
  baseline of a truncated reference does not isolate the ν-effect (at 30M: +0.24%
measured against +3.10%; at 20M the sign flips, −3.1% vs +6.03%) (97b0). de98's instrument-domain finding stands, strengthened: the certified domain is p̄ ≳ 65M,
  not 50M.
- **"Uncertifiable by any PN-truncated oracle" below p̄ ≈ 50M (de98's strong form):**
  a resummed ν→0-exact EOB — itself PN-truncated — certifies with a bracket down to
  p̄ ≈ 12M (97b0).
- **1/√(1−6/j²)−1 as an exact Schwarzschild advance:** its j²-expansion has 27/2j⁴
  where the true series has 45/2j⁴; the 0.2–0.85% ecfd attributed to "the closed
  form's e-dependence" is this 2PN error (97b0).
- **"r3's family certifies the two-body doll at strong field":** the sampler never opens
  p̄ < 20M, and inside its own range the truncation rule (τ = 8M/p) loosens the
  precession bar to 81% at p̄ = 20M — the rule excludes exactly the seeds where the
  premise could fail (20261015-1747-redteam-de98; the fifth oracle-domain defect after
  B11, B12, B13, B17).
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
4. **Freeze r3 v4's strong-field leg on the 97b0 oracle, or state the doll's certified
   domain as p̄ ≥ 65M (e ≤ 0.6; ≈80M at e = 0.9 — checker2)** (de98 wanted 50M; the
   measured contour crosses 1% at ≈65–79M at ν = 0.25). The oracle is a validated 8 s
   script (ν→0-exact, RK-checked, 2PN-consistent
   with DJS at p̄ = 400M); its bracket (2PN↔3PN) opens past 8 points below p̄ ≈ 12M, so
   the v4 sampler should run [12, 80]M — the 1% crossing is ≈79M at e = 0.9 (checker2);
   inside 12M nothing analytic vouches without an
   NR-calibrated EOB (the next refinement, one run).
5. **The galaxy doll's unmeasured half:** how the multipole cells produce the smooth
   Φ(r) program at galactic scale, and the kick-layer re-anchoring that owns bar churn —
   eps_eff ≈ 0.008–0.025 is the measured switch-on to design against (6765's checker;
   aac1; 2da8).
6. **Land the Kerr guard** (19 lines, gate-neutral, verified): `main` carries the
   compiler without it, so the whirl cap's silent band (k ≥ 44, errors to 1.1e−2) and
   the negative-a `isco` slide ship unfixed (fa4b; 6586).
7. **Fix B11's precession oracle to 2PN** before the motion law v2's binaries are judged
   — a 1.5 s reference closes it (ecfd).
8. **Inclined Kerr** — the one named hole in the doll inventory; nothing tests it
   (fa4b's domain).

## Contradictions

- ~~**ecfd's +0.36% vs de98's +13.1%/+16.2% baseline at (ν=0.25, p̄=20M, e=0.6).**~~
  **Resolved (97b0):** both numbers were instrument artifacts — ecfd's wrong p_r²
  coefficient (which cancels the ν-effect; V7 at p̄=400M: +0.005%/ν vs DJS
  −0.504%/ν) and de98's baseline subtraction on a truncated reference (which
  undershoots 1.5–13× below p̄≈80M and flips sign at 20M). Third-oracle value at the
  contested point: +6.03% (3PN EOB, matched invariants; bracket +3.4% 2PN / +5.96%
  4PN-fit); under ecfd's turning-point convention with the correct coefficient:
  +5.93%. No contradiction remains.
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
- 20261015-1747-redteam-de98 (silver): the two-body doll's ν-blindness uncertifiable below p̄≈30M — the DJS-2PN oracle is 5–16% from the doll's own geodesic at ν→0; ecfd's +0.36% not reproducible at matched invariants; r3 v4 needs a numerical-GR oracle or a stated p̄≥50M domain.
- 20261015-1926-second-20261015-1747-redteam-de98-97b0 (awaiting grade): the contradiction adjudicated with a primary-source 3PN EOB — ecfd's number is a wrong-coefficient artifact, de98's corrected contour undershoots 1.5–13×; measured: 1% crossing at p̄≈65M (ν=0.25), fabricated-plunge band ≥2M wide at ν=0.25; r3 v4's oracle exists.
