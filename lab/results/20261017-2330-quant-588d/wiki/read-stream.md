topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-2330-quant-588d

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best

**[20261017-2330-quant-588d] Direction 2's gate is measured: the fit-compile memo's sharing
is priced on flown inputs, and it splits three ways — the exact `ShapeMemo` is dead on the
whole fit path (hit 0.0001 over 157k–180k cycle fits at N=3000/10⁴ coast), the 44-bit
`MemoCode` cell hits 0.936–0.971 at a per-body cell count (≈1.1–1.5 cells a body; the hit
falls with N — checker: 0.861 at N=3×10⁴, still ~1.04 cells a body), and the
shape CLASS `QuantizedMemo` actually shares (17 bits on the weak branch) hits 0.978–0.992
across paces (rtf 600–1800) from 1,161–1,491 classes that saturate in N (1.22× classes for
3.3× bodies; checker: N=3×10⁴ coast 1,656 classes at hit 0.9926 — 1.11× classes for 3×
bodies — and burn N=3000 hit 0.9913 at 1,324), log-shaped
trail 1,160@32k→1,223@157k calls) — a population-level cache of ≈1.5–16 MB at N=10⁴
(`OrbitShape` 224 B + 88 B knots), three orders under any budget.** Boundaries never
re-enter `from_state` (P1 failed: their identical plans are carried state — confirming
kick-cadence 3570's no-op reading at the fit's own entry), so memo.rs's exact-key law
extends from kicks to every fit entry. Instrument: print-only env-gated census at
`from_state` (three levels: exact `ShapeKey`, `MemoCode`, `MemoCode::shape_bits`), patch =
work/patch.diff (also cfg-gates nladder's `proc_pid_rusage` so the ladder links on Linux);
controls: `ladder_digest "N=3000 coast through"` bit-identical pristine vs census-off vs
census-on (`d2632de90255f5c1…`, kicks 34537, encounters 934, contacts 0; no abort), and the
N=0 plane reproduces memo.rs's law at the new site (quant hit 0.9921, exact 0.0017)
[checker: digest-neutral also on `belt crossing L10` (N=1000/3000, incl. d399's `4995f384…`)
and `key mashing` (N=100/1000/3000), all bit-identical; and the boundary reading has a count
proof in the arms' own logs: cycles ≈ kicks (154,992 vs 154,043) while boundary events ≈ kicks
in count (152,489) — boundary events add no `from_state` fits]. Instrument artifact recorded:
inside `ladder_digest` the exact keys recur ≈96% between
schedules 2¹⁵→2¹⁶ (the same flight re-flown per schedule in one process) — cross-schedule
censuses inherit that recurrence; the arms are single flights. What stands between this
and a delete: the compile's shared-quadrature vs per-key glue split (unmeasured; the
12.33 µs compile is the ceiling), and the one law decision memo.rs owns — quantized key
(2⁻¹¹ period, known law change) vs `from_shape(exact key, quantized shape)` (exactness
unmeasured).**

**The fit's mass is now decomposed stage by stage on flown belt inputs, one of its three
trajectory evaluations is measured dead, and the page's direction-2 hypothesis is refuted:
`at_radius` is 1.1 µs (4% of the fit) — the fit's beyond-compile mass is the two time→psi
Newton solves (`decoded_event` 3.67 µs + `bind_in`'s `decode` 3.66 µs), and the first of
them computes a residual the flown path never reads** (20261017-1829-spacex-d399, spacex;
24,576 `bind_surface` inputs captured from the flown `N=3000` belt crossing and replayed;
instrument env-gated, digest-neutral — the bench's own flight reproduces pristine
`4995f384…`, kicks 40,106, bit for bit). Stage means per call: `fit_key` 4.03, `compile`
**12.33 (49% of the stage sum — correcting this page's "~26%": 5eb2's 4.4 µs median priced
`Orbit::compile` on belt-class keys, not on the keys the flight actually binds)**,
`at_radius` 1.16, `decoded_event` 3.67, `residual_between` 0.02, `bind_in: decode` 3.66,
turn+residual 0.34; total p50 17.2 µs. **The delete — skip
`fit.residual = Residual::between(state, fit.decoded_event()?)` (`binding.rs:447`; `bind_in`
builds its own residual from its own `decode`, and the universe reads only `trajectory`,
`periapsis_angle`, `periapsis_time`, `clockwise` from a fit; the residual's real consumer is
space's `TubeEvent::bind` → `reconstruct()`, off the plane's path) — is bit-identical on all
five `N=3000` ladder_digest cases (digests, kicks, encounters, contacts; four schedules per
case [checker: identity extends to all eight N=100/N=1000 cases, and a probe finds 0
`decoded_event` errors on the three heaviest N=3000 cases — the one corner where the arm
could bind where shipped refused]) and cuts the fit −18.6% ns/call (21,892→17,813) and the
wave flight's `bind_surface` 617.1→502.6 µs/frame [checker regen: −17.1%, 614.6→509.4 µs/frame,
21,785→18,054 ns/call; engine process −6.6%, p50 −6.8% — the −18.3% p50 was one pass, the
reproducible engine-level drop is ~7%, inside P2's predicted 3-8%]**; adoption is an API split
(~10 lines, residual opt-in for space's handoff path), no law change — the certificate is
the bit-identity. Next term named by the same table: the compile (49%) runs with **no
`ShapeMemo`** on `from_state`'s path, and the belt's 44-bit `MemoCode` keys make a shape-key
memo the next delete-class candidate (sharing rate on flown fit keys unmeasured
**[20261017-2330-quant-588d: now measured — see above]**).

**The redundancy of the per-event sources rebuild is now measured, and it is large: the
`(doll, tick)` key of `Ctx::secondaries` is shared 2.66×-7.81× in flight (64-89% of all
calls), so direction 1's shared field read is real — but priced in wall time it buys only
~8-10% of the belt kick, because the kick's own mass is the fit, and the fit's mass is not
the quadrature.** Print-only nested stages (`READOUT`, `SECONDARIES`) plus a `(doll, tick)`
census in `Ctx::secondaries` (digest-neutral: `ladder_digest` N=3000 bit-identical with the
patch, prof off) on the shipped plane (20261017-1447-components-5eb2, Linux/x86):
N=3×10⁴ rtf 600 — kick clock item 46.3 µs/call, `bind_surface` 20.9 µs at 1.00 calls/kick
(45%), `secondaries` 6.25 µs (13.5%, 0.97 calls/event), `readout` 3.77 µs (372 calls/frame);
census 84,254 calls at 31,652 distinct keys = **2.66× redundancy, 63.9% of calls at
multiplicity ≥ 2, 62.6% at ≥ 8, 42% at ≥ 64**; held-out N=10⁴ rtf 1800 — 51.6-52.9/30.4/5.35/4.84
µs, census **7.8-8.2× (89-90% at ≥ 2, two runs)**: the budget-sliced drain does NOT batch events at shared
ticks — the ticks are already shared and every event re-reads them. [d399's replay confirms
the wall shape on captured inputs: `bind_surface` p50 17.2 µs standalone.]

**The stream's shared-field premise is now measured from the inside: 64.5% of the
`secondaries`-driven `state_of` stream is bit-identical repetition — 169,145 of 262,198
calls repeat an exact (source, tick) key, 0 bit-conflicts anywhere — and the split is
structural, not uniform: the belt's birth wave is ONE field read evaluated 29,142 times
(j0/j1/j2 at t=0, 9,714 identical reads each, once per belt body), the locals' doll batches
naturally (its source read 112,277 times at 3,579 distinct ticks, 96.8% repeated, top 342×),
while the belt's kick comb does not batch at all (74% distinct ticks ex-birth) — so
direction 1's lever splits in two: a per-(j,t) memo in `Ctx` is bit-safe (mechanism:
bindings change only at the source's own events, resolved in tick order; measurement: 0
conflicts) and free (~1.7× on the N-linear `secondaries` term), but it cannot touch the
belt comb's structural 74%, whose cure is one canonical-tick field read per comb (BELT_SPLIT's
legality class) or the belt layer itself (20261017-1447-system-6671, system;
`nladder 10000 coast 60 600`, print-only census, digest-identical on `ladder_digest
"N=3000 coast through"` both arms).** Checker arms (20261017-1447 check): burn at 10⁴
(61.4% repeated, 0 conflicts, comb ex-birth 74.6% distinct), rtf 120 (77.9%, 0 conflicts)
and N=10⁵ (43.9% overall, 0 conflicts, same split) — the headline fraction is window-mix
dependent; the decomposition and the 0 conflicts are the invariants, over ~2.1M reads.

**The wave's read stream is censused by call site on shipped main, and its N-linear half is
60% the per-event `Ctx::secondaries` rebuild — not the player's scan** (20261017-0428-spacex-d959,
spacex; prior best retained: 5.0 readouts/body/event, 45,161 + 3·bodies `state_of` calls,
flight totals N-flat at 10⁴/10⁵, ~3×10⁸ lookups/s at 10⁹ — orders, three instruments).

