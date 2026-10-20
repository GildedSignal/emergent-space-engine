topic: frame-cost
status: open
closed-by:
valid-while:
updated: 20261020-2004-quant-b6ef

# The frame loop and the kick resolver: cost per body and per kick

## Current best

**NEW (b6ef, quant — aa42's named unpriced term priced with one timer layer, and it is not miscellaneous: at belt e the outside-`from_state` scaffolding is 57% two proper-time decodes, both redundant and deletable with no law change for a measured -19…-22% of the rebind wall; on the plane the same bill is 88% `plan_terminal`, the crash search b583 already retired).** `ES_SCAFFOLD_AUDIT`, print-only (bench `digest`+`replay_digest` identical on vs off; belt kicks/events/refusals identical; one settled `LazyLock` load when off), disjoint buckets (the retry's inner stages suppressed), on the standing belt and the bench seed 1: **belt (273,767 / 203,735 rebinds, N-flat within 2%): rebind 27.97 / 28.64 µs = fit 56.8 / 57.5% + tau-at-t 3.41 + tau-at-event 3.44 (pair 6.85 µs = 57% of the 12.08 µs outside `from_state`) + decode/turn/residual 3.80 + `plan_terminal` 0.55-0.71 + ~1 misc; bench (2,349): rebind 146.65 = fit 45.2% + `plan_terminal` 71.98 (49.1%) + tau-pair 7.30 + decode/turn 4.14.** The two tau reads are full trajectory decodes, scene-flat at 3.4-3.7 µs, and both pay for known values: `orbit_state(old.event_time)` recomputes what the old bind computed and discarded (`Bound.orbit.proper_time` — one 16 B Scalar per Binding makes it free), and `orbit_state(t)` repeats the decode `kick`'s own `readout(t)` just paid (3.70 vs 3.41 µs/call — one fused decode returns state + proper time). **Deletion: -5.39 / -6.19 µs per belt rebind (kick share 57.2% / 81.1% at rtf 1800, cadence-elastic) = -19.3% / -21.6% of the rebind wall, ~-13% of the kick item, zero new compute, digest-neutral by construction (same decode outputs reused).** Also priced: the coarser-word retry is dead as a belt/bench term (0.014% / 1.3% of calls, but 242-268 µs — a whole second fit — when it fires); aa42's belt 12.7 µs scaffolding reproduces (12.08) while their bench internals are refined: there the bill is 88% the crash search. Domain: coasting belt + one bench seed, Linux/x86 shared, walls ±load (the two belt arms agree within 2% on shares); the fusions themselves are unflown (20261020-2004-quant-b6ef; regen ~3 min; P1/P2/P4/P5/P6 held, P3 half-failed — the retry is a hand-out term, not a kick term).
[Checker (silver): all arms reproduced (regen; plus bench seed 7, belt 10⁴ burn, 10⁵ coast, 10⁴
rtf 300 — the first three out of the author's domain). The τ-pair is the largest scaffolding term
in every arm (55.3–57.0% of outside-`from_state` at 10⁴/3×10⁴/10⁵ and on burn; 45% at rtf 300),
and digests are identical audit on/off at seed 7 too. But the deletion band's lower end is
elastic, not flat: the kick share of rebinds is N-elastic as well as cadence-elastic (30.2% at
10⁵ coast → deletion 16.0% of the wall; 74.6% at rtf 300 → 17.5%; 80.3% on burn → 19.7%), so the
honest band is −12% (the event-τ cache alone, N-flat at 12.2–12.3% of the wall) to −22%. The
event-τ cache half is a re-price of 2833's flown `proper_at_event` cache (this page's Runs:
+18 B/body, kick −9–10%, bit-identical, silver, unadopted) and must cite it; the fused kick
decode half and the pricing itself are new. The deletion is unflown (shares-only arithmetic).]

