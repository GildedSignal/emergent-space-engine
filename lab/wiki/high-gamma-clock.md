topic: high-gamma-clock
status: open
closed-by:
valid-while:
updated: 20261013-1428-second-20261013-1145-dynamics-0e79-8574

# The ship at high γ: its clock, its energy, the wall after the exact-in-E merge

## Current best

- **The held brake's crash basin is real, Λ-ordered at the low orbit only, and beyond the reach
  of attitude control — and the 1145 record now regenerates in full
  (20261013-1428-second-20261013-1145-dynamics-0e79-8574).** The second checker's one
  experiment is done: one committed flight list (D levels [0,2,4,5,6,8,15]) regenerates all 22
  rows of 1145's grids bit-identically from the shipped tree (regen.sh); the frozen
  pre-registration stays unrecoverable (declared, per the checker's alternative). Three
  corrections to what the page carried:
  **(1) The Λ constant was wrong, twice-checked.** μ̃ measured from the shipped state (β²·r on
  the circular start orbit = 8.845×10⁻¹⁰ Home radii = 2⁻¹⁸ of the star's μ; v_c = 8.51 km/s,
  T = 5,172 s, confirmed by the coast row's own Ψ) gives surface g = 12.47 m/s² and local
  weight 10.33 m/s² at 1.099R — Home is 1.27 Earth masses, not 1. Corrected ladder
  **Λ(L) = 0.3355·2^L** (0.34/1.34/5.37/10.7/21.5/85.9/1.10×10⁴); **Λ\* ∈ (5.37, 10.7)**; the
  level bracket L4-crash/L5-graze is untouched. Both of 1145's checkers "verified exact" the
  same Earth-mass assumption — agreement is not independence (the 5-October lesson, again).
  **(2) Λ is not the HUD's one number: the basin fades with the brake's start radius.** Raised-
  apoapsis brakes (nose tracked to v, cos0 0.997–1.000): from 1.445R L1 (Λ 1.16) crashes at
  7.83 km/s and L4 (Λ 9.26) lives; from 1.665R L1 (Λ 1.54) crashes while L2 (Λ 3.07) grazes
  1.0396R and lives (checker; Λ*(1.665R) ∈ (1.54, 3.07)); from 2.228R and 4.211R no **tested**
  level crashes (Λ 2.75–78.7 alive; the Λ 2.75 ship dips to 1.4586R and lives) — but the basin
  does not vanish there: the checker's L0 from 2.228R (Λ 1.38) crashes at 10.25 km/s at 2:02,
  so **Λ*(2.228R) ∈ (1.38, 2.75)**.
  Crash at Λ 5.37 from 1.099R against alive at Λ 2.75 from 2.228R kills Λ — and L4 living from
  1.445R kills level — as rulers across r; Λ\* falls ≥ 2–4× between 1.099R and 2.228R. The
  mechanism reading: a **margin** race (the osculating periapsis walks under the surface before
  tangential v cancels), so the binding quantities are start radius and v₀, not local weight
  (PRINCIPLES 33: the doorstep's number wearing a universal's clothes).
  **(3) The boundary is attitude-invariant at the shipped turn rate.** A tracking brake
  (nose re-pointed along v every check, ±2.5° band) keeps the fixed-nose bracket: L4 still
  crashes (9.14 km/s, 6:27), L5 lives (checker: to 2^37, still bound — 128 revolutions,
  minRpost 1.0293 unchanged, not a transient); the nose lags 24.6°/47.5°/144.2°/163.5° at L0/L2/L4/L5
  because the turn tier (2⁻³⁰ turns/tick = **4.08°/min**) cannot follow the terminal fall's
  ≈ 24°/min v-rotation — factor ≈ 6 short, and the controller is rate-saturated (cadence not
  binding; no player cadence beats the per-tick ceiling). Open direction 3's "attitude control
  or a law change?" resolves to **neither**: the timed cut (first checker: crosses 158,743.8 s,
  cuts, rests at γ 1.0004) is the only safe arrival, and the turn tier's rate is a fourth named
  wall for the range/turn job. **The refusal storms decomposed**: 100.0% of both (13,386 /
  12,762) accrue inside the held off-axis burn — a steady ~6.5 refusals per check on 91% of
  checks (off45: first at γ 2.10, band 1.72–2.42; off90: first at γ 3.19, band 3.19–5.01;
  doll constant "star"; checker: at γ₀ 1.5 the storm still fires — 13,784, first refusal at
  γ 1.32, again 100% in-burn and doll-constant, so the bands are those two trajectories', not
  a floor) — **0% at doll changes**: not rekey bursts; the off-axis burn state
  (nose 45–90° off v) refuses the kicks, while every θ = 0 pumped flight to γ 63 shows zero.
  Frame-time cost still unmeasured (the allocator half stays open).
- **The held brake under the merged prograde nose: no γ threshold exists, and the real boundary at
  the low orbit is Λ = thrust/local-weight (20261013-1145-dynamics-0e79, constants corrected
  above).** Open direction 3 asked whether 1890's pump threshold "γ ≈ 1.2" moves under the
  prograde nose; the answer is that it was never a threshold. On a 15-flight settle grid (levels
  2–15, γ₀ 1.1–30, nose offsets 45–180°, checks every 2^24 ticks, horizon 2^35 = 169,239
  game-s, seed 1): **every held brake that can reach rest does** — γ_min ≤ 1.0005 at all six
  detected crossings (γ₀ 1.1/1.5/3/10 at L15, and L15 from γ 30 at Ψ₀ 0.0008), rest is 1890's
  "crossing" — **and then pumps monotonically at the law's own α** (A-L15's tail fits
  4.0×10⁻⁴/s against α = 3.8×10⁻⁴/s at γ̄ ≈ 2; end γ = max γ on every pumped flight; none
  captured, zero refusals: 4.1/44/58/62/63 by horizon). The first-order ruler of the crossing
  depth is the **transverse rapidity at hold start, η₀·sinθ** (off45 crossed at γ 1.723;
  cosh(η₀ sin 46.6°) = 1.92 predicted, gravity's rotation shaves it; every θ = 0 row sits at
  1.0000–1.0005 with Ψ₀ = t_brake·ω spanning 0.0008–0.57, so Ψ is second order here); measured
  Δφ_v reads exactly π at every **θ = 0** crossing — the thrust-cancellation flip of v̂, not
  gravity — while off-axis crossings read below π (1.40 at off45 in the run's own grid, 1.98 at
  off30, checker2; the run's dossier overstates this as "every crossing" — corrected in
  checking). **The crash basin the pumped axes never enter** (every γ₀ ≥ 1.1 pump-up ejects
  through Home's SOI in seconds; minR/R stays 1.0990) **opens on the from-orbit brake** (the
  arrival maneuver at the low orbit): Λ orders it there — L0/L2/L4 (Λ 0.34/1.34/5.37) all
  **crash into Home** (5.35–8.47 km/s relative, world time 6:03–12:38, minR/R 0.946–0.970);
  **L5 (Λ 10.7) grazes at 1.014 R and escapes at γ 1.002 — the separatrix specimen**; L6 dips
  to 1.059 R and drifts out at γ 1.008; L8/L15 escape (γ 1.12 / 64.0). Brake-to-rest needs the
  timed cut (P1's, already shipped; checker flew it at L15 from γ 30: crosses at 158,743.8 s,
  cuts, rests at γ 1.0004, zero refusals), never a held key. Two walls for the `range` job:
  **turn keys ≥ ~135° at escape speed die mid-turn** (`Kick(0): Space(Range)` at 0.9435 c =
  γ₀, before any brake key), and the off-axis held burns accrue 13,386 / 12,762 refusals while
  alive and still accelerating (decomposed above: steady in-burn tax); A-L2 (braking too weak
  to bind from γ 30) is also lost by `Range` at 0.9994 c, a refusal inside a braking phase.
