topic: high-gamma-clock
status: open
closed-by:
valid-while:
updated: 20261013-0236-inversion-57ce

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
- **The gentle half of the throttle never reaches the crossing: it dies silently at the surface.**
  The same held key at L1–L4 (checker flew L1; the author L2–L4): DEAD `fault=None`, zero refusals,
  r_at_death 1.05–1.09×10⁹ < surface 1.1306×10⁹ (the kill is `step.rs`'s `r < surface`, not the
  leave — leave needs r > 2^40), event_time ∈ (7.0×10⁷, 1.12×10⁸], monotone in level (the stronger
  burn inspirals sooner) — the sweep's crash-into-Home regime with its threshold measured:
  crash below L5, exact crossing from L5 up (this scene, the retrograde nose on main). The crash and
  the leave are both `fault=None`: the record cannot tell them apart.
- **A held brake key is a pump, not a brake, below γ ≈ 1.2.** Retro L15 from γ 30.7 brakes
  smoothly to γ 1.208, then the same held key pumps back through γ 186.7 (still rising).
  Brake-to-rest by a held key is impossible: rest is a crossing, not a fixed point; the
  playability plan needs attitude-keeping. A turning flight survives 69,660 rebind refusals on
  its old binding (γ → 1.19, periapsis → 2.1e10 M): refusal counts cannot certify a lost flight.
- **The pump also owns the arrival maneuver:** from the root passage near periapsis
  (E−1 = 1.2×10⁻⁵, r = 9.76×10⁷), a held reverse at L8 never captures — E rises to 4.29 by
  t = 2.87×10¹¹, zero refusals, alive (20261013-0236-inversion-57ce). The downward E→1 crossing
  in flight is unreachable by a held key; it needs a timed flip burn and stays unmeasured.
- **The far hyperbolic `Range` wall is the fit's arithmetic, not the key.** The acceptance map
  (22 E × 22 periapsis exact states through the shipped `Rebinding::from_state`): E → 1⁺ compiles
  at every periapsis 10 M … 1.6e10 M (the parabolic edge is safe); `Range` refuses on a jagged
  boundary (E=1.1 at 2e9 M; E=2–100 at 4e8 M; E ≥ 1e4 at 3e8 M). At E ≥ 100 the accepted
  k ≈ 1/periapsis, E-independent — the shape carries no E, the gap does. At every tested refusal
  point `OrbitKey::from_invariants` builds the same (peri, k) key and it compiles: the fix is the
  far-field fit path (fit from invariants), not a representation change.
- **Slow far flights end at the leave, not the key wall.** An L2 escape settles onto a bound
  orbit (k > 1/2) whose apoapsis passes 2^40: silent death (`fault=None`), a leave, not a
  refusal.
- Domain: one plane seed, the unfixed retrograde nose (main), settle-based flights to t=2^38,
  my wall cap 55 s per flight (fwd15's γ-1800 tail not re-flown; the checker's extension flew it
  to the 2^40 window end, alive at γ 2,056). The crossing grid adds: 48 members, forward holds,
  brackets at 0.2%. Not the seed: `plane` spends its rng only on the 23 free ships (the player's
  and the planets' orbits are literals), so the player's flight is seed-exact — the checker flew
  seed 2 bit-identical. Not measured: the nose (wt/play prograde), other scenes, non-forward
  input patterns.

## Refuted
- Brake-to-capture by a held reverse key — the pump owns it: E 1+1.2×10⁻⁵ → 4.29 with no Cycle
  through t = 2.87×10¹¹ (20261013-0236-inversion-57ce).
- The in-flight near-parabolic landing as a risk — every measured crossing lands inside
  E−1 ≤ 6.5×10⁻¹⁰ and compiles with the clock at 10⁻¹⁴…10⁻¹⁵ (20261013-0236-inversion-57ce).
- "The wall is the representation" — at every tested `from_state` `Range` point (author and
  checker, out to periapsis 1.6e10 M) the same key builds via `from_invariants`, peri exact and k
  to 4–5 digits; `Passage::compile` accepted 5 of the author's 8 points (the 3 refusals also hit
  ok rows: the reconstruction's edge, not the key) (20261013-0037-dynamics-1890).
  E-independent (20261013-0037-dynamics-1890).
- The pre-merge list (clock saturates; register/word is the wall; no tube past γ 2000) — see
  20261011-1600-inversion-e128 and 20261009-2043-scout-a1a4 below; all superseded by the merge.

## Open directions
1. **The far-field fit path**: build the key from invariants (or carry the fit's intermediates
   wider) where the state→key cancellation bites; a checker should re-derive L from the flight's
   own tube words first (my discriminator reconstructed L, and 3 of 16 of its compile calls hit
   `Topology` also on ok rows — my edge, not theirs).
2. **The pump under a prograde nose** (the wt/play build): does the threshold γ ≈ 1.2 move, and
   does brake-to-rest need attitude control or a law change? Now coupled to capture: the downward
   E→1 crossing in flight is reachable only by a scripted flip burn — the named next experiment
   (fly reverse near periapsis, flip at apoapsis, bracket the Passage→Cycle flip).
3. **The crash threshold's dependence** (seed, nose, scene): the L4/L5 boundary is one seed on
   the retrograde nose; the playability HUD's impact warning is the fix this measures for.
4. **Refusal semantics**: 69,660 refusals survived — what does the scheduler do with a body
   whose every rebind refuses? (frame-cost's rebind bookkeeping, from the events side.) The
   mirror: death with zero refusals and `fault=None` — the crash and the leave are
   indistinguishable in the record; a `fault` for the surface kill would cost one tag.
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
