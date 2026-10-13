topic: frame-cost
status: open
closed-by:
valid-while:
updated: 20261013-0236-second-20261013-0037-system-174d-0f2a

# The frame loop and the kick resolver: cost per body and per kick

## Current best

**The burn-input waterfall is the velocity word's sampling of an exactly-solvable burn, not a replan
storm and not field work — so the burst can be deleted, not spread (20261013-0037-system-174d).**
Decomposed on shipped code (env-gated probe, counters only; demand-mode worst frames reproduce the
published 42/579/1,036 at L8/L12/L15 digit for digit): every burst item is the player's own
Kick(0)+Boundary pair (opens 0, one decide per input; there is no refit of scheduled kicks — quant-32ab's
standing guess for the mechanism is wrong); the chain's step is the law's thrust step
`2^⌊log2(β·2⁻⁶/α)⌋` (α = 2^(thrust_log2+level), thrust_log2 = −44; 2,283/2,293 kicks match exactly, the
rest are `aligned()`/MIN_STEP remainders) — one rebind per 1/64 of |v|; and each event's gravity content
is tide/burn = 2.6×10⁻¹²…1.3×10⁻⁹ (median 2.8×10⁻¹¹) over all 2,293 burst kicks (demand, seed 1; at
seed 7 the L8 max reaches 7.6×10⁻⁹ — 10⁸–10¹⁰ across seeds, checker), all 906 L15-demand
kicks below 2⁻³⁰. The counterfactual, completed at the law's own regime-scaled cadence
(`step_for` before the thrust clamp, recorded per kick by the second author's probe): the tide
behind a held burn costs **~0–24 events where the burst costs 377–1,085 kicks (45–377×)** — L8 6,
L12 23, L15 24, brake 5, turn-then-burn 1 (paced 8 s, seeds 1 and 7 agreeing to 3 digits; demand 4 s
within 3×) — set by the dive the burn produces, not by the throttle level (20261013-0236-second-20261013-0037-system-174d-0f2a).
Checker2: duration co-sets it away from the dive — at 16 s L8 grows 6→24 and brake 5→19 while L12/L15
stay 23/24 (reverse L15: 2,219 kicks → 23 events, 96×; seed 3 and rtf 20 agree, L15 = 24
pace-invariant) — the 0–24 envelope holds through the next decade of flight duration.
The fixed-granularity carry (the coast's 4.98×10⁸ quanta/event applied to the plunge) mints 31,286 at
paced L15 8 s — an artifact of the fixed divisor, not of the lever: on the dive (r → 9.4×10⁷, β →
0.231) the burned conic becomes an escape passage, the law's cadence **coarsens** to ~2³² ticks, and
the 149 deep kicks carrying 100% of the tide sum (1.56×10¹³ quanta) contribute 0.02 of the 24 law
events. The per-event tide budget the law itself scales through the dive: ~1.25×10⁸ at coast radii,
up to ~1.5×10¹³ per window at the plunge (20261013-0236-second-20261013-0037-system-174d-0f2a); the honest tide/burn range is median 10⁻¹⁰…10⁻¹²
with a plunge tail to 1.5×10⁻⁴.
The lever for the sweep's fix: carry the held burn in the tube's generator (the representation already
holds all three pieces — `rec.b.kick`'s ramp for readers, `thrust::owed` exact in rapidity, `rec.carry`
for the tide), with events only when the tide's carry crosses its quantum or the keys change; spreading
the waterfall (HANDOFF item 3's shape) buys smoothness while paying the same empty work. The exception the first run named (the
plunge-adjacent strong-tide kicks) is where the law's own cadence is coarsest, not finest — the
field does not want the burn's fine sampling there (20261013-0236-second-20261013-0037-system-174d-0f2a).**

**The fixed tier is deleted outside sustained starvation; inside it the fleet cap breaks canon
(checker).** The missing experiment of open direction 1 is built: due-ness served from a tick-keyed
calendar (one peek; the drain that set aside every non-due entity is gone), the `rekey` sweep gated
on the player's displacement since the last sweep (`wander ≥ want/64`, so between sweeps every
stored deadline is within `wander` light-ticks of its truth, and the overflow horizon takes that
slack off), and `settle` draining by the same tick-due-ness (20261012-2257-spacex-5eb6). Measured on
the probe's quiet populations (200 frames, rtf 100): median 1.34–1.49 µs **flat in n** from 428 to
2×10⁵ bodies against legacy 16.45 µs → 14.7 ms (~73 ns/body) — 11× at 428, 10,872× at 2×10⁵; the
amortized sweep is the p99 (5.1 ms at 2×10⁵, 2 sweeps in 200 frames); full rekeys on the same
flights drop from 1,719–80,005 to 1–219. Checker-reproduced and extended: flat at 4×10⁵ (22,000×),
a same-tick tie storm, and a player at ~2×10⁻³ c (25× the wander rate: rekeys 2→33, lazy median
4.2 µs) — digests bit-identical across both arms on all 15 schedules and every checker case
**except sustained starvation**: under a 3-event budget at 5×10⁶ rtf (200/200 overflow frames) the
shipped gate `work_per_frame_is_bounded_and_overflow_is_a_dip_not_a_hitch` fails deterministically
on the patched tree and passes on base — the budgeted fleet commits to cut+128 ticks while the
settled fleet stops at the cut, and the run's own `starve` probe prints three digests at one cut
(e7472f50… / 314b1bbc… / 94096d75…). Tick-due order lets the fleet resolve early in the frame and
commit past the presented time; the shipped deadline order was the regulator that prevented it.
The dossier's "the universe suite passes" is wrong: regen.sh runs the clock tests unskipped (17 s on
the checker's machine), and plane.rs fails. The trap's fix in the patch is park-and-retry
(`cap ≤ tick` parks the fleet for the pass; `resolve_fleet` only runs at `cap > tick`), not the
`cap.max(tick + 1)` the dossier names (20261012-2257-spacex-5eb6, checker).

**The fixed tier is deleted outside sustained starvation; the second author's starvation fix holds on the gate's own scene and not beyond it (checker), so it is not yet merge-ready.** Due-ness
is read from a tick-keyed calendar (one peek; the quiet frame never walks a queue), the `rekey`
sweep is gated on the player's displacement (`wander ≥ want/64`; between sweeps every stored
deadline is within `wander` of its truth and the overflow horizon takes that slack off), and the
due work is served in **causal-deadline order** — the shipped regulator, restored
(20261013-0037-second-20261012-2257-spacex-5eb6-8b43, on 20261012-2257-spacex-5eb6). Quiet frames
(200, rtf 100): median 1.35–1.36 µs **flat in n** from 428 to 4×10⁵ bodies against legacy
15.8 µs → 29.6 ms (~73 ns/body) — 11× at 428, 10,872× at 2×10⁵, 22,144× at 4×10⁵; the amortized
sweep is the p99; rekeys 2 in 200 quiet frames (1,719–80,005 shipped). Sustained starvation
(3-event budget, rtf 5×10⁶, 200/200 overflow): at the gate's own scene (seed 11, threads 1) the
shipped plane gate **passes** and the starve probe prints **one digest for budgeted-then-settled,
stepped-settle and freshly-settled**, with the budgeted fleet's committed tick exactly at the cut.
**Checker: the closure is scene-specific, not general** — on seeds 2, 5 and 9 and at threads 4,
budgeted ≠ settled (equal kicks, encounters and contacts, +26–161 events in battle slices, digest
moved) where the shipped loop holds every one of those cases; at budget 1 and 500 frames seed 11
still holds but stepped ≠ settled returns, so that arm's agreement at seed 11 is an accident of
the case, not a property (predictions.md expected the difference). The starvation break's
mechanism, measured: tick-due order let the player's item resolve early (its pull committed the
fleet megaticks past a pinned presented time) and each fleet cap commit landed `slack − dist` past
the horizon, exactly (fleet 54,525,951 = cut + 128 with dist 4,160 < slack 4,288). The fix is
three pieces: the deadline-ordered due pass (it restores the shipped regulator; the fleet still
commits past the pinned presented time in 6 of 200 frames — its chunk boundary above a horizon
clamped by other deadlines, a work-ahead dip of ≤ 4.8% that the gate tolerates), the fleet's cap
minus the same staleness slack the horizon subtracts with a park for a
fleet within `slack` light-ticks of the player (its own requeued deadline cannot justify its
commit under the blanket −slack), and a rekey at the player's pull and at a park-induced stall
(the pull is canonical and must commit, so it commits against fresh deadlines; without the stall
rekey the frame presents nothing forever — found as a hang in the view suite's replay test).
Digests bit-identical across both arms on all 15 fly schedules, the tie storm (3,002 events), the
fastest bindable player (~2×10⁻³ c) and the replay schedule; the universe suite 58/58 (2 ignored
clock flights). Residue named: in deadline order a body's `event_time` may exceed the cut by
≤ slack + 1 in principle; measured zero here (the gate's digests agree bit-exactly), unbounded
nowhere — the next builder bounds it or the merge review does.

**The zero-event fixed tier (the hidden tick), as shipped.** Shipped `Universe::advance` touches
every body every frame whether or not anything is due: an unconditional `rekey` (one deadline
recompute plus one heap set per entity, `universe.rs:493`), then the defer/drain/requeue passes
that pop and re-push every non-due entity (`universe.rs:790`) — three Calendar touches per body per
frame, always, all outside `Budget` (20261010-0656-quant-d540, 20261012-1019-quant-b29b). Measured
slopes, by population and cache regime: ~29 ns/body (rekey only, 428 bodies,
20261011-1917-second-…-762d-119f), 43–60 ns/body (rekey, 4×10³–2.6×10⁵, linear with a growing
coefficient, 20261012-0036-quant-115e), 0.25 µs/entity cache-resident rising to ~1.1 µs at 1.2×10⁵
where the pass streams the 448-byte `BodyRec`s three times (20261012-1019-quant-b29b), 0.43 µs/body
defer-slope with quiet haulers (20261010-0656-spacex-2439), ~0.7 µs/body for belt tubes
(20261010-0656-quant-d540). Consequences, measured with zero events resolved: the 16.7 ms frame
breaks at ≈1.5–6×10⁴ root entities (20261012-1019-quant-b29b; ≈3×10⁴ tubes,
20261010-0656-quant-d540); at 10⁶ bodies the frame costs 0.06–0.8 s (rekey-only extrapolation
60–75 ms, 20261012-0036-quant-115e; 721 ms measured on belt tubes, 20261010-0656-quant-d540). The
tier is serial — 8 threads leave the empty frame unchanged (20261012-1019-quant-b29b) — and no
body class escapes it: a root-doll control of "inert" haulers pays the same, because the planets
are root-doll sources so every ship is a planned, queued body (20261012-0036-quant-115e). In an
unlimited settle the pass runs only twice; it bites exactly in the session's per-presented-frame
`frame_to` (20261012-0036-quant-115e). The digest itself is Θ(N) (341 ms at 1.2×10⁵): keep it per
settle, never per frame (20261012-1019-quant-b29b). At plane scale (≈428 bodies) the tier is still
small — 15 µs/frame, 99% rekey (20261011-1917-second-…-762d-119f) — so it is a scale wall, not a
today wall.

**The flight regime (the sweep's L8+ stutter): the burn-input replan waterfall, not the fixed
tier.** On shipped code (clock fix in), the sweep's flights paced at the page's 12 ms budget jump
from 0.038 s worst lag (L0–L6) to 1.43–1.66 s with 22–55 capped frames at L8–L15, and demand mode
(unlimited budget) attributes it: player items are 79–91% of the flight's CPU (rising with level;
checker-corrected from 87–91), the Stats remainder
(the fixed tier at 48 members) is ≈0, and the worst frame is the frame the burn input lands
(wall second 1.0, within 3% from L10 up; at L8 within 7%) — a replan waterfall of 42 (L8) → 166 (L10) → 579 (L12) → 1,036 (L15)
player items in that one frame, deterministic in count, decaying over 2–4 frames, while the whole
flight's median frame stays 39–125 µs. The pure resolve (`step::process` on the player's record)
is ~29 µs at coast and ~140–150 µs under burn once past the first post-burn seconds (up to
~390 µs inside them), flat in speed from 0.12c to 0.55c — the jet-era
compile is not the flight's problem either; the item totals ~430–500 µs at 48 members and
~1.7–2.9 ms at 400 members, the difference being the O(all-bodies)
scan riding player items plus apply/requeue (the pure resolve is population-flat: ~143 µs at 400
members too, checker), so the same waterfall costs 2.4 s in one frame at 400 members. The
per-frame burst concentration scales with rtf (53 items at rtf 1, where the worst frame stays
under 12 ms, to 1,036 at the sweep's rtf 100 — checker); the stutter binds at and above the
sweep's flying pace. Even the coast control is
not sub-millisecond: the 48-member idle plane has p99 ≈ 1.3 ms and worst ≈ 13 ms frames. Gate F1's
"no frame over 12 ms **after the first second**" excludes the worst burst frame itself (the
sweep's burns start at wall second 1.0; the decay tail, 50–60 ms in demand, is past it), so that
clause can pass while the burn frames hitch — though F1's zero-lag clause still catches the
stutter. Spreading the
waterfall across frames is digest-safe by the schedule-independence gold (20261007-1234-system-2517)
(20261012-2257-quant-32ab; the waterfall's mechanism and content are now measured — see the
waterfall block above).
**The deadline heuristic is schedule-only, proven by divergence (20261012-2257-scout-64e4).** Three
genuinely divergent rekey policies — shipped every-advance, never (frozen observer and deadlines),
lazy-on-player-motion — end every probe with a bit-identical canonical digest (seeds 1/3, 48/400
members, 8/60 game-s, starved to one resolved item per frame so the calendar alone picks the
order): the per-frame queue-front fingerprints, frame counts and event streams differ (3637/3634/
3636 frames at 60 s), the digests match exactly (`e38b245b…`/`35812c30…`/`2dbc92e4…` ×3), kicks
and encounters counted equal. The only channel demonstrated to break digests on the shipped engine
core is the session's key logging at the presented tick: reproduced on the shipped API
(`input(u.now,…)`,
three digests across 30/60/144 Hz, encounters 39/37/38), and the two-line fix shape validated
(decision tick derived from the wall timeline, snapped up to a 2²⁰-tick grid via `schedule`: one
digest per seed across all rates; two flips inside one cell both land, in order — checker).
Quantizing the presented tick itself does *not* fix it (adjacent pacings straddle cell boundaries:
raw ticks 19912096/20250432 fall either side of 19×2²⁰). A second, structural channel exists
outside this run's deadline-value domain: 1537's tick-keyed calendar broke via the fleet commit cap
and `pull`'s stale slots (its own diagnosis, no player keys involved). The rekey walk alone is
10–34% of the quiet frame (188.6→152.7 µs at 1,001 bodies; 2.30→2.07 ms at 10,001; plane
16.7→11.1 µs) — drain/requeue own the rest. Checker domain extension: identity holds at 1,600
members (1,642 kicks, 662 encounters, seed 7), under 64-decision scripts, and at threads 4.

**The kick.** The shipped kick resolver costs a median 75.6 µs (made 34–38, leavers 92–102, p99.9
11× the median, boundaries only 3.5×) against a measured information floor of 42–56 ns per kick
(2.2 ns memory-only streamed, 139–161 ns in causal random order) — an idiot index of ~1,400–1,800×
(20261011-1729-components-b063). The cost is the bookkeeping, not the physics: rebind/refit is
70.7–89% (20261012-0036-quant-115e; 20261011-1729-components-b063), `bind()` alone is 63.5–64.4 µs
≈ 84% of a kick (20261011-1729-components-b063, checker), force arithmetic 1–2.7%
(20261012-0036-quant-115e; 20261008-0234-quant-2300), and the wall inside it is `Orbit::compile`'s
certified quadrature (compile/bind 0.85–0.90 on fresh seeds; front-half micro-optimization caps at
≈1.2×, 20261009-2043-autoresearch-d4f1; 60–66% remains after the cheap deletions,
20261007-1646-autoresearch-a191). Every distinct kick re-fits a fresh exact cycle — 1,125 of 1,158
(20261011-1729-components-b063), 1,125/1,125 on the integer resolver (20261011-2306-system-3367),
0 of 203,017 on the belt at both 2⁷ and Saturn 2⁻¹² cadence (20261010-1544-system-97ce) — so the
exact memo hits 0%; the 12+12-bit quantized memo hits 94–97% but changes orbits (a law change, 5
October correction; 20261011-1729-components-b063, 20261011-2306-system-3367). Bit-identical
micro-deletions exist and are real but small: −9.5% made (20261006-1135-autoresearch-eb29), −16–21%
made / −6–11.5% leavers (20261007-1646-autoresearch-a191; scope-free rebuild in
20261007-1801-second-…-18df), −9–10% via a `proper_at_event` cache (20261010-1947-autoresearch-2833),
−36% on the ship class in ~14 lines (20261010-1302-spacex-6785; its Dense baseline row is
unregenerable, disclosed). Related event prices: changeover levels cost ~11× a plain kick (371.8 vs
34.0 µs), player items 151 µs vs ship 36 (the encounter search rides them), `apply` after every
event is 6.9 µs of which 97% is `root_state` (20261012-0036-quant-115e); the belt's event stream at
10⁹ is ≈3.4% of one core, so the record format, not the kick stream, is the belt's risk
(20261010-1544-system-97ce).

**The frame loop as allocator, and its contract.** The engine core is schedule-independent — one
digest per canonical cut across budgets, threads, pace, checkpoints, observation and starvation
(9 adversarial paths × 3 seeds, 20261008-0615-taleb-40c0; 12 runs through 100% overflow,
20261007-1234-system-2517) — so scheduler changes that alter only *when* work happens are
digest-testable (the lazy tier is the strongest instance: tick order instead of deadline order,
digests unchanged, 20261012-2257-spacex-5eb6). At plane scale the allocator is at its floor: idiot
index 1.01, 0.3–0.4% deferrable, slack median 0 (20261011-0736-components-825f); the frame's tail
is demand, not scheduling — single player events of 1.3–3.4 ms, 4–28× every other item, monotone in
doll population, via the O(all-bodies) `PlayerNeighbourhood` scan (20261010-2141-constraint-ae40,
20261006-1354-constraint-df79, 20261011-0736-components-825f), linear at ~1.6–3 µs/body and alone
breaking 16.7 ms at ≈8×10³ bodies (20261010-0656-quant-d540; 33 ns/body/item,
20261010-1920-spacex-cb3f); at the 400-member clamp one player item took 68% of the frame budget
(20261006-1354-constraint-df79). Under sustained overload the global horizon collapses presented
time ~600× (a cliff, not a dip: RTF 309→0.03) while events/s stay budget-proportional
(20261007-1234-system-2517); the silent freeze has no per-frame prologue floor — delivered equals
throughput ÷ event density, and the 400-member opening needs 293× the budget, so the allocator must
shed target rtf on density, not audit prologues (20261011-1917-second-…-762d-119f). One player
order wakes a bounded transient: ~2,000 extra events, 94–116 budget-saturating frames, RTF floor
0.23× (20261008-1252-quant-291f). Threads hurt at this scale: the wave (threads > 1) pessimizes
1.5–2.7× (20261007-1234-system-2517) and 4 threads worsened overflow 301→507
(20261006-1354-constraint-df79). One live contract hole: the interactive loop logs the player's key
changes at the frame's *presented* tick (`session.rs`, `step`), so frame rate and load rewrite
canonical history — encounters 68–102, contacts 0–14, four digests per seed
(20261008-0615-taleb-40c0); the quantized-decision-tick fix was built and held on the second
author's branch (one digest per seed across play60/30/144/starve at rtf 100 and 1, plus a 12 s
regression test, 20261008-0743-second-…-a342) but that run is ungraded (no check.md) and the fix is
not on main (verified: `session.rs` still logs at the presented tick, 12 October).

**Domain.** All numbers are from shipped code on shared Linux/x86 runners (i7-4790-class),
single-system plane scenes and synthetic tube populations (Home orbiters, haulers, Hill-orbit
fleets, belt tubes) up to ~2.6×10⁵ bodies, rtf 1–10⁴, orders of magnitude only. Not tested: the M1,
10⁹ bodies, region scale, fleets beyond 25,600 members, and the memory ceiling of fleet members
(~150–330 KB/member resident; 8 GB caps ≈5×10⁴ members, 20261009-2043-quant-3cfc — plain tubes are
1.9 KB each, 20261010-0656-quant-d540). Any capacity claim about `--members` above 400 must lift
the xtask clamp first: unpatched `--members 1024` silently returns the 400-member digest
(20261010-1920-quant-9464, 20261011-1729-second-…-07b8). The median *delivered* frame is
view-bound, not engine-bound (gather 54–86% of frame CPU, engine ≤ 5–24%) — that half belongs to
the `view` page (e.g. 20261011-0324-constraint-986f, 20261012-1227-constraint-cf31). The flight
regime (20261012-2257-quant-32ab) adds: one seed, one scene, forward holds, members 48 and 400;
the burst frame's wall cost moved 0.38 s → 2.4 s across processes on the shared box (item counts
deterministic); not tested there: other input patterns, the M1. The lazy
tier's digest identity is tested on plane scenes and quiet tubes to 4×10⁵ (checker), a tie storm
and a 25×-wander player; under sustained starvation (3-event budgets, 200/200 overflow) it holds
at seed 11 threads 1 and fails on seeds 2/5/9 and threads 4 (checker,
20261013-0037-second-…-8b43); not tested: checkpoints, the M1. The waterfall decomposition
(20261013-0037-system-174d, 20261013-0236-second-20261013-0037-system-174d-0f2a) covers seeds 1, 3 and 7, one scene, 48 members,
forward/brake/turn patterns at levels 8–15, flights 2–8 s (16 s, rtf 20 and a reverse-L15 brake,
checker2) including the plunge approach (r to
9.4×10⁷, β 0.231) and demand mode; not tested: 400 members (the scan rider is priced elsewhere),
other scenes, the M1.

## Refuted

- The thrust word's refit against every scheduled kick as the waterfall's mechanism — no such refit
  exists: `decide` clears the plan and plans one kick; the burst is the player's own burn-cadence
  chain of Kick(0)+Boundary pairs (20261013-0037-system-174d, correcting 20261012-2257-quant-32ab's
  stated guess).
- "The burst's events carry the field" — tide/burn median 10⁻¹⁰…10⁻¹² with a plunge tail to
  1.5×10⁻⁴ over all measured burst kicks (both seeds, both modes); at the law's own cadence the
  counterfactual tide-carry mints ~0–24 events for the same flights at every level, and the
  fixed-granularity inversion at paced L15 (~2.6–3.1×10⁴ events) is the fixed divisor's artifact
  (20261013-0037-system-174d; completed and re-priced by 20261013-0236-second-20261013-0037-system-174d-0f2a).
- The deadline order as load-bearing for canon, outside starvation — tick order with (tick, id)
  ties gives byte-identical digests across 15 schedules, both arms and the checker's tie storm; the
  order is a schedule (20261012-2257-spacex-5eb6, confirming 20261008-0615-taleb-40c0 at the
  frame-loop level). **Under a starving budget the deadline order IS load-bearing for the fleet**
  (it caps the battle's committed tick at the presented time); tick order lets the fleet commit
  past it, and the plane gate fails (checker) — fixed by restoring that order for the due pass
  (20261013-0037-second-20261012-2257-spacex-5eb6-8b43).
- Tightening the fleet cap below the fleet's own next tick (staleness slack on the cap) — deadlocks
  `run_to` at `to == tick`: the fleet is due every tick, and only the second-in-line's resolution
  raises the cap; the patch's answer is to park the fleet for the pass and retry at the next
  advance (20261012-2257-spacex-5eb6; the dossier's `cap.max(tick + 1)` names a superseded draft).
  **Superseded:** the slack on the cap stands once the park also covers proximity (`dist < slack`)
  and a parked fleet that is the only due work forces a rekey — no deadlock, gate passes
  (20261013-0037-second-20261012-2257-spacex-5eb6-8b43).
- A fixed per-frame prologue floor (0.2–1 ms) as the freeze mechanism — directly measured at
  15 µs/frame at 428 bodies, no knee in events-per-budget (20261011-1917-second-…-762d-119f).
- "Delivers 0.00×" under stall — a median-frame artifact; the stalled run delivers 28.8× unpaced
  as a 39-frame stutter (20261011-1917-second-…-762d-119f).
- The rekey walk alone owning the per-frame slope — deleting it changed nothing at 6,203 haulers
  (20261010-0656-spacex-2439); the tier is rekey + drain + defer/requeue together
  (20261012-1019-quant-b29b, 20261010-0656-quant-d540).
- The fixed tier (or lazy re-keying) as the fix for the flight sweep's L8+ stutter — at 48 members
  the tier is ≈0% of the flight's CPU; the stutter is the burn-input player-item waterfall plus the
  per-item scan (20261012-2257-quant-32ab).
- Per-item player cost growing with speed/γ in the flight regime — flat at 75–80 µs from 0.12c to
  0.55c; the frame is item-count, not item-cost (20261012-2257-quant-32ab).
- Kick memoization — exact hit 0% everywhere measured (1,125 distinct shapes in 1,158 kicks; 0 of
  203,017 on the belt); the quantized key hits 94–97% but changes orbits (20261011-1729-components-b063,
  20261010-1544-system-97ce, 20261011-2306-system-3367; 5 October correction).
- A least-slack/QoS scheduler as the next build — the frame loop already is the allocator at plane
  scale (20261007-1234-system-2517) and sits at its floor (20261011-0736-components-825f).
- "Scene saturates at 428 bodies" — an xtask `--members` clamp at 400, not physics; 4,331 bodies at
  15 s with the clamp lifted (20261010-1920-quant-9464, 20261011-1729-second-…-07b8).
- A source-state memo on the settle — deletes <5% and is 8% slower at 10¹¹ ticks
  (20261010-1920-spacex-cb3f).
- The kick as memory-bound or clone-bound — record clone is 0.14% of a kick and the median is flat
  as the store passes L3 (20261011-1102-quant-ba35).

## Open directions

1. **Close the starvation hole for real, then merge the deleted tier**: the second author's fix
   (deadline-ordered due pass, slack on the cap with a proximity park, rekey at the pull and at a
   park-induced stall) passes the plane gate, `starve` prints one digest across three arms and the
   suite is 58/58 — at seed 11, threads 1 only. The checker broke it on seeds 2/5/9 and threads 4
   (budgeted ≠ settled with equal kicks: the battle's stop-point history leaks into the digest)
   where the shipped loop holds; find the stop-point invariant that makes budgeted == settled
   scene-independent before adopting the patch — do not merge as-is. When it holds: delete the
   `ES_EAGER` legacy arm and `debug_queues`, re-run the behave suite on the M1, and bound the named
   residue (a body's `event_time` may exceed a cut by ≤ slack + 1 in principle; measured zero). The
   merge cost to know: with-work frames now pay the shipped deadline walk (the
   quiet frame still peeks once), and fleet scenarios pay a sweep per stale pull.
   What remains after it: the amortized sweep is still Θ(N) when it fires (p99 5.1 ms at 2×10⁵) —
   the bucket wheel (2.1–4.4×/event, 20261007-2246-components-4955) and the dyadic wheel + skin
   (7–20× at 10⁶–3×10⁶, 20261007-2344-quant-4211) are the measured next rungs for it. Unblocks any
   doll holding ≥10⁴ ships and decides whether the belt may join the root queue as entities (it
   must not, 20261012-1019-quant-b29b).
2. **Carry the burn in the tube's generator, deleting the waterfall (not spreading it)** — the
   pricing is now complete at every level: the tide behind a held burn costs ~0–24 law-cadence
   events against 377–1,085 burst kicks (45–377×; paced 8 s, both seeds, demand within 3×), with
   the plunge's whole tide riding ~zero of the law's own events (20261013-0236-second-20261013-0037-system-174d-0f2a). The burst is 10¹⁰–10¹²
   parts burn to one part tide at the median (20261013-0037-system-174d), the burn is exact in
   rapidity (`thrust::owed`), the binding already holds a kick ramp for readers (`rec.b.kick`), and
   the law already carries sub-quantum tide dv (`rec.carry`) — so a held burn can ride the tube as
   an unending ramp with events only when the tide's carry crosses its quantum or the keys change.
   This is the kick-jet retirement applied to the one influence that is exactly solvable. What
   adoption must still answer: the word-margin the thrust step protects must survive at readout,
   and the near-periapsis tide window (up to ~10¹³ quanta of tide in one law event — the shipped
   law's own operating point for a coasting body on the same escape conic) must be bounded against
   the B-series gates; the read side (a ramp read every frame per viewer) is direction 3's standing
   counterweight. Spreading the waterfall across frames (digest-safe,
   20261012-2257-quant-32ab) remains the scheduling-only fallback; it pays the same empty work.
3. **The kick as an addition**   (`ΔL = x×Δv`, `ΔE = v·Δv + |Δv|²/2`, carries as today); fit the tube once per *read* (plan
   tick, certificate, view gather) instead of once per kick — reads are per frame per visible
   body, kicks are 128 per radial period, and the fit stays exact so digests survive where the
   memo could not (20261011-1729-components-b063). Unmeasured: scenes where reads outnumber kicks
   (a watched fleet at rtf 1) — the read side's cost at scale is the named counterweight
   (20261011-1729-components-b063, lens). Cadence is a separate, priced door: halving kicks halves
   work (exponent ≈1) at ≈4× B13 error per halving (20261007-1801-second-…-18df).
4. **Per-region staleness rung** (survive sustained overload): horizon from the player's own chain;
   a lagging region's sky goes stale, the player never waits — kills the ~600× presented-time
   cliff (20261007-1234-system-2517). Must be shown to move no digest.
5. **A density/throughput gate** (end the silent freeze): shed target rtf when local density ×
   target exceeds the budget's sustainable events/s; dashboard arithmetic only
   (20261011-1917-second-…-762d-119f).
6. **Land the decision-tick quantization** (close the canon leak): two lines in
   `session.rs`/`kick_bench.rs`, already built and held on an ungraded branch — bring it through a
     graded run (20261008-0615-taleb-40c0, 20261008-0743-second-…-a342; the leak reproduced and the
   wall-grid fix shape validated on the shipped API by 20261012-2257-scout-64e4 — quantizing the
   presented tick does not fix it).
7. **Replace the player scan** (the frame's p99, and the flight's per-item cost): the Binet
   cone over `PlayerNeighbourhood`'s exact O(all-bodies) check (20261010-0656-quant-d540,
   20261010-1920-spacex-cb3f, 20261011-0736-components-825f); in the flight regime it prices every
   player item at ~430–500 µs (48 members) to ~1.7–2.9 ms (400 members), of which the pure
   resolve is only ~140–150 µs (20261012-2257-quant-32ab).
8. **Hand-out cost at fleet scale**: 443 µs per hand-out, 12× a kick, plus deadline pinning
   (20261011-1102-quant-ba35).

## Contradictions

- **The fleet exodus: one slice or many? — resolved into a regime boundary by this run's
  probe.** One indivisible `Fleet::advance` item of 630–742 ms (`slices: 1`) at 3,200–25,600
  members (20261009-2043-quant-3cfc) versus, at 400–4,000 members, one 20 ms slice plus 2,091
  hand-out events of 443 µs already split across frames by the 5 ms budget
  (20261011-1102-quant-ba35). Probe on shipped code (the one-line `--members` clamp lift; seed 1,
  rtf 100, 10 s, paced 60 Hz): the delivered frame's worst hitch is 39/100/98/146 ms at
  1,600/3,200/4,000/6,400 members — no ≥0.6 s stall anywhere in ba35's domain (paced timing
  inflates hitches, so the absence is robust), so the budget does split the fleet's work there;
  3cfc's ≥0.6 s form, if real, binds only at ≳12,800 members, which the probe did not reach
  (20261012-1621-q-wiki-frame-cost-ae6a).
- **Rekey's share of the fixed tier.** Deleting the rekey walk changed nothing at 6,203 haulers
  (20261010-0656-spacex-2439), yet at 4×10³–2.6×10⁵ Home orbiters the rekey pass equals the whole
  empty frame within ±0.3% (20261012-0036-quant-115e), and 215 µs at 10³ rising superlinearly to
  37 ms at 6.4×10⁴ (20261012-0616-system-1537) against linear-with-growing-coefficient to 2.5×10⁵
  (20261012-0036-quant-115e, 20261012-1019-quant-b29b). Body class and cache regime plausibly
  explain the spread; nothing measured the same population both ways.

## Runs
- 20261006-1135-autoresearch-eb29 (silver): deleting `bind_in`'s residual decode is bit-identical; made kick −9.5%.
- 20261006-1354-constraint-df79 (silver): the spike is the player's O(doll) encounter scan (one item 68% of frame); 4 threads worsen overflow.
- 20261007-1234-system-2517 (gold): the frame loop already is the allocator (digest invariant through 100% overflow); sustained overload collapses presented time ~600×.
- 20261007-1646-autoresearch-a191 (silver): two redundant tube decodes per kick deleted: bit-identical, made −16–21%; `Orbit::compile` remains the wall.
- 20261007-1801-second-20261007-1646-autoresearch-a191-18df (silver): scope-free rebuild regenerates the record; cadence priced (work exponent ≈1, B13 error ×4 per halving).
- 20261007-2246-components-4955 (silver): shipped 4-ary heap 4–8× off its workload's floor; monotone bucket wheel 2.1–4.4× cheaper per event.
- 20261007-2344-quant-4211 (silver): deadline calendar O(N)/frame (rekey-all, drain, requeue); dyadic wheel plus deadline skin 7–20× at 10⁶.
- 20261008-0234-quant-2300 (silver): kick resolver O(1) in universe size, ~90 µs/kick; 79–88% Kepler tube refit, 1–2% force.
- 20261008-0615-taleb-40c0 (gold): engine core schedule-independent (one digest, nine paths); the loop logs keys at the presented tick, so frame rate rewrites canon.
- 20261008-0743-second-20261008-0615-taleb-40c0-a342 (missing): decision-tick quantization built and held (one digest per seed across rates and load); ungraded, not on main.
- 20261008-1252-quant-291f (silver): one held player order wakes ~2,000 events and 94–116 saturating frames; digest fixed at the cut.
- 20261009-0709-quant-6766 (silver): three O(N) schedule passes at zero events (drain 5.8× over break); the naive break breaks digest identity.
- 20261009-2043-autoresearch-d4f1 (silver): `Orbit::compile` is the kick's cost (compile/bind 0.85–0.90); front-half micro-optimization caps at 1.2×.
- 20261009-2043-quant-3cfc (silver): smoothness breaks at ~1,600 members (one exodus item 0.6–1.5 s); 8 GB caps ≈5×10⁴ members.
- 20261010-0656-quant-d540 (gold): frame Ω(N) at zero events (~0.7 µs/body, three Calendar touches); breaks 16.7 ms at ≈3×10⁴ tubes; player find 1.6–3 µs/body.
- 20261010-0656-spacex-2439 (gold): hidden tick: 0.43 µs × N per frame, walked/frame = N; the rekey walk acquitted; digest neutral.
- 20261010-1302-spacex-6785 (silver): ship class −36% (32.0→20.4 µs/item, ~14 lines); rebind 11.3 µs the next lever; Dense baseline defect.
- 20261010-1544-system-97ce (silver): belt path: every kick rebinds and rekeys (0/203,017 memo hits); bind 43.7% of wall; re-anchor buys 1.7×.
- 20261010-1920-spacex-cb3f (silver): per-event ~50 µs vs ~3.6 µs physics; the player scan is 30–36% of settle (33 ns/body/item); memo no.
- 20261010-1947-autoresearch-2833 (silver): `proper_at_event` cache plus cartesian-free `orbit_state`: kick −9–10%, bit-identical, +18 bytes/body.
- 20261010-2141-constraint-ae40 (silver): p99 frame = single player events 1.3–3.4 ms (O(all-bodies) scan, monotone in members); median frame is view-bound.
- 20261011-0736-components-825f (silver): allocator at its floor (idiot index 1.01, 0.3–0.4% deferrable); the demand tail is the `PlayerNeighbourhood` scan.
- 20261011-0836-autoresearch-469c (lead): kick attribution (rebind 87.2%, quadrature ~61%) reproduces; the kept change breaks digests, killed.
- 20261011-1102-quant-ba35 (silver): kick path compute-bound and flat; the 0.95 s "slice" is 2,091 hand-out events of 443 µs, already split.
- 20261011-1729-components-b063 (gold): kick 75.6 µs vs 42–56 ns floor (~1,800×); the refit is 84–89%; exact memo 0%.
- 20261011-1917-second-20261011-1814-taleb-762d-119f (gold): no per-frame prologue floor (15 µs at 428 bodies); freeze = throughput ÷ density (opening needs 293× budget).
- 20261011-2306-system-3367 (silver): every distinct kick re-fits a fresh exact cycle (1125/1125); motion-law v2 player events 0.5–1.0 ms.
- 20261012-0036-quant-115e (gold): rekey tax 43–60 ns/body, linear to 2.6×10⁵ at zero events, no class escapes; kick 70.7% rebind, 11× tail.
- 20261012-0616-system-1537 (silver): hidden O(N) rekey tick (215 µs at 10³ → 37 ms at 6.4×10⁴); the naive tick-keyed calendar breaks digest identity.
- 20261012-1019-quant-b29b (gold): unbudgeted Θ(N) fixed tier (rekey + drain): 38% of frame at 12k, 8× over at 120k; ceiling ≈1.5–6×10⁴ entities.
- 20261012-2257-quant-32ab (this run): the sweep's L8+ stutter is the burn-input player-item waterfall (1,036 items in the input frame at L15) on the O(N) scan, not the fixed tier (≈0% in flight); per-item cost flat in γ.
- 20261012-2257-scout-64e4 (proposed): rekey policy proven schedule-only (divergent schedules, identical digests); the digest break is presented-tick key logging; wall-grid fix holds.
- 20261012-2257-spacex-5eb6 (silver): the lazy deletion built — quiet frame O(1) (1.35 µs flat to 2×10⁵, 10,872×; 4×10⁵, tie-storm and 25×-wander cases hold, checker), digests identical across arms and 15 schedules; sustained starvation breaks the fleet cap (the shipped plane gate fails) — one experiment from merge.
- 20261013-0037-second-20261012-2257-spacex-5eb6-8b43 (silver): the seed-11 starvation fix — deadline-ordered due pass, slack on the cap, proximity park, pull/stall rekey; gate passes, one digest in three arms, quiet flat to 4×10⁵, suite 58/58; checker: breaks on seeds 2/5/9 and threads 4 where shipped holds.
- 20261012-2257-quant-32ab (silver): the sweep's L8+ stutter is the burn-input player-item waterfall (1,036 items in the input frame at L15) on the O(N) scan, not the fixed tier (≈0% in flight); per-item cost flat in γ.
- 20261012-2257-scout-64e4 (silver): rekey policy proven schedule-only (divergent schedules, identical digests); the digest break is presented-tick key logging; wall-grid fix holds.
- 20261013-0037-system-174d (this run): the waterfall decomposed — all burst items are the player's burn-cadence chain; tide/burn ≤ 1.3×10⁻⁹; delete by carrying the burn, don't spread.
- 20261013-0037-system-174d (silver): the waterfall decomposed — all burst items are the player's burn-cadence chain; tide/burn ≤ 1.3×10⁻⁹; delete by carrying the burn, don't spread.
- 20261013-0236-second-20261013-0037-system-174d-0f2a: the law's own cadence re-prices the tide counterfactual — ~0–24 events against 377–1,085 burst kicks at every level incl. paced L15 8 s; the fixed-granularity inversion was the divisor's artifact; lever adoptable.