- The merged exact-in-E clock (f7f6d87, 12 October) holds in every regime the pre-merge record
  never flew, and the old wall is replaced by two cheaper walls (20261013-0037-dynamics-1890):
- **The clock is exact wherever it is readable.** Braking reversals at γ 30 (dt/dτ = u^t to
  2×10⁻⁶ through the reversal) and — measured by the checker, the author's window held only one
  post-switch checkpoint — at γ 300 (brakes 315 → sampled min 12.5, repumps through 393; ≤ 5.6×10⁻⁶)
  and γ 5 (min 1.018, repump through 21.9; ≤ 4.5×10⁻¹²). A sustained turning burn (γ → 1.19, tail
  errors ≤ 4×10⁻⁷), far bound orbits at r ~ 1e9 M (4e-12 at E = 1.000000), and the forward burn
  (checker, flown to the 2^40 window end: alive at γ 2,056, k flat at 1.09×10⁻⁸, zero refusals —
  the old γ ≈ 1,800 Range wall is gone on the shipped tree; worst relerr 1.3×10⁻⁵ at γ 1,879). The
  pre-merge saturation at dt/dτ = 2 is gone everywhere sampled. The old `E_key` reconstruction from
  k alone (clock_pin's formula) is now off by design — 0.62% at γ 307 (regenerated; the 1.6%-at-γ-334
  checkpoint was not regenerable) — E lives in the key's gap.
