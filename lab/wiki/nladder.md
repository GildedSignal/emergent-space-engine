topic: nladder
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261016-0504-dynamics-4c22
=======
updated: 20261016-0504-system-e070
>>>>>>> 20261016-0504-system-e070

# The N ladder: 28 live bodies toward 10⁹

## Current best
<<<<<<< main
<<<<<<< main
**The locals' storm is grid lock, not begin lock: the conjectured transplant of the belt's
stagger is refuted by the letter, and the grid-translate flattens the term 2.0-2.4x at both
seeds, N-independent (20261016-0504-components-4534).** The locals' standing train (335
events/frame max, period exactly 5,283 game-s, event counts bit-identical at N = 600/1e4/1e5;
the N=0 floor is 60) is the shared block-step grid of `step::aligned` ("every pair shares
boundaries"), not the shared clock begin: `ES_STAGGER_LOC=1` (the letter of open direction 1,
a hash-spread first plan begin) leaves the storm bit-unchanged (max 335, same frames 317/634 —
the population re-locks within one step), while `=2` (each doll!=0 ship's grid translated by
o = hash(id) mod step, dyadic, constants-only at genesis) deletes the standing train (worst
frames become the genesis transient 74-92, not 317/634): max 335 -> 141, p99 229 -> 131,
worst frame 12.9 -> 6.7 ms, kicks +0.3%, flat in N from 600 to 1e5; held-out seed 7: 359 ->
177 (2.0x). OFF arm bit-identical to pristine main's deterministic columns at every N. Two
named caveats: the event totals move under the phase shift (+6% seed 1, +73% seed 7, slices
12,837 -> 45,751 — kick cadence is intact, so the growth is in the between-kicks structure,
undiagnosed here), and the legality gates (B13/B14-class under shifted phases, ed3a's
direction 2) remain unflown — a measured lever, not an adoption.

