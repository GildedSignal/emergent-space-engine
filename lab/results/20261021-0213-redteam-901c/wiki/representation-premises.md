topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261021-0213-redteam-901c

# The premises of docs/representation.md: a census against the record

## Current best

**NEW (901c, redteam — the kink law measured for the first time: the letter's work-rule clause is dead, the shipped thrust.rs is exact and implements something else, and no rung has any thrust arm).** L50 "in a field, E and L change by the work done": its Newtonian reading under-reads a prograde burn's ΔE/ΔL at 0.51/0.43 (r=6M, η=0.05/0.25), 0.85/0.76 (20M), 0.97/0.95 (10⁴M) — and 0.62/0.52 in FLAT space (the SR kinetic channel, ~1/γ³, any r) — and over-calls the burn-to-escape 3.04× at 6M, 1.61× (10M), 1.22× (20M), 1.04× (100M).
The exact replacement is one multiply-add in the frame the boost already lives in: **ΔE = √f·Δγ, ΔL = r·Δp_φ**. The shipped `burn`'s algebra matches the exact invariants to 0.0–1.3e-13 (float replica, controls green: geodesic drift 0.0, flat lump composition 1.3e-15 at any cadence) and its `along = n + u(u·n)/(γ+1)` satisfies |along|²−s² = 1 ⇒ felt α exactly at any attitude — clause 1 holds in the engine's convention (prograde lumps compose exactly at any cadence; at oblique attitude a finite lump is *not* the flow of its own field — flat 45°, η=0.25: |Δu| 1.7e-3, first order in the flush quantum), so `thrust.rs` L7's own comment ("changed by the work done, and nothing else") misstates its law. [Checker: the shipped cosh_sinh is a 6th-order truncation (~4e-10 at η=0.25) and the integer path is unmeasured — the *algebra* is exact.]
The sentence under-determines direction: at a radial impulse (6M, η=0.25) ΔL = 0 (axis-boost reading) vs +3.14% of L₀ (shipped/FW) vs 0 (letter); the impulsive reading also breaks clause 1 (felt α√(γ²+s²) > α). [Checker-corrected: the two clause-1-consistent continuous readings, FW-nose vs gimbal-held compass, do NOT coincide — 1.8e-4 in E ≈ 13% of ΔE at the run's own radial case (the 1e-5 was an unconverged q=2⁻⁸ lump whose deferral error cancelled the gap) and 10–15% of ΔE at oblique attitudes/longer burns; the shipped quantum's lump sits 1.8e-4 from its own q→0 limit.]
Flush deferral is first order in the flush quantum: relerr_E −0.184% (q=2⁻⁶) → −0.047% (2⁻⁸) at 6M, −0.0016%→−0.0004% at 20M, exact in flat prograde; no rung sees any of this (no thrust arm in r1–r13).
Standing (f2e3, corrected census): the χ-blind/|b|-keyed Kerr view dead (edges off 2.5°–43.9°, retro rim dark fraction = fate census 46.2/44.7/43.0%, not α⁺−α⁻; r15-kerr-shadow freeze-ready with census references; the closed form (180°+α⁺−|α⁻|)/360 matches at rim rows only). 9c08 one-sample dead on observer-γ; 915d additive attitude dead; 1885/7bcf one-sample dead on dispersion; e59e opacity missing; 22d1 per-row worldtube occlusion; 12db kick cost 34.8 µs shipped.
**Ranked census: view — all three aggregate channels, the occlusion law and the spinning-hole gather dead by type; Binet→Darwin (r1v2); kink law: work-rule clause dead, rapidity clause exact in the engine's convention (felt-α identity; speed-rapidity linear only prograde) — this run**; doll 1PN survives; dense≡sparse survives (r5); undisturbed≈0 survives by rate. (1645, f2e3, 901c; checkers: letter ratio 0.19–0.24 at 4M, 0.09–0.12 at 3.5M, 0.059 flat at γ 2.3 and 0.0019 at γ 7 — the kill deepens toward the hole; checker2 adds sign flips, see Refuted.)

## Refuted

- **"In a field, E and L change by the work done" (representation.md L50 — the same sentence also at
  law.md:42 and plane.md:21, and repeated by thrust.rs L7's comment; checker found the extra copies):
  dead as written, at two stacked channels — the SR kinetic one (Newtonian ½v² under-reads dγ
  longitudinally: 38–48% at w 0.5–0.577 flat, 94% at γ 2.3, any r) and the GR one (√f, and the γ in
  L = r·p_φ) — worst 0.43 of the true ΔE at r = 6 M, η = 0.25, deepening to 0.09–0.24 at r = 3.5–4 M (0.09 at 3.5 M, toward the photon sphere);
  the letter over-calls the escape burn 3.04× at 6 M. The shipped code does not implement
  it (its algebra exact to 1.3e-13; its own doc comment repeats the dead sentence). Cure: the exact
  closed form ΔE = √f·Δγ, ΔL = r·Δp_φ, plus naming the nose convention (FW-carried, the shipped
  choice). No rung has any thrust arm (20261021-0213-redteam-901c).**
[Checker2, blind: every dossier number regenerates in 0.7 s; the kill survived all out-of-range attacks and gained sign errors — on an E = 1 radial-infall event at 6 M the letter flips ΔE's sign (ratio −0.17), and an eccentric-event radial burn reads ΔL at −0.33; 0.059 flat at γ 2.3, 0.0019 at γ 7; the shipped replica stays exact (≤ 3e-15) at every out-of-range case; the shipped cosh_sinh is a 6th-order truncation whose error is 0.0 at the engine's per-flush η ≤ 2⁻⁶ and 3.7e-10 at η = 0.25 — exactness holds in the operating domain and fails only for single-shot η ≳ 1, which the flush quantum forbids.]

[standing refuted entries follow, unchanged]

- **The χ-blind / |b|-keyed view at every spinning hole (1645; corrected to
  the exact static tetrad by its checker, completed and census-corrected by
  f2e3): the two shadow edges sit at b_c per sense (±4.10/∓6.14 at χ=0.5 …
  ±2.11/∓7.00 at χ=0.998), edges misplaced ≈2.5°–43.9° over the χ 0.5–0.998
  grid (→0 continuously as χ→0: crosses 2.5° at χ≈0.44/20M and χ≈0.15/6M),
  arc centre displaced up to −19.8° retrograde-side (at 6M), near-hole
  bearings ±5–7° at |b|=10M; the retrograde edge is tangential exactly at
  r_o = r_ph⁻ (3.3–4.0M) and never past for a static observer (prograde
  tangentiality only exists at χ ≤ √2/2 — beyond that the ring is inside the
  ergosphere); inside the retrograde ring the true dark fraction carries the
  dark retrograde cap (fate census 46.2/44.7/43.0% at 3.2M, not the
  α⁺−α⁻ 29.0–40.5% — the χ-blind arc error at the rim is only 0.4–3.7
  points while its edge errors reach 43.9°); the rim wall splits by sense
  (δb/b = 8.8e-2 prograde vs 3.3e-4 retrograde at χ=0.9, against 1.86e-3
  flat); cure = the shipped signed-b law + (sense, b) memo key + gate r15
  (freeze-ready, census references) (20261020-2102-redteam-1645;
  20261020-2159-second-20261020-2102-redteam-1645-f2e3).**
- **The per-row chord worldtube occlusion law at every black hole (039d): the shadow is
  2.598× the silhouette in radius at every distance; the naive composition fabricates
  66.7%/100% of far rows at r_o 6M/≤4M; the served-row form misclassifies near-hole
  occluders by BOTH signs (chord 6.9/12.0/6.9% vs truly eclipsed 11.9/8.8/6.9% at Φ
  2.6/2.9/3.1, R_p 0.2M — misses 5.0pp at Φ 2.6, fabricates 3.3pp at Φ 2.9; checker-fixed
  constants: the author's 0%/100%-missed/never-fabricated was a mirrored-chord artifact);
  near-side companions vanish on
  7.9–11.3% of their ring at 20M; the rim memo key needs ≈2⁻²⁰ relative at 6M; cure = the
  deletion (no horizon test; shadow = absence) + path-tested occluders + the wrap-cutoff
  clause (20261020-1503-redteam-039d).**
- **"Aggregates are one sample each" on the observer's-γ channel too (9c08): with a cold
  sky (zero dispersion — where 1885's and 7bcf's channels read zero) one shift per sky
  cell errs the forward sky's brightness by E(γ·θ_f) alone — 18% at γ 125 stock (the
  plane's own burn red is at γ≈120), saturating 69–141%; k-halving at γθ_f = 1 exactly;
  colour to 0.86 octaves; cure = Σ(lum·k⁴) running sum (1 FMA) + log-k table
  (4–64 bins); the record's license needs the γ clause (flown only to γ 1.3). [870b: the letter
  is dead as a rule, rung-guarded (r13 PASS, 2D numbers 27.8% p99 at γθ_f=1, saturation 77.2%);
  but the record itself is exempt — it serves the exact seen-flux sum, so the one-shift kill
  never touched it.]**
- **"Aggregates are one sample each" on the flux channel too (7bcf, r12 executed): p99
  one-sample error 0.21–1.11 across comoving formations at β 0.5–0.99, worst at player
  speed with σ 0.10; dead in every convention; the cure (moments/formation quadrature,
  constant ops) licensed and rung-guarded.**
- **"Aggregates are one sample each" on the occlusion channel (representation.md L59/L116):
  all-or-nothing fleet eclipses — 89.1%/99.0% mid-transit flux error at R_f = 3/10·R_p
  with total blinks while ≥ 89% of flux is visible; survives exact retardation and k⁴
  beaming at β 0.5 (checker: β 0.9 peaks 0.695/0.856; the 400-ship arc formation
  errs 1.000 — the record's own fleet shape); orthogonal to the dispersion channel
  (fails at β = 0, uniform); cure = per-pixel exact predicates (145 samples → 3.0%;
  density-dependent compression) or the overlap closed form, licensed to uniform
  discs at β → 0 only (checker: 11–31pp outside) (20261019-0141-redteam-c78d).**
- [standing] The additive-attitude premise (915d); the aggregate readout on dispersion
  (1885); opacity absent (e59e); snapshot/sprite occlusion (22d1); the kick multiply-add
  cost (12db, b063); the Hashlife memo fast path (12db); "crosses once" (6eae); the
  cold no-memo fallback and any-cache cost (13c6); "r5 uncreatable off-Mac" (68e7).

## Open directions

1. [901c; checker-amended] Commit a burn rung (none exists): r16-burn — the engine's burn against
   an exact powered-geodesic oracle at one event and over a held-heading burn, with the oracle side
   converged (q→0; the shipped-quantum lump sits 1.8e-4 from its own limit at the radial case);
   the letter's work rule as the negative (its flat-space 0.52 ratio at w 0.5, 0.06 at γ 2.3, is the
   cleanest bar); the axis-boost vs FW-nose disambiguation arm (ΔL = 0 vs +3.14% at a radial impulse,
   6M, η=0.25) and the FW vs compass arm (13% of ΔE at the radial case, 10–15% oblique); deferral
   scaling arm (first order in q measured here: 0.184%→0.047%). Amend the dead sentence in all four
   copies (representation.md L50, law.md L42, plane.md L21, thrust.rs L7) to the closed form
   ΔE = √f·Δγ, ΔL = r·Δp_φ + the nose convention, and fix thrust.rs's comment to the FW map.
2. [f2e3] r15-kerr-shadow is freeze-ready (census references in f2e3's
   dossier: edges within 1% of the exact tetrad table; dark fraction within
   1 point of the fate census — the census, not α⁺−α⁻, at r_o = 3.2M; the
   tangential-at-r_ph⁻ clause with the prograde scoped to χ ≤ √2/2; the
   negative bar scoped to the frozen grid (crosses 2.5° at χ≈0.44/20M,
   0.15/6M); the memo key resolves the retrograde winding gap 3.3e-4; χ=0
   controls reproduce 039d and exactly 50% at r_o = 3M). Commit it, then
   amend the letter's L57 sentence: deflection is a two-branch function of
   signed b at every spinning doll; the memo keys (sense, b). Then the named
   unmeasured halves: the comoving observer at the Kerr rim (2fa4's
   instruments + this geometry), the off-equatorial shadow curve
   (inclination ≠ 0 — the census here is equatorial), and a read of what
   the plane's view path keys on today.
3. [standing] The integrator's one-pass amendment of representation.md — now also strike
   L59's first clause ("aggregates are one sample each") and keep the second (the pixel
   cap) with c78d's numbers, or replace both with the derivable-overlap law; 7bcf adds
   the flux half's replacement sentence (moments/formation quadrature, 7bcf's numbers);
   9c08 adds the sky-cell sentence: per-cell seen-flux running sum (Σ lum·k⁴, exact, one
   FMA per due event) + type × log k table for colour; the single-shift aggregate is
   licensed nowhere above γ ≈ 0.6/θ_f at the 5% bar (p99 bar: γ ≈ 44 stock). [901c adds
   L50 to the same amendment pass.]
