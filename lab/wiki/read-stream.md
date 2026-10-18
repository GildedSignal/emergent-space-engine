topic: read-stream
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261018-0722-components-d4ce
=======
updated: 20261018-0722-quant-0355
>>>>>>> 20261018-0722-quant-0355

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best

<<<<<<< main
**[20261018-0722-components-d4ce] The compile's per-node arithmetic is measured in situ, and
the division slice is dead as a lever: replacing `fast_quad`'s four per-node wide `u128/u128`
divisions with the crate's own exact `div_word` primitive (the `as u64` casts at the sites
are themselves the precondition proof: quotient < 2⁶⁴ ⟺ n>>64 < d) is bit-identical on every
instrument — 75 crate tests (release and debug, div_word's asserts live), ~50k certified-bank
rows across all ten rungs (no column moves but compile-µs), five `ladder_digest` cases × four
schedules (digests and counters equal to the record's `d2632de90255…`/`4995f384…`) — and it
cuts the fast-path compile by far less than the ~25% the isolated micro of od 7 implied
(4 × 22.4 → 2.8 ns). Checker, who re-ran the pair three ways: the in-situ magnitude is
load-dependent and no single number is stable — four passes of the same paired instrument
span 0–15% per key (author quiet pass p50 5.3%, ns/panel 1216 → 1118; author regen 4.0%;
runner regen 9.3%, ns/panel 1373 → 1165, banks 10/10 faster with R2 −10.8%, R5 −5.3% — so
the author's "R2/R5 unchanged" holds only on their own pass; checker's clean drift-controlled
triple reads probe p50 0.8–0.9% with the patched arm 1–2% slower per panel, and clean
strong-rung banks are mixed: G24edge −1.3%, G24 +0.1%, R4 +5.9%). The author's quiet-pass
CSVs were overwritten by regen, so 5.3%/8.1% is not regenerable from the artifacts. The
load-independent facts: the bit-identity everywhere, and every pass far under 25% — adopt as
an exactness-preserving cleanup (four lines, `work/fastquad_divword.diff`, no canon change),
book no speed gain. Checker additions: bit-identity extends to 180 dense near-separatrix keys
(p = (6+2e)(1+t), t ∈ [3×10⁻¹⁰, 10³], e ≤ 0.99999 — the word_root = false band, hashed
full compile outputs), to `N=1000 belt crossing` (`ef19d3de…`), and to a div_word sweep on
the four sites' exact operand shapes at the precondition boundary; exactness is structural
on the whole compiled domain (fast gate delta ≥ 2³⁰ forces root ≥ 2⁴⁶; the separatrix
refusal forces horizon > 2⁶¹; floor ≤ x on every walked node), not merely sampled.**
Consequence for the compile's floor hunt: the node's remaining ~280 ns (cos, isqrt, the
multiply chain, knot push) and 588d's shape-class memo (99.2% hit) are the levers; arithmetic
width is not.
=======
**[20261018-0722-quant-0355] Direction 2's two halves are measured on the flown key mix, and
the memo verdict is now a priced law decision, not an open question: the compile is 92.3%
shared quadrature (`OrbitShape::bound` 5,451 of 5,906 ns; `from_shape` glue 454 ns), so a
class-keyed shape cache deletes ~85% of the compile term at a 0.40 µs hit price — and
`from_shape(exact key, class shape)` moves the clock increments by p50 1.9×10⁻⁶ / p99
1.7×10⁻⁴ relative (period, τ, advance alike), 61× less than the shipped quantized-key arm's
p50 1.2×10⁻⁴ (memo.rs's 2⁻¹¹ law change), mechanism the class's k quantum at ~half the
Newtonian sensitivity 3k/(2k−1) (measured/predicted 0.53).** So the exact-key form is NOT a
bit-exact delete (bits move at almost every key) — it is a law change two orders cheaper in
error than the shipped alternative, at 7% of a compile per hit. Instrument: keys captured at
`Orbit::compile` entry from `ladder_digest "N=3000 coast through"` (148,996 compiles, 0
errors; **digest bit-identical pristine vs capture-on: `d2632de90255f5c1…`, kicks 34537**),
bench `compmemo` (interleaved arms, second execution within 1%; controls both sides: identity
path 0/500 bit mismatches; wrong-class negative p50 1.6–2.1×10⁻³ run-varying, ~1000× the signal).
Census reproduces 588d: 37,245 distinct keys / 37,230 shape keys (exact repeat 4×10⁻⁴ on the
unique stream — exact is dead), 1,163 classes, hit 0.9922 stream / 0.9688 unique-stream (the
stream rate inherits ladder_digest's 4-schedule re-flight artifact 588d flagged; the
replayed-stream `ShapeMemo` hits 111,766 are that artifact, not flight structure). Unmeasured
before any adoption: the READOUT half (position interpolation on the representative's knots —
first order in the shape difference, only partly absorbed by the bind residual), the
class-centre representative (first-seen used; centre halves the error), and the class count on
a stirred/driven belt (588d's corner) [checker, 0355 check: both probed — `key mashing`
N=3000: 1,831 classes, stream hit 0.927, unique-stream 0.708 (sharing degrades, cache still
viable), exactness survives (C p50 3.5×10⁻⁷, p99 2.1×10⁻⁴); `belt crossing L10` N=3000:
1,389 classes, hit 0.992, C p50 2.3×10⁻⁶, split 92%; and the readout half measured at 8
phases via public `state()` on all three mixes: C radius p50 ~1×10⁻⁶ / p99 ~2×10⁻⁴, angle
p50 ~2×10⁻⁷ turns — the clock order carries to positions, C ~100× under B at p50, ~2× at
p99]. The wiring itself is one line in
`QuantizedMemo::get` (pass the exact input key to `from_shape`) + the identity check scoped
to the exact path; the legality flight is a B-gate-class decision (the integrator's).
>>>>>>> 20261018-0722-quant-0355

**[20261017-2330-quant-588d] Direction 2's gate is measured: the fit-compile memo's sharing
is priced on flown inputs, and it splits three way — the exact `ShapeMemo` is dead on the
whole fit path (hit 0.0001 over 157k–180k cycle fits at N=3000/10⁴ coast), the 44-bit
`MemoCode` cell hits 0.936–0.971 at a per-body cell count (≈1.1–1.5 cells a body; the hit
<<<<<<< main
falls with N — checker: 0.861 at N=3×10⁴, still ~1.04 cells a body), and the shape CLASS
`QuantizedMemo` actually shares (17 bits on the weak branch) hits 0.978–0.992 across paces
(rtf 600–1800) from 1,161–1,491 classes that saturate in N — a population-level cache of
≈1.5–16 MB at N=10⁴, three orders under any budget.** Boundaries never re-enter
`from_state` (their identical plans are carried state), so memo.rs's exact-key law extends
from kicks to every fit entry. What stood between this and a delete: the compile's
shared-quadrature vs per-key glue split (unmeasured; the 12.33 µs compile is the ceiling)
and the one law decision memo.rs owns (quantized key vs `from_shape(exact key, quantized
shape)`). [20261018-0722: the compile's own node cost is now half-measured — its division
slice is 0–15% by load (checker), so the glue split and the memo are where the 12.33 µs actually falls.]
=======
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
censuses inherit that recurrence; the arms are single flights. What stood between this
and a delete: the compile's shared-quadrature vs per-key glue split (unmeasured; the
12.33 µs compile is the ceiling), and the one law decision memo.rs owns — quantized key
(2⁻¹¹ period, known law change) vs `from_shape(exact key, quantized shape)` (exactness
unmeasured). **[0355: both halves now measured — see above: split 92/8, exactness p50
1.9×10⁻⁶, a law change 61× cheaper than the quantized key, not a bit-exact delete.]**

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
>>>>>>> 20261018-0722-quant-0355

**[20261017-1829-spacex-d399] The fit's mass decomposed stage by stage on flown belt inputs
(stage means per call: `fit_key` 4.03, `compile` 12.33 (49% of the stage sum), `at_radius`
1.16, `decoded_event` 3.67, `residual_between` 0.02, `bind_in: decode` 3.66 µs; total p50
17.2 µs), one of its three trajectory evaluations is measured dead (the residual the flown
path never reads; the delete is bit-identical on all cases, fit −18.6% ns/call, engine
~7%), and `at_radius`'s search hypothesis is refuted (the radius cut is closed form).**

**Prior bests retained (5eb2's kick-inside pricing, 6671's 64.5% shared-read census,
d959's by-site census) stand unchanged — see the page history in git.**

## Refuted
<<<<<<< main

- **"Adopt `div_word` in `fast_quad`'s four wide divisions" as a compile lever of the
  micro's size (od 7's 4 × 22.4 → 2.8 ns reading, ~25% of the node): exact and free but
  worth 0–15% per key depending on load (author quiet 5.3%, runner regen 9.3%, checker clean
  0.9%) — the isolated-division latency is mostly hidden by
  out-of-order execution inside the node (20261018-0722-components-d4ce).**
- [Standing refutations of 588d, d399, 5eb2, 6671, d959 unchanged: exact `ShapeMemo` dead
  on the bind path (hit 0.0001); `at_radius` has no search to speed (1.16 µs, 4%); compile
  is 49% of the fit stage sum on flown keys (not ~26%); steady flight does NOT read the
  field mostly alone (63.9–89% share their (doll, tick)); the belt comb's kick-time reads
  are 74% distinct ticks ex-birth; the scan does not own the burn read stream; b063's
  refit-share reading.]

## Open directions

1. [d399's delete stands: adopt the residual API split — bit-identity already measured on
   all cases; route `ending_at`'s success path too.]
2. **The compile's node mass (new, from 20261018-0722): the division slice is measured dead
   (0–15% by load, checker); price the remaining ~280 ns/node — cos table reads, the u64 `isqrt` (and
   `num::isqrt`'s own wide Newton division on the `word_root = false` side, delta < 2⁶²/4,
   unflown below p ≈ 6.6-class keys), the multiply chain, the per-knot push — against a
   bit-exact restructure, beside 588d's shared-quadrature-vs-glue split and the shape-class
   memo (the two composition levers on the same 12.33 µs).**
3. [d399's second Newton solve direction stands: a representation question for the
   residual's reference frame, not a free delete.]
4. [6671's (j,t) memo adoption stands: 64.5% of the secondaries stream deletable,
   bit-exact.]
5. ~~**Adopt `div_word` in `fast_quad`'s four wide divisions** (micro-measured 4 × 22.4 →
   2.8 ns, unflown).~~ **Flown and closed** (20261018-0722-components-d4ce): exact
   (bit-identity on tests, ~50k bank rows, all digests; the `as u64` casts prove the
   precondition), worth 0–15% by load (book nothing), four lines, no canon change — adopt as a
   free exactness-preserving cleanup; do not book it as a compile lever.
6. [The clock step's and scheduler's per-body reads: cadence's page, unchanged.]
7. ~~`fast_quad`'s divisions~~ — was od 7; closed by this run (see 5).
=======
- **"The exact `ShapeMemo` pays on the bind path" (this page's direction 2 as first imagined,
  and b139's reading before it): measured dead at `from_state` over ALL fit entries — exact
  hit 0.0001 at N=3000/10⁴ (157k–180k fits), and boundaries never re-enter `from_state` at
  all (their no-op plans are carried state); the only exact recurrence in a process is
  ladder_digest's own cross-schedule re-flight (≈96% between schedules, an instrument
  artifact, not flight structure) (20261017-2330-quant-588d; unique-stream reproduction in
  20261018-0722-quant-0355: 4×10⁻⁴).**
- **"The exact-key form of the class memo might be a bit-exact delete" (direction 2's open
  half as hoped): measured a law change — p50 1.9×10⁻⁶ relative on period/τ/advance, p99
  1.7×10⁻⁴, bits move at almost every key; what it buys is a 61× smaller law change than
  the shipped quantized-key memo at a 0.40 µs hit against a 5.9 µs compile
  (20261018-0722-quant-0355).**
- **"The readout half moves with the clock half" — NOT measured; the increments census is
  the clock half only, position interpolation on the representative's knots is unmeasured
  (domain note, 20261018-0722-quant-0355).**
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
   inputs before designing anything.~~ **Measured and split** (588d + 0355): shape-class
   hit 99.2% at ~1.2–1.5k saturating classes (MB-scale), quant cell hit 0.936–0.971 at
   ~1.2–1.5 cells/body, exact dead; the compile is 92.3% shared quadrature (glue 454 ns),
   so the cache deletes ~85% of the compile at a 0.40 µs hit. **What remains is a law
   decision with numbers on both sides**: exact-key + class shape = clock law change p50
   1.9×10⁻⁶ / p99 1.7×10⁻⁴ (61× under the shipped 2⁻¹¹ arm at p50, 3.2× at p99 — tails
   decide), wiring one line in `QuantizedMemo::get`. Before it: (a) the readout-half
   census (position error on the representative's knots at N phases); (b) the class-centre
   representative (halves the error); (c) the class count on a stirred/driven belt.
3. **The second Newton solve** (`bind_in`'s `decode`, 3.66 µs): not dead — its output
   defines the residual the tube's later readouts are measured against — but it inverts the
   same elapsed time `at_radius` just produced (± the periapsis tick rounding); a shared
   warm start or a carried (psi, sum) is a representation question for the residual's
   reference frame, not a free delete.
4. **Adopt the (j,t) memo** (`Ctx`, keyed on exact ticks): 64.5% of the secondaries stream
   measured deletable, bit-exact by construction and by the 0-conflicts census; a
   stream/frame lever, not the kick's cure (watch: 5ade's spread-belt memo hit 0.029 — a
   different regime).
5. ~~**Time `at_radius` and `decoded_event` directly** (5eb2's named probe)~~: **done and
   closed by d399** — see Current best and Refuted.
6. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body): each is a read of the body itself; the
   lever is fewer events (cadence), not cheaper reads.
7. **Adopt `div_word` in `fast_quad`'s four wide divisions** (strong field: 4 × 22.4 ns →
   4 × 2.8 ns per node, exact by the primitive's contract): found and micro-measured,
   unflown — the belt path (`weak_quad`) already uses it.
>>>>>>> 20261018-0722-quant-0355

## Contradictions

- [Standing, unchanged: the three-instrument reads/body orders never cross-run on one
  binary; 5ade's spread-belt memo hit 0.029 vs the plane's 2.66–28× sharing (regime
  difference); a765/b063 rebind shares unengaged.]
- New, named: the prior micro (od 7: 4 × 22.4 ns per node) and this run's in-situ Δ
  (24.5 ns/node) are not in conflict — isolated latency vs pipelined in-situ cost; recorded
  so no future run prices a node by its isolated-op sum.

## Runs
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside; the
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured — 64.5%
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site.
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside.
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured.
- 20261017-1829-spacex-d399 (awaiting grade): the fit decomposed on flown inputs — one of
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by call site.
- 20261017-2330-quant-588d (quant, awaiting grade): the fit-key census — exact dead on the
- 20261017-1829-spacex-d399 (awaiting grade): the fit decomposed; the residual delete.
- 20261017-2330-quant-588d (quant, awaiting grade): the fit-key census — exact dead, class
- 20261018-0722-components-d4ce (awaiting grade): `fast_quad`'s four wide divisions flown
- 20261018-0722-quant-0355 (quant, awaiting grade): the memo's halves measured — compile 92% shared quadrature, exact-key form a 61×-smaller law change (p50 1.9e-6), not a bit-exact delete
