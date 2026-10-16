# Dossier — 20261016-2229-quant-7343 (Quant lens)

## Claim

The in-belt scan read is decomposed on shipped code: **89% of the 3.7 µs is the tube solve's
own arithmetic (`entry.trajectory.state`), warm≈cold with 7-knot tables, so no deletion of
wrappers, packing or layout can reach even 2× — the "~50× cheaper reads" cure is dead on the
shipped representation, and the belt band's live cures are not-reading (phase-neighbour rank,
population answer) or a re-certified readout law.**

## Bottleneck

`scan-queue`, the answer half in the belt band (the page's open direction 1): 3999 measured
S = (N−314)·4.2 µs and named three ways out — certificate (done by 1250, insufficient
in-band), ~50× cheaper reads, phase-neighbour rank. This run prices the second: it decomposes
the per-read cost stage by stage, which no run had done (cdf0 timed the whole read). Expected
gain: kills one of three candidate cures and redirects the effort (a 10×-class decision, not a
10× speedup).

## Evidence

Print-only probe `crates/universe/examples/read_split.rs` (in `work/patch.diff`; no engine
line touched) on the shipped decision path (`encounter.rs` verbatim: window, fallback walk,
filter, `answer`). Belt bodies of `plane_extra`, root doll, t = 256, one thread. All arms:

| arm | fallback | candidates | answer | µs/read | traj µs (share) | pred | p99/p50 | addr-order Δ |
|---|---|---|---|---|---|---|---|---|
| 10⁴ s1 lo/mid/hi | yes ×3 | 9714 | 37.0–38.8 ms | 3.81–3.92 | 3.28–3.37 (87–90%) | 0.17–0.20 | ≤1.68 | <1% |
| 10⁴ s2 lo | **no** (kept 1055) | 1054 | 4.14 ms | 3.93 | 3.16 (89%) | 0.15 | 1.25 | <1% |
| 10⁴ s2 mid/hi | yes | 9714 | 37.3–38.8 ms | 3.84–3.99 | 3.31–3.35 | 0.19 | ≤1.30 | <1% |
| 10⁵ s1 lo/mid/hi | yes ×3 | 99714 | 385–399 ms | 3.86–4.00 | 3.34 (89%) | 0.19–0.21 | ≤1.52 | <1% |
| 10³ s1 lo/hi | **no** (kept 113/87) | 112/87 | 0.39–0.41 ms | 3.68–4.45 | 3.04–3.08 | 0.15 | ≤1.20 | <1% |
| 10³ s1 mid | yes | 714 | 2.58 ms | 3.61 | 3.08 | 0.16 | 1.06 | <1% |

Stage medians at 10⁴ s1 mid (ns/read): binding_at 66; **traj 3365**; decode−traj (unit/time
conversions) ~340; turn+fit (readout−decode) ~0 (≤1%); Scalar wrap (cartesian−readout) ~85
(2.3%); integer predicate 186 (5%). **Everything except the tube solve totals ≈ 0.45 µs
(12%).**

- **Compute-bound, not memory:** warm re-read p50 3.19–3.32 µs vs cold 3.4–3.7 µs (1.10–1.15×);
  knot tables are tiny (7.0–8.5 knots, 3.3–5.6 crossings mean); every candidate carries its own
  compiled `Entry` (distinct = candidates, 99714/99714 at 10⁵) — nothing to share, nothing to
  keep hot: the cost is the wide-integer readout arithmetic itself.
- **The arithmetic floor:** one checked Scalar `mul` = 3.27 ns, so the 3.3 µs solve is ~10³
  mul-equivalents — structural (panel evaluation, integer cos/atan, mul_shr chains in
  `space/src/lib.rs::Cycle::state`), not a wrapper tax. [op-mix inferred from code; the split
  around it is measured]
- **Reproduction:** 3999's belt-bin numbers regenerate — 2.58 ms at 10³ (theirs 2.9–3.1),
  37–40 ms at 10⁴ (41), 385–399 ms at 10⁵ (415–419); 0 encounters in every arm; per-read
  3.6–4.5 µs everywhere, regime- and N-independent (kept-88 arm ≈ fallback arm).
- **New term, small:** the capture **reuse** walk (the memo hit's price) re-walks and
  re-compares the whole candidate list before `same_inputs` returns it: 23 µs (10³), 2.1–3.1 ms
  (10⁴), 30–33 ms (10⁵) — at 69f3's λ = 14.4 mints/s (half duplicates) that is ~0.5 s/s of wall
  at 10⁵ for answers it already holds.
- **Band edges leak** (held-out, honest miss): out-of-band windows kept 87–1055 bodies, not
  3999's "3–7 outside the band" — my lo/hi picks (r ≈ 1.66–1.73, 2.9 AU) sit in partial
  windows whose edges move with N and seed; per-read cost there is unchanged, so the
  decomposition is unaffected.

### Reproduce

```
git apply work/patch.diff
cargo run --release -q -p emergent-universe --example read_split -- 10000 8 1   # ~13 s
cargo run --release -q -p emergent-universe --example read_split -- 10000 8 2   # held-out seed
cargo run --release -q -p emergent-universe --example read_split -- 100000 2 1  # ~10 s
cargo run --release -q -p emergent-universe --example read_split -- 1000 8 1
```
(all under 60 s each on this box, after a one-off `cargo build --release` of the workspace;
`regen.sh` does exactly this).

## Predictions

`predictions.md` was written before the decisive run. **P1 held** (fallback, 0 encounters,
3.5–5 µs/read, 3999 regenerated). **P2 held, stronger** (traj > 55% predicted, 87–90%
measured; wrapper+fit+predicate ≈ 12%). **P3 held** (p99/p50 ≤ 1.68; address order < 1%
off). **P4 held with the floor lower than guessed** (Scalar mul 3.27 ns vs the predicted
5–20: the read is ~10³ ops, not ~10²; warm≈cold kills the last layout hope). **P5 split:**
per-read regime-independence held in every arm; "out-of-band keeps < 10" inverted (kept
87–1055) — the band edges are fuzzy windows, not a cliff.

## What would make it wrong

Timings are Linux/x86 on a shared box (orders of magnitude; the M1 re-measures) and single
runs per arm — but every claim rests on ratios (stage shares, warm/cold, order-invariance)
that repeated across 3 probes × 2 seeds × 3 N to within a few percent. The op-mix *inside*
`traj` is read from the code, not per-op measured; if `Cycle::state` hides an avoidable
serialisation the 89% share stands but the "structural" reading would need a rung. If the
integrator adopts a different readout law (a certificate question), the shares move with it.

## Cost of adopting

Nothing to adopt in the engine: this is a kill (one of three named cures) plus a redirect —
effort goes to the phase-neighbour rank or a population answer, both already on the page; and
one cheap named hygiene fix, the reuse walk (memo the candidate list per (body, t, interval)
instead of re-walking N bodies per duplicate mint), worth ~0.5 s/s at 10⁵ under burn, an
outcome-free scheduler-side change for the integrator to judge.

## Fit with PRINCIPLES

- "the cheapest compute is compute not done" — the read is re-derived physics per candidate
  per answer; the rank certificate is the compute-not-done.
- "we just need to have the right representation so that math is trivial" — measured: on this
  representation the readout math is ~10³ wide-integer ops and no deletion reaches 2×; a
  trivial-math readout would be a representation change, priced here at its full 89%.
- Lens blind spot checked: this Quant run prices nanoseconds, but its verdict sends the work
  away from shaving them (the wrappers) toward deleting reads — the simplicity the lens
  cannot price is what it recommends.

## The lens

Quant timing can miss law-level structure: I priced the readout as a latency budget and did
not question whether the answer needs cartesian readouts at all (a phase-space test on the
key could skip the solve entirely — that is 3999's rank direction, and this run's numbers
make it the only live one). Canaries/multiple-testing: one probe, pre-registered, no variant
swept before the pass; the stage split is confirmatory, not selected post hoc.