*[Checker (silver): every deterministic column reproduced bit-exact on a clean tree (OFF/BEGIN/GRID
at 600/1e4/1e5 seed 1; both seed-7 arms; a repeat identical), and the OFF arm equals a
pristine-physics build column-for-column — main's own example does not link on Linux
(`proc_pid_rusage`), so the flown control is main's `step.rs`/`universe.rs` plus the print-only
Linux port. Beyond the flown domain: GRID 176 at 1e5 seed 7 and 143 at 3e5 (2.3x) — storm and
cure both N-flat there too; burn composes (p99 96->75 ms) and leaves the burn's own monster
untouched (719->747 events at frame 60, a different population). Two notes for adoption: the
+73% event inflation is exactly the fleet battle's slicing (`fleet.rs advance`, +32,914 of
+32,977 events at seed 7 are slices — the diagnosis is nearer than "undiagnosed"), and the
staggered class is broader than the 300 locals: the plane's own doll!=0 ships are in it (N=0
GRID max 60->47, != OFF). GRID also gives up `aligned`'s every-pair-shares-boundaries invariant
for arbitrary pairs; no consumer of it was found, but it is a law-level change to name at
adoption. Not gold: 2.0-2.4x, the author's own >150 kill bar fired at seed 7 (177), and the
legality gates are unflown.]*
=======
**The locals' storm is measured as a standing comb phase-locked to `aligned`'s absolute power-of-two
grid, and open direction 1's lever is refuted: the one-step birth spread that cured the belt wave is
re-absorbed by `aligned` within one period (the comb re-forms to ~93% of its envelope, p99 136
unchanged, events/game-s unchanged), while a PERMANENT per-body phase (a constant id-derived fraction
of the body's own step, ES_LOCAL_PHASE) collapses the storm to the no-locals plane: max events/frame
334→53 (= N=0's own 51-class floor), p99 136→25, worst-frame structure = the N=0 plane's, at the
price of +19-41% total events and the pair-shared-boundary property (a law change: digests differ;
legality gates unflown) (20261016-0504-dynamics-4c22, dynamics; budget-free coast, rtf 100, N in
{0, 600, 10³, 10⁴}, 2,000 and 6,000 game-s, digests of the OFF arm bit-identical to the record
N=100/1000/3000 coast).** The mechanism: the clock law chains each kick's time from the previous
kick (an offset persists — why the belt stagger worked), but the interval law re-anchors every
interval to the ABSOLUTE grid, so a doll's population born at one tick boundaries and kicks at
identical ticks forever: a standing, non-decaying comb (top-envelope per time-slice 198/192/178/210
over 6,000 game-s; the belt wave decays ×0.72), N-independent for N ≥ 600 (locals capped at 300),
max 334 at 10³ = 917c's 10⁵/3×10⁵ number, N=0's 51 reproduced. Composition [checker-corrected,
20261016-0504 check]: the run's ES_ATTRIB instrument pushed two takes per frame (a duplicated block),
so its per-frame attribution was misaligned 2:1 (odd rows read drained zeros) and its "unattributed
pull-lane residue" is an artifact. With a frame-aligned instrument the worst-12 storm frames are
~93% Home-doll items — k 26–32 kicks + b 135–197 boundaries each, unattributed ≈ 12.7 of 177.6
events — and the beats land every ~330 game-s (frames 198/396/594/793/991/1189): the comb is the
doll-2 locals' own boundaries, with no second lane. Consequence for the letter: the locals'
~334-event ≈ 9.8 ms
M1-rate recurring term drops ~6× under a de-phase, and the frame's 12-ms letter is then set by the
belt stream alone (≈ 4.6×10⁶ by 917c's own stream rate), past the memory break (1.3-1.6×10⁶): after
the wave cure and a locals de-phase, memory binds the flyable N, not the frame. The honest levers
now: (a) the de-phase's price must be paid down (+20% events, and the pair-boundary property is a
law change: B13-class gates unflown — direction 2's analogue for this lever); (b) the doc's own
step 5 (secular kicks for stable planet-doll bodies) deletes the comb's events instead of spreading
them; (c) whatever keeps `aligned` shared must de-phase at birth PER INTERVAL, not once.
>>>>>>> 20261016-0504-dynamics-4c22

**d31c's first named rung is flown and it is a pure deletion: `plan_clock` reads the body's own
synchronised state up to three times per plan (the birth's `pt_exp` read inside `ext::constants`
setup, the projection's `readout`, the drift fit's `readout`); one `readout` serving all three
cuts the birth pass 6.05-7.43 us/body (18.2-22.2%) and the whole birth rail 42.4-43.7 ->
35.8-37.4 us/body (-14.5%), with the universe digest byte-identical at every (N, seed) flown
and the OFF arm digest-identical to pristine main (20261016-0346-quant-3ec8, quant; `ES_ONE_READ`
0/1 inside one binary, `pass_bench` on `plane_extra`, N in {1e4, 3e4, 1e5, 3e5} x seeds {1, 7
held out}, 18 interleaved flights, arms A/B).** Flat in N (cut 6.05-7.43 across the decade and a
half, belt-only cut ~2 readouts ~6.8-7.6 us: a `readout` is the tube walk, the same object b8fc
priced 4.0-5.4 us), flat across seeds, requeue+rekey still <= 0.099 us/body, peak RSS identical
to +-0.05%. Anchors reproduced on this box: shipped pass 32.1-33.5 (d31c: 32.8-33.9), rail
42.4-43.7 (404b: 42-44). The reuse is exact because `Binding::readout` is pure and nothing moves
the binding between the three reads (only `ext::constants`, which reads other bodies, and
`rec.ext` writes intervene); only doll-0 ships plan through `plan_clock`, so the ~300 locals and
the plane's doll!=0 ships are untouched. Composes with d31c's shared planets readout (disjoint:
secondaries vs own state). NOT flown: re-plans in flight (handoffs, decisions) and the thrusting
path, where `kick_clock`'s post-burn `project(t)` still reads once more per thrusting kick (its
state was mutated by the kick: the honest hoist there needs the post-rebind state -- the named
next rung); the digest here is tick-0, so adoption should re-fly the ladder digests.
=======
>>>>>>> 20261016-0504-system-e070

**[This run, 20261016-0504-system-e070, system lens] The main-tree storm is the belt's
wave, and the locals are the stream, not the frame: the isolation control 917c never flew
inverts the page's next-lever reading.** On shipped main (no belt stagger; the off-arm of
this run's patch is digest-identical to pristine, 5b2d998b…), budget-free coast flights at
rtf 1000/30k game-s: the worst frame's bucket holds 922 events at 1e4 / 8,482 at 1e5
(linear, 9.2×), of which **872 / 8,432 are doll-0 belt first kicks and only 50 / 50 are
N-flat, as their count is); the heaviest tick is 2,873,098,240 = 14,151 game-s [checker: the run
wrote 14,177; TICK_SECONDS × tick = 14,151.4], seed- and N-independent, with later waves at 2T
and 3T (checker, 55k game-s: top frames f837–852, then f2538 = 3T, decaying) — the belt clocks
fire together at one half-interval of the ≈2.83e4 s recurrence ("exactly half of cf45's
2.814e4" is 0.6% off). Deleting all 300 locals (`ES_NO_LOCALS`) moves the worst bucket 922 → 894
and the max 479 → 447, but cuts total kicks 55,985 → 15,785 (**72% of the event stream**;
4.5e-3 kicks/local/game-s = 82× the belt's 5.4e-5, which matches a9d7/cf45). A locals'
first-plan stagger (ed3a's law shape on secondary-doll ships, per-id offset, digest-
changing) moves the frame peak by **exactly 0** at 1e4 and 1e5, both seeds (479/671/4,241
identical) [checker: the flown stagger re-times ≤16 of 40,200 local kicks (bits 24) and is a
complete no-op at bits 20 — the 0 measures the belt's composition, not the stagger's power].
Consequences: (1) on main the frame lever is the unmerged **belt** stagger,
not a locals spread — 917c's "the locals class is the next frame term" holds only
post-stagger (their branch) and their 334-residue attribution was uncontrolled: the
locals' whole worst-frame contribution on main is ~50 events at the wave frame, N-flat there
— but seed-dependent: at seed 3 [checker] the locals bind the worst frame (689 vs 441 without
them, ≥284 events; their frames beat the 1e4 wave); (2) the locals
cadence dial, not a stagger; (3) instrument caveat for every frame letter on this page:
`xtask universe --bench` measures the engine alone only behind this run's `ES_ENGINE_ONLY`
arm — the served loop adds the view's Θ(N) gather (62c1) and player-driven reads.

*[Predictions 1–3 (storm = locals' birth synchrony ≥ 80%) FAILED in one direction — the
belt is 94–97% of it; held: off-arm bit-identity and the locals' N-flatness. The control,
not the stagger, was the run's product.]*

<<<<<<< main
**The staggered wave is flown budget-free through FOUR wave periods and the cure is permanent,
not one-wave: the staggered train's TOP 250-s windows are flat to ±3–4% across 60k game-s at 10⁵ and 3×10⁵ (the full window
distribution is 1,544–2,775 — beat/no-beat bimodality, no spikes [checker]; top
250-s windows 2,700–2,775 and 6,288–6,366 events — no structure at 28.3k/42.5k/56.6k where the
unstaggered arms peak at 2,223/1,579/1,194 and 6,603/4,443/3,437 after 4,243/12,729 at wave 1;
the wave period is exactly 14,167 game-s, peaks decaying ×0.72 per unstaggered wave; the birth
wave costs 50.8–53.6 µs/event vs 12.2 at wave 2 — this box, 47–51 and 29.3 M1-projected)
(20261016-0346-scout-7da3, scout; ed3a's ES_STAGGER patch verbatim, off arms regenerate the
record's crests to 87/96%; its µs/event only on the author's load — the checker's re-run reads
74–79 µs/ev on the shared box; rtf 1000, budget-free, coast).** The run's letter arithmetic
(rtf 100, 12 ms, 29.3 µs/ev) is REFUTED at the letter's own width [checker]: the ÷10
conversion of the rtf-1000 crest (27.3/42.7 ev/game-s → 45.5/71.1 events per rtf-100 frame) breaks
on the train's real fine structure — direct rtf-100 budget-free flights (10⁵ and 3×10⁵, 42k game-s,
`chk_*_r100long`) measure a worst frame of **342/366 events = 10.0/10.7 ms at the M1 rate, N-flat
(1.07× for 3× N)**: the crest is a ~660-game-s sub-grid beat of ~200–350 events (spacings exactly
660/662 game-s; present in the off arm's train between waves at 333-s spacing), not the belt's
stream. The staggered letter therefore HOLDS at both N at the M1 rate; the first N-scaling letter
term is the smooth stream (4.62×10⁻⁵ ev/body/game-s on-arm), which meets the beat at the 12-ms
letter around **N ≈ 6×10⁵ — below the memory break (1.3×10⁶), not past it; +7× over the unstaggered
8.4×10⁴, not +20–26×**. Composed 10⁹ at the key arm the same way: stream alone 8.5 ms =
**~0.7× the letter — the BOTTOM of fermi-1a1c's 0.5–2.7× band, not its top** (the author's 2.2×
rested on the same ÷10 conversion). P1's "passes with margin at rtf 100 (45.5 events / 1.65 ms)"
is refuted: measured 342 events / 10.0 ms M1 (25.5 ms this box).

**The checker's named gold experiment is flown and the stagger configuration is KILLED on the
legality instrument: ES_STAGGER armed fails B13 outright — 0/64 judged flybys (worst relative
ΔE/ΔL 4.65e0) against the off arm's 60/64 baseline-red 2.12e-2 — and changes all 13
`ladder_digest` case digests (9 with identical counts, 4 with changed kicks, e.g. 32,537→31,973),
so the checker's "armed digest identity 13/13" was an unarmed-run artifact — the proven mechanism
(checker 2 of this run, on the runner's own regen): regen.sh's build line is target-filtered
(`--example …` with `-p xtask`) and never rebuilds xtask, so an armed gate invocation can run a
leftover pre-stagger binary and report armed == off; every armed number engagement-verified via the
id=1 shift 0.5666·step and PLANE_TRACE's kicks 305→213 through the same flyby). The mechanism:
a bare-born ship's first kick window IS its first encounter, and an encounter is aperiodic — the
uniform-in-one-step phase shift that is second order for the belt's periodic sequence is first
order for the assist (20261016-0504-second-20261016-0346-spacex-917c-c840, second author; the
parent's patch verbatim, off arm bit-identical to pristine; B14 frozen times out in both arms;
B14-class probe: escape classes identical across off/armed/reference on 8 moons, apsidal rates
within 2.9% of the reference between arms, inside B14's 10% wherever the law already is).**
The frame record stands (the 28× collapse, the locals' floor); the CURE must be birth-time-lawful
(spread the birth program's tick grid — B18's domain — so first kicks land spread by construction
and lone ships are untouched), and its first gate is the same armed B13 flight.

**Checker 2's named gold rung is flown and it splits: the readout lever alone stays under its own bar, and the pass's shared-recompute family is the real bill (20261016-0346-second-20261016-0213-system-d31c-79ca, second author; `ES_STATE_ONCE` = one own-state read serves the plan's three (register word, projection, tail) and reuses the projection's Kepler, `ES_CONSTANTS_ONCE` = the per-doll `(Δs, c, b)` Hill sum served from d31c's table (a source reading its own doll sums live), off = shipped verbatim; two integer counters aboard).** Belt 10⁴/3×10⁴/10⁵ × seeds 1/7/11 (11, 3×10⁴ and the 10⁵ s7 full cell held): pass off 33.6–36.4 / on 23.4–24.3 (digests equal d31c's record) → state 16.4–17.2 = **on/state 1.39–1.46× — the named own-state lever misses the ≥ 1.5× bar at every cell** (one readout is 3.4–4.0 µs; the arm deletes two of three calls plus the duplicated Kepler, ~0.3 µs) → full **11.23–11.48 µs/body, on/full 2.07–2.15×, shipped→full ≈ 3.0×, flat in N**, digests bit-identical across all five arms at all seven cells, suites 77/0 in all five knob configurations; integers: readout calls 2.91–2.99 → 0.97–1.00 per body (**the shipped pass reads each clock body's exact state three times**), constants 5.2–5.4 → 0.03 µs/body (hits 0.97–1.00). The pass after both is per-body by right: apply 4.4–4.6 (40%), ONE integer Kepler decode 3.7–3.9 µs (53% of the surviving replan — at t = 0 it returns the state `add_body` just bound), project 2.3–2.5, ticks ~0.9. Next rungs: thread the just-bound state (deletes the last birth readout) or b29a's program store (never plans); also closed here: d31c's checker's latent catch — `PlanetsAt::build` now refuses to arm if any live read errs.

**The named rung is flown and the wave retires as a frame term: the staggered first-kick wave,
flown BUDGET-FREE at 10⁵ and 3×10⁵ (stagger rebuilt on this tree, default off, off-arm
bit-identical 13/13 digests), collapses the belt's own frame peak 28× — 994 → 35 attributable
events at 3×10⁵ (~1.0 ms at the M1's 29.3 µs/event) — and sinks BELOW the ladder's own
N-independent baseline, the 300 locals' storm floor of 334 events pre-wave (measured: N=0
without ladder locals peaks at 51 events; pre-wave max is 334 at every N flown — 10⁵, 3×10⁵
and the checker's 4×10⁵; the earlier "452" was a post-wave wave+locals frame, not a locals'
storm; the locals are secondary dolls the stagger never touches) (20261016-0346-spacex-917c).** Window-level, ed3a's
instrument now budget-free: 45,950→2,737 (16.8×) at 10⁵, 136,718→6,342 (21.5×) at 3×10⁵, and
the staggered window-peak rate 25.4 events/game-s IS the steady stream — the birth arrival
rate equals the steady phase, as ed3a composed. Unstaggered anchors land bit-exact on 1a1c's
record (487 and 1,328 peak events — the schedule is deterministic; ms are this box's
50–80 µs/event under 2–3-way load). Consequences: (1) **the "staggered-break at ~1.4×10⁶" is
not a findable break** — the belt's staggered frame term (35 events at 3×10⁵, linear:
11→35 from 10⁵; checker: 48 at 4×10⁵, on the line) reaches parity with the locals' storms
only at N ≈ 3×10⁶ and is never the frame's binding term [checker correction: the total
frame's 12-ms letter (M1, locals included) extrapolates to ≈ 6×10⁵ — before the memory break
1.3–1.6×10⁶, and locals-driven, not a wave break], so at 10⁹ the wave contributes only the steady-stream term (148× over at the
shipped kick, exactly cf45's number — the kick and memory levers stand); (2) **the frame's
binding N-scaling term after the stagger is the unstaggered locals class** (the ladder's 300
about Home/Moon; at 10⁹-scale populations the analogue is any dense short-period population
— the same one-step spread applies, one lever, one law); (3) the wiki's own "peak ≈ 29 events
≈ 0.9 ms at 10⁵" instrument error is now measured: 29-equivalent ≈ 11 attributable events ✓,
but the FRAME peak is the locals' floor — wave numbers must be stated belt-attributable
(post-wave max minus pre-wave baseline), or they measure the wrong population. Still open on
the stagger itself: the behaviour gates under the shifted first-kick tide phase (ed3a's
direction 2) and the M1 re-measure of the letter margins.

*[Prior best retained — see lab/wiki/nladder.md's standing text: d31c's shared planets
readout, the 10⁹ budget assembly and its instrument rules (1a1c), the scan cure (e28f/51b7),
404b's birth-rail split, the scout's last-segment floor, the depth axis (398f/57ec), the
seam/retention family, 8b89's ES_LAZY_ALL, b172's formation falsifier, 1343/3dc8's passage
pricing. This proposal is additive and sides with neither of the page's standing conflicts;
the merge resolves against whatever side stands.]*
=======
**[prior bests stand below — d31c's one-read plan_clock cut, 3ec8; the staggered wave
flown budget-free through four periods with the 660-s beat and the ≈6×10⁵ corrected
break, 7da3/917c; the seam/retention family and the 10⁹ ledger (1a1c, effb, 0619, 0757);
the floor deletion, d86c. Unchanged by this run.]**
>>>>>>> 20261016-0504-system-e070

## Refuted
<<<<<<< main
- **"The same one-step first-kick spread (secondary dolls' clocks) flattens them; one law,
  one lever" (open direction 1's letter, ed3a direction 3 / 917c direction 1): the begin-
  stagger transplanted to the locals leaves the storm bit-unchanged (max 335, same frames) —
  the belt's cure works because ext-clock bodies plan each next kick at their own tick, while
  block-stepped bodies snap back to the shared dyadic grid within one step; the lock is the
  grid, and the lever that moves it is the per-body grid translate (20261016-0504-components-4534).
=======
- **Open direction 1's lever as stated ("the same one-step first-kick spread flattens the locals"):
  the spread is re-absorbed by `aligned` within one period.** ES_LOCAL_STAGGER (a planet-doll ship's
  first interval offset by a uniform id-derived fraction of its own step): max 334→260, p99 136→136,
  top envelope 198/192/178/210 → 180/188/178/195 (the comb stands at ~93%), events/game-s identical
  (4.02 = 4.02); the clock law's cure does not transpose because the interval law anchors to the
  absolute grid, not to the previous kick (20261016-0504-dynamics-4c22).
- **The run's own "unattributed residue" readings (both the fleet-lane guess and its one-population
  revision) [checker, 20261016-0504]:** both rest on the ES_ATTRIB double-push misalignment (odd
  frames read drained zeros, even frames read the half-index frame's counters). With a frame-aligned
  instrument the residue is ≈ 12.7 of the worst-12 frames' 177.6 events (~7%): there is no second
  lane, fleet or pull; the storm is ~93% doll-2 boundaries+kicks. The direction-1 refutation above
  is unaffected (it rests on event counts and digests, not attribution).
>>>>>>> 20261016-0504-dynamics-4c22

- **ES_STAGGER as a post-hoc first-kick mover, armed, as a birth default (spacex-917c's adoption
  direction, ed3a's open direction 1):** B13 armed 0/64 (off 60/64, worst 4.65e0 vs 2.12e-2);
  all 13 armed ladder_digest digests change; the checker's armed-digest identity did not
  reproduce (an unengaged armed run: the regen build line never rebuilds xtask — the `--example`
  target filter drops it — so a stale pre-stagger binary reports armed == off; verified by
  checker 2, who also flew the bounded variant: a quarter-fraction stagger still fails B13 at
  2/64, so the kill is generic to the configuration, not the 0.5666 draw). Killed as a
  configuration; the wave's frame findings and the
  birth-time-lawful cure stand (20261016-0504-second-20261016-0346-spacex-917c-c840).

- **917c's reading of the main-tree pre-wave storm as the locals' ("the locals are
  secondary dolls the stagger never touches... pre-wave max is 334 at every N") in the
  one place it was actionable — as the next frame lever on main:** the isolation control
  (delete the locals) moves main's worst frame by 3% (922→894) and the peak by 7%
  (479→447) at seed 1, and a flown locals stagger moves the peak by 0 at two N and two seeds;
the storm is the belt's first kicks at Δs/2, linear in N (20261016-0504-system-e070).
[checker: the isolation control was flown at seed 1 only; at seed 3 the locals bind main's
worst frame (689→441 without them, ≥284 of 689), so the refutation is established at 1e5+
and at seed 1's 1e4, not universally at the ladder's low end.]
On
  917c's own branch (belt stagger in force) the 334 residue may still be the locals'; that
  reading is uncontrolled, not refuted.

## Open directions

<<<<<<< main
<<<<<<< main
1. **The locals class is the next frame term** (ed3a's direction 3, now measured as the
   binding one): the 300 ladder locals storm at 334 events/frame pre-wave at every N flown — the same
   one-step first-kick spread (secondary dolls' clocks) flattens them; one law, one lever. [Answered this run: the letter is refuted (BEGIN leaves max 335); the grid-translate form
   flattens it 2.0-2.4x, both seeds, N-flat — what remains of this direction is the seed-7
   event-total diagnosis, the burn/fleet arms, and the legality gates.]
=======
1. **The de-phase's legality and price (the next rung on this finding):** ES_LOCAL_PHASE gives up
   "every pair shares boundaries" (docs/law.md's own invariant) and pays +19-41% events over the
   first 6,000 game-s [checker: the stub price is front-loaded — +10.8% over 12,000 game-s
   (46,655 vs 42,112 events), phase slices 8,337 vs base 3,951]; the gates
   that must hold are B13/B14-class under the shifted phases, and the price to beat is the ~+11-20%
   event count (the stubs the phase grid mints at step changes). Alternative inside the law: birth
   de-phase PER INTERVAL (an offset the body keeps against the absolute grid) is the same property
   change; step 5's secular kicks for stable planet-doll bodies delete the events instead.
>>>>>>> 20261016-0504-dynamics-4c22
2. The stagger's legality gates (B13/B14-class under the shifted tide phase) and the M1
   re-measure — unchanged from ed3a's direction 2.
3. (prior directions stand: the compact store's wiring, the cadence law, the page's standing
   conflicts for the integrator)
=======
1. **[relocated] The locals class is the event-rate lever, not a frame lever:** 300 locals
   = 72% of all kicks at 1e4, 82× the belt per body — the 10⁹ CPU ledger's hot population
   is dense short-period groups; the dial is the cadence law (cf45), and any spread buys
~50 events at the wave frame at most (measured, N-flat there; seed-dependent elsewhere —
seed 3's locals frames reach 689 vs 441 without them, checker). The frame lever on main stays ed3a's belt
   stagger (merge it, then re-run this control to price the true post-stagger residue).
2. [unchanged: the stagger's legality gates under the shifted tide phase; the M1
   re-measure; the page's standing conflicts for the integrator; the compact store's
   wiring; the cadence law.]
>>>>>>> 20261016-0504-system-e070

## Contradictions

- [new, resolved by regime] 917c's "pre-wave max 334 at every N" (their branch, belt
  stagger on) vs this run's linear-in-N 479→4,241 (main, belt stagger off): both true on
  their own trees; the page's frame letters must name the tree. The locals' residue
  (~50/worst frame here) is the candidate 917c's 334 needs on theirs — unmeasured there.
- The page's standing merge conflicts (main vs d86c vs 51b7 vs e28f) remain the
  integrator's; this run sides with neither and its section is additive.

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261014-0000-fermi-3071 (awaiting grade): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (awaiting grade): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor; checker: cold-belt 13×, 6.4× at σ0.3, darwin domain p ≤ 8192 M.
- 20261014-1221-components-0e37 (this run, awaiting grade): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (this run, awaiting grade): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (this run, awaiting grade): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (this run, awaiting grade): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-dynamics-bf21 (this run, awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt (its 1-2 AU core numbers move little; the anchor does not); shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the checker's named gold
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at
- 20261014-1631-library-7f99 (gold): the deletion program's method — 26 kills, the 10% add-back
- 20261014-1511-components-a2c1 (silver): break 3's scan half decomposed — the cap's monotone walk
- 20261014-1221-components-0e37 (silver): break 2's lever — the compiled orbit is write-only memory,
- 20261014-0450-scout-b29a (silver): the smallest promotion is no promotion.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law code-verified.
- 20261014-0000-fermi-3071 (silver): rule 2 dead by decomposition; the tail manufactured.
- 20261014-0000-fermi-3071 (silver): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-1221-components-0e37 (silver): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than at 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (gold): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain; the mid-drain cut and the belt digest's wall-schedule instability named.
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions (checker: 0.15–0.16 ms even uncapped; silver).
- 20261014-2012-second-20261014-1631-library-7f99-5903: sensors deleted digest-identical (10^3 walk 15x); horizon not belt-scale; chatter 193 -> 0 under refusal at 3.9x events.
- 20261014-2012-system-a669 (silver): key quantum vs per-kick dL — breaks 1/2/4 one dial; flip-gated rebind.
- 20261014-2130-quant-d7e3 (this run, awaiting grade): in-band wave exposure measured — OOM at
- 20261014-2130-second-20261014-2012-system-a669-eb2d: flip-gated rebind wired, default-neutral; the dial's run caps at 4 — 10^2x refuted, mint counted 1.00/kick.
- 20261014-2130-taleb-625b (silver): the player in the belt band: in-band burn = memory ruin (11.2 GB, killed); scan 214-1,087x; coast monster 2 s.
- 20261014-2248-fermi-b30b (awaiting grade): the steady state through waves measured — memory plateaus 4.85-5.06 kB/body (slope <= 5 B/wave; churn killed 3 orders), rate 3.33-3.50e-5 confirmed end-to-end, train ~27-28 k game-s; memory binds the flyable N at every point.
- 20261014-2248-inversion-4af4 (this run, awaiting grade): the wave train flown — memory a step not a staircase, the train shears, and the digest wobble is the presented-time cut.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (second author, awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer; transit linear, ruin band [1.7,3.0] AU.
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (this run, awaiting grade): the checker's named in-box experiments done — 25 wave periods flat (700 k game-s, digest-stable), dissolution measured (floor rises to the belt-rate equilibrium), 4.2x10^5 at the box ceiling, 4af4's record made to regenerate.
- 20261015-0250-scout-760f (awaiting grade): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; knots 672 B/body (13.7% of the plateau) — eviction 1.16x, the wall is the record stack; 10^9 lives in programs.
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (this run, awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10^5); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0358-taleb-d7bc (awaiting grade): the ruin fenced — byte cap on held scans, RSS flat 290-311 MB vs ~315 MB/s climb and death; digest identical at 10⁴; the hidden answer bill measured (4-28× play).
- 20261015-0724-components-e0f9 (this run): the seam rebuilt, committed and re-flown — five arms digest-identical, 10⁵ = the scout's anchor with 273,200 demotions, standing 1,603→930 B/body, rss −28%; the machinery free, the no-retention re-mints the whole bill.
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10^5); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (awaiting grade): 25 wave periods flat (700 k game-s, digest-stable), dissolution measured (floor rises to the belt-rate equilibrium), 4.2x10^5 at the box ceiling, 4af4's record made to regenerate.
- 20261014-2248-inversion-4af4 (awaiting grade): the wave train flown — memory a step not a staircase, the train shears, and the digest wobble is the presented-time cut.
- 20261014-2130-quant-d7e3 (awaiting grade): in-band wave exposure measured — OOM at the cap's arithmetic.
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17-0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10^5, 1,213→90.3 at 2×10^5, bit-exact at every canonical cut past the drain.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-dynamics-bf21 (awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10^5 burn at 11.97 ms max (114×) with the digest bit-identical.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10^5/2×10^5 burn; fix named (hold the scan).
- 20261014-1631-library-7f99 (awaiting grade): the library mined verbatim; deletion audit 26 kills / 2 landed add-backs; promotion = refusal filter.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N; fixes named in cost order.
- 20261014-1221-components-0e37 (silver): compiled orbits are write-only in flight; the view's ramp is the one reader; floor 673 vs standing 1,806 B/body.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law rate = 2⁷/P code-verified.
- 20261015-1338-quant-1d52 (this run, awaiting grade): the retention rule built and priced — promotions = demotions exactly (85-90% hits, wall +6.5-12.5% over shipped, digests identical, the record's anchors reproduced); global retention erases the memory win (retained set = every kicked body), the redundancy is N-independent (the locals) — adopt bounded, not global.
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (second author, awaiting grade): the bounded cache built and flown — digests identical on 23 flights, retained <= cap by construction, 962 B/body kept (rss 393-414 vs global 548-554 at 10^5), promotions at the kick floor at sufficient cap (exactly 1.00x and 0 evicts on burn at 65,536), ~0.15 cores re-mint at 10^9; the cap curve is the law's read pattern (coast ~4k, burn ~40k).
- 20261015-1450-taleb-b0ed (this run, awaiting grade): the bounded cache built and priced — digest-identical, ratio flat in N at matched cuts (≤1.026 at 4,096 to 2×10⁵), the deep-cut +74-78% bill is history depth (2×N read-once fills), not N; adopt S=16,384.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt; shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at 10⁵/2×10⁵ burn; fix named (hold the scan).
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (this run, awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10⁵); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10⁵); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, bit-exact at every canonical cut past the drain.
- 20261014-1719-dynamics-bf21 (awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at 10⁵/2×10⁵ burn; fix named (hold the scan).
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (second author, awaiting grade): the bounded cache built and flown — digests identical on 23 flights, retained <= cap by construction, 962 B/body kept (rss 393-414 vs global 548-554 at 10⁵), promotions at the kick floor at sufficient cap (exactly 1.00x and 0 evicts on burn at 65,536), ~0.15 cores re-mint at 10⁹; the cap curve is the law's read pattern (coast ~4k, burn ~40k).
- 20261015-1615-quant-0619 (this run, awaiting grade): the burn knee is the demotion count, not a working set — WS = demotions = N + 30,187 integer-exact at four N, seed and cut; price law exact 7/7 (promos − dem = hits_sat − hits_cap); fixed cap degrades with N (1.24→7.23→8.50×); ring pins +27,911 zombies over global; no bounded cap ships burn at 10⁹ (knee ≈ 1.4 TB) — price the re-mints or delete the reads.
- 20261015-1615-second-20261015-1450-taleb-b0ed-f55d (second author, awaiting grade): the burn knee measured — 1.31xN exactly at 10^5 and 2x10^5, mints = apply not the resolver, hits = the scan (26->71% with N), kick-anchored admission refuted; identity 26/26; regen fixed.
- 20261015-1615-spacex-1343 (silver): the passage tail priced — 96 B/panel, 10.74 panels/octave past the 2^10 join, universal in w; re-mint bit-identical, so never-demote is for plunges alone (checker: the cap is on outer, not w — star-grazing mints w=20, 25.7 kB alive; unflown on the seam).
- 20261015-1747-inversion-b172 (this run, awaiting grade): the formation falsifier measured — concentration collapses the burn knee from ~1.31×N to ≤ N/24 (1.014×dem at cap 4,096 vs the belt's 7.23×), same kicks/demotions/digests; the no-cap law is the belt's geometry, not burn's.
- 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (this run, awaiting grade): the checker's named gold experiment flown — demote-passages digest-identical on 18 flights (standard ladder + mixed-peri comet stream), record 113 B vs 18.8–25.3 kB, bill 5.9×dem at 421–583 µs p50, rss 445–979→27–51 MB (Live-arc pinning deleted).
- 20261015-1926-spacex-8b89 (this run): the class list dies — ES_LAZY_ALL demotes every keyed entry (births, no-kick settles), 7 scenes digest-identical, standing arcs → the centres (680 B/body at the belt's birth state), rss 979→20 MB on mixed; no state birth mints a Plunge.
- 20261014-1719-dynamics-bf21 (silver): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (silver): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt; shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (silver): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain.
- 20261014-2012-components-38bf (silver): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer; transit linear, ruin band [1.7,3.0] AU.
- 20261015-0250-scout-760f (silver): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; knots 672 B/body (13.7% of the plateau) — eviction 1.16x, the wall is the record stack; 10^9 lives in programs.
- 20261015-0724-components-e0f9 (silver): the seam rebuilt, committed and re-flown — five arms digest-identical, 10⁵ = the scout's anchor with 273,200 demotions, standing 1,603→930 B/body, rss −28%; the machinery free, the no-retention re-mints the whole bill.
- 20261015-1338-quant-1d52 (silver): the retention rule built and priced — promotions = demotions exactly (85-90% hits, wall +6.5-12.5% over shipped, digests identical, the record's anchors reproduced); global retention erases the memory win, the redundancy is N-independent — adopt bounded, not global.
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (gold): the bounded cache built and flown — digests identical on 23 flights, retained <= cap by construction, 962 B/body kept, promotions at the kick floor at sufficient cap, ~0.15 cores re-mint at 10⁹; the cap curve is the law's read pattern.
- 20261015-1450-taleb-b0ed (silver): the bounded cache built and priced — digest-identical, ratio flat in N at matched cuts, the deep-cut bill is history depth, not N.
- 20261015-1615-quant-0619 (gold): the burn knee is the demotion count, not a working set — WS = demotions integer-exact at four N; price law exact; fixed cap degrades with N; ring pins zombies over global; no bounded cap ships burn at 10⁹ — price the re-mints or delete the reads.
- 20261015-1615-second-20261015-1450-taleb-b0ed-f55d (silver): the burn knee measured — 1.31xN exactly at 10^5 and 2x10^5, mints = apply not the resolver, hits = the scan, kick-anchored admission refuted; identity 26/26.
- 20261015-1747-inversion-b172 (awaiting grade): the formation falsifier measured — concentration collapses the burn knee from ~1.31×N to ≤ N/24 at cuts under one wave period, same kicks/demotions/digests; the no-cap law is the belt's geometry, not burn's.
- 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (awaiting grade): the checker's named gold experiment flown — demote-passages digest-identical on 18 flights, record 113 B vs 18.8–25.3 kB, bill 5.9×dem, rss 445–979→27–51 MB.
- 20261015-1926-taleb-d6ba (this run, awaiting grade): the seam residue censused on the belt — a wave pulse (711 B/body just after a settle, 8.6 at depth), not a standing class; plunges mint zero; dead hold ~1 arc/death; the record stack is the depth term.
- 20261015-2041-inversion-398f (this run, awaiting grade): the history stack's growth law measured per class — the belt flat (1.04 seg/body at every cut, arm-independent), the infalling comet class linear (+0.99 exponent, 46.5->480 by 32k, rss 2.8 GB on 174 bodies); keep-behind = 2*light_distance makes the term causal; single-cut adoption flights are blind to it.
- 20261015-1926-taleb-d6ba (silver): the seam residue censused on the belt — a wave pulse (711 B/body just after a settle, 8.6 at depth), not a standing class; plunges mint zero; dead hold ~1 arc/death; the record stack is the depth term.
- 20261015-2041-second-20261015-1926-taleb-d6ba-57ec (this run, awaiting grade): the comet class is standing — the same 100 passages at 32k and 48k, one arc per live comet (the belt drains at 0.2 kicks/ks; comets stand at 28); ctl is 2.1 GB linear ruin at 32k; the belt floor is 87 kB total, N-constant; record stack 1.0–1.3 TB at 10⁹.
- 20261016-0023-quant-404b (this run): the birth rail split — plan pass 32.5–33.5 µs/body (76–78%
- 20261016-0023-scout-1652 (this run, awaiting grade): the last-segment floor priced against the prune's own keep window — 98.3–98.4% of the belt's standing segments are past it at steady cuts (91.2% in-window just past a wave; keep p50 2,764 s = 9.8% of the interval), but the view's gather serves eras to 27,645 s (≈ the full interval, past every keep): retention's horizon today is the view's partial-step walk, not the light cone; ~10× standing cut (353 GB → ~35 GB inline at 10⁹) sits behind the view's documented outcome-free fallback.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured.
- 20261014-1221-components-0e37 (silver): compiled orbits are write-only memory; the view's ramp is the one reader.
- 20261014-1511-components-a2c1 (silver): the scan seam censused; fixes named in cost order.
- 20261014-1631-library-7f99 (gold): the library mined verbatim; deletion audit 26 kills / 2 landed add-backs.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured; fix named (hold the scan).
- 20261014-1719-dynamics-bf21 (silver): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn with the digest bit-identical.
- 20261014-2248-fermi-b30b (awaiting grade): the steady state through waves measured; memory binds the flyable N at every point.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer.
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (awaiting grade): 25 wave periods flat (700 k game-s, digest-stable), dissolution measured, 4af4's record made to regenerate.
- 20261015-0250-scout-760f (silver): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; 10^9 lives in programs.
- 20261015-0358-taleb-d7bc (awaiting grade): the ruin fenced — byte cap on held scans; the hidden answer bill measured.
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical on 4 arms; standing knots -> 0 MB.
- 20261015-0724-components-e0f9 (silver): the seam rebuilt, committed and re-flown — five arms digest-identical, rss −28%.
- 20261015-1338-quant-1d52 (silver): the retention rule built and priced — promotions = demotions exactly; adopt bounded, not global.
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (gold): the bounded cache built and flown — the cap curve is the law's read pattern.
- 20261015-1450-taleb-b0ed (silver): the bounded cache built and priced — the deep-cut bill is history depth, not N.
- 20261015-1615-quant-0619 (gold): the burn knee is the demotion count, not a working set — no bounded cap ships burn at 10⁹.
- 20261015-1615-second-20261015-1450-taleb-b0ed-f55d (silver): the burn knee measured — 1.31xN exactly; mints = apply not the resolver; kick-anchored admission refuted.
- 20261015-1615-spacex-1343 (silver): the passage tail priced — 96 B/panel, 10.74 panels/octave; re-mint bit-identical.
- 20261015-1747-inversion-b172 (silver): the formation falsifier measured — concentration collapses the burn knee from ~1.31×N to ≤ N/24 at cuts under one wave period; the no-cap law is the belt's geometry, not burn's.
- 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (awaiting grade): demote-passages digest-identical on 18 flights; record 113 B vs 18.8–25.3 kB.
- 20261015-1926-spacex-8b89 (this run): the class list dies — ES_LAZY_ALL demotes every keyed entry; standing arcs → the centres.
- 20261015-1926-taleb-d6ba (silver): the seam residue censused — a wave pulse, not a standing class; plunges mint zero.
- 20261015-2041-inversion-398f (awaiting grade): the history stack's growth law measured per class — the belt flat, the infalling comet class linear.
- 20261015-2041-second-20261015-1926-taleb-d6ba-57ec (awaiting grade): the comet class is standing — the same 100 passages at 32k and 48k; ctl is 2.1 GB linear ruin at 32k.
- 20261016-0023-second-20261015-1747-inversion-b172-f56e (this run): b172's gold step closed — the depth arms landed (29.26 at 48k, 26.07 at 32k, horizon one wave recurrence), the bill scene-invariant at depth (270,979), and the matched-fills control kills the angular reading (fills 616,250 invariant in w and K; 1.013 at full diffusion).
- 20261016-0117-library-cfe5 (this run): the plan pass attributed — secondaries 30% of birth
- 20261016-0117-second-20261016-0023-scout-1652-d86c (silver): the floor deletion flown — digests identical coast and burn (checker: also at 150k and 5x10^4), 16x coast / 3.3x burn standing cut at 60k (decaying to 1.6x at 150k, the in-window residue), view-only cost (refused walks, disc shifts <= 40 m at the flown cuts but past-disc at >= 90k; fleet lights <= 15.5 km; one observer-fallback mode), engine reads untouched.
- 20261016-0117-taleb-51b7 (this run, awaiting grade): the flight into the belt flown on merged main — the quiet belt and the wave mint zero scans (the instrument is cadence-off at belt radii); the burn mints one scan per binding change, 11.3 MB marginal each at 10⁵, p50 29 ms standing, fenced at 1.92 GB in 2.5 s; SCAN_BACKLOG's count cap can never engage (240 GB at 10⁹).
- 20261016-0213-fermi-1a1c (this run, awaiting grade): the assembled 10⁹ budget on merged main —
- 20261016-0213-second-20261016-0117-taleb-51b7-e28f (this run, awaiting grade): the cure's first rung flown — candidates shared behind an Arc, mint per candidate-set change (1 snapshot per burn, 971 consecutive changes), the 1.92-GB fence deleted (720 frames at 307 MB), answers bit-identical (5 robust A/B digest equals + 10/10 record ladder_digest rows, 14/14 regen), the 10⁵ answer bill measured 0.39 s/scan.
- 20261016-0213-system-d31c (this run, awaiting grade): one shared planets-at-t readout for both birth read paths — pass 33→22.7 µs/body, digest-identical everywhere; the element read ≤0.4 µs, the ≲13 prediction dead: the pass is arithmetic.
- 20261016-0346-quant-3ec8 (this run, awaiting grade): plan_clock's three own-state reads served by one readout - birth pass -18-22%, rail -14.5%, digests identical; thrusting-kick readout named next.
- 20261016-0346-scout-7da3 (this run, silver [checker]): staggered wave flown four periods budget-free, window-level cure permanent (held at 10⁴ by the checker); the run's letter break 1.7–2.2×10⁶ REFUTED at rtf 100 (crest 342/366, N-flat, a 660-s beat) — corrected break ≈ 6×10⁵, composed 10⁹ ≈ 0.7× at the key arm; wave period 14,167 game-s, decay ×0.72.
- 20261016-0346-second-20261016-0213-system-d31c-79ca (second author): the pass's shared recomputes deleted — one state read (3 calls → 1/body) + per-doll constants (5.3 → 0.03 µs); pass 34 → 11 µs/body (≈3×), digest-identical; the readout lever alone 1.4×, under checker 2's bar.
- 20261016-0346-spacex-917c (this run, awaiting grade): staggered wave flown budget-free at
- 20261016-0504-components-4534 (this run): the locals' storm is the block-step grid, not the begin — BEGIN refuted bit-exactly, the grid-translate flattens 335 -> 141 (2.0-2.4x, both seeds, N-flat), event totals move +6/+73% (undiagnosed), gates unflown.
- 20261016-0504-dynamics-4c22 (silver [checker]): the locals' storm is a standing comb phase-locked to aligned's absolute grid; the belt's one-step cure is absorbed; a permanent per-body phase collapses it 334→53 at +11-20% events (a law change); the run's attribution instrument was 2:1 misaligned (checker-corrected: the storm is ~93% doll-2 boundaries, no pull lane).
- 20261016-0504-second-20261016-0346-spacex-917c-c840 (second author): the checker's gold step flown — B13 armed 0/64 vs off 60/64, all 13 armed digests change; the stagger configuration killed, the cure goes to the birth program.
- 20261016-0504-system-e070 (this run, awaiting grade): the locals isolated on main — 3%
