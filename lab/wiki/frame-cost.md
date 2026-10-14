topic: frame-cost
status: open
closed-by:
valid-while:
updated: 20261014-1511-quant-7226

# The frame loop and the kick resolver: cost per body and per kick

## Current best

**The crash search is counted probe by probe on shipped code, and the naive smarter-probe
lever on it is killed with the mechanism named (20261014-1511-quant-7226).** Additive
counters in `step.rs` (`step::searches`, printed by `--kick-bench`; digest
`36637e67…` = the pristine build's, off = shipped verbatim): at the flying arm
(m400/s3/rtf100, 8 game-s) the kick's surface search runs **802 `next_impact` searches
paying 23,552 exact readouts — mean 29.4, worst 32 per search** (held-out s7: 1,225 /
36,367, mean 29.7, worst 33); 29.4 ≈ log₂ of the ~2^30-tick half-orbit bracket, so the
midpoint bisection sits at its policy class's floor — no probe is wasted, the policy wastes
them. `next_exit` searches are **0** wherever the passage's analytic guess applies (its
endpoint probes: 1,188) — the guess retires the whole exit search, not just accelerates it.
The lever this count invites — choose the probe by the radius value the predicate already
reads, float places / integer decides — was built three ways (Illinois on values, Illinois
on signed distances, vertex-quadratic matched to the flat periapsis, plus a pure secant),
**digest-identical in every arm and seed** (canonical + replay; refused 0; a new crate test
asserts fast = slow on every dipping tube of a settled plane, two surfaces, two starts) and
**killed by the pre-registered rule**: best arm −4.6 % probes, worst 57–58 (the 30-probe
fallback fired), leaver median +55 % on the final arm. Mechanism from probe traces: the
crossings are mid-branch with deep dips (periapsis 3–7× the level deeper than the miss
end), local slopes healthy and consistent (~4.4 units/tick over 2×10⁷ ticks), but every
chord through the retained miss anchor (signed distance ~10⁸) lands a fraction
|d_hi|/d_lo across — a one-sided crawl at ratio ≈ 0.23 that no halving rule in this family
breaks fast enough. The named survivor: **Anderson–Björck (or inverse-quadratic through the
newest three probes) — checker-measured, not just named: mean 21.3/22.3 probes at seeds
3/11 (−28/−24 % vs bisection), leaver median −25/−26 %, digests identical, but worst 38
> 30, so the frozen tail rule kills plain AB too**; the update rule must penalize the
retained miss anchor multiplicatively **and** bound the degenerate tail (a bail at 8
probes measured worse: mean 27.5). The counters and
the equality test are adoptable as-is (zero cost unread); they are the contract for the
warm start's freeze and for any Carlson readout change that touches the search. Domain:
Linux/x86 shared box, one scene family (plane battle, seeds 3 and 7), flying pace only
(battle pace fires no surface searches at m400); the grazing-dip regime (crossing near the
periapsis) is where the warm start already settles in two readouts and would flatter a
quadratic policy. Regeneration: `lab/results/20261014-1511-quant-7226/regen.sh`.

**Prior best (20261014-1010-second-20261014-0450-quant-1845-0b85):** the warm start is
built, measured and exact — the kick's rebought crash-tick search falls 38–44 % for zero
fallbacks, shipped digests never move; and (20261014-0450-quant-1845) the fired kick is
46 % bind, 45 % one `next_impact` bisection (≈ 25 readouts × 4.6 µs), 9 % the rest; the
search fires on every fired kick because `rebind` resets `Binding.impact`.
## Refuted
- **"A value-guided probe policy cuts the crash search" as a one-hour build**: three
  bracketed policies (Illinois absolute/signed, vertex-quadratic) plus a pure secant all
  crawl one-sidedly at ≤ 1.4 bits/probe and lose to midpoint bisection (worst 57–58
  probes, leaver kick +55 %; digests identical everywhere) — the miss anchor's value
  dominates every chord until an Anderson–Björck-class update replaces plain halving
  (20261014-1511-quant-7226). The lever itself is not refuted: the pre-registered kill is
  of the update rules built, and the traces name the survivor.
