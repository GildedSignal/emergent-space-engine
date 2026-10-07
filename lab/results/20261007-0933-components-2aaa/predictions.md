# Predictions — run 20261007-0933-components-2aaa

Component: the event queue ("one clock, one queue", plane.md foundation 2). Current design:
`crates/space/src/events/calendar.rs` — a 4-ary **indexed heap**, one slot per body, keys
inline `(Scalar, u32)` plus a separate `pos: Vec<u32>` backpointer array (≈20 B/entity).

Candidate floor design: a **hierarchical timing wheel** on root-clock integer ticks
(world.md: "a queue of ticks needs no conversion"), intrusive doubly-linked buckets,
deterministic `(tick, id)` order kept by draining a whole due-tick bucket and delivering
sorted by id. Power-of-two levels mirror the doll clock exponents.

Workload (the engine's op mix): every slot holds exactly one pending deadline; each pop is
followed by re-inserting that slot at `t + interval` (intervals fixed per body, log2-uniform
— doll exponents are powers of two). This is the universe's cancel+requeue pair per event.

## Pre-registered expectations (not tuned on)

Machine: GitHub Actions Linux x86, 8 vCPU. Orders of magnitude only.

1. **heap4 mean cost grows with N** (cache misses along the sift path + random `pos[]`
   writes per swap): roughly ~15–40 ns/op at N ≤ 10⁶ (working set ~20 MB, near L3),
   rising to ~150–500 ns/op at N = 3×10⁷ (600 MB, DRAM-bound).
2. **wheel stays flat**: ~10–30 ns/op across all N (≈3–5 random touches per op:
   link/unlink + drained slot), plus an amortized sort cost that grows only with
   events-per-tick density (narrow distribution).
3. **Idiot index** (heap4 ÷ wheel, median over seeds): ≥ 5× at N = 3×10⁷; between
   1× and 2× at N ≤ 10⁵ (heap fits in cache). The crossover sits around N ≈ 10⁶.
4. **heap2 (binary control) is 1.3–2× worse than heap4 everywhere** — if not, my heap
   implementations or harness are broken and the run is VOID.
5. **Tails (p99 of 64-op batches):** heap4's p99/median ≤ 1.5 (cost is a near-uniform
   walk); wheel's p99/median ≥ 2 in the wide distribution (cascade bursts land in a few
   batches). The wheel trades a fatter per-op tail for a 5× lower median — relevant to
   PRINCIPLES #12 and worth reporting either way.
6. **Density (narrow intervals, 2^10–2^14):** mean chain per due tick ≈ N×2⁻¹²; at
   N = 10⁷ that is ~2,500 events/tick. The wheel's batch drain must stay under
   ~2× its wide-distribution cost; if chain sorting dominates, the wheel loses its
   advantage exactly where the engine is densest, and that kills the design at scale.

## Kill criterion (written before the run)

If heap4 ≤ 2× wheel at N = 3×10⁷ on the median seed of both distributions, the component
is already within a small factor of its floor: the dossier reports "no gap worth a change"
and nothing is proposed. A wheel win smaller than 5× at 3×10⁷ is a lead, not gold.

## Controls

- Positive: at N ≤ 10⁴ a linear-scan oracle checks the first 20k pops are the true
  `(t, id)` minimum; all structures must produce bit-identical pop-sequence hashes per seed.
- Negative: heap2 must lose to heap4 (a harness that cannot show a known-worse structure
  losing measures nothing).
