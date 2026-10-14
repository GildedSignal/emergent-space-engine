topic: frame-cost
status: open
closed-by:
valid-while:
updated: 20261014-0727-quant-af8f

# The frame loop and the kick resolver: cost per body and per kick

## Current best
**The crash-tick bisection is now a built, verified lever: threading the retired binding's own
impact tick back as a seed — predicate-verified, bisection as fallback, the passage branch's own
house pattern — cuts the search 38-54% bit-identically on every arm, and the half it cannot touch
is exactly the first-binding (hand-out) half, for which no predecessor exists
(20261014-0727-quant-af8f).** Env-gated probe on shipped code (`ES_IMP_WARM`;
`next_impact_hinted` + `plan_terminal` threading `retired.last().b.impact`; count/timer
counters; battle arms m4000/s3, m1500/s3, held-out m4000/s7 and m1500/s11, flying m400/s3 rtf
100, hand-out m16000/s3, unlimited budget, 8 game-s, digest at the canonical cut): digests
identical off/on at **6/6 arms**. The search is 29.4-29.9 readouts and 107-115 µs as shipped
(3.6-3.9 µs per readout — each `inside(t)` is a full tube readout that rebuilds a cell's panel
quadrature); with the warm seed 13.8-19.0 readouts and 51-70 µs. First-guess hit rate 83-91% on
the battle and 16k arms, every miss within 2⁶ ticks (a kick moves the impact tick by a handful of
ticks); 68% at flying pace with a tail to 2¹³ — still cheap, a miss pays a narrowed bisection.
Wall: flying −17% (the arm where the search is the biggest kick share), battles and 16k −3-6%
(bind-dominated). **The float Kepler model guess is dead in this regime** (0 hits at every arm;
fires on ~2% of searches, misses by 2²⁶ ticks): the members' dips are grazing crossings of
near-circular orbits, where any radius-model error divides by a near-zero radial speed — a seed
must be a tick, not a model. Structure: every fired kick pays two searches (the kick's rebind and
the next boundary's; each rebind resets `Binding.impact`, and the `a == after` memo holds only
within one binding); the unseedable "no hint" half (1,032/2,064 at m4000/s3; 6,874/13,741 at 16k;
227/3,842 at flying) is the hand-out's first binding — orthogonal to the word-fix, composes with
it on the same kick.

### Prior best

**The kick's non-bind half is one bisection, rebought every kick and every dipping hand-out (20261014-0450-quant-1845).** Sub-stage prof counters inside `P_KICK` on shipped code (battle arms m4000/s3, m1500/s3, held-out m4000/s7, rtf 1, 8 game-s; `ES_MEMBERS` clamp lift env-gated; prof-vs-pristine digest bit-identical, m1500/s3 reproduces be78's `7b33d0b866149e71`): the fired kick 254/299/257 µs is **46% bind (117 µs), 45% one `next_impact` bisection (115 µs ≈ 25 readouts × 4.6 µs, bracket half an orbit wide)**, 9% everything else (forces 1.2 µs, ctx 7.6, readout 4.9, quantize+word 0.2, tau pair + three entry clones 7.9 — the clones are 3%, dead as a lever). The search fires on **every** fired kick because `rebind` resets `Binding.impact` (`impact: None`), p…

**Checker (this run): every number reproduced, and the domain extends past every edge the author tested.** Own regen (158 s): identity control passes, m4000/s3 251.8 µs kick = 46% bind + 46% bisection with counts bit-stable across three runs (1032/2064/1034), m1500 digest `7b33d0b866149e71` = be78's. Outside the author's domain: **flying pace** (m400/s3/rtf 100) the bisection is **57%** of a 192 µs kick (K_IMP/kicks 1.01 — every kick, no other callers); **held-out seed 11** (m1500) 47%, digest `5093fe58d892f6bd` = be78's checker2; **16,000 members** (a decade past 4000) the fired kick vanishes entirely (480/480 overflow, all budget to hand-outs) while the same search is **43% of a 302 µs hand-out** (6,865 searches = 97% of hand-outs; digest `4df28df692b3b7bf…