4. [039d] Commit r14-rim-occlusion (freeze-ready criterion in the run's dossier: the
   deletion cure positive, the chord law negative on three channels, the 12-bit rim key
   negative), and amend the letter's occlusion sentence: the horizon occludes nothing the
   gather serves (shadow = emergent absence); occluders are tested along the deflected
   path; the deflection memo carries its wrap cutoff with the b-resolution it implies.
   Then the unmeasured halves: Kerr dolls (1645+f2e3 took the static half; the comoving
   occluder remains) and the comoving occluder (2fa4's exact moving-observer instruments
   composed with the eclipse geometry).
5. [executed aggregate half, 4ff1] The eclipse-parity rung's aggregate arm is r11:
   frozen (hash in the run), executed, PASS, on the corrected bars — 5% p99 vs exact
   Σk⁴ at player β both orientations; fmin within 5% of the arm's exact minimum;
   false-blink type bar; samples ≤ 150 pinned at R_f = 3·R_p plus the scale-aware
   ratio ≤ 1.1 (measured 0.998–1.000 to R_f = 30·R_p). Awaiting the integrator: commit
   r11 to lab/rungs/, then the absence half (22d1's per-row law).
6. [flux half executed, 7bcf] Commit r12-seen-flux to lab/rungs/ (frozen hash in the
   run; executed PASS). Remaining named arms: heterogeneous member luminance (weighted
   moments); the sprite TYPE table (binned log k — 1885's 40% median was reported there;
   bin-boundary interaction with dispersion is unmeasured); moment drift under stirring
   (how often σ must be re-estimated — kick-cadence territory). EOB strong-field flank
   (NR oracle) still standing. The moment representation now has both halves measured:
   spatial (c78d/4ff1: support radius + density profile) and velocity (7bcf: squads +
   formation shape; the γ² channel is the observer-frame swarm's).
7. [sky-cell half, 9c08] Freeze r13-sky-shift (criterion in the run's dossier: one-shift
   negative vs seen-flux-sum candidate at γθ_f ∈ {1, 4, 8000}; γ 1 and 1.33 controls must
   read 0). [870b: frozen and executed PASS.] Named arms beyond it: the cold-sky floor
   plus real dispersion (additive in quadrature with 1885/7bcf); clustered skies.
8. [standing tails, narrowed by 039d, 1645 and f2e3] The strong-field rim is measured
   for a static Schwarzschild doll (039d) and the static Kerr edges + dark fraction for
   a χ-blind law (1645 + f2e3, exact tetrad, fate census);
   remaining: occluder+observer comoving; extended occluders (fleet dolls); the
   off-equatorial Kerr shadow curve; strong-field occlusion inside r < 3M skims.

## Contradictions

None. c78d's transit-plane occluded fraction (46% at β 0.5) and its sky-plane one (17%)
are two orientations of one cone geometry, not a conflict — the rung judges both. 7bcf's
CV=4σ (comoving) and 1885's CV law (observer-frame) are two conventions of one channel,
bracketed by the rung's frozen comoving cases and the observer-frame diagnostic — the
v2-freeze sentence names both. 9c08's geometric channel composes with both dispersion
channels (it is the σ = 0 floor; real dispersion adds on top). 039d's corrected chord both
misses and fabricates near-hole eclipses, and e59e's "fabricated sky" is the same wrong
predicate seen whole — one mechanism, not a conflict. 1645's χ-blind kill composes with
039d's (a spinning doll's occluders are tested along the deflected path of the correct
sense; the two kills are orthogonal halves of the same gather). f2e3's census corrects
1645's checker at the rim rows — the record now carries the census numbers; the
retrograde-side centre displacement (measured) against the naive prograde intuition is
not a contradiction of the record: no prior run claimed a direction. 901c's letter kill
does not contradict the engine's exactness — the code never implemented the sentence;
the finding is a doc/code divergence plus a rung gap.

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's 50 ns
- 20261017-1018-redteam-13c6 (silver): r6 created, frozen and executed — PASS for the
- 20261017-1330-redteam-68e7 (awaiting grade): r5 created and PASSES on Linux — dense≡sparse 20/20, the "uncreatable here" blocker refuted; GPU arm stays M1-side
- 20261017-1447-second-20261017-1330-redteam-68e7-506c (awaiting grade): r5-starve frozen and executed — dense≡sparse holds under starvation and load, 11/11 + 27 allocator cells, allocator arm first for EventCore
- 20261017-2142-redteam-e59e (awaiting grade): opacity missing from the view's premises — stars through planets (16.7% of sky at 2R) and black holes (25% at r_o 6M); no rung sees it
- 20261018-0035-redteam-22d1 (silver, checker-corrected): the occlusion cure measured —
- 20261018-0143-second-20261018-0035-redteam-22d1-9ffc (awaiting grade): instrument fixed in the run's own script; every corrected number regenerates, closed-form certified per row (0 mismatches, onsets to 1e-12 s); the W2 deficit is the 1/γ arc exactly
- 20261018-1126-redteam-1885 (awaiting grade): the aggregate one-sample readout refuted
- 20261018-1433-redteam-915d (awaiting grade): additive attitude refuted — Thomas rotation
- 20261019-0141-redteam-c78d (silver; gold blocked on the rung freeze, done by 4ff1): aggregate readout refuted on occlusion — 89–99% fleet blinks; cure priced
- 20261019-0325-second-20261019-0141-redteam-c78d-4ff1 (awaiting grade): r11 aggregate arm frozen + executed — PASS; one-sample negative fails 3 bars; cure licensed at 29–113 samples; c78d's β-arm doppler typo corrected (~1pp, conclusions stand)
- 20261019-2339-redteam-7bcf (awaiting grade): r12 seen-flux frozen + executed — PASS; one-sample dead on flux (0.21–1.11 p99, worst at player speed); moment/formation readout licensed (≤3.8e-4 vs 1e6 truth, constant ops); the γ² channel located: observer-frame swarms (exact CV 4.05 vs the linear law's 0.70 at its own headline point), comoving formations CV = 4σ
- 20261020-0440-redteam-9c08 (this run): one-sample dead on the observer's own γ (cold sky): E(γθ_f) alone, 18% at γ 125 stock, halving at γθ_f = 1 exact, saturates 69–141%; cure = seen-flux running sum (1 FMA) + log-k table; record's license needs the γ clause; no rung sees it
- 20261020-1002-second-20261020-0440-redteam-9c08-870b (awaiting grade): r13-sky-shift frozen and executed PASS; struct read: the record stores Σ lum·k⁴ already (9c08's cure = the shipped field); letter L59 dead as a rule; 2D law at p99 confirmed
- 20261020-1503-redteam-039d (this run, awaiting grade): the chord occlusion law dead by type at every black hole — shadow 2.598× silhouette, near-hole occluders misclassified by both signs (checker-corrected), 66.7–100% far rows fabricated at r_o ≤ 6M; cure = deletion + path tests + memo wrap cutoff; no rung sees it
- 20261020-2102-redteam-1645 (this run, awaiting grade): the spinning-hole view measured — χ-blind/|b|-keyed gather dead by type (edges off 2.7°–28.3°, centre off up to 33°, retro edge wraps at r_o≤3.2M, rim wall splits by sense 8.8e-2/3.3e-4); shipped signed-b Kerr geodesics match the oracle exactly; r15-kerr-shadow freeze-ready; no rung sees it
- 20261020-2159-second-20261020-2102-redteam-1645-f2e3 (this run): the checker's named
- 20261021-0213-redteam-901c (this run): the kink law measured against GR — the letter's work-rule clause dead (0.43× at 6M, escape over-called 3×, flat-space 0.52× channel), the shipped thrust.rs exact (FW nose, felt-α identity) and not implementing its own comment, no rung has any thrust arm