- Illinois's halving applied to the **value** rather than the signed distance to the level:
  2.0× the probes (the halved anchor leaves the level's neighbourhood entirely) — a
1. **Anderson–Björck / inverse-quadratic probe update with a tail guard on the same exact
   predicate** — the named experiment this run leaves, half-built by the checker: plain AB
   already gives mean 21.3 probes (seeds 3/11), −25/−26 % leaver median, digests identical,
   but worst 38 (the frozen rule's tail); a bail to bisection at 8 probes measured worse
   (mean 27.5). The open part: bound the degenerate tail without paying the typical case —
   then compose with the warm start (it deletes searches that moved < 1 tick; AB cuts
   probes on those that did not). Budget: one hour — the harness (counters, env gate,
   equality test, kill rule) is already in the tree. Note: of the four killed policy rows,
   only the pure secant is regenerable from `work/patch.diff`; Illinois-on-signed was
   reproduced by the checker at mean 28.0 (author 28.0, worst 30, digest identical).
2. The warm start (0b85) then lands on top: it deletes the search where the crossing moves
   by under a tick; AB deletes the probes where it does not.

## Contradictions
- (unchanged) The stack's lazy-tier gate regression and the frame-cost page's merge
  conflict are the integrator's to resolve; this run's page proposal folds into whichever
  side stands.

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
- 20261013-1428-system-2964 (this run): the cadence's two edges priced — deletion collapses events 19–204× and the lag to 0.038 s but breaks at the velocity word (prograde burns lost, refusals, envelope to 4.2e-2 c; retrograde lands ~7% low); 16× refinement keeps the stutter and shows the shipped arm ~1% off its own fine limit; the carry's contract measured.
- 20261013-1915-fermi-367f (silver, checker-corrected): the plane's first N-wall is the fleet frame's leak into sticky promotions (~0.5 ms, ~8.3 kB each, no demotion); the frame's own advance is only ≈N^0.6–0.8 (the N^1.9 "fleet item" includes the hand-outs).
- 20261013-2005-quant-7055 (silver, checker-corrected): the hand-out's exact-memo edge priced — 33% of hand-out compiles are same-member coarser-word retries (bind −39%/hand-out −31%, bit-identical; member-to-member sharing ~0; 0.6% at rtf 100); the retry and the sticky promotion stay the levers.
- 20261013-2005-spacex-3989 (silver, checker-corrected): dormant leavers cure the first N-wall at every seed and size tested (286->0 overflow, rtf 0->1 at 4000/rtf1; flyable at 8000) but break the digest in 3 of 4 far seeds, and the arm is load-nondeterministic; the gate's bound and the arm's determinism, not the dormancy, gate adoption.
- 20261013-2130-second-20261013-2005-spacex-3989-bc2b (second author): the dormancy arm's seed breaks and load nondeterminism were one bug (the settle's one-shot drain losing settle-time leavers); fixed, identity at seeds 1/3/7/11 near and far, one digest across budgets and 4-way load, cure intact to 8,000; the canon-exact doll rule kills the same-doll flying cure (393/480) — the win needs other dolls or the unproven drift bound.
- 20261013-2252-components-be78 (author, unchecked): word-before-bind deletes the fit-again retry (40-62% of hand-outs, hand-out -16...-45%), digests identical on 7 scenes + plain build.
- 20261013-2252-system-ad26 (this run, awaiting grade): one wall — the bind is 41–65% of every event-carrying item class (80% of a hand-out, 45% of a battle kick; the retry 18–39% of the bind); the four unmerged levers compose to 22% of the battle cost, ceiling ~10^5 members; projection, composite unverified.
- 20261014-0000-second-20261013-2252-system-ad26-790b (second author, awaiting grade): the stack measured — word fix+lazy tier bit-identical, D+fixed 50% on one binary; memo 0/3,225 hits on the word-fixed bind and Carlson not a bind lever kill the 22%/10^5 endgame; ceiling measured ≈2.8e4.
- 20261014-0450-quant-1845 (silver, checker-extended): the fired kick is 46% bind, 45% the crash-tick bisection (115 µs, ~25 readouts, every kick and the dipping half of hand-outs, cache reset per rebind; 57% at flying pace, 43% of the hand-out at 16k); warm-start bracket priced −45%/kick, −10%/hand-out at the battle arm.
- 20261014-1010-quant-036c (silver): the crash search's warm start built — search −38…−60% µs/call, leaver kicks −35…−40% at flying pace (~0 at battle pace), digests bit-identical at 8 arms + bench; guess settles 42–69%, half the priced win.
- 20261014-1010-second-20261014-0450-quant-1845-0b85 (second author): the warm start built — kick −43%/−38%/−44% (battle/battle/flying), 0 fallbacks in 3,928 warm searches, warm search ~13 µs, digests = shipped everywhere incl. clamp-only reference; prior record reproduced at base; hand-out half unchanged.
- 20261014-1511-quant-7226 (this run, awaiting grade): the search census (29.4 probes mean,
