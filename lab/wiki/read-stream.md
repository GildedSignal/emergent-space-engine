topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261018-1237-components-271c

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best

**[20261018-1237-components-271c] The compile node's last unpriced arithmetic slices (od 2's
isqrt pair) are priced with a bit-identical arm, and the arithmetic lane's ceiling is now
measured: a u128 Newton whose every step pays one hardware `div_word` (f64 seed of the full
operand, exact bounded floor correction) plus an f64-seeded u64 sqrt cut the shipped compile
−2.6% to −13.0% in situ across every key class — weak belt (the flight's belt path: census
`fast=false, word_root=false`, the compactness-zeroed weak branch, no per-node isqrt at all)
−2.6/−6.4/−3.4%; planet/strong `word_root=true` −8.1 to −10.5%; the `word_root=false` band
(p ∈ (6+2e, ~8+2.7e), delta ∈ [2.3×10⁻¹⁰, ¼]) −8.1 to −8.4%; held-out near-separatrix
e 0.56–0.96 −7.9% to −13.4% [checker: the quoted −10.5 floor covered only
the word_root=true rungs; the sweep's first two (word_root=false) sit at −7.93/−8.24] —
bit-identical on every instrument (3×10⁶ fuzz operands
0 mismatches, 34/34 compile hashes MATCH, 74 crate tests, refusals included) — with
isolated slice prices wide 110.6→80.6 ns (−27%) and std u64 27.8→10.0 ns (−64%), so
roughly half to two-thirds of the isolated gain is OoO-absorbed in situ (d4ce's division
lesson generalises, with a measurable residue). Census facts (new): the belt compile's
isqrt bill is per-compile (5–24 wide calls, ~2.05 Newton iterations each), growing with
crossings (cut() → ratio_sqrt → isqrt), not knots; the per-node wide isqrt lives only in
the razor-thin word_root=false band; std's u64 isqrt runs per node on every fast
word_root=true key. Consequence for od 2: with division (0–15%, d4ce) and isqrt (≤13%,
this run) both priced and the cos law-owned (its nested-floored value IS the bits), NO
bit-exact arithmetic lever above ~13% remains in the node — adopt as cleanup (~60 lines,
no law change), and the compile's 10× levers stay where 0355 put them: structural (class
memo, a law change) or node count (a law change). The instrument's one unflown corner:
the slow `node()` path (delta < 2^30) is unreachable through `bound(p,e)` at integer p
and was not timed (Linux/x86, load recorded, orders of magnitude).**

