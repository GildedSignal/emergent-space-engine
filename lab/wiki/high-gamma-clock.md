topic: high-gamma-clock
status: open
closed-by:
valid-while:
updated: 20261013-0350-second-20261013-0236-inversion-57ce-41b5

# The ship at high γ: its clock, its energy, the wall after the exact-in-E merge

## Current best

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
- Domain: one plane seed, the unfixed retrograde nose (main), settle-based flights to t=2^38,
  wall caps 55 s per flight (fwd15's γ-1800 tail not re-flown; the checker's extension flew it
  to the 2^40 window end, alive at γ 2,056). The crossing grids add: 48 members, forward holds,
  brackets at 0.2%, and (this run) re-asserted brakes at fixed cadences, held keys, one 180°
  turn flight. Not the seed: `plane` spends its rng only on the 23 free ships (the player's
  and the planets' orbits are literals), so the player's flight is seed-exact — the checker flew
  seed 2 bit-identical. Checker's extensions this run: the same-tick one-world control (X8.3),
  G at two more relights, C12 (captures; clock 5.7×10⁻¹¹), E11.3 (held key crosses). Not
  measured: other scenes, noses that start far off v̂ (the turn tier is proven once, at L8).
## Refuted
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
   cut (C/T prove it) — what does the HUD/plan surface to the player about the transient
   capture window (~2×10⁷ ticks here), and does the crash threshold (below) interact with a
   cut flown one flush late? Probe-side rule for every run: never exit on the first family
   flip — read to a fixed horizon, or a transient poses as an outcome (X8.3's lesson).
2. **The far-field fit path**: build the key from invariants (or carry the fit's intermediates
   wider) where the state→key cancellation bites; a checker should re-derive L from the flight's
   own tube words first (my discriminator reconstructed L, and 3 of 16 of its compile calls hit
   `Topology` also on ok rows — my edge, not theirs).
3. **The pump under a prograde nose** (the wt/play build): does the threshold γ ≈ 1.2 move, and
   does brake-to-rest need attitude control or a law change? The capture side is now closed on
   main's nose (fixed and turned); the prograde nose changes the brake geometry everywhere.
4. **The crash threshold's dependence** (seed, nose, scene): the L4/L5 boundary is one seed on
   the retrograde nose; the playability HUD's impact warning is the fix this measures for.
   Now with the planet-crossing silent death beside it (F8.2) and the `fault`-tag proposal
   covering all three silent ends (crash, leave, planet).
5. The `seen`/Doppler instruments at high γ (unread, carried from before).

## Contradictions
- None open. My Q48-k mechanism (prediction 5) died against the measured k ≈ 1/peri; the
  fit-arithmetic reading is the standing one, one checker away from confirmation.

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