- **The in-flight E→1 crossing is measured — and safe (20261013-0236-inversion-57ce).** A held
  forward burn from the plane start, ×1.25 ladder bracketing every (doll, kind) transition to 0.2%,
  the gate's own f64 readout oracle: the Cycle→Passage flip lands within 10⁻⁹ of parabolic at every
  level L5–L15 (E−1 ∈ [5.6×10⁻¹¹, 6.5×10⁻¹⁰], level-independent — the burn's own quantum), with the
  clock at its best there (relerr ≤ 6.5×10⁻¹⁴, vs 10⁻¹²…10⁻⁶ elsewhere) and zero refusals; crossing
  times scale roughly as 2^−level, ratios 9.3/7.4/14.6 against 8/8/16 (the start orbit sits just
  below parabolic; checker: L6 too, E−1 7.0×10⁻¹⁰, relerr 1.2×10⁻¹³). The mid-flight doll
  handoff (Home-Passage → root-Passage) compiles at E−1 = 1.8×10⁻⁶ (L5) to 1.4×10⁻³ (L15), relerr
  ≤ 5.9×10⁻¹², zero refusals — far inside the acceptance map's safe parabolic edge.
- **The downward crossing (Passage→Cycle capture) is measured — the seam retires
  (20261013-0350-second-20261013-0236-inversion-57ce).** The checker's named experiment: a
  scripted brake from the bcoast passage (re-asserted every 2^(27−L) ticks, flush quantum
  7.6×10⁻⁶) captures at every level L5–L15 from the fixed nose, and after a full 180° nose flip
  (T8, the turn keys at 2⁻³⁰ turns/tick); **a plain held key crosses E→1 downward too** — one
  assertion, never re-asserted, the flip lands at E−1 ≈ −2×10⁻⁹ (E8.0–E8.3, checker: E11.3
  also) — **but the held-key capture is transient**: uncut, the ship re-flips to Passage
  1.8×10⁷ ticks later (E8.3: Cycle 730,062,627 → Passage 747,888,419; checker control X8.3) and
  pumps out — E8.2's world holds F8.2's death (same relight, same event_time 1,315,545,753).
  The arrival maneuver still needs the timed cut, which C and T make after the flip. Every
  C/T capture: zero refusals, clock relerr ≤ 2.4×10⁻¹¹ at the tested levels (5.7×10⁻¹¹ at the
  checker's L12), landing 1−E ≤ 8.4×10⁻⁹, captured apoapsis 10⁸–10¹⁰ (all inside the 2⁴⁰
  leave), survival at 2× the capture tick with E constant to 9 digits. The engine's own flush
  grid resolves the boundary to 2×10⁻¹² (the last Passage state before the C8 flip:
  E−1 = +2.2×10⁻¹²). The arrival nose alignment at this scene is ~0.5° (the escape burn itself
  pushed the ship along the nose), so the fixed nose is already a retro brake; wider arrivals
  need the turn tier, which T8 proves works.
- **No schedule dependence — one world (checker control, X8.3).** The author's "canonical
  outcome depends on the settle schedule" is an artifact of the probe stopping at the flip:
  continued on the identical input log at the fixed 2²⁰ cadence, E's world reads **all 31 of
  G8.3's settle ticks bit-identically** (E−1, r, v, err, events — e.g. t = 759,364,739:
  E−1 = +3.646×10⁻⁸, events 2766; t = 4,630,731,179: E−1 = +1.589×10⁻³, events 3735) and
  contains the same capture tick 730,062,627. The capture exists in every world; the ×1.25
  ladders (B8/F/G) straddle the ~1.8×10⁷-tick transient window, and the "moving" capture tick
  (729.5M–735.3M) is each cadence's first tick past the one flip event. Truth's
  "independent of … observation, schedule" **held**; the defect to carry is probe-side: a
  probe that exits at the first flip reports a transient as an end-state, and outcomes read at
  different horizons are not outcome comparisons (20261013-0350-second, checker).