**The adoption queue is measured as one stack and it is worth 2×, not 4.5×: the composed
endgame is refuted, the interlock is confirmed (20261014-0000-second-20261013-2252-system-ad26-790b).**
The three engine-path levers stacked on one binary against shipped f687ec25 (009b's word fix
ported onto the post-plunge `bind_surface` — every engine bind now passes a surface, so the
original patch's path is dead and the port chooses the word pre-compile for keyed fits only;
7055's memo routed inside `from_fit`; 8b43's lazy tier rebased onto the frame merge): digests
bit-identical to shipped at **every** comparable arm (7/7, incl. held-out seed 7, both flying
paces, the 12,000 rung where counts move with the wall — 7,439 leavers vs 5,856–6,016 — but the
canonical digest does not), and at m4,000/rtf 1: fit2 1,141 calls → **0**
(hand-out bind −45.7%), fixed tier 2.09 M requeues → 12.6 k (D+fixed 286 → **142 ms/game-s,
50% on one binary**; ~61% against the pristine shipped fixed tier). Two of ad26's four factors
die on the stack: the memo's hit rate is 33% on shipped and **0 of 3,225** compiles on the
word-fixed bind (the −31% was the retry's recompile; the endgame counted both), and Carlson's
kernel is not a bind lever — `from_shape` reads the three increments off the walk's last knot,
the compile exists to build the panel grid the readout interpolates, so the kernel's home is
increments-only consumers (cadence, envelopes), not `bind_surface`; priced onto the bind anyway
it lands D → 95–100 ms/game-s. Measured composite **141 ms/game-s (71% of shipped D)**, measured
ceiling **≈ 2.8×10⁴ members** (≈ 4×10⁴ Carlson-priced), not 42.3 and not 9.5×10⁴. Tails after
the whole queue: p99 47.6 → 41.7 ms (−12%), hitches >50 ms/hr −57%, overflow 309 → 194 — the
burst (the bind concentration at the settle) survives the queue; the kick's non-bind 55% is the
next wall. **Checker (this run): the rebased lazy tier re-breaks the shipped gate at its own
scene** — `work_per_frame_is_bounded_and_overflow_is_a_dip_not_a_hitch` (seed 11, threads 1)
fails deterministically on the stacked default paths and passes with `ES_EAGER=1` (shipped
loop, stacked bind), a regression against 8b43 where the deadline-ordered fix made this gate
pass at that scene; the stack is not one merge queue until that is restored, and the dossier's
"suites green (0 failed)" does not regenerate (1 failed, `-p emergent-universe --test plane`).

## Refuted

- **The analytic-guess escape (the passage branch's own `at_radius` pattern) as the cycle branch's
  fix — a float Kepler inverse from the key is dead on the battle regime**: 0 first-guess hits at
  2,064-13,741 searches per arm; it fires on ~2% and misses by half an orbit, because the dips are
  grazing crossings of near-circular orbits (the crossing tick divides any radius-model error by a
  near-zero radial speed). The seed must be a tick (the retired binding's), not a model
  (20261014-0727-quant-af8f).
- A padded f64 drift guess as *proof* of sound dormancy — the bound ignores acceleration, so it cannot decide the scan's reach; measured to miss nothing at every far cell tested, but the seed-3/7/11 digest breaks first cited as its failures were the settle drain bug, not the gate (20261013-2005-spacex-3989; evidence corrected by 20261013-2130-second-20261013-2005-spacex-3989-bc2b).
- Dormancy without the settle-loop drain — a one-shot drain loses every leaver handed out during the settle (a wall-budget-dependent count), which was both the seed breaks and the load nondeterminism (two digests at one cut, kicks 115/112, 0 wakes): fixed by draining inside the loop, identity and load stability proven after (20261013-2005-spacex-3989, checker; root cause and fix by 20261013-2130-second-20261013-2005-spacex-3989-bc2b).
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

1. **The first-binding search still has no seed** (the warm lever's named hole): a hand-out's first
   binding has no predecessor tube — 50% of searches at the 16k arm, 6% at flying pace. Candidate
   seeds to measure: the member's compact fleet state (its radius and phase on the formation's
   orbit) as a one-probe bracket, or the compiled crossing table's band cut at the surface's u (the
   walk already cut the orbit at every band edge; the surface is just another u, and the bracket
   between two cuts is a table lookup). Success bar: lands within 2⁶ ticks as the warm seed does.
2. **A radius-only readout** (3.6-3.9 µs per `inside` today): the predicate needs only
   `norm2(position(t))` but `readout` decodes velocity too; a radius-only channel of the panel walk
   multiplies with the warm seed on the ~4 readouts a hit still pays, and covers the unseedable
   half.
3. **Close the starvation hole for real, then merge the deleted tier**: the second author's fix
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
4. **Carry the burn in the tube's generator, deleting the waterfall (not spreading it)** — the
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
5. **The kick as an addition**   (`ΔL = x×Δv`, `ΔE = v·Δv + |Δv|²/2`, carries as today); fit the tube once per *read* (plan
   tick, certificate, view gather) instead of once per kick — reads are per frame per visible
   body, kicks are 128 per radial period, and the fit stays exact so digests survive where the
   memo could not (20261011-1729-components-b063). Unmeasured: scenes where reads outnumber kicks
   (a watched fleet at rtf 1) — the read side's cost at scale is the named counterweight
   (20261011-1729-components-b063, lens). Cadence is a separate, priced door: halving kicks halves
   work (exponent ≈1) at ≈4× B13 error per halving (20261007-1801-second-…-18df).
6. **Per-region staleness rung** (survive sustained overload): horizon from the player's own chain;
   a lagging region's sky goes stale, the player never waits — kills the ~600× presented-time
   cliff (20261007-1234-system-2517). Must be shown to move no digest.
7. **A density/throughput gate** (end the silent freeze): shed target rtf when local density ×
   target exceeds the budget's sustainable events/s; dashboard arithmetic only
   (20261011-1917-second-…-762d-119f).
8. **Land the decision-tick quantization** (close the canon leak): two lines in
   `session.rs`/`kick_bench.rs`, already built and held on an ungraded branch — bring it through a
     graded run (20261008-0615-taleb-40c0, 20261008-0743-second-…-a342; the leak reproduced and the
   wall-grid fix shape validated on the shipped API by 20261012-2257-scout-64e4 — quantizing the
   presented tick does not fix it).
9. **Replace the player scan** (the frame's p99, and the flight's per-item cost): the Binet
   cone over `PlayerNeighbourhood`'s exact O(all-bodies) check (20261010-0656-quant-d540,
   20261010-1920-spacex-cb3f, 20261011-0736-components-825f); in the flight regime it prices every
   player item at ~430–500 µs (48 members) to ~1.7–2.9 ms (400 members), of which the pure
   resolve is only ~140–150 µs (20261012-2257-quant-32ab).
10. **Hand-out cost at fleet scale**: 443 µs per hand-out, 12× a kick, plus deadline pinning
   (20261011-1102-quant-ba35).
11. **Adopt dormancy: the drain fix is unconditioned; the wake rule is a priced choice** (the silver
   run's gold experiment, done): the settle must drain its dormant list inside its loop (9 lines — no
   dormant arm is a certificate without it), and then the rule is either `doll` (canon-exact by
   construction, identity measured; pays every bind in same-doll scenes — the far-scene cure dies at
   flying pace, overflow 393/480) or `drift` (keeps the cure, 0 misses measured, the f64 bound
   unproven — its soundness against a leaver that truly closes to within `1024 x reach` mid-flight is
   the one unmeasured scene; constructing it is the next rung on this lever). Other-doll dormancy is
   canon-free by the scan's candidate filter either way — the 10⁹ case (a fleet per doll, readers
   elsewhere) never needs a gate (20261013-2130-second-20261013-2005-spacex-3989-bc2b, on
   20261013-2005-spacex-3989).

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
- 20261014-0727-quant-af8f (this run): the crash search cut 38-54% bit-identically by threading the retired binding's impact tick as a predicate-verified seed; hand-out first bindings are the unseedable half; the Kepler model guess dead (grazing dips).
- 20261014-0450-quant-1845 (silver, checker-extended): the fired kick is 46% bind, 45% the crash-tick bisection (115 µs, ~25 readouts, every kick and the dipping half of hand-outs, cache reset per rebind; 57% at flying pace, 43% of the hand-out at 16k); warm-start bracket priced −45%/kick, −10%/hand-out at the battle arm.
- 20261014-0000-second-20261013-2252-system-ad26-790b (second author, awaiting grade): the stack measured — word fix+lazy tier bit-identical, D+fixed 50% on one binary; memo 0/3,225 hits on the word-fixed bind and Carlson not a bind lever kill the 22%/10^5 endgame; ceiling measured ≈2.8e4.
- 20261013-2252-system-ad26 (this run, awaiting grade): one wall — the bind is 41–65% of every event-carrying item class (80% of a hand-out, 45% of a battle kick; the retry 18–39% of the bind); the four unmerged levers compose to 22% of the battle cost, ceiling ~10^5 members; projection, composite unverified.
- 20261013-2252-components-be78 (author, unchecked): word-before-bind deletes the fit-again retry (40-62% of hand-outs, hand-out -16...-45%), digests identical on 7 scenes + plain build.
- 20261013-2130-second-20261013-2005-spacex-3989-bc2b (second author): the dormancy arm's seed breaks and load nondeterminism were one bug (the settle's one-shot drain losing settle-time leavers); fixed, identity at seeds 1/3/7/11 near and far, one digest across budgets and 4-way load, cure intact to 8,000; the canon-exact doll rule kills the same-doll flying cure (393/480) — the win needs other dolls or the unproven drift bound.
- 20261013-2005-spacex-3989 (silver, checker-corrected): dormant leavers cure the first N-wall at every seed and size tested (286->0 overflow, rtf 0->1 at 4000/rtf1; flyable at 8000) but break the digest in 3 of 4 far seeds, and the arm is load-nondeterministic; the gate's bound and the arm's determinism, not the dormancy, gate adoption.
- 20261013-2005-quant-7055 (silver, checker-corrected): the hand-out's exact-memo edge priced — 33% of hand-out compiles are same-member coarser-word retries (bind −39%/hand-out −31%, bit-identical; member-to-member sharing ~0; 0.6% at rtf 100); the retry and the sticky promotion stay the levers.
- 20261013-1915-fermi-367f (silver, checker-corrected): the plane's first N-wall is the fleet frame's leak into sticky promotions (~0.5 ms, ~8.3 kB each, no demotion); the frame's own advance is only ≈N^0.6–0.8 (the N^1.9 "fleet item" includes the hand-outs).
- 20261013-1428-system-2964 (this run): the cadence's two edges priced — deletion collapses events 19–204× and the lag to 0.038 s but breaks at the velocity word (prograde burns lost, refusals, envelope to 4.2e-2 c; retrograde lands ~7% low); 16× refinement keeps the stutter and shows the shipped arm ~1% off its own fine limit; the carry's contract measured.
- 20261013-0037-system-174d (silver): the waterfall decomposed — all burst items are the player's burn-cadence chain; tide/burn ≤ 1.3×10⁻⁹; delete by carrying the burn, don't spread.
- 20261013-0236-second-20261013-0037-system-174d-0f2a: the law's own cadence re-prices the tide counterfactual — ~0–24 events against 377–1,085 burst kicks at every level incl. paced L15 8 s; the fixed-granularity inversion was the divisor's artifact; lever adoptable.
- 20261013-0037-second-20261012-2257-spacex-5eb6-8b43 (silver): the seed-11 starvation fix — deadline-ordered due pass, slack on the cap, proximity park, pull/stall rekey; gate passes, one digest in three arms, quiet flat to 4×10⁵, suite 58/58; checker: breaks on seeds 2/5/9 and threads 4 where shipped holds.
- 20261012-2257-spacex-5eb6 (silver): the lazy deletion built — quiet frame O(1) (1.35 µs flat to 2×10⁵, 10,872×; 4×10⁵, tie-storm and 25×-wander cases hold, checker), digests identical across arms and 15 schedules; sustained starvation breaks the fleet cap (the shipped plane gate fails) — one experiment from merge.
- 20261012-2257-quant-32ab (silver): the sweep's L8+ stutter is the burn-input player-item waterfall (1,036 items in the input frame at L15) on the O(N) scan, not the fixed tier (≈0% in flight); per-item cost flat in γ.
- 20261012-2257-scout-64e4 (silver): rekey policy proven schedule-only (divergent schedules, identical digests); the digest break is presented-tick key logging; wall-grid fix holds.
- 20261012-1621-q-wiki-frame-cost-ae6a: the exodus contradiction resolved into a regime boundary (no ≥0.6 s stall to 6,400 members at flying pace).
- 20261012-1019-quant-b29b (gold): unbudgeted Θ(N) fixed tier (rekey + drain): 38% of frame at 12k, 8× over at 120k; ceiling ≈1.5–6×10⁴ entities.
- 20261012-0616-system-1537 (silver): hidden O(N) rekey tick (215 µs at 10³ → 37 ms at 6.4×10⁴); the naive tick-keyed calendar breaks digest identity.
- 20261012-0036-quant-115e (gold): rekey tax 43–60 ns/body, linear to 2.6×10⁵ at zero events, no class escapes; kick 70.7% rebind, 11× tail.
- 20261011-2306-system-3367 (silver): every distinct kick re-fits a fresh exact cycle (1125/1125); motion-law v2 player events 0.5–1.0 ms.
- 20261011-1917-second-20261011-1814-taleb-762d-119f (gold): no per-frame prologue floor (15 µs at 428 bodies); freeze = throughput ÷ density (opening needs 293× budget).
- 20261011-1729-components-b063 (gold): kick 75.6 µs vs 42–56 ns floor (~1,800×); the refit is 84–89%; exact memo 0%.
- 20261011-1102-quant-ba35 (silver): kick path compute-bound and flat; the 0.95 s "slice" is 2,091 hand-out events of 443 µs, already split.
- 20261011-0836-autoresearch-469c (lead): kick attribution (rebind 87.2%, quadrature ~61%) reproduces; the kept change breaks digests, killed.
- 20261011-0736-components-825f (silver): allocator at its floor (idiot index 1.01, 0.3–0.4% deferrable); the demand tail is the `PlayerNeighbourhood` scan.
- 20261010-2141-constraint-ae40 (silver): p99 frame = single player events 1.3–3.4 ms (O(all-bodies) scan, monotone in members); median frame is view-bound.
- 20261010-1947-autoresearch-2833 (silver): `proper_at_event` cache plus cartesian-free `orbit_state`: kick −9–10%, bit-identical, +18 bytes/body.
- 20261010-1920-spacex-cb3f (silver): per-event ~50 µs vs ~3.6 µs physics; the player scan is 30–36% of settle (33 ns/body/item); memo no.
- 20261010-1920-quant-9464 (silver): the 428-body "saturation" is the xtask clamp; 4,331 bodies at 15 s with it lifted.
- 20261010-1544-system-97ce (silver): belt path: every kick rebinds and rekeys (0/203,017 memo hits); bind 43.7% of wall; re-anchor buys 1.7×.
- 20261010-1302-spacex-6785 (silver): ship class −36% (32.0→20.4 µs/item, ~14 lines); rebind 11.3 µs the next lever; Dense baseline defect.
- 20261010-0656-spacex-2439 (gold): hidden tick: 0.43 µs × N per frame, walked/frame = N; the rekey walk acquitted; digest neutral.
- 20261010-0656-quant-d540 (gold): frame Ω(N) at zero events (~0.7 µs/body, three Calendar touches); breaks 16.7 ms at ≈3×10⁴ tubes; player find 1.6–3 µs/body.
- 20261009-2043-quant-3cfc (silver): smoothness breaks at ~1,600 members (one exodus item 0.6–1.5 s); 8 GB caps ≈5×10⁴ members.
- 20261009-2043-autoresearch-d4f1 (silver): `Orbit::compile` is the kick's cost (compile/bind 0.85–0.90); front-half micro-optimization caps at 1.2×.
- 20261009-0709-quant-6766 (silver): three O(N) schedule passes at zero events (drain 5.8× over break); the naive break breaks digest identity.
- 20261008-1252-quant-291f (silver): one held player order wakes ~2,000 events and 94–116 saturating frames; digest fixed at the cut.
- 20261008-0743-second-20261008-0615-taleb-40c0-a342 (missing): decision-tick quantization built and held (one digest per seed across rates and load); ungraded, not on main.
- 20261008-0615-taleb-40c0 (gold): engine core schedule-independent (one digest, nine paths); the loop logs keys at the presented tick, so frame rate rewrites canon.
- 20261008-0234-quant-2300 (silver): kick resolver O(1) in universe size, ~90 µs/kick; 79–88% Kepler tube refit, 1–2% force.
- 20261007-2344-quant-4211 (silver): deadline calendar O(N)/frame (rekey-all, drain, requeue); dyadic wheel plus deadline skin 7–20× at 10⁶.
- 20261007-2246-components-4955 (silver): shipped 4-ary heap 4–8× off its workload's floor; monotone bucket wheel 2.1–4.4× cheaper per event.
- 20261007-1801-second-20261007-1646-autoresearch-a191-18df (silver): scope-free rebuild regenerates the record; cadence priced (work exponent ≈1, B13 error ×4 per halving).
- 20261007-1646-autoresearch-a191 (silver): two redundant tube decodes per kick deleted: bit-identical, made −16–21%; `Orbit::compile` remains the wall.
- 20261007-1234-system-2517 (gold): the frame loop already is the allocator (digest invariant through 100% overflow); sustained overload collapses presented time ~600×.
- 20261006-1354-constraint-df79 (silver): the spike is the player's O(doll) encounter scan (one item 68% of frame); 4 threads worsen overflow.
- 20261006-1135-autoresearch-eb29 (silver): deleting `bind_in`'s residual decode is bit-identical; made kick −9.5%.