**[20261018-0722-quant-0355 — retained; the conflicting sides reconcile: d4ce prices the
node's division slice dead (0–15% by load), this run prices its isqrt pair at ≤13%, and
0355's class memo remains the compile's structural lever.]** Direction 2's two halves are
measured on the flown key mix, and the memo verdict is now a priced law decision, not an
open question: the compile is 92.3% shared quadrature (`OrbitShape::bound` 5,451 of 5,906
ns; `from_shape` glue 454 ns), so a class-keyed shape cache deletes ~85% of the compile
term at a 0.40 µs hit price — and `from_shape(exact key, class shape)` moves the clock
increments by p50 1.9×10⁻⁶ / p99 1.7×10⁻⁴ relative (period, τ, advance alike), 61× less
than the shipped quantized-key arm's p50 1.2×10⁻⁴ (memo.rs's 2⁻¹¹ law change), mechanism
the class's k quantum at ~half the Newtonian sensitivity 3k/(2k−1) (measured/predicted
0.53). So the exact-key form is NOT a bit-exact delete (bits move at almost every key) —
it is a law change two orders cheaper in error than the shipped alternative, at 7% of a
compile per hit. Instrument: keys captured at `Orbit::compile` entry from `ladder_digest
"N=3000 coast through"` (148,996 compiles, 0 errors; digest bit-identical pristine vs
capture-on: `d2632de90255f5c1…`, kicks 34537), bench `compmemo` (interleaved arms, second
execution within 1%; controls both sides: identity path 0/500 bit mismatches; wrong-class
negative p50 1.6–2.1×10⁻³ run-varying, ~1000× the signal). Census reproduces 588d: 37,245
distinct keys / 37,230 shape keys (exact repeat 4×10⁻⁴ on the unique stream — exact is
dead), 1,163 classes, hit 0.9922 stream / 0.9688 unique-stream. Unmeasured before any
adoption: the READOUT half (measured by the checker at 8 phases on all three mixes: C
radius p50 ~1×10⁻⁶ / p99 ~2×10⁻⁴, angle p50 ~2×10⁻⁷ turns — the clock order carries to
positions, C ~100× under B at p50, ~2× at p99), the class-centre representative, and the
class count on a stirred/driven belt (`key mashing` N=3000: 1,831 classes, hit 0.927;
`belt crossing L10` N=3000: 1,389 classes, hit 0.992, C p50 2.3×10⁻⁶). The wiring is one
line in `QuantizedMemo::get` + the identity check scoped to the exact path; the legality
flight is a B-gate-class decision (the integrator's).

**[20261018-0722-components-d4ce — retained, unchanged: `div_word` in `fast_quad` is
bit-identical everywhere and worth 0–15% by load; the node's remaining ~280 ns and the
shape-class memo are the levers; arithmetic width is not. See the standing text in git
for the full entry; this run closes its named isqrt half.]**

## Refuted

- **"Adopt `div_word` in `fast_quad`'s four wide divisions" as a compile lever of the
  micro's size (~25% of the node): exact and free but worth 0–15% per key depending on
  load — the isolated-division latency is mostly hidden by out-of-order execution inside
  the node (20261018-0722-components-d4ce).**
- **"The node's isqrt slices are a ≥25% lever" (this run's own P3) and "no bit-exact
  arithmetic lever ≥ 10% remains" (its kill criterion): both wrong in opposite
  directions — the arm is real, bit-identical, and worth −2.6% to −13.0% of compile in
  situ (best on eccentric strong keys), with the isolated −27%/−64% gains half-to-two-
  thirds OoO-absorbed (20261018-1237-components-271c).**
- **"Std's `u64::isqrt` could be ≥ 20% of the belt compile node" (P4's alternative
  reading): the belt node has no isqrt at all — the belt compiles on the weak branch
  (compactness zeroed at q ≤ 2⁻¹⁸, `fast=false`), and its isqrt bill is per compile
  (5–24 wide calls), not per node (20261018-1237-components-271c).**

## Open directions

1. [d399's delete stands: adopt the residual API split — bit-identity already measured on
   all cases; route `ending_at`'s success path too. This run adds a sibling cleanup:
   the isqrt arm, ~60 lines, bit-identity proven the same way.]
2. **The compile's structural levers, now the only 10× class left in it: 0355's
   class-keyed shape memo (a law change at p50 1.9×10⁻⁶ error, 61× cheaper than the
   shipped quantized key — the integrator's B-gate decision) and the node count (a law
   change). The arithmetic lane is closed at ≤13%: cos is law-owned bits, division and
   isqrt are priced. The one unflown arithmetic corner: the slow `node()` path
   (delta < 2^30) needs `from_invariants`-class keys to reach.**
3. [The readout half and read-amortization questions stand as before — see the page
   history in git for 4ea0's census and e106's Carlson wiring refutation.]

## Contradictions

The 0722 three-way (d4ce vs 0355 vs the merge conflict on this page) resolves: d4ce's
"the levers are the node's remaining ~280 ns and the memo" splits into isqrt (≤13%, this
run) and multiply-chain/push (law-owned or bandwidth-priced, ceb2), while 0355's memo
share stands. No live conflict.

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
- 20261018-1237-components-271c (components, awaiting grade): the isqrt pair priced —