- **The gentle half of the throttle never reaches the crossing: it dies silently at the surface.**
  The same held key at L1–L4 (checker flew L1; the author L2–L4): DEAD `fault=None`, zero refusals,
  r_at_death 1.05–1.09×10⁹ < surface 1.1306×10⁹ (the kill is `step.rs`'s `r < surface`, not the
  leave — leave needs r > 2^40), event_time ∈ (7.0×10⁷, 1.12×10⁸], monotone in level (the stronger
  burn inspirals sooner) — the sweep's crash-into-Home regime with its threshold measured:
  crash below L5, exact crossing from L5 up (this scene, the retrograde nose on main). The crash and
  the leave are both `fault=None`: the record cannot tell them apart — and the planet-crossing
  death joins them (F8.2 = G8.2 = E8.2's world: DEAD `fault=None` at r = 9.81×10⁷, just inside
  Home's orbital radius 9.93×10⁷, zero refusals, same event_time 1,315,545,753;
  20261013-0350-second).
- **A held brake key is a pump, not a brake, below γ ≈ 1.2.** Retro L15 from γ 30.7 brakes
  smoothly to γ 1.208, then the same held key pumps back through γ 186.7 (still rising).
  Brake-to-rest by a held key is impossible: rest is a crossing, not a fixed point; the
  playability plan needs attitude-keeping. A turning flight survives 69,660 rebind refusals on
  its old binding (γ → 1.19, periapsis → 2.1e10 M): refusal counts cannot certify a lost flight.
- **The far hyperbolic `Range` wall is the fit's arithmetic, not the key.** The acceptance map
  (22 E × 22 periapsis exact states through the shipped `Rebinding::from_state`): E → 1⁺ compiles
  at every periapsis 10 M … 1.6e10 M (the parabolic edge is safe); `Range` refuses on a jagged
  boundary (E=1.1 at 2e9 M; E=2–100 at 4e8 M; E ≥ 1e4 at 3e8 M). At E ≥ 100 the accepted
  k ≈ 1/periapsis, E-independent — the shape carries no E, the gap does. At every tested refusal
  point `OrbitKey::from_invariants` builds the same (peri, k) key and it compiles: the fix is the
  far-field fit path (fit from invariants), not a representation change.
- Slow far flights end at the leave, not the key wall: an L2 escape settles onto a bound orbit
  (k > 1/2) whose apoapsis passes 2^40 — silent death, a leave, not a refusal (20261013-0236).
