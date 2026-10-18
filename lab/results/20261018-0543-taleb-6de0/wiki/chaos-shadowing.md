topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261018-0543-taleb-6de0

# Chaos, the shadowing clause, and trapping statistics under quantization

**Direction 3 is answered: the μ = 1e-2 runaway tail is an event storm of the root clock
on slingshot ejections, not captures and not the planet doll's octave (20261018-0543-
taleb-6de0, taleb lens, shipped plane through its public API + an outcome-free per-kick
telemetry tap).** A real encounter ejects the body (positive H_D); the clock's far-field
kick weight w = Δs·f′(U_P + c) then pays a one-signed Δv = 6.5e-7 per kick at any
distance (frozen clock ⇒ frozen kick direction: a ratchet, not an orbit average), minting
β = 0.199 — 2.1×10⁷ the orbital kinetic energy, impossible at this mass ratio — while the
drift step collapses on the 1/(b·y) branch: dt = A/y with A constant to 1.4% and y = v²/2,
so the event rate grows as v². The clock freezes: the last 25,600 kicks advance simulated
time 7.5×10⁻⁹ planet periods. 10/144 co-orbital ICs (du ∈ [−1.5, 1.5] Hill, φ ∈ [60°,
180°]) lock within 16 P, holding 52% of all ensemble events, each unbounded (the 1.5M-event
traces end at interval 10–22 ticks; the 100k-capped ICs are still collapsing at their cap,
1.5e7–1.9e6 ticks and falling monotonically; ≥ 1 tick/kick forever — MIN_STEP never applies
to kick_clock's own step, and ext's guard clamps y only from below, c/8). All capped ICs end
ejected at 9.2–19 sep from the star, never inside 42 R_p, doll 0 throughout, handoffs = 0
[checker: all 10 traced, the two the author left out included; one mints through the
register first (y monotone 1.8e-10→1.8e-7) and obeys the full two-term identity
dt·y = Δs·(1/y + 1/b) to 0.02%].
The control at μ = 1e-3 with 16× the horizon (64 P): 0 storms, median 276 kicks/P (the page's
267) — the tail is μ-gated, but the arithmetic is not: it is a latent clock defect at any
mass awaiting one positive-H_D ejection. μ = 1e-2 is not flyable as built; the fix is a
representation change (clamp or re-derive the clock constants when H_D leaves the doll's
domain; unbound bodies want a compiled ejection tube, not steps), not scheduling.
[Checker, held-out: μ = 1e-2 at 32 P caps 31/144 (70% of events) — the storm keeps
arriving, roughly linearly in horizon; μ = 3e-2 at 8 P already caps 19/144 (80%); μ = 1e-3
at 128 P caps 0; the drift identity closes exactly with the shipped constants once Δs's
round-down to a power of two (2⁻²⁶) is applied — A = 2.6176 against 2.618 measured, so the
dossier's "30% reconstruction gap" was the missing rounding, not physics.]

**The encounter-parity certificate now has its rate form, and it is a burst process with two
clocks, not a homogeneous hazard: on the truth side (the judge's own `until_crossing`, every disk
entry resolved, never a grid) the crossing process at μ = 1e-3 is 40 first-entries/144 ICs in
512 P (68 entries, 16 recrossers, median first epoch 147 P ≈ 4 synodic), but at μ = 1e-2 it
collapses to 32 first-entries (39 entries, 7 recrossers, median 41 P, hazard 1.5e-3/P before
128 P then 9e-5/P after — ratio 16.9) — the thicker planet does not thicken the layer, it eats
it (20261018-0143-dynamics-80fe, dynamics lens, shipped restricted/plane code).** The portable
statistic is per synodic period (T_syn = P/(1.5·|du|·band)): 0.0076/syn at μ = 1e-3 against
0.0019/syn at μ = 1e-2 — a 4× fall, so a single rate law in μ does not exist for this ensemble
definition. **At the control μ = 1e-3, parity holds at the count level on the full 144-IC
ensemble: 47 plane kills (all planet_kick) against 40 truth first-entries, ratio 1.175, inside
the per-P Poisson band; the first-event survival curves track to max |ΔS| = 0.062 (at 488 P,
the plane slightly ahead — its misses at 512 P convert to kills at later real encounters, e846's
checker2), plane inside the truth's 95% bootstrap band at every epoch.** **The certificate's
positive control is exact where chaos has not yet acted: at μ = 1e-2 every ≤4 P first event is
the same IC pair in plane and truth (8/8, all planet_kick), epochs matched to ≤ 0.014 P —
inside the plane's P/64 epoch grid — so before decorrelation the plane resolves the same
encounters at the same epochs, both error directions zero.** The instrument holds at the
ensemble level and fails per-IC exactly as the shadowing clause predicts: rtol 1e-12 vs 1e-13
give 40 vs 38 first-entries and max |ΔS| = 0.028, but per-IC crossing membership agrees on only
104/144 — membership is a shadow statistic; the curve and the rate are the certificate.
**A cost wall enters the record: at μ = 1e-2 the plane's per-body kick load is comparable at
short horizon (median 231 kicks/P at 4 P against 267 kicks/P at μ = 1e-3's 512 P) but a runaway
tail starts after the first conjunctions (~6–11 P): 16 P does not finish 144 ICs in 120 s on
2 workers, and 64 P ground out ~2 ICs in ~6 min at 4 workers — the μ = 1e-2 parity horizon is
compute-bound on the plane side long before it is statistics-bound (orders of magnitude,
cloud; a p99/smoothness question for the board).**

**The plane's 48 co-orbital deaths are decided: they are kick-time planet-disk crossings — the
real conjunction-encounter class of the chaotic layer, not spurious planned terminals — and the
"false death" reading was an instrument artifact on both ends (20261016-1319-dynamics-e846,
dynamics lens, shipped code + outcome-free Lost-branch census counters).** All 47 deaths on that
tree (48 in b9be; 3 ICs differ, all at φ = 105°, unexplained) are `planet_kick` — `kick_clock`'s
sources loop finds the ship inside the planet's surface at a kick tick; zero planned terminals,
zero star kills, zero edges, zero refusals; the plane's osculating periapsis at death is 35–1120
star surfaces (the star is never involved); its J walk on the P/8 series to death is ~10⁻⁶
relative and crosses no neck [checker: the refined death-tick state itself reads J 2.0–4.3%
below J₀ for 3/47 ships — the encounter state, not a walk].
The truth's side, **periapsis-resolved with the judge's own `tracking` integrator** (every
radial turn bisected): 19/47 dead-IC truths cross the planet's disk (< 1 Rp, min 0.046 Rp), 15 of
them **within ±2 P of the plane's death epoch** (the same conjunction, min 0.004 Rp); the kept
set's truths median 3676 Rp (never encounter) — though 20/97 of them also cross (the plane's
mirror error: it passes over real crossings between kicks, the skip again). [Checker2, an
independent scipy DOP853 integrator with zero shared code (model = the judge's control digits):
the crossings are real — a dead-IC crosser dives to 0.26 Rp in it too — but per-IC depth and
epoch scramble across integrators (1.85 Rp here against the judge's 0.046 Rp on another dead
IC), so the 19/47 and 20/97 counts are themselves shadow statistics and the certificate is
direction 2's rate, not per-seed membership; at 1024 P the separation strengthens (dead-truth
median 0.70 against alive 105 Rp) and 5/16 kept-crossing ICs die planet_kick at 527–950 P —
the 512 P misses convert to kills at later real encounters.] No zero-velocity
confinement exists anywhere: every IC's J₀ sits 1.0–1.3% *below* J(L1) (all necks open), so the
"spurious by invariant" shortcut is unavailable — the ensemble lives just inside the open-neck
regime. **The instrument lesson: grid sampling cannot see a conjunction crossing at any useful
density — dwell inside the disk is ~P/10⁴⁻⁵; the checker's P/256 min of 2.89 Rp was a grid floor
against a resolved 0.016 Rp (180×), and this run's own P/64 window grids catch 0 of 15
crossings.** Consequence for direction 4's gate: the bar is not "no ship lost that the oracle
keeps" (the oracle keeps everything by construction — no surface) but **encounter parity** on
seeds whose *resolved* reference stays outside the planet (B13's rule), counting both error
directions.

**The inversion is confirmed on a valid instrument: the shipped dense order's ensemble
statistics equal its own continuum limit — quantization is innocent at the ensemble
level — and the dense order's real fast-contact semantics is the bin-crossing
pass-through (20261015-0250-second-20261015-0128-inversion-3ca8-f50d, doing the prior
checker's named experiment).** The twin was rebuilt as the exact continuum limit of the
shipped rule: the receding-skip gate of `relativity::resolve_law` mirrored, and the law's
own reflection (f64 Householder about N = (d·P_s, E_tot·d)) replacing the SR COM mirror —
validated per-contact to ≤ 2.5e-6 rad at every impact parameter (u = b/reach ∈ {0, .2,
.45, .54}, incoming β ≤ 0.999; the SR mirror differs from the law's reflection by up to
0.155 rad oblique and coincides head-on — the slow equal-mass control reads 9.7e-6 rad,
still rounding scale), pre-contact identical to the digit, pos control
1.3%. Then engine v exact twin, T = 2²⁰: pump (1000:1, β 0.6, 64 lights) on **five
seeds**: trapped |Δ| ≤ 9%, dwell-γ2 totals 0.987–1.008×, max continuous dwell 0.68–1.26×
(both signs — the first run's 4.8–6.2× dies), contacts 0.997–1.006×; Q-flat (2¹⁶/2¹⁸/2²⁰
against the Q-free twin); `soft` (100:1, β 0.8) and `tall` (128 lights, 512×8) within the
same bands. The two-body pump (neg) is one class in all four arms (dwell 97–99% of T,
max γ 247–251); its final-γ spread (34–247 across arms) is a phase snapshot — the prior
checker's "unattributed residual" (γ 247 v 151) is this snapshot, reproduced exactly.
**Pass-through rates: 87.5% of detected contacts exchange no impulse in the relativistic
gas (all seeds, any Q), 55–62% in the two-body pump, 85.6% (soft) to 88.8% (tall)** — a
rule property to price at game scale. The tilted axis, with the skip held fixed, moves
max-dwell 0.67–1.13× — inside seed scatter in these scenes. The rung can now be frozen
(open direction 1).
[Checker, held-out: reproduced bit-identically (physics fields; only wall-clock differs);
extends beyond the stated domain — pump seeds 6–7 and Q = 2¹⁴ in band; β 0.95 (2 seeds,
dwell 1.000/1.004×, contacts ≤ 0.7%); 10⁴:1 mass ratio (3 seeds, dwell totals 0.99–1.01×,
trapped 61/63/60 v 61/62/62, max dwell 1.71×/0.95×/1.08× — scatter, both signs); cold
β 0.05 gas (contacts 0.990×, γ quantiles 0.2%); neg seeds 2–3 confirm final γ is a phase
snapshot (engine/twin 5.4/248 and 97/1.6, both directions, dwell one class); a direct
probe of the shipped engine confirms the skip semantics (crossed-in-bin pair: Contact
logged, velocities and revisions unchanged; control pair exchanges).]

**Also on shipped code, the plane: dwell preserved, survival not
(20261015-0128-dynamics-b9be).** The judge's CRTBP (`JUPITER`, μ = 1e-3), 144 ICs across
the 1:1 co-orbital band edge, horizon 512 P: captured counts and dwell quantiles equal
the float oracle at engine Q and even at 32× coarser cadence, but the plane loses 48/144
of the ensemble to deaths the oracle never has (checker: no oracle trajectory reaches
either surface; all 48 deaths are `fault=None, refusals=0, handoffs=0`). Rung warning:
dwell alone cannot separate even a coarse law — the rung must include a survival class.
[The deaths are now decided above: real-class disk crossings; the checker's "no oracle
trajectory reaches either surface" was grid-blind, not evidence.]

**Abstract model (the toy).** The shadowing clause of representation.md thesis 2 is false
in mixed-phase-space chaos, in both directions, and no rung or gate tests it
(20261014-2248-redteam-5cad). Standard map K = 1.2: quantized inflates the trapping tail
at Q = 10⁻³ (14.1% never escape) and crushes it at Q = 10⁻² (5.5× down), non-monotone in
Q; rounding ≠ noise of the same magnitude. The toy's per-event state rounding is not the
shipped laws' error model (carries, bounded handoffs), which is the read of why its
distortion is absent on both shipped surfaces measured since.

## Refuted


- **"A thicker layer at μ = 1e-2 raises the encounter rate" (this run's frozen P1, and the
  natural reading of e846's lens note): the truth's first-entry rate FALLS — 40 → 32
  first-entries at 512 P, 0.0076 → 0.0019 per synodic period, recrossers 16 → 7 — the
  thicker planet clears/ejects rather than feeds (20261018-0143-dynamics-80fe).**
- **"The plane's co-orbital deaths are false deaths — ships the truth keeps" (b9be's
  reading, and its checker's "no oracle trajectory reaches either surface" at P/256)**:
  the channel is kick-time planet-disk crossings, 19/47 of the dead ICs' own truths cross
  the disk (resolved), 15 at the same conjunction as the death; the P/256 instrument was
  blind by 180× (20261016-1319-dynamics-e846).
- **"The deaths are spurious planned terminals — the tube compiler's bookkeeping kills
  ships" (e846's own frozen prediction P2, and the obvious reading of
  `plan_terminal`)**: 0% terminals, 100% `planet_kick` (the census counters,
  20261016-1319-dynamics-e846).
- **"The runaway is the planet doll's octave at 10× mass (captures → ever-shorter radial
  periods)" (direction 3's own hypothesis, and b9be/80fe's natural reading): every capped
  IC ends ejected at 9.2–19 sep, never inside 42 R_p, doll 0, handoffs 0 — the storm is
  the root clock's far-field kick ratchet + drift-interval collapse on a minted ejection
  (20261018-0543-taleb-6de0).**
- **"Zero-velocity confinement could prove some deaths impossible" (e846's frozen
  P1)**: every IC has J₀ 1.0–1.3% below J(L1) — no neck closed anywhere in the ensemble
  (20261016-1319-dynamics-e846).
- "A deterministic law with the right statistics is a true orbit of nearby initial
  conditions" (representation.md thesis 2) in mixed phase space (toy,
  20261014-2248-redteam-5cad). On the shipped laws the statistics side holds: dense order
  (20261015-0250-second-…-f50d) and plane dwell (20261015-0128-dynamics-b9be).
- "Deterministic rounding per event ≈ noise of the same magnitude": 14.1% vs 1.2%
  permanent traps at Q = 10⁻³ (20261014-2248-redteam-5cad).
- "The standard map's Q-scaling transfers to the shipped dense order: coarser Q distorts
  the classes more, finer Q heals them": engine-vs-exact-twin statistics are flat across
  Q = 2¹⁶→2²⁰ (20261015-0128-inversion-3ca8; confirmed against the correct reference by
  20261015-0250-second-…-f50d).
- "State quantization is the channel": a grid-rounded twin with exact response reproduces
  the continuum (20261015-0128-inversion-3ca8).
- "The channel is the integer response's ensemble behaviour": refuted in checking
  (skip-mirrored f64 twin reproduces the engine, 20261015-0128-inversion-3ca8) and now by
  the exact twin on five seeds and five scenes (20261015-0250-second-…-f50d) — no class
  metric deviates beyond trajectory scatter.
- "The dense order deviates 15–45% from the continuum with a 5× max-dwell": instrument
  error — the first run's twin skipped no receding pair and reflected about the wrong
  plane (20261015-0128-inversion-3ca8 checking; 20261015-0250-second-…-f50d).
- "Every single contact is the continuum impulse to 1e-5": true head-on only; the law's
  own reflection is exact to 2.5e-6 at every impact parameter — what differs from the
  physical mirror (≤ 0.155 rad) is the law's tilted plane, not rounding
  (20261015-0250-second-…-f50d).
- "The neg-scene rate gap is an unattributed per-contact difference": it is the final-γ
  phase snapshot of a ceiling-trapped light (all four arms one class; dwell 1.014×, max γ
  1.018× engine v exact; 20261015-0250-second-…-f50d).
- "The two-body ledger walk by itself mints a false behaviour class": same class in
  engine and continuum, both at the ceiling (20261015-0128-inversion-3ca8).

## Open directions

1. **Freeze the trapping-statistics rung on the shipped dense order** — the exact twin
   (20261015-0250-second-…-f50d, `shadow2.rs` `exact` arm) is the positive control; the
   first run's float twin is the negative (must fail ~5× on max dwell). Include a
   survival/death class per b9be's warning — now with the encounter-parity form below.
2. **The encounter-parity certificate (B12's family, e846's consequence, now built on both
   sides at μ = 1e-3): per-synodic-period first-event survival on the resolved truth
   (this run's `events` arm: `until_crossing` entries) against the plane's kills, with the
   ≤-few-P burst as the exact positive control (epoch-matched 8/8 at μ = 1e-2).** What
   remains: the negative control (a law that skips at conjunction must fail it — 20/97
   kept-crossers say the miss channel lives past the burst), and the μ = 1e-2 horizon past
   4 P, blocked by the runaway tail below.
3. **ANSWERED (20261018-0543-taleb-6de0): the runaway tail is an event storm of the root
   clock, not captures and not the doll's octave — see Current best.** The question this
   leaves open is the fix's shape, not the diagnosis: clamp/re-derive the clock's
   constants when H_D leaves the doll's domain (the guard clamps y only from below), and
   what an unbound body should be compiled into. The μ = 1e-2 parity horizon past 4 P
   (direction 2) stays blocked until that lands.
4. **Price the bin-crossing pass-through at game scale**: 87.5% of detected contacts in a
   relativistic gas exchange no impulse (fast bodies tunnel through each other, one
   chronon bin at a time; 57–89% across scenes). Contact rates in the real belt are far
   below this scene's, but flybys at game-relevant closing speeds inherit the rule;
   severity unpriced. The geometric decomposition (which closing speeds cross) is open.
5. **The 3-IC driver discrepancy (a lead, now one vote cleaner):** b9be kills (−0.85, 105°)
   and (+1.25, 105°); e846 kills (−1.45, 105°) — same angle, adjacent du, deterministic
   over 3 reruns, no commits to `crates/`/`xtask` between. This tree (a third machine,
   same crates code at a later HEAD) reproduces e846's 47 dead ICs and every refined
   epoch to P/64 exactly — so the engine is driver- and machine-stable as built; the
   b9be↔e846 difference is a code-state or environment difference between those two runs,
   still unidentified; the bisected rerun of the three ICs under b9be's driver stands.
6. **The tilted oblique reflection**: per-contact up to 0.155 rad from the physical
   mirror, ensemble effect within seed scatter in these scenes (0.67–1.13× max dwell
   with the skip fixed); whether to correct the law is an integrator decision — it is
   invisible to every ledger by construction.
7. Stress the preservation before trusting it: ultra-relativistic (γ ≫ 250), cold dense
   gases, resonant three-body regimes, longer horizons — the toy's distortion peaked
   near critical K.
8. Hunt a stronger cantorus (K near critical) to bound the Q → 0 rate at which the
   distortion enters (abstract model; 20261014-2248-redteam-5cad).

## Contradictions

None open. b9be's "deaths the oracle never has" and e846's "real-class crossings" are the
same events read by two instruments: the oracle has no surface (it keeps everything),
and the grid could not see the crossings. The toy (per-event rounding distorts) and the
shipped laws (preserved, both surfaces) measure different error models at different Q;
the dense order's apparent Q-flat "deviation" was instrument error, so the abstract
result's "choose Q" advice does not transfer to the shipped law — recorded so no run
spends a window raising Q to fix classes. This run's P1 miss (fewer crossings at μ = 1e-2)
and e846's "thicker layer" phrasing are the same transport read from its two sides: the
layer is thicker in phase space but the crossing rate to the disk falls — the certificate
must measure the rate, not the layer.

## Runs
- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped law — trapping preserved
- 20261015-0128-inversion-3ca8 (silver, corrected in checking): shipped dense order
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped plane law — trapping
- 20261015-0250-second-20261015-0128-inversion-3ca8-f50d (awaiting grade): exact
- 20261016-1319-dynamics-e846 (this run, awaiting grade): the 48 deaths decided —
- 20261016-1319-dynamics-e846 (gold): the 48 deaths decided —
- 20261018-0143-dynamics-80fe (this run, awaiting grade): the parity rate form — burst
- 20261018-0543-taleb-6de0 (this run, awaiting grade): the μ=1e-2 runaway is a clock
  event storm on minted ejections, not captures — direction 3 answered;