*[Prior best retained below.]*
**NEW (077c, quant — the standing contradiction adjudicated with one instrument on both scenes
plus a controlled e-grid: the compile's share is a property of eccentricity, crossing the rest of
the rebind at e ≈ 0.2, and the two censuses also measured different boundaries; at belt e the
rebind has no single 74% owner).** Print-only `ES_REBIND_AUDIT` stage census inside
`Rebinding::from_state` (FIT=`fit_key`, COMPILE=`Orbit/Passage::compile`, ANCHOR=`at_radius`
+ orientation, RESIDUAL=`decoded_event`+`Residual::between`; digests identical on vs off;
+ checker2 correction: audit-off still executes five unconditional `Instant` reads per call, so
+"off = shipped bits" is approximate — pristine-code walls sit ≤ ~6% below audit-off bare walls
+(load-confounded; the clock reads themselves are ~0.2–0.3 µs, ≤ 2% of the belt wall)), flown on
+a765's scene and 7fd3's, plus `rebind_stages`, a 3-radius × 8-e grid
(min of 5 batches per cell — this box's vCPU steal is bimodal ~±35%, first execution kept
disclosed as load-hit): **plane kick-bench (63 rebinds ×2): compile 90.1–90.5%, fit 3.1%,
anchor 1.4%, residual 4.9–5.3%, wall 147.6–148.2 µs (a765's 84–87% reproduced, stronger);
belt nladder 3×10⁴ coast (276,703 rebinds): compile 43.3%, fit 25.6%, anchor 8.7%,
residual 21.7%, wall 15.95 µs; N=10⁴ (203,802): 44.8/24.9/8.5/21.0, 16.59 µs — N-flat.**
The grid: compile is e-monotone 3.4 → 46.8 µs (13.8×) from e 0.07 to 0.9 at every radius
(e 0.99 cells are dropped — checker2: at r17 the key and compile bind and the state generator
loses the cell (51/72 states); e 0.95 binds at 66.6 µs r17, extending the tail — the plane's
52–65 µs compiles are that tail), while
fit+anchor+residual is flat ≈ 8.3–9.0 µs — **the crossing sits at e ≈ 0.2** (below: the stack
owns 71/29 at e 0.07; above: compile owns 85/15 at e 0.9). The boundary half [INFERENCE with
arithmetic]: my belt compile absolute (6.9–7.4 µs) matches 7fd3's (7.6–7.8) while my
`from_state` wall (15.95–16.59) is 1.8× below their "rebind" (28.7–30.0) — a uniformly slower
box would have inflated the compile too, so their bucket carried ~12–13 µs outside
`from_state` (the `bind_in` decode/tube/entry attendants), diluting 43% → 26%. **Consequence
for the two forked programs: at belt e (the 10⁹ scene) the Carlson compile buys ≤ 2× on a 43%
share and the readouts are the bigger combined cut (30%: two ~4–5 µs readout prices on a fresh
compile, P6 — the readouts outweigh the root search 4.9–5.9 vs 3.4–3.9 µs at every radius); at
plane e the compile alone is 90% and the Carlson wiring is the whole program.** Both censuses
were right about what they measured ("Measure before claiming, and never strawman"). Domain:
Linux/x86, orders of magnitude; the grid samples exact-orbit states (the fit's degenerate-kick
tail is censused by the belt arm, not the grid); the plane arm is 63 rebinds, deterministic
(20261020-1729-quant-077c; regen ~3 min warm; predictions P1/P3–P7 held, P2 half-failed on its
compile-share letter — the failure located the boundary difference, which is the finding.)
[Checker (gold): all arms reproduced and extended out of domain — grid radii 5/12/23/40 and
e 0.95 keep the compile monotone (58–94 µs at 0.95) with e 0.99 refusing at all seven radii;
the held-out belt **burn** arm holds the regime (compile 49.1%, readouts 27.7% > fit 22.6%);
N=10⁵ is N-flat (42.5%); a765's own rtf-100 populations regenerate exactly (1,467/1,737/1,349
calls; compile 81.9–84.8%). The boundary half is verified from 7fd3's published patch: their
REBIND_NS wraps the universe `rebind()` (bind_surface → bind_in adds decode, turn, tube, entry
beyond `from_state`), and their 10⁴ mint count 203,485 matches this audit's 203,880 calls
within cadence. Caveats: belt walls and rebind counts are cadence-elastic (two audit-off
flights differ 3.6% in kicks — the on/off kicks delta is inside off/off noise); the plane's
63-rebind population is passage-heavy (22/63), so a765's cycle-heavy populations are the
cleaner plane anchor; the plane rebinds' e distribution is unmeasured, so "that tail" stays
inference.]
[Checker2 (gold, blind to the first check): independently reproduced — plane 90.1% (wall
149.0 µs, digests bit-identical), belt regen 44.6% (shares stable across a ~15% wall shift),
grid crossing between e 0.2 and 0.4 at r17. Held-out flown: burn 49.2% (readouts 27.5% >
fit 22.6%), N=10⁵ 42.0% (415,454 calls, N-flat a decade on), pristine-probe radii 5/12/23
with e 0.95 monotone to 66.6–104 µs. The P4 control measures counter-add cost only (the
timer reads are unconditional); the pristine bound above closes that gap.]

*[Prior best retained below.]*


