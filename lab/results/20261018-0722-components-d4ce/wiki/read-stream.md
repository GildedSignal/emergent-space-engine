topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261018-0722-components-d4ce

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best

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

**[20261017-2330-quant-588d] Direction 2's gate is measured: the fit-compile memo's sharing
is priced on flown inputs, and it splits three way — the exact `ShapeMemo` is dead on the
whole fit path (hit 0.0001 over 157k–180k cycle fits at N=3000/10⁴ coast), the 44-bit
`MemoCode` cell hits 0.936–0.971 at a per-body cell count (≈1.1–1.5 cells a body; the hit
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

**[20261017-1829-spacex-d399] The fit's mass decomposed stage by stage on flown belt inputs
(stage means per call: `fit_key` 4.03, `compile` 12.33 (49% of the stage sum), `at_radius`
1.16, `decoded_event` 3.67, `residual_between` 0.02, `bind_in: decode` 3.66 µs; total p50
17.2 µs), one of its three trajectory evaluations is measured dead (the residual the flown
path never reads; the delete is bit-identical on all cases, fit −18.6% ns/call, engine
~7%), and `at_radius`'s search hypothesis is refuted (the radius cut is closed form).**

**Prior bests retained (5eb2's kick-inside pricing, 6671's 64.5% shared-read census,
d959's by-site census) stand unchanged — see the page history in git.**

## Refuted

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

## Contradictions

- [Standing, unchanged: the three-instrument reads/body orders never cross-run on one
  binary; 5ade's spread-belt memo hit 0.029 vs the plane's 2.66–28× sharing (regime
  difference); a765/b063 rebind shares unengaged.]
- New, named: the prior micro (od 7: 4 × 22.4 ns per node) and this run's in-situ Δ
  (24.5 ns/node) are not in conflict — isolated latency vs pipelined in-situ cost; recorded
  so no future run prices a node by its isolated-op sum.

## Runs

- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site.
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside.
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured.
- 20261017-1829-spacex-d399 (awaiting grade): the fit decomposed; the residual delete.
- 20261017-2330-quant-588d (quant, awaiting grade): the fit-key census — exact dead, class
  sharing 99.2%.
- 20261018-0722-components-d4ce (awaiting grade): `fast_quad`'s four wide divisions flown
  as exact `div_word` — bit-identical everywhere, 0–15% in situ by load; the division slice dead as
  a compile lever.