## Refuted
- **"The exact `ShapeMemo` pays on the bind path" (this page's direction 2 as first imagined,
  and b139's reading before it): measured dead at `from_state` over ALL fit entries — exact
  hit 0.0001 at N=3000/10⁴ (157k–180k fits), and boundaries never re-enter `from_state` at
  all (their no-op plans are carried state); the only exact recurrence in a process is
  ladder_digest's own cross-schedule re-flight (≈96% between schedules, an instrument
  artifact, not flight structure) (20261017-2330-quant-588d).**
- **"If the repeated `state()` calls of `at_radius`'s binary search own the fit's residual
  mass, the refit's lever is a smarter search" (this page's direction 2 as hypothesized):
  `at_radius` has no search to speed — the radius cut is closed form (one division, one
  `acos`, one `quad`, one `read`) and measures 1.16 µs, 4% of the fit; the two time→psi
  Newton solves (`decoded_event`, `bind_in: decode`, 2.755 µs each at ~3 iterations) own
  the beyond-compile mass, and one of them is dead work in the flown path
  (20261017-1829-spacex-d399).**
- **"The quadrature is ~26% of the fit" (5eb2's share, from `Orbit::compile` on belt-class
  keys): on the keys the flight actually binds, compile is 12.33 µs of a 25.2 µs stage sum
  — 49% (20261017-1829-spacex-d399; the flown key mix, including word-rebind repeats, is
  heavier than the sampled belt-class keys).**