**NEW (aa42, second author on 7fd3 — the checker's named experiment run whole: the
compile-share contradiction is DISSOLVED, both standing numbers reproduced in their own
cells, and the term neither run had measured is named: the rebind scaffolding OUTSIDE
`from_state`).** One binary, one instrument (7fd3's census verbatim + two stage timers
inside `Rebinding::from_state`, so a765's compile/(fit+compile+tail) reads off the same
counters), run on both scenes: a765's arm (`--kick-bench` seeds 1/42/7 + repeat) and
7fd3's belt (`nladder 10000/30000 coast`). Cells — compile/rebind-WALL (7fd3's metric):
**belt 0.254-0.266 (reproduces 7fd3), bench 0.365-0.427**; compile/from_state (a765's
metric): **belt 0.44-0.45, bench 0.842-0.861 (reproduces a765's stored 0.877-0.894)**.
The pre-registered fork's mixed band fired: neither supersession. Both terms are real —
**denominator** (the wall carries 41-57% outside `from_state` on both tested scenes;
checker probes: 35% on a 10⁴ burn belt, 37% at bench rtf 30 — still the second-largest
term there:
`bind_in`'s decode/turn/residual + `word_for` retry + `Work::rebind`'s two `orbit_state`
τ-reads, segment retirement, binding construction — 12.7 µs belt, 84-101 µs bench, the
largest single measured term on BOTH walls (checker2: 11.5-12.7 µs vs the compile's
7.3-8.2 on the belt too), unnamed by a765's
stage audit and folded into 7fd3's "fit 74%") and **scene** (only the compile is
scene-dependent: 7-8 µs/mint belt vs 55-74 bench, cd6e's e-monotone curve; `fit_key`
4.2-5.9 and the from_state tail 5.1-6.8 are flat). Consequences: (1) every compile-share
citation must name denominator AND scene; (2) the kick's next cut on both scenes is the
outside-from_state scaffolding (35-57% of the wall across author and checker scenes vs
`fit_key`'s 3-15%), internals named above, unpriced — one timer layer prices it; (3)
a765's compile-bound reading stands inside `from_state` on the plane (Carlson owns that
term); 7fd3's fit-redirect is belt-wall-only, and even there 74% = fit_key 15 + tail 17 + scaffolding 41. Bench
reads/mint 35-37 (P5 killed: the bench's own frame traffic counts), history 100%
(663/663). Domain: coasting belt + plane kick-bench rtf 100 (checker arms: bench seed 2026
and seed 3 at rtf 30, belt 10⁵ coast, belt 10⁴ burn — the cell structure holds, the
scaffolding band relaxes to 35-57%, the rtf-30 wall share reaches the 0.55 fork edge;
checker2 arms: bench seed 1234 / seconds 30 / rtf 300 (wall 0.405-0.409, stage
0.844-0.846, scaffolding 52%) and belt 3×10⁴ burn (wall 0.297, stage 0.494, compile
8.8 µs/mint — the burn belt keeps the belt's cheap compile, so the scene variable is the
population's e, not the activity; scaffolding 39.9%, hist 259373/259376)),
Linux/x86 shared, orders
of magnitude; bench counters deterministic, wall shares ±0.03 with load
(20261020-1729-second-20261020-1621-system-7fd3-aa42; regen ~4 min; predictions
pre-registered, P1/P2/P5 killed at their bands, P3/P4 held).**


**(7fd3, system — the whole-system census: the mint's consumers are counted, and both
deletion candidates die; the kick's unnamed core is the FIT, not the compile).** Print-only
census (`ES_MINT_CENSUS`, relaxed atomics beside the same paths; the shipped digest path
untouched) on the standing belt (`nladder 10000/30000 coast 60 1800`, rtf 1800, ≈3.7 doll
intervals): every fired kick's `rebind` mints a compiled trajectory (mints 203,485 /
247,760; +16.4% over fired kicks + births at 10⁴ — the boundary-exit and hand-off
rebinds), the rebind is 86% of the kick item's wall (41.2/44.0 µs per kick, 28.7/30.0 µs
per rebind), and **inside the rebind the compile is only 26% (7.6/7.8 µs): the fit
(`fit_key`, the witness inversions, `at_radius`, residual, word choice) is the unnamed
74%.** [077c: adjudicated above — 7fd3's bucket was wider than `from_state` and the belt's
`from_state` share is 43%; the 74% decomposes as fit 26 + anchor 9 + residual 22 +
bind_in attendants. The census's readers/mint numbers stand untouched.]
[Checker: the 26% contradicts standing measurements — a765 holds compile at 84-87% of
the rebind and this page's own d4f1 entry 0.85-0.90; unresolved (scene/era/instrument);
adjudication on a765's arm is the named experiment to gold. → flown by 077c: regime (e ≈ 0.2
crossing) + boundary, not instrument error.] The store is NOT a one-reader
cache: **19.96 / 19.53 external reads per mint** (`Trajectory::state` walks; `at_radius` ≈
0.003), and **retained history answers 1.05 / 0.66 reads per mint at a 100% hit rate
(213,940/213,940; 164,410/164,410)** [checker: at 10⁵ coast the hit rate is 99.97% (21 misses
in 71,531) and reads/mint 28.6; the burn arm holds all ratios] — so 225d's "kick mint = the
memory ratchet's outright deletion target" is dead **as read-time recompile** (it would
multiply compiles ~20×) on the flyable path, and any last-only pruning of the *segments*
breaks a measured reader; the lazy/bounded-cache store lever (b9ae's knots→0 flown
digest-identical; 0757's bounded cache, gold — both on the mint-knots page this run did not
cite) is untouched by this census. [Checker attribution probe: the readers are NOT the crash
bisection (probes 0.2-0.4/mint) — they are the general event/readout traffic (~5-6 per kick
path, ~13-25 outside it); the call-site split stays open.] Predictions P2/P3 killed at their
pre-registered criteria, P1 half-killed (compile ≥ 50% of rebind: measured 26%), P5 held
with the excess named. Consequences: (1) the kick's next 10× is the fit, not the compile —
the jet's retirement killed the cheap cycle update; the cheap exact fit (reusing the
previous binding's key when the state is inside its basin) is the untried half of the same
bill; (2) readers, not the mint, are the census's next cut (20 readers unattributed:
boundary predicates, view gather, `state_of` secondaries, planning); (3) the history reads'
owner is an inference (likely `secondaries(d, t)` reading a body bound later than t), not
measured — attribution is the follow-up. Domain: coasting belt, Linux/x86, orders of
magnitude only; a burn arm adds readouts (ff42's crash search), which raises reads/mint,
against the deletion (20261020-1621-system-7fd3; regen ~4 min; predictions pre-registered).


**The crash search is retired behind its inverse, flight-proven: the verified structural
guess with the window sized by the offset's own law fires 100% and falls back never
(20261016-1740-second-20261016-1637-system-ff42-b583, second author; the checker's named
gold experiment, run whole).** The guess mirrors `at_radius` around the **unrounded**
periapsis epoch (`periapsis_epoch`, extracted; `next_periapsis` is its ceil) and verifies
`g, g±1, …` out to `k = ceil((‖offset‖_1 + 8 quanta)/|dr/dt| per tick)` (cap 8; the miss
law is measured: predicted 0.98/1.59 ticks, observed 1, the only two ±1-window misses).
Result: author grid 29/29 fired (readouts 10.92→1.67, 3.49× per call), held-out battery
52/52 (after-phases, e 0.1–0.97, grazing 0.995–0.9999, μ=3/2 dolls, 30 random draws; 0
readouts per search**, digests bit-identical at every arm (kick-bench seeds 3/7/11 flying
and battle; frame_digest 3 burn both flights × 4 schedules; checker-rebuilt pristine and
patched binaries, interleaved). The flying **leaver kick halves: 211→113, 205→110,
201→104 µs median** (−46…−48%, author arms); the checker's clean interleaved rebuild
reproduces −47/−48% (292→155, 283→146 µs at its load) with identical digests and counters
— which is the census's 45% search share gone; p99 ~flat. Instrument: statics inside
`next_impact` (fires/fallbacks/window readouts) — no replication, ff42's defect cured at
the source. The bisection stays as fallback; the policy layer's domain (warm start,
AB-IQI) is empty on every scene shipped main can run (2ae0's patch no longer applies to
main even standalone). **Checker (silver): the regen.sh flight arms are broken** — its
`cargo build -p xtask -p emergent-universe --example frame_digest` never builds xtask
(the `--example` filter selects targets in every package), so both arms copied the same
stale patched binary and the runner's regen compared patched-with-itself (109→112 µs);
the arms also run as two blocks, not interleaved. The patch additionally deletes the
`refused`/`replay_digest` fields from kick-bench's JSON — the replay-identity instrument
itself. Domain (checker's battery, 13 out-of-domain cases, 0 mismatches, 0 fallbacks):
clock_exp −5/12, surfaces near apoapsis (1999/1950/1500 vs apoapsis 2000 — fires with 2
reads), e 0.99/0.999 grazing, 100× scale all hold; **μ far from 1 (16, 1/8) declines the
guess** — exact answer via bisection, no fire, so the 100%-fire domain ends at
near-unit dolls. Remaining for adoption: the regen fix (build xtask per arm, interleave,
restore the deleted fields), the replay arms, and the M1 re-measure — the same gates
2ae0's composed stack owes. Lesson: pristine/patched wall arms must interleave on this
box — minutes-apart arms mislead by ±45%.

*[Prior best retained below.]*


**The crash search and the trajectory inverse are one mechanism shipped as two, and wiring
the second into the first is tick-exact and 2.0× mean (20261016-1637-system-ff42, system;
`levelbench`, 36 crash-course bindings, bound cycles at periapsis fractions 0.05–0.99 ×
both senses × clock_exp 0/6 and unbound flybys e 1.05–3).** `Trajectory::at_radius` — one
knot lookup and one partial quadrature, exact — was already shipped and already wired as
`next_exit`'s verified guess for passages, while `next_impact` (45% of a flying kick, this
page's own census) bisected blind over ticks (mean 10.9, worst 18 full Cartesian readouts
in the bench; 29.4 on the flying arm). The 11-line verified-guess block (the identical
pattern `next_exit` uses, guess checked against the shipped predicate, bisection kept as
fallback) answers **36/36 bit-identical**, mean 55.5 → 27.9 µs; the timing splits the
paths: ~21/36 rows collapse to ~18–21 µs (one inverse + two verifications, 3.2–4.9×),
~8 fall back (shipped cost + one wasted inverse), the O(1) paths (plunge terminal,
periapsis above surface) unchanged. **The honest cap: the guess fires on only about half
the cases (predicted <2% fallback).** The bench's own "5/36 verified" counter is an
artifact — it mirrors the guess around the raw `tube.periapsis_time` instead of
`next_periapsis(b, after)`, off by whole periods for cycles; the corrected replication
and the timing both say ~half fire, ~half fall back (checker, this run): the guess tick
is the pure-tube crossing at `fixed_ceil`, the predicate reads
tube + turn + integer offset, and a slow fall moves the readout crossing past the ±1-tick
verification window — the cure is named (verify a window sized by the local fall speed,
then fall back), and the residual offset is part of the crossing law, not noise the
structure can ignore. Flight digest flown by the checker: bit-identical patched vs
pristine on two kick-heavy flights × four schedules (`frame_digest 3 burn`); the replay
arms remain open.
This composes with the warm start and AB-IQI (they
optimize the fallback this keeps as the safety net), and it is the structural exit from
the probe-policy class this page measured to its floor — the representation already held
the answer's index.

*[Prior best retained below.]*
**The crash search's probe bill is cut 6× exact and digest-identical, and the named
AB experiment is done and passes the frozen rule (20261014-1631-second-20261014-1511-quant-7226-2ae0).**
The guarded Anderson–Björck/IQI policy (`ES_FP=3`: inverse-quadratic probe through the
three newest readouts, AB decay of a retained anchor's distance by the measured same-side
ratio, a crawl bail — two consecutive sub-half cuts force one midpoint) holds **worst
11–18 probes per search against the frozen ≤ 30 (mean 10.6–11.1 vs bisection's 29.4)** at
3 seeds × both paces, cuts probes **−62…−64 %** everywhere, and the **flying leaver kick
−34…−35 %** (199→122–131 µs); digests bit-identical (canonical + replay) at every arm,
ladder rung and warm layer, refused 0, crate suite 11/11 with the equality test extended
to every policy. At battle pace the leaver **median** is flat because the descents sit in
the dipping minority (3,096 searches vs 2,064 kick samples) — the saving lands at all-kick
p99, the wobbliest column (−1…−18 % across the author's, the regen's and the checker's runs,
direction consistent everywhere); the lever is
the same, only its visible term moves. **Composed with the
warm start (0b85's carry merged in, `ES_IMP_WARM`)**: exact readouts fall **−78…−83 %
against shipped** (flying s3: 23,552→3,932; ~29.4→~4.9–5.3 flying, ~6.6 battle
readouts/search; worst 32→11),
flying leaver −43…−47 % (199→105 µs), the savings of the two levers add (warm deletes
searches that moved < 1 tick, the policy cuts the rest), and the warm path's own tail
(worst 32 under plain bisection) drops to 11–12. The kill table of
20261014-1511-quant-7226 now regenerates from the patch (`ES_FP`=1 secant row exactly,
35,621/57): the prior Illinois/AB variants lost their gain to the retention discipline —
the **retained** anchor decays, the fresh side resets (policy 4 = one-half decay: mean
10.9, worst 11). Adoption is a default flip of two env gates (off = shipped verbatim,
verified digest-level — this checker re-verified the OFF arm against a pristine build at
four flying seeds and battle m400; the m4000 battle scene is reachable only through
the patch's `ES_MEMBERS` bench unlock, so its OFF reference is patch-internal, and 0b85's
Crash-retain removal in `rebind` is unconditional, digest-neutral on every measured scene;
`ES_FP=""`/`0` and `ES_IMP_WARM=""`/`0` mean off — the checker's
footgun closed). Domain: plane battle, seeds 3/7/11, flying (m400/rtf100) and battle
(m4000/rtf1), one shared Linux box; wall columns wobble a few %, counts and digests are
deterministic. Regeneration: `lab/results/20261014-1631-second-20261014-1511-quant-7226-2ae0/regen.sh`.

**The census and the mechanism stand (20261014-1511-quant-7226).** At the flying arm the
search pays mean 29.4, worst 32 readouts ≈ log₂ of the ~2^30-tick half-orbit bracket — the
midpoint bisection was at its policy class's floor; `next_exit` fires 0 searches behind
the passage's analytic guess (1,188 endpoint probes). The plain secant crawls one-sidedly
(chord through the retained miss anchor, distance ~10⁸, lands |d_hi|/d_lo ≈ 0.23 across)
— the curvature story the IQI guard confirms by passing.

**Prior best (20261014-1010-second-20261014-0450-quant-1845-0b85):** the warm start alone
is built, measured and exact — the rebought crash-tick search falls 38–44 % for zero
fallbacks, shipped digests never move; and (20261014-0450-quant-1845) the fired kick is
46 % bind, 45 % one `next_impact` bisection, 9 % the rest; the search fires on every
fired kick because `rebind` resets `Binding.impact`.

## Refuted
- **The coarser-word retry (`bind_surface`'s second `bind_in`) as a belt/bench scaffold term: dead on both scenes measured (0.014% of belt `bind_surface` calls, 1.3% on the bench; 7055's 33% was the hand-out path) — each firing still pays a whole second fit, 242-268 µs (b6ef).**
- **aa42's bench scaffolding internals (decode/turn/tau/word_for) as the bench's outside-`from_state` owners: refined — on the bench that bill is 88% `plan_terminal`, the crash search (71.98 µs/call, 49.1% of the rebind; b583's branch retires it); their internals hold on the belt, 12.08 vs their 12.7 µs (b6ef).**
- **"The compile share of the rebind is one number" (the contradiction carried as 7fd3's 26%
  vs a765's 84–87%): dissolved — the share is a property of e (crossing at e ≈ 0.2; compile
  90% on the plane, 43% on the belt at the `from_state` boundary) and the two runs measured
  different boundaries (7fd3's bucket ≈ `bind_in`, 1.8× wider, same compile absolute);
  neither instrument was wrong (20261020-1729-quant-077c).**
- **The <2% fallback prediction for the ±1-window guess (ff42's own pre-registered
  prediction 3)**: the guess fired on only about half the battery that passes
  tick-equality (20261016-1637-system-ff42; the run's own "~40%" and the bench's "5/36
  verified" were artifacts of a replication that mirrored around the wrong periapsis
  tick — checker-corrected). **Cured by b583**: the window sized by the offset's reach
  over the fall speed fires 100%, fallbacks 0 in 155 synthetic + 2,723 flight searches.
- **"A value-guided probe policy cuts the crash search" as a one-hour build**: three
  bracketed policies (Illinois absolute/signed, vertex-quadratic) plus a pure secant all
  crawl one-sidedly at ≤ 1.4 bits/probe and lose to midpoint bisection (worst 57–58
  probes, leaver kick +55 %; digests identical everywhere) — the miss anchor's value
  dominates every chord until an Anderson–Björck-class update replaces plain halving
  (20261014-1511-quant-7226). The lever itself is not refuted: the pre-registered kill is
  of the update rules built, and the traces named the survivor — built and passed by the
  second author (above).
- Illinois's halving applied to the **value** rather than the signed distance to the level:
  2.0× the probes (the halved anchor leaves the level's neighbourhood entirely) —
  20261014-1511-quant-7226; still the one kill-table row that does not regenerate from
  either run's patch.
- **The leaver-median cut as a both-pace criterion**: at battle pace the median leaver
  kick does not track the search (dipping minority; the saving lands at p99) — no probe
  policy can move a search-free median (20261014-1631-second-…-2ae0).

## Open directions
1. **The tau deletion (b6ef), ahead of Carlson and the readout program at belt e: -19…-22% of every belt rebind for one 16 B `Scalar` per `Binding` (the event proper time) plus a fused kick decode — zero new compute, no law arithmetic changed; the fused-decode half costs no bytes, the Scalar half is the memory page's call at 10⁹. Unflown: fly it digest-identical (the same class as eb29/a191's deletions).**
   [Checker: the event-τ half re-derives 2833's flown `proper_at_event` cache (this page's Runs,
   +18 B/body, kick −9–10%, bit-identical) — diff against it before building; and the band is
   −12…−22% of the rebind wall, not flat −19…−22%: the kick share of rebinds is N-elastic too
   (30.2% at 10⁵ → 16.0%; 74.6% at rtf 300 → 17.5%; the event-τ half alone is N-flat 12.2–12.3%).]
2. At belt e the fit's own readouts (anchor 8.7% + residual 21.7% of `from_state`) remain the next cut after the tau deletion (077c's od 1, demoted one step); deeper and invasive: `bind_in`'s post-fit decode and the fit's own `decoded_event` read the same trajectory at the same elapsed time — one fused decode serves both (unpriced).
3. **Adoption gates for the retired search (b583), now carrying a measured main-side price: `plan_terminal` is 49.1% of the bench rebind, 71.98 µs/call (b6ef) — the regen fix, the replay arms, and
   the M1 re-measure** — regen.sh must build xtask per arm (a plain `cargo build
   --release -p xtask`; the `--example` filter never builds it), interleave the arms per
   seed, and restore the `refused`/`replay_digest` kick-bench fields the patch deleted,
   so the flight table regenerates from the script; the identity record now covers
   canonical flights at 3 seeds × both paces + frame_digest's 8 schedules, all
   bit-identical (checker-verified with correctly rebuilt binaries); the replay arms are
   the last unflown identity gate, then the integrator's default flip (the bisection
   stays as insurance).
4. **Freeze the composition** (warm start + guarded AB-IQI as the shipped default): the
   identity record is now three seeds × two paces × every layer, digests bit-identical —
   what remains is the integrator's call on the two env gates and a re-measure on the M1.
   The search then sits at ~5 readouts against the bind's ~46 % share: the kick's next
   lever is the bind (H0209-…-ad26 line), not the search.
5.  The `next_exit` fast path (Illinois + vertex quadratic, author-built, 0 searches in
   every arm measured so far) is inherited, unexercised; a scene that fires it should
   first run the equality test against it. **ff42: the Cycle branch of `next_exit` has no
   guess at all — the same `at_radius` wiring applies verbatim, rarer but the same lever.**

## Contradictions
- The page's own merge conflict (077c vs aa42, published the same window) is resolved by this proposal: both blocks stand as prior bests — they measured consistent cells (compile/`from_state` belt 0.44-0.45 in both).
- (unchanged) The stack's lazy-tier gate regression and the frame-cost page's merge
  conflict are the integrator's to resolve; this run's page proposal folds into whichever
  side stands.
- **RESOLVED (aa42 + 077c, and priced by b6ef):** the compile-share contradiction (7fd3's 26% vs a765's 84-87% and d4f1's 0.85-0.90) was two true measurements of different scenes and different boundaries — the compile is e-dependent (7-8 vs 55-74 µs/mint) and 41-57% of the rebind wall sits outside `from_state`. Every citation names denominator AND scene. 7fd3's "deletion dead" reads as read-time recompile only: the mint-knots page holds b9ae's flown lazy store and 0757's gold bounded cache standing.

## Runs
- 20261020-2004-quant-b6ef (quant): the scaffolding priced — belt 57% tau-pair, both reads redundant (-19…-22% of the rebind deletable, no law change); bench 88% `plan_terminal` (49.1%, the retired search); retry dead on belt/bench.
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
- 20261011-0836-autoresearch-461c (lead): kick attribution (rebind 87.2%, quadrature ~61%) reproduces; the kept change breaks digests, killed.
- 20261012-2257-spacex-5eb6 (silver): the lazy deletion built — quiet frame O(1) (1.35 µs flat to 2×10⁵, 10,872×; 4×10⁵, tie-storm and 25×-wander cases hold, checker), digests identical across arms and 15 schedules; sustained starvation breaks the fleet cap — one experiment from merge.
- 20261013-0236-second-20261013-0037-system-174d-0f2a: the law's own cadence re-prices the tide counterfactual — ~0–24 events against 377–1,085 burst kicks at every level incl. paced L15 8 s; lever adoptable.
- 20261013-1428-system-2964 (silver): the cadence's two edges priced — deletion collapses events 19–204× and the lag to 0.038 s but breaks at the velocity word; 16× refinement keeps the stutter; the carry's contract measured.
- 20261013-1915-fermi-367f (silver, checker-corrected): the plane's first N-wall is the fleet frame's leak into sticky promotions (~0.5 ms, ~8.3 kB each, no demotion); the frame's own advance is only ≈N^0.6–0.8.
- 20261013-2005-quant-7055 (silver, checker-corrected): the hand-out's exact-memo edge priced — 33% of hand-out compiles are same-member coarser-word retries (bind −39%/hand-out −31%, bit-identical); the retry and the sticky promotion stay the levers.
- 20261013-2005-spacex-3989 (silver, checker-corrected): dormant leavers cure the first N-wall at every seed and size tested but break the digest in 3 of 4 far seeds, and the arm is load-nondeterministic.
- 20261013-2130-second-20261013-2005-spacex-3989-bc2b (second author): the dormancy arm's seed breaks and load nondeterminism were one bug (the settle's one-shot drain losing settle-time leavers); fixed, identity at seeds 1/3/7/11; the canon-exact doll rule kills the same-doll flying cure.
- 20261013-2252-system-ad26 (awaiting grade): one wall — the bind is 41–65% of every event-carrying item class; the four unmerged levers compose to 22% of the battle cost, ceiling ~10^5 members; projection, composite unverified.
- 20261014-0000-second-20261013-2252-system-ad26-790b (second author): the stack measured — word fix+lazy tier bit-identical, D+fixed 50% on one binary; memo 0/3,225 hits on the word-fixed bind and Carlson not a bind lever kill the 22%/10^5 endgame; ceiling measured ≈2.8e4.
- 20261014-0450-quant-1845 (silver, checker-extended): the fired kick is 46% bind, 45% the crash-tick bisection (115 µs, ~25 readouts, every kick and the dipping half of hand-outs); warm-start bracket priced −45%/kick.
- 20261014-1010-quant-036c (silver): the crash search's warm start built — search −38…−60% µs/call, leaver kicks −35…−40% at flying pace, digests bit-identical; guess settles 42–69%.
- 20261014-1010-second-20261014-0450-quant-1845-0b85 (second author): the warm start built — kick −43%/−38%/−44%, 0 fallbacks in 3,928 warm searches, digests = shipped everywhere.
- 20261014-1511-quant-7226 (silver): the search census (29.4 probes mean, worst 32; exit search retired by the passage guess) and the naive probe policies killed with the crawl mechanism named.
- 20261014-1631-second-20261014-1511-quant-7226-2ae0 (this run): the guarded AB-IQI policy passes the frozen rule (worst 11–18, probes −62…−64%, flying leaver −34…−35%, digests identical at every layer); composed with the warm start, readouts −78…−83%, worst 11–12; the kill table regenerates from the patch.
- 20261008-0743-second-20261008-0615-taleb-40c0-a342 (missing): decision-tick quantization built and held; ungraded, not on main.
- 20261013-0037-system-174d (silver): the waterfall decomposed — all burst items are the player's burn-cadence chain; delete by carrying the burn, don't spread.
- 20261013-0236-second-20261013-0037-system-174d-0f2a: the law's own cadence re-prices the tide counterfactual — ~0–24 events against 377–1,085 burst kicks; lever adoptable.
- 20261013-1428-system-2964 (silver): the cadence's two edges priced — deletion collapses events 19–204× but breaks at the velocity word; 16× refinement keeps the stutter; the carry's contract measured.
- 20261013-1915-fermi-367f (silver, checker-corrected): the plane's first N-wall is the fleet frame's leak into sticky promotions; the frame's own advance is only ≈N^0.6–0.8.
- 20261013-2005-quant-7055 (silver, checker-corrected): the hand-out's exact-memo edge priced — 33% of hand-out compiles are same-member coarser-word retries (bit-identical); the retry and the sticky promotion stay the levers.
- 20261013-2005-spacex-3989 (silver, checker-corrected): dormant leavers cure the first N-wall but break the digest in 3 of 4 far seeds, and the arm is load-nondeterministic.
- 20261013-2130-second-20261013-2005-spacex-3989-bc2b (second author): the dormancy arm's seed breaks and load nondeterminism were one bug; fixed, identity at seeds 1/3/7/11; the canon-exact doll rule kills the same-doll flying cure.
- 20261013-2252-components-be78 (author, unchecked): word-before-bind deletes the fit-again retry (40-62% of hand-outs), digests identical on 7 scenes + plain build.
- 20261014-0000-second-20261013-2252-system-ad26-790b (second author): the stack measured — word fix+lazy tier bit-identical, D+fixed 50% on one binary; memo 0/3,245 hits and Carlson not a bind lever kill the 22%/10^5 endgame; ceiling measured ≈2.8e4.
- 20261014-0450-quant-1845 (silver, checker-extended): the fired kick is 46% bind, 45% the crash-tick bisection (~25 readouts, every kick and the dipping half of hand-outs); warm-start bracket priced −45%/kick.
- 20261014-1631-second-20261014-1511-quant-7226-2ae0 (gold): the guarded AB-IQI policy passes the frozen rule (worst 11–18, probes −62…−64%, flying leaver −34…−35%, digests identical at every layer); composed with the warm start, readouts −78…−83%, worst 11–12; the kill table regenerates from the patch.
- 20261016-1637-system-ff42 (this run, awaiting grade): the crash search and `at_radius` are one mechanism — the verified-guess wiring is tick-exact 36/36, 2.0× mean (3.2–4.9× where it verifies, ~40% fallback named with its cure); `next_exit`'s Cycle branch is the same lever unclaimed.
- 20261016-1740-second-20261016-1637-system-ff42-b583 (this run): the windowed guess retires the crash search — 100% fire, 0 fallbacks (155 synthetic + 2,723 flight searches), leaver kick −46…−48%, digests identical; policy layer's domain empty on main's scenes.
- 20261020-1621-system-7fd3 (this run, awaiting grade): the mint census — 20 reads/mint, history hits 1.05/mint at 100%; compile 26% of the rebind, the fit is the 74%.
- 20261012-2257-quant-32ab (silver): the sweep's L8+ stutter is the burn-input player-item waterfall on the O(N) scan, not the fixed tier; per-item cost flat in γ.
- 20261012-2257-spacex-5eb6 (silver): the lazy deletion built — quiet frame O(1) (1.35 µs flat to 2×10⁵, 10,872×; tie-storm and 25×-wander cases hold, checker), digests identical across arms and 15 schedules; sustained starvation breaks the fleet cap — one experiment from merge.
- 20261013-2252-system-ad26 (awaiting grade): one wall — the bind is 41–65% of every event-carrying item class; the four unmerged levers compose to 22% of the battle cost, ceiling ~10⁵ members; projection, composite unverified.
- 20261014-0000-second-20261013-2252-system-ad26-790b (second author): the stack measured — word fix+lazy tier bit-identical, D+fixed 50% on one binary; memo 0/3,245 hits and Carlson not a bind lever kill the 22%/10⁵ endgame; ceiling measured ≈2.8e4.
- 20261016-1637-system-ff42 (awaiting grade): the crash search and `at_radius` are one mechanism — the verified-guess wiring is tick-exact 36/36, 2.0× mean; `next_exit`'s Cycle branch is the same lever unclaimed.
- 20261016-1740-second-20261016-1637-system-ff42-b583: the windowed guess retires the crash search — 100% fire, 0 fallbacks (155 synthetic + 2,723 flight searches), leaver kick −46…−48%, digests identical; policy layer's domain empty on main's scenes.
- 20261020-1621-system-7fd3 (awaiting grade): the mint census — 20 reads/mint, history hits 1.05/mint at 100%; compile 26% of the rebind, the fit is the 74%.
- 20261020-1729-quant-077c (this run, awaiting grade): the compile-share contradiction adjudicated — e-crossing at ≈ 0.2 (plane 90%, belt 43% at `from_state`) plus a boundary difference; belt rebind has no single majority owner (readouts 30% > fit 26%).
- 20261020-1729-second-20261020-1621-system-7fd3-aa42 (second author): the checker's