- Domain: one plane seed, the merged prograde nose, settle-based flights to t=2^38 on the main
  tree, wall caps 55 s per flight (fwd15's γ-1800 tail not re-flown; the checker's extension
  flew it to the 2^40 window end, alive at γ 2,056). The crossing grids add: 48 members, forward
  holds, brackets at 0.2%, re-asserted brakes at fixed cadences, held keys, one 180° turn
  flight. Not the seed: `plane` spends its rng only on the 23 free ships (the player's and the
  planets' orbits are literals), so the player's flight is seed-exact — the checker flew seed 2
  bit-identical. The pump grid (1145 + 1428) adds: levels 0–15, γ₀ 1.1–30, nose offsets 30–180°,
  the from-orbit D row (all seven levels, now committed), raised-apoapsis brakes at 1.445R /
  1.665R / 2.228R / 4.211R (achieved e 0.14–0.59 — r and e swept together, not separately;
  checker adds L0 at 2.228R — crash — and L2 at 1.665R — live), the tracking
  brake at L0/L2/L4/L5, and the refusal decomposition; horizons 2^35 (L12's "no crossing" is a
  horizon bound: at 2^38 it crosses at 713,479 s = 4.2×, γ_min 1.0000, pumps to 30.3, zero
  refusals); one seed, one scene. Not measured: circular starts at chosen radii (an r-only
  sweep), hyperbolic arrivals at speed, the Moon's engagement, the storms' frame-time cost.

## Refuted
- **Λ = thrust/local-weight as the HUD's one number across scenes (20261013-1428-second):** the
  basin it orders at the low orbit (Λ\* ∈ (5.37, 10.7) corrected) vanishes for brakes from
  apoapses ≥ 2.228R at every Λ 2.75–78.7, while Λ 5.37 crashes from 1.099R — and level fails
  the other way (L4 lives from 1.445R up). Neither Λ nor level rules across r; the race is the
  periapsis margin vs the braking time.
- **"The fixed nose's misalignment is a controllable cost" (20261013-1428-second):** a
  v-tracking brake at the turn tier's ceiling keeps the same L4/L5 boundary (lags 144–164°);
  the wall is the turn rate (4.08°/min vs the fall's ≈ 24°/min), not the nose choice.
- **The rekey-cluster reading of the 13k refusal storms (20261013-1428-second):** 100% accrue
  inside the held off-axis burn, 0% at doll changes — a steady ~6.5/check tax, off-axis burn
  state only.
- **1890's "γ ≈ 1.2" as a pump threshold** (superseded, not contradicted): on the merged prograde
  nose every reachable crossing lands at γ_min ≤ 1.0005 and the crossing depth is set by the
  hold-start transverse rapidity η₀·sinθ (1890's 1.208 was one trajectory's η⊥, retro-fixed nose);
  there is no threshold to move (20261013-1145).
- "The downward E→1 crossing in flight is unreachable by a held key" (20261013-0236's own
  wording, its B8): a held key asserted once drives E through 1 downward and the Passage→Cycle
  flip compiles (E8.0–E8.3; 20261013-0350-second). The letter is dead; the operative rule
  survives in corrected form: a held key cannot END captured — the fixed nose accelerates past
  periapsis, the capture is transient, and the arrival needs the timed cut (C/T).
- "B8's ×1.25 ladder measured no capture, so none existed": the ladder straddled the
  ~1.8×10⁷-tick transient window (checker X8.3); the pump it saw afterwards is the law, not a
  sampler artifact — the two effects were conflated in the run's own reading
  (20261013-0350-second).
- The in-flight near-parabolic landing as a risk — every measured crossing (up and now down)
  lands inside |E−1| ≤ 8.4×10⁻⁹ and compiles with the clock at 10⁻¹¹…10⁻¹⁵
  (20261013-0236; 20261013-0350-second).
- The pre-merge list (clock saturates; register/word is the wall; no tube past γ 2000) — see
  20261011-1600-inversion-e128 and 20261009-2043-scout-a1a4 below; all superseded by the merge.

## Open directions
1. **The playability consequence** (the seam's residue): the arrival maneuver needs a timed
   cut (C/T prove it; the tracking brake's failure closes the attitude alternative) — what does
   the HUD/plan surface to the player about the transient capture window (~2×10⁷ ticks here)
   and the crash margin? The Λ rule is now scoped: at the low orbit, below Λ ≈ 5–11 (=
   0.3355·2^L) a held brake dies; from raised starts the margin, not Λ, decides — the HUD's
   second number is the brake's start radius (or the periapsis walk). Probe-side rule for every
   run: never exit on the first family flip — read to a fixed horizon, or a transient poses as
   an outcome (X8.3's lesson). The `range`/turn defect list now has four entries: turn-key
   deaths at escape speed (135°/180°), A-L2's braking-phase Range loss, the jagged fit
   boundary, and the turn tier's 2⁻³⁰ rate being ~6× too slow to follow a terminal fall.
2. **The crash basin's true ruler:** Λ fails across r, level fails across r — the margin race
   (periapsis walk vs braking time; start radius and v₀) is the standing mechanism but is not
   yet a dimensionless number with a measured threshold. The r-only sweep (circular starts at
   chosen radii — a scenario change) and hyperbolic arrivals at speed are the flights that
   would name it. L5's graze (1.014 R at γ 1.002) remains the separatrix specimen at 1.099R.
3. **The far-field fit path**: build the key from invariants (or carry the fit's intermediates
   wider) where the state→key cancellation bites; a checker should re-derive L from the flight's
   own tube words first. Now owns the four named defects above (the turn tier's rate included).
4. **The storms' cost:** when they fire is answered (steady in-burn tax, off-axis burn state,
   γ ≥ ~2, no doll changes); what a refused kick costs a frame, and whether the tax scales with
   cadence, are the allocator's remaining half (needs a timing harness; M1-side).
5. The `seen`/Doppler instruments at high γ (unread, carried from before).

## Contradictions
- None open. My Q48-k mechanism (prediction 5) died against the measured k ≈ 1/peri; the
  fit-arithmetic reading is the standing one, one checker away from confirmation. 1890's
  γ ≈ 1.2 threshold is retired as a reading (one trajectory's η⊥), not contradicted.

## Runs
- 20261011-1600-inversion-e128 (gold): clock saturates at dt/dτ 2; the wall (γ≈1800) is the rebind's k word; gate dead above β 0.25.
- 20261009-2043-scout-a1a4 (silver): plunge, capture and γ-2000 orbits compile into the same ψ-panel tube, exact to 1.3×10⁻¹⁰.
- 20261008-1947-redteam-efb2 (silver): doll-frame crossing solver exact to γ 2×10⁶; observer-frame form mis-locates emission; the view aliases (→ view).
- 20261008-2031-second-20261008-1947-redteam-efb2-4d7e (silver): confirms the solver (0 fails to γ 2808 under acceleration); the view's PASS is convention-carried (→ view).
- 20261013-0037-dynamics-1890 (pending): post-merge: clock exact in all new regimes; held brake
- 20261011-1600-inversion-e128 (gold): clock saturates at dt/dτ 2; the wall (γ≈1800) is the
- 20261009-2043-scout-a1a4 (silver): plunge, capture and γ-2000 orbits compile into the same
- 20261008-1947-redteam-efb2 (silver): doll-frame crossing solver exact to γ 2×10⁶;
- 20261008-2031-second-20261008-1947-redteam-efb2-4d7e (silver): confirms the solver (0 fails
- 20261013-0236-inversion-57ce (silver): in-flight E→1 crossing measured safe (E−1 ≤ 7×10⁻¹⁰
- 20261013-0037-dynamics-1890 (silver): post-merge: clock exact in all new regimes; held brake below γ 1.2 is a pump; the forward wall is gone.
- 20261013-0236-inversion-57ce (silver): in-flight E→1 crossing measured safe (E−1 ≤ 7×10⁻¹⁰,
- 20261013-0350-second-20261013-0236-inversion-57ce-41b5 (silver): the downward crossing
- 20261013-1145-dynamics-0e79 (this run): no γ pump threshold on the prograde nose (γ_min ≤ 1.0005 at every crossing, ruler η₀·sinθ); from-orbit held brake crash basin ordered by Λ, boundary Λ* ∈ (6.8, 13.6); turn-key Range deaths and 13k refusal storms named.
- 20261013-1145-dynamics-0e79 (silver, twice-checked gold/silver): no γ pump threshold on the
- 20261013-1428-second-20261013-1145-dynamics-0e79-8574 (this run): the record regenerates
