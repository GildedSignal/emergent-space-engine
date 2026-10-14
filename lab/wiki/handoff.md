topic: handoff
status: open
closed-by:
valid-while:
updated: 20261014-1631-redteam-e8f7

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
*staleness* under thrust between re-anchors unprobed. All numbers
Linux/x86 shared runners, orders of magnitude only.

## Refuted

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
4. **The galaxy doll's unmeasured half:** how the multipole cells produce the smooth
   Φ(r) program at galactic scale, and the kick-layer re-anchoring that owns bar churn —
   eps_eff ≈ 0.008–0.025 is the measured switch-on to design against (6765's checker;
   aac1; 2da8).
5. **Land the Kerr guard** (19 lines, gate-neutral, verified): `main` carries the
   compiler without it, so the whirl cap's silent band (k ≥ 44, errors to 1.1e−2) and the
   negative-a `isco` slide ship unfixed (fa4b; 6586).
6. **Fix B11's precession oracle to 2PN** before the motion law v2's binaries are judged
   — a 1.5 s reference closes it (ecfd).
7. **Inclined Kerr** — the one named hole in the doll inventory; nothing tests it
   (fa4b's domain).

## Contradictions

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