- **"Steady flight reads the field mostly alone at its tick"** (this page's own assumption
  under direction 1, and 5eb2's pre-registered prediction): measured wrong — 63.9% of
  secondaries calls share their `(doll, tick)` at rtf 600 pre-crest, 89.1% at rtf 1800 in
  the crest (20261017-1447-components-5eb2).
- **"The belt comb's shared ticks make the per-event rebuild a free batch"**: the belt's
  kick-time source reads are 74% distinct ticks ex-birth; only the locals' doll and the
  birth wave collide exactly (20261017-1447-system-6671).
- **b063's refit share (84-89% of the belt kick), read as `bind_surface` alone**: the fit
  is the largest term but 45-59% at the arms flown (20261017-1447-components-5eb2).
- **"The scan owns the burn read stream"** and **"the read stream is burn-specific"**
  (20261017-0428-spacex-d959).

## Open directions
1. **Adopt the dead-evaluation delete** (d399): an API split making `Rebinding`'s residual
   opt-in (the plane's `bind_in` never reads it; space's `TubeEvent::bind` does);
   bit-identity certificate already measured on all five `N=3000` cases (checker: plus all
   eight N=100/N=1000 cases), fit −18.6% ns/call, engine ~7% (regen; the author pass read
   −18.3% p50). Closed by checker probe: 0 `decoded_event` errors on the three heaviest
   N=3000 cases, all schedules — the error corner never fires in the corpus. Route
   `ending_at`'s success path too: it early-returns `from_state`'s fit, so surface binds
   (creation, kicks, handoffs) also lose the residual under the arm.
2. ~~**The compile's 49% with no memo**: measure shape-key sharing on flown fit
   inputs before designing anything.~~ **Measured** (20261017-2330-quant-588d): shape-class
   hit 99.2% at ~1.2–1.5k saturating classes (MB-scale), quant cell hit 0.936–0.971 at
   ~1.2–1.5 cells/body, exact dead (0.0001). What remains of the direction: (a) the
   compile's split — shared quadrature (`OrbitShape::bound`) vs per-key glue — which bounds
   the actual delete; (b) the law decision: quantized key (memo.rs's 2⁻¹¹-period change)
   vs `Orbit::from_shape(exact key, quantized shape)` (exactness unmeasured, the cheapest
   next probe if pursued); (c) the class count on a stirred/driven belt (the census never
   left the birth program's coverage).
3. **The second Newton solve** (`bind_in`'s `decode`, 3.66 µs): not dead — its output
   defines the residual the tube's later readouts are measured against — but it inverts the
   same elapsed time `at_radius` just produced (± the periapsis tick rounding); a shared
   warm start or a carried (psi, sum) is a representation question for the residual's
   reference frame, not a free delete.
4. **Adopt the (j,t) memo** (`Ctx`, keyed on exact ticks): 64.5% of the secondaries stream
   measured deletable, bit-exact by construction and by the 0-conflicts census; a
   stream/frame lever, not the kick's cure (watch: 5ade's spread-belt memo hit 0.029 — a
   different regime).
5. **Time `at_radius` and `decoded_event` directly** (5eb2's named probe): **done and
   closed by d399** — see Current best and Refuted.
6. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body): each is a read of the body itself; the
   lever is fewer events (cadence), not cheaper reads.
7. **Adopt `div_word` in `fast_quad`'s four wide divisions** (strong field: 4 × 22.4 ns →
   4 × 2.8 ns per node, exact by the primitive's contract): found and micro-measured,
   unflown — the belt path (`weak_quad`) already uses it.

## Contradictions
- promotion.md's b = 11.48 reads/body/20k gs (cache lookups, patched binary, 20k-gs horizon
  incl. post-wave), d959's 12.9 counted readouts/body at 14.6k gs, and 6671's 2.42
  `state_of`/event: three instruments, same order, never cross-run on one binary.
- 5ade's source memo on the spread belt (hit 0.029) and 5eb2/6671's 2.66-28× key sharing in
  the plane's steady/crest flight: same lever, different regimes (wave vs plane); unresolved
  until the cache is flown on both.
- a765's rebind share 84-87% beside b063's 84-89%: same tension, unengaged by these runs.

## Runs
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside; the
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured — 64.5%
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by call site.
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside.
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured.
- 20261017-1829-spacex-d399 (awaiting grade): the fit decomposed on flown inputs — one of
- 20261017-2330-quant-588d (quant, awaiting grade): the fit-key census — exact dead on the
  whole fit path (0.0001), shape class 99.2% at ~1.5k saturating classes (MB), quant cell
  0.936–0.971 at ~1.3 cells/body; boundaries never re-enter `from_state`; digest bit-identical.
