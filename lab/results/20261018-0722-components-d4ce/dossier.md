# Dossier — 20261018-0722-components-d4ce

**Lens:** first principles, one component at a time (the compile's per-node arithmetic).

**Claim:** the fast-path compile's four per-node wide `u128/u128` divisions are exactly
replaceable by the crate's own `div_word` primitive — bit-identical on every instrument
(75 crate tests, ~50k certified-bank rows, 5 ladder-digest cases × 4 schedules) — and the
cut it buys in situ is **~5% of the fast-path compile** (quiet-box paired probe: ns/panel
median 1216 → 1118, −8.1%, per-key p50 5.3%; the loaded regen pass reads 4.0%/2.0%),
not the ~25% the isolated micro-benchmark of read-stream od 7 implied: the division slice
is real but small, so the node's remaining ~280 ns (cos, isqrt, products, walker overhead)
is where the compile's next 10× lives, not arithmetic width.

## Bottleneck

The kick's fit (read-stream: `compile` = 12.33 µs of the 25.2 µs stage sum on flown keys,
49%; d399). Component: `fast_quad` (`crates/space/src/orbit.rs:401`), the quadrature every
compactness≠0 key walks, 4 nodes/panel, 4 wide divisions/node — read-stream od 7 found and
micro-measured them (4 × 22.4 ns → 4 × 2.8 ns) but never flew them. Expected gain: this run
measures it — the honest number is ~5–8% of strong compiles (engine frame: ~1–2% at most,
orders). What it deletes: the last "free arithmetic" lever on the compile's node, and the
od 7 reading that it was bigger.

## The exactness argument (why bit-identity is structural, not lucky)

At all four sites (`orbit.rs:429-433` shipped) the quotient is cast `as u64`; a truncating
cast would already be a shipped bug. For integers, quotient < 2⁶⁴ ⟺ `n>>64 < d`, which is
exactly `div_word`'s precondition (`num.rs:9`) — so the replacement is exact wherever the
shipped bits are defined. `a > 0` on every walked node (x > 0 is enforced at `orbit.rs:413`,
and x > 0 ⟹ cos > −k/(1−k) ⟹ a = 6k+2·ac > 4k ≥ 0), so no site wraps.
## Evidence (all from `regen.sh`; timings quoted from the quiet-box pass — the shared box
reprints them load-scaled, the bit-identity lines are load-independent)

- **Probe** (`strong_compile_probe`, new print-only example, (p, e) grid p ∈ 6.6–10⁶,
  e ∈ 0–0.99999; 94 keys compile, 14 refuse — refusals and panel counts **identical** in
  both arms, so the walk's decisions did not move):
  ns/panel median **1216 → 1118 (−8.1%)**, per-node 304 → 279 ns (Δ 24.5 ns/node);
  per-key compile cut p50 **5.3%**, p10 −0.2% (noise), p90 9.8%; 5-panel circles −7.7%.
- **Bit-identity:** all ten bank rungs (R0–R5, G22, G24, G24edge, FB; 22,092 + 22,400 +
  ~4.8k further rows) differ in **no column except compile-µs**; `ladder_digest "N=3000"`
  — all five cases, four schedules each, digests/kicks/encounters/contacts identical, and
  equal to the record's (`d2632de90255…`, `4995f384…`); 75 crate unit tests pass in
  release **and debug** (div_word's `debug_assert` is a live tripwire there — never fired).
- **Primitive sweep** (new test `div_word_matches_wide_on_composed_quotients`): 2M
  composed quotients n = d·q + r plus boundary-biased pairs, `div_word == n/d` everywhere,
  on top of the shipped digit-correction test.
- **In-situ corroboration on bank keys** (certified_bank col-10, compile µs): the patched
  arm is faster in 9–10 of ten rungs on both passes, biggest on the strong-grid rungs
  (regen pass: R4 29.9 → 25.4, G24 928.8 → 722.5, G24edge 1268.7 → 1159.5; quiet first
  pass: R3 1355.6 → 1306.0, R4 484.4 → 471.5); the column's absolute medians are
  load-sensitive on this shared box (one rung's baseline median moved 1355.6 → 53.3 µs
  between passes), so the bank's reproducible invariants are the 0-diff bit-identity and
  the sign; the probe supplies the magnitude.

## Predictions (predictions.md was written before the paired run)

- P1 exactness: **held** (all instruments above; no debug-assert fire; no refusal drift).
- P2 site cost: **held in direction, overestimated in situ** — Δ 24.5 ns/node measured
  against ~78 ns/node predicted from the isolated micro (4 × (22.4 − 2.8)); out-of-order
  overlap hides ~70% of the isolated-division latency inside the node's dependency chain.
- P3 compile cut 15–40% (point 20–30%): **failed** — measured 5.3% p50 per key (8.1% per
  panel). The naive serial-latency model of a node is the wrong cost model; the honest
  reading is that the four divisions were never 25% of this node.
- P4 engine: digests bit-identical (held); wall change inside noise, as predicted.

## What would make it wrong

A key whose node makes any of the four shipped `as u64` casts truncate (that corner breaks
div_word's precondition *and* is a pre-existing shipped bug). None found: 94 probe keys
(including p → 6+2e refusals, e = 0.99999, p = 10⁶), ~50k bank rows incl. whirls/passages,
and the full digest set. `word_root = false` keys (delta < 2⁶²/4) pay `num::isqrt`'s own
wide division inside Newton — untouched here, once per node, and on this grid unreachable
(delta ≥ 0.4 at p = 6.6); a deep strong-field sweep below delta = 1/4 is the one unflown
corner (the bank's whirl rows cover it only via refusals).

## Cost of adoption, and fit with PRINCIPLES

Four lines in `fast_quad` (`work/fastquad_divword.diff`), no canon change, no API change,
same bits by proof and by instrument. PRINCIPLES 16: "it's about what's cheapest to
compute"; the primitive's own contract ("any faster implementation must return the same
bits", `num.rs:1-2`) is the certificate. PRINCIPLES 1 (less is more): the deeper result is
via negativa — the division slice is now measured dead as a compile lever, which points the
compile's floor hunt at the node's other 280 ns and at 588d's shape-class memo (99.2% hit),
not at arithmetic.

## The lens (what it may have made me miss)

A component-floor reading can over-value a slice whose isolated cost is real but whose
in-situ cost is hidden by the pipeline; the instrument that caught it is the paired
in-situ probe, not the micro. The neighbours: the read stream and the panel count are where
the compile's mass actually is (5a3b's floor: 12–27 panels; the flown keys carry 130–294).
A run that prices the node's remaining 280 ns (cos table, u64 isqrt, multiply chain, knot
push) against a bit-exact restructure is the named next experiment.

## Commands (each ≤ 75 s, < 100 MB)

See `regen.sh` (~8 min total, both arms + tests + comparisons). Key single commands:
`strong_compile_probe` (65 s), `ladder_digest "N=3000"` (72 s), `certified_bank R4
--budget 60 --out DIR` (< 1 s per rung), `cargo test -p emergent-space` (10 s).
