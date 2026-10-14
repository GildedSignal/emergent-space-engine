# Dossier — 20261014-0201-library-4df1 (library lens)

**Claim.** Julien's library, read against the nladder's top open direction (compaction as
the scheduled spike), yields five decision-changing lessons — and the cheapest test of the
first two, run on shipped code, shows the one-shot compaction call is a 117–206 ms wall
(7–12 frames at 60 fps) that group-granularity budgeting cuts 20–28× wherever the burst
spreads, but **cannot touch on `battle`, where every event converges on the doll's one
loose group: 114 of 117 ms is a single intra-group step** — the spike must be split
inside the group, not scheduled around it.

**Bottleneck.** nladder open direction 3 (compaction as the scheduled spike, the primary
direction after rule 2's death). Expected gain: the store's worst idle-time term from
~10² ms to a frame-slice (~2 ms), i.e. deleting the p99 frame's largest single term; it
unblocks the promotion work (rules 3–4) at belt scale.

## Evidence (all numbers from this run; commands below, each ≤ 3 s)

Shipped `Shelf::compact` (crates/shipmem/src/shelf.rs) drains the whole hot tier in one
call. Probe: `compact_budgeted(max_groups)` added next to it (seals ≤ k groups per call,
keeps the rest hot, `forward`/`dead` restored; oracle-checked bit for bit —
`updates_roundtrip:true` on every row), driven by `SHIPMEM_SLICE=<k>` in
`examples/measure.rs`. n = 4e5, updates = 1e5 (2 rounds of 5e4), bsize 128, release,
Linux/x86 (orders of magnitude only; `before`/`after` machine strings in measure.jsonl;
load shared with the window's other runs).

| pop | arm | hot p99 | compact ns/upd | max group step | slices | max slice | p99 slice |
|---|---|---|---|---|---|---|---|
| battle | one-shot | 53 ns | 2 340 | **114.4 ms** | 2 | 116.9 ms | 116.9 ms |
| battle | k=1 | 55 ns | 2 344 | **115.2 ms** | 2 | **117.9 ms** | 116.3 ms |
| convoy | one-shot | 1 210 ns | 2 493 | 0.54 ms | 2 | 148.6 ms | 100.1 ms |
| convoy | k=1 | 1 142 ns | 14 753 | 0.58 ms | 1 452 | **7.41 ms** | 2.05 ms |
| stream | one-shot | 1 242 ns | 2 142 | 7.79 ms | 2 | 172.0 ms | 41.8 ms |
| stream | k=1 | 1 169 ns | 2 930 | 6.76 ms | 86 | **10.53 ms** | 8.40 ms |
| formation | one-shot | 1 226 ns | 3 307 | 0.84 ms | 2 | 205.7 ms | 124.0 ms |
| formation | k=1 | 100 ns | 14 819 | 0.75 ms | 1 482 | **7.43 ms** | 1.88 ms |
| traders | one-shot | 332 ns | 934 | 2.74 ms | 2 | 44.7 ms | 33.2 ms |
| traders | k=1 | 169 ns | 1 257 | 2.84 ms | 32 | **9.57 ms** | 8.14 ms |

Readings: (i) the event path is never the problem (hot p99 ≤ 1.2 µs); all frame-scale
variance is the idle-time seal. (ii) Where events land at slots (convoy, formation) the
burst spreads and k=1 caps the slice 20–28× below one-shot. (iii) On battle every
contact's scar targets the doll's loose group (measure.rs: "any other kicked ship joins
the doll's loose group"), so the whole 5e4-event round is ONE step (115 ms ≈ the repack
of a MAXG = 2¹⁶ group) — scheduling at group granularity cannot engage (slices stays 2).
(iv) Slicing's price is the re-sort of the remainder per call: 1.35× total (traders,
sparse) to 5.9× (convoy, dense) — a persistent sorted cursor deletes that overhead; the
budget is sound, my implementation pays rent.

## Predictions (predictions.md, written before any run)

1. max_slice(1) ≈ worst single-group step × ~1.5 — **held on stream (10.5 vs 6.8+sort),
   failed on convoy/formation (7.4 ms vs 0.5–0.8 ms steps: the per-slice re-sort
   dominates); diagnosis above.**
2. Amortization ≤ ~1.3× total — **failed as implemented (1.35–5.9×), cause isolated to
   re-sorting per slice; fix (cursor) named, not yet measured.**
3. The floor is the group, above the frame slice — **confirmed, stronger than predicted:
   on battle the floor is the whole burst (115 ms), not ~0.5 ms.**
4. Burst structure survives amortization — **confirmed** (sliced p99/max 0.25–0.97;
   one-shot max/p50 ≫ 3 on every pop).
5. Held-out pops (stream, formation) milder magnitudes, same shape — **held.**

## The five lessons (the lens deliverable)

1. **Fragility first** — Taleb, *Antifragile*: "if something is fragile, its risk of
   breaking makes anything you do to improve it or make it 'efficient' inconsequential
   unless you first reduce that risk of breaking." Mechanism: a dominated tail makes mean
   improvements invisible. Change: bound the compaction call (measured above) **before**
   any cheaper-kick or memory rung on the ladder. Test: this probe.
2. **Amortize the capital cost** — Kaufman, *The Personal MBA*: "Amortization is the
   process of spreading the cost of a resource investment over the estimated useful life
   of that investment." Mechanism: charge each period the share it benefits from.
   Change: adopt `compact_budgeted(k)` as the idle-time service (149→7.4 ms convoy,
   206→7.4 formation, 45→9.6 traders at 1.35× cost). Test: this probe, oracle-verified.
3. **Attack only the rate-determining step** — Young, *Ultralearning*: "The
   rate-determining step is the slowest part of this chain of reactions, forming a
   bottleneck that ultimately defines the amount of time needed for the entire reaction
   to occur." Mechanism: the chain's slowest link sets throughput; drills isolate it.
   Change: on battle the destination group is 98% of the step — the next rung is
   intra-group (chunk the repack by block range, or cap the loose group's size), not a
   cheaper kick or a smarter queue. Test: re-run battle with the loose group chunked.
4. **The waiting room is always full** — mentor quote, Sahil Bloom's *Curiosity
   Chronicle*: "The waiting room is always full." Mechanism: backlogs are structural;
   serving to empty is itself the spike. Change: serve compaction as a fixed per-frame
   budget with a persistent cursor (the k=1 loop is that server; the cursor is the
   missing half — my 5.9× is the rent of re-sorting); accept bounded lag, never catch up.
   Test: cursor variant, compare ns/upd and p99 slice.
5. **Barbell the content policy** — Taleb, *Antifragile*: "…so is the barbell a
   domestication, not an elimination, of uncertainty." Mechanism: two modes and nothing
   in the middle beats one sized-for-the-average mode. Change: for effb's step_log2
   decision (open direction 8): belt at minimum cadence + a hot tier sized by ea91's
   measured tail (Fano 8–28; top 1% of frames carry 10–26%), nominal ≤ a fraction of
   budget — never a mid-cadence compromise. Test: arithmetic on effb's ledger + ea91's
   tail; no new compute.

## What would make it wrong

The 115 ms battle step is a repack of one MAXG group at n = 4e5; if at belt scale
(n ≥ 10⁶, several shelves) the loose group lands alone on its own shelf and stays
MAXG-bounded, the intra-group rung shrinks but does not disappear (115 ms is still 7
frames). The convoy/formation 20–28× relies on slots absorbing scars; a belt where
conjunctions churn ranks would re-concentrate. The barbell lesson is unfalsified
arithmetic until shipmem's belt is wired.

## Cost of adoption, PRINCIPLES fit

`compact_budgeted` is ~40 lines beside `compact`, oracle-checked, default path unchanged
(one caller); the cursor is another ~20. Fit: "minimize spike compute and average
compute usage" (#12); "Use idle time to compute ahead" (#17); "the cheapest compute is
compute not done" (#1 — the budget deletes nothing, it moves the spike; lesson 3 is the
deleting one). The lens: this corpus is business/decision-heavy (Taleb 300 highlights,
Kaufman 315) and holds no LSM or engine-craft books, so lessons 2–3 lean on accounting
and learning analogies — the probe, not the analogy, carries them; also everything here
biases to structure and scheduling, nothing to arithmetic.

## Reproduce

`lab/results/20261014-0201-library-4df1/regen.sh` (applies `work/patch.diff`, builds,
runs the 10-row matrix, ~40 s). Raw rows: `measure.jsonl` in this folder; quotes
verbatim from `readwise-highlights.jsonl` (4 580 highlights, fetched this run).
