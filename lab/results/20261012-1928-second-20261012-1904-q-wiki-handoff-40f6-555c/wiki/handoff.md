topic: handoff
status: open
closed-by:
valid-while:
updated: 20261012-1928-second-20261012-1904-q-wiki-handoff-40f6-555c

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
**The composition law for whatever surface ships (a7f7).** Pair maps derived as exact
products of per-frame quantized Lorentz matrices close every loop bit-exactly;
independently quantized pairwise pure boosts cannot (the Wigner rotation, ~10⁻²·|s| per
non-collinear loop at β ≈ 0.3 — a theorem, not rounding); integer shear loops drift
linearly (exponent 0.989) unless each shear carries its sigma-delta remainder (66× at
10³ loops; with it, ~0.095 units/loop ≈ 2 units per B12's 20 crossings, the residual
being pair-parameter rounding — NB 24→28 drops it 0.0547→0.0059 — and at β 0.85/0.78 the
carry still removes floor drift, 80 vs 4172 at 1024 loops). Two instrument warnings from
its checker: the exact inverse of a floored shear subtracts the same floored amounts
(negated coefficients fail 0/500), and closure/round-trip controls are direction-blind —
the probe's own derived atlas mirrored its boosts (~sinhη·|s| per handoff, corrected
constants: carry drift 97, not 58, at 1024 loops) and every closure control passed; a
physical anchor (a known event's image) is required. The mirrored builder
(`handoff_params_derived`) lived in that run's probe code and never existed on `main`.
Boundary placement is the priced lever: τ₀ belongs at the averaged law's e-pump
tolerance (≈ 0.25–0.30 R_Hill, not the 0.45 escape onset), and placement alone is worth
100× in handoff chatter (3d2c).

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
(E, L) tube plus 4×4/2×2 monodromies, one build step. **The interior slow flow and the
changeover (13ae).** Keeping one slow harmonic — the evection term, as a single-averaged
quadrupole generator — holds the 10% apsidal-precession gate to a ≈ 0.20–0.25 R_H
prograde (retrograde 0.18–0.20; at e₀ = 0.15 retrograde already broken at 0.20 R_H) at
0.39–2.92 events per moon orbit at rtol 10⁻¹⁰ (0.08–0.58 at behaviour tolerance; the
checker's independent recount 0.30–2.18 and 0.05–0.43) against the design's 32 kicks,
where r9's double average is 14–127% wrong — truncation, not method: r9's τ₀ = 0.0036
tracks the double average's e₀-mix crossing its truncation boundary. The changeover to
kicks is the adoptable boundary: kicks win from ≈ 0.22–0.26
R_H outward (at 0.30 retro, kick-8 reaches 3.8% and kick-32 0.6% against avg1Q's 46.7%;
the interior kick floor is N ≈ 4–8/orbit, error ≈ N⁻¹, and 64 kicks still sit at 8.8% at
0.30). Beyond it the missing piece is the second-order (Lie/Deprit) generator, not
multipoles (single-average residual 2.8–4.7% of the evection amplitude). **The tide's
kernel form near a compact mass (21db).** The Newtonian-form tensor is O(1)-wrong, and
even the Riemann-projected tensor needs its sign: R_r̂φ̂r̂φ̂ = −M/r³ gives the radial tide
−w(3γ²−1) (−2w×1.50 at 6M, ×16.0 at 3.1M); with the sign fixed, member errors halve.

**The dolls the boundary schedules across.** The two-body doll's premise — exact
Schwarzschild geodesic + 1PN energy map, ν only through the map (r3 v3; its eob-doll
kill sat on a handoff criterion the integrator himself called a criterion weakness —
a noise floor) — survives its first 2PN measurement: worst +0.36% periastron at ν = 0.25,
p̄ = 20M, e = 0.6 (c₂ gap 0.058, apsidal drift 0.0044 rad/orbit at the hardest seed)
(ecfd). Kerr's spin χ is compiled — `crates/space/src/kerr.rs`, equatorial,
bound/plunging/unbound/photons through one phase on `Scalar` integers — and gate B19 passes all six criteria (cycles 256/256, advance
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
re-anchoring, and the quiet/churned boundary follows the pattern speed in space. The
Schwarzschild doll's radial singular set — L = 0, plunge, near-radial, where the engine
refuses `NoBoundOrbit` (the boundary 6765's domain inherited) — has an exact regular
representation: Levi-Civita (z = u²) serves it exactly at K events independent of depth,
where stepping pays 18–93× at matched error and non-termination on the singular set
(7a46, gold).

**Domain.** Keys: one 0.5 c doll, 1,000 members, the plane; no depth-2 doll in the shipped
scenes (the checker's probe composed one and it held to ±0.49 tick at moon speed; a fast
grandchild, where the O(β²) Galilean carry binds, untested). Surface: six (f, sense) cases
at 0.3–0.9 R_H, β ≤ 0.9; P4's remaining cases and the player's own handoff unmeasured;
atlas constants measured on three dolls at β ≤ 0.9, integer coordinates, 2D log kernel
(a7f7); τ₀ placement measured on the averaged law's own grid (3d2c). Tide certificate:
eccentric equatorial geodesics r_p/M = 10–10⁶, e ≤ 0.6, moons at 10⁻³ mass ratio; not
inclinated, not the belt's conjunction regime. Slow flow: planar, µ_p = 10⁻³, parent's
tide only, non-resonant (n/n_p ≈ 10–55); circular births keep e ≡ 0 (forced
eccentricity needs the second-order term); per-event cost asserted, not measured. Kernel
form: 6M/3.1M windows, planar probe. Kerr: equatorial
only; inclined Kerr untested anywhere. Galaxy: a *given* smooth Φ(r) — how the multipole
cells produce that program, and bar/arm lumps as kicks, is the unmeasured half; a disc
that turns needs rtf ≳ 2e10 (disclosed); near-radial orbits (r_p 1e−4, r_a 11) converge
only algebraically, the plane's own `NoBoundOrbit` boundary inherited. All numbers
Linux/x86 shared runners, orders of magnitude only.

## Refuted

- The hysteresis-free single surface at `r < R_H/2` as built: Jacobi decade ratios 20.0 /
  4,455 / 104.5 on the un-run cases and 210 handoffs per 20 periods of chatter at 0.49
  R_H retrograde (18d2, checker's completed table).
- Independently quantized pairwise pure boosts as a handoff atlas: every non-collinear
  loop leaks the Wigner rotation (~10⁻²·|s| at β 0.3), a theorem; derived maps plus
  per-shear sigma-delta carries are the consistent form (a7f7).
- "One tick is the same physical time in every doll": the identity-key control fails by
  −110.52 ticks and ties events 16,384 ticks apart (ae29).
- The silent high-β key fallback — 52/200 members keyed unsheared when the centre's
  readout leaves its word; replaced by `key_fault` (4e9c).
- A static resonance flag from initial-cycle frequencies as the galaxy doll's regime
  gate: recall 13.2% at fpr 14.4% (aac1); censuses at 60 periods err both directions
  (2da8).
- Orbit-averaged member tides as a default: blind to all parametric pumping bands; on
  the coupled frame misses 127/144 and overstates ruin speed 2–4× (3851; 0d8c).
- r9's τ₀ = 0.0036 as a method boundary for averaging: it is the double average's
  truncation boundary crossing an e₀-mix; the single average with the evection harmonic
  holds to 0.20–0.25 R_H (13ae).
- The scalar (trace-only) Floquet certificate: misses 142/144 bands on the coupled frame
  (0d8c).
- The Newtonian-form tide tensor (and a +M/r³ Riemann sign): O(1)-wrong near a compact
  mass; the radial tide is −w(3γ²−1) (21db).
- B11's precession leg as a GR certificate: its 1PN oracle sits 34–718× farther from the
  shipped law than GR is and it passes a sign-flipped-2PN law at every seed (margins
  ≥ 3.6×) — the fourth member of the oracle-domain defect family (B12, B13, B17) (ecfd).

## Open directions

1. **Adopt the root-clock keys** (silver → one step): re-emit ae29's patch with 4e9c's
   `key_fault` guard, run a graded run. Deletes a wrong convention that every
   relativistic doll inherits; no compute gain claimed (ae29, 4e9c).
2. **Rebuild the surface rule.** The fixed predicate's failure cases are the test set:
   a chatter-free condition (hysteresis or rate-based) at r_c, judged on the checker's
   six-case table plus P5 and the moon test. The clock side (shears, simultaneity
   offset, the derived-atlas + carry composition law) already passes and is reused
   as-is; its constants want one re-measure on a direction-anchored atlas at β ≥ 0.8
   with 4–5 frame chains (18d2; a7f7).
3. **Wire the coupled Floquet chart** (gold, one build step): one 4-column quantized
   table per (E, L) tube plus 4×4/2×2 monodromies; fences H0190's 114× averaging exactly
   where it is safe and flags pumping members (3851, 0d8c).
4. **The second-order (Lie/Deprit) averaged generator, or the changeover to kicks at the
   0.22–0.26 R_H crossover:** extends the 10% gate to ≥ 0.30 R_H at ≤ 3 events per moon
   orbit; the retrograde low-e corner and circular-birth forced-e are the gates (13ae's
   named experiment).
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
9. **Wire Levi-Civita into the Schwarzschild doll's radial singular set** where
   `NoBoundOrbit` refuses today — measured exact at K events independent of depth,
   unmeasured inside the shipped tube (7a46).

## Contradictions

- **"The galaxy doll is a frozen program" (6765) versus "14–55% of the disc churns"
  (aac1, 2da8).** Composed, not contradicted: 6765's claim is scoped to the smooth field
  and playable rtf (the disc never turns), and its own checker names the perturbation
  half as unmeasured; aac1/2da8 measure exactly that half. Recorded so the next galaxy
  run measures both on one sample instead of citing either alone.
- **18d2's P4 line:** the dossier reports 0.3-pro failing at 2.18; its checker shows that
  number is an unsorted-median artifact (sorted 0.998, bounded) while other cases fail
  catastrophically. Resolved in the checker's favour; the surface is refuted either way
  (chatter), but the 0.3-pro case itself is not a failure.
- **fa4b's grade:** the branch commit says "silver (second checker disagreed)" but the
  second checker's own record shows gold — the silver was a missing `Grade:` line that
  `run.sh:99` greps for (6586). Bookkeeping, not physics; the page stands on gold+gold.
- **a7f7's atlas constants:** the author's D2 numbers (carry drift 58 at 1024 loops)
  were measured on the checker's mirrored-boost atlas; corrected to 97 on the
  direction-fixed atlas, and the page quotes only the corrected values. The direction
  defect itself was never in shipped code (`handoff_params_derived` absent from `main`,
  re-checked this run).

## Runs

- 20260930-1250-rung-r3-two-body-doll-v3-3565 (silver): two-body doll premise measured: ν only through the energy map; eob-doll killed on a noise-floor criterion.
- 20260930-2250-taleb-3d2c (silver): τ₀ belongs at the averaged law's e-pump tolerance (0.25–0.30 R_Hill); boundary placement worth 100× in chatter.
- 20261002-0539-redteam-fermi2-21db (silver): tide kernel's Newtonian tensor O(1)-wrong; Riemann sign fixed, radial tide −w(3γ²−1); errors halve.
- 20261003-0520-components-13ae (silver): evection slow flow holds 10% precession to 0.20–0.25 R_H at ≤ 2.9 events/orbit; kick crossover 0.22–0.26.
- 20261005-1540-m-macro-structure-a7f7 (silver): consistent handoff atlas: derived maps close, pairwise boosts leak Wigner, carries remove floor drift.
- 20261006-1135-scout-7a46 (gold): Levi-Civita serves the radial singular set exactly at K events independent of depth; stepping pays 18–93×.
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
