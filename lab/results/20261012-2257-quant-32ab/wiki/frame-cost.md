topic: frame-cost
status: open
closed-by:
valid-while:
updated: 20261012-2257-quant-32ab

# The frame loop and the kick resolver: cost per body and per kick

## Current best

**The zero-event fixed tier (the hidden tick).** Shipped `Universe::advance` touches every body
every frame whether or not anything is due: an unconditional `rekey` (one deadline recompute plus
one heap set per entity, `universe.rs:493`), then the defer/drain/requeue passes that pop and
re-push every non-due entity (`universe.rs:790`) — three Calendar touches per body per frame,
always, all outside `Budget` (20261010-0656-quant-d540, 20261012-1019-quant-b29b). Measured
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
(20261012-2257-quant-32ab).

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
digest-testable. At plane scale the allocator is at its floor: idiot index 1.01, 0.3–0.4%
deferrable, slack median 0 (20261011-0736-components-825f); the frame's tail is demand, not
scheduling — single player events of 1.3–3.4 ms, 4–28× every other item, monotone in doll
population, via the O(all-bodies) `PlayerNeighbourhood` scan (20261010-2141-constraint-ae40,
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
deterministic); not tested there: other input patterns, the M1.

## Refuted

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

1. **Delete the fixed tier** (unbounded at scale): lazy deadlines — rekey only on player motion;
   serve tick-due-ness by min-peek instead of drain; deadline keys as slack lower bounds rechecked
   on pop (20261010-0656-quant-d540, 20261012-1019-quant-b29b, 20261012-0036-quant-115e). Takes the
   per-frame cost from Θ(N·log N) to O(events); unblocks any doll holding ≥10⁴ ships and decides
   whether the belt may join the root queue as entities (it must not, 20261012-1019-quant-b29b).
   The naive variants so far break cross-schedule digest identity (6766's break: different digests
   and a broken settle contract; 1537's tick-keyed calendar: quiet frame 0.1 µs flat but fleet
   digests move) — the determinism-safe construction is the missing experiment. Supporting
   internals already measured: a monotone bucket wheel on event time (2.1–4.4× cheaper per event,
   4–9× under co-orbital concentration, rare O(n) rebuild stalls,
   20261007-2246-components-4955) and a dyadic wheel plus triangle-inequality skin (7–20× at
   10⁶–3×10⁶, canonical states bit-identical, 20261007-2344-quant-4211). Note: at flight scale this
   deletes ~15 µs/frame — it does not touch the sweep's L8+ stutter
   (20261012-2257-quant-32ab).
2. **Spread or cap the burn-input replan waterfall** (the flight's worst frame): one input mints
   up to 1,036 player items due in the input frame (L15, 48 members; 2.4 s at 400 members);
   resolving them across frames is digest-safe by schedule independence
   (20261012-2257-quant-32ab). Unmeasured: why the replan mints that many items (the thrust word's
   refit against every scheduled kick), and the waterfall's size under other input patterns.
3. **The kick as an addition** (10²–10³× per kick): keep additive integer invariants between kicks
   (`ΔL = x×Δv`, `ΔE = v·Δv + |Δv|²/2`, carries as today); fit the tube once per *read* (plan
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
   graded run (20261008-0615-taleb-40c0, 20261008-0743-second-…-a342).
7. **Replace the player scan** (the frame's p99, and now the flight's per-item cost): the Binet
   cone over `PlayerNeighbourhood`'s exact O(all-bodies) check (20261010-0656-quant-d540,
   20261010-1920-spacex-cb3f, 20261011-0736-components-825f); in the flight regime it prices every
   player item at ~430–500 µs (48 members) to ~1.7–2.9 ms (400 members), of which the pure
   resolve is only ~140–150 µs
   (20261012-2257-quant-32ab).
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
