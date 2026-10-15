# Dossier — 20261015-1338-quant-1d52 (quant lens)

**Claim.** The record's retention rule for the lazy-Entry seam is built and priced, and it is
half right: with the cache shared across slot clones, promotions fall to **exactly one per
demotion** (85–90% of reads hit; the compile bill 12.41 s → 1.37 s, wall within +12.5% of
shipped at 10⁵/48k, digests bit-identical on four scenes incl. the held-out seed) — but
**global retention erases the seam's memory win** (rss 548–554 MB vs shipped 538–539, because
the resolver's own kick planning reads every kicked body, so the retained set is 100–200% of
bodies, not a view window), while the redundancy it deletes is **N-independent** (hits
identical, 763,888, at 10⁴ and 10⁵) — so the adoptable rule is a **bounded hot cache**
(O(10²–10³) entries: the locals), not "keep until the next kick".

## Bottleneck

The board's first gap (bodies in the flyable engine, 10⁶ → 10⁹). The record (e0f9, silver:
committed, second check 429'd) deletes the standing compiled-orbit store (1,603 → 962 B/body,
−41%) at the price of no-retention re-mints (~9.9 per demotion, ~130 cores extrapolated at
10⁹ rtf 100), and names the fix: "promote once per demotion, keep until the next kick" — the
integrator's open call #1 on the nladder page. This run builds that rule and prices it. The
lens's question: is the read stream clustered (cache pays) or spread (cache thrashes), and
what does each variant cost in CPU and in standing memory — judged at the flown rungs, not by
the promotions-per-demotion average.

## The build (work/patch.diff = e0f9's seam + this run's retention, 14 files)

- `RetainCache` inside `EntrySlot::Demoted`: `Arc<Mutex<Option<Arc<Entry>>>>`, **shared by
  every clone of the slot** (the store's `get` clones records, body.rs:130 — a cold-cloning
  cache was measured first and is the lower bound, see below); first read of a kick interval
  mints and keeps, reads until the next kick hit it (a refcount bump), the kick's settle
  writes a fresh cold slot. `ES_RETAIN=1`, inert unless `ES_LAZY_ENTRY=1`; both off = shipped
  verbatim. Counters: cache hits, live retained caches; `retain hits/retained_now` printed.
- Instrument: e0f9's `examples/lazy_flight.rs` unchanged except the two counters.

## Evidence (this box: 8 vCPU x86 shared, load ~3; walls are order-of-magnitude; counts,
digests and ratios deterministic)

Same binary, three arms per scene (control / seam / seam+retain), canonical cut:

| scene | digest (all arms) | ctl wall / rss | seam wall / rss | **retain wall / rss** | promotions seam → retain | hits (share) | retained_now |
|---|---|---|---|---|---|---|---|
| 10⁴ c20k s1 | `5e8c9e24…` identical | 4.7 s / 61 MB | 9.5 s / 47 MB | **5.6 s / 62 MB** | 804,941 → **41,053** | 763,888 (94.9%) | 10,788 |
| 10⁴ c20k s7 (held-out) | `bc8b489a…` identical | 4.6 s / 60 MB | 9.7 s / 46 MB | **5.5 s / 61 MB** | 754,881 → **39,459** | 715,422 (94.7%) | 10,786 |
| 10⁵ c20k s1 | `a287f479…` identical | 13.7 s / 538 MB | 18.4 s / 386 MB | **14.6 s / 548 MB** | 894,941 → **131,053** | 763,888 (85.4%) | 100,788 |
| 10⁵ c48k s1 (3 waves, the scout's anchor) | `2109a2e0…` identical | 24.4 s / 539 MB | 37.9 s / 394 MB | **27.5 s / 554 MB** | 2,709,722 → **273,200** | 2,436,522 (89.9%) | 200,500 |

Under retention, **promotions = demotions exactly** at every scene (41,053/41,053;
131,053/131,053; 273,200/273,200; 39,459/39,459): every kick interval mints once, every other
read hits — the record's "folds into the kick's own compile", now measured as an identity.
Compile time at 10⁵/48k: 12.41 s → 1.37 s (9.1×); wall 37.9 → 27.5 s (+12.5% over shipped
control; the residue is the seam's machinery — cold slots, locks, Arc traffic — not compiles).

**The cold-clone variant (retention that does not survive the store's record clones), measured
on the same scenes before the fix: only 35–39% of reads hit** (10⁵/20k: 581,551 mints +
313,390 hits), retained_now ≈ 340, rss stays at 386 MB. It is the lower bound: retention that
lives only inside one resolver pass keeps the memory win but keeps ~65% of the bill.

**Reproduction anchors (the record's own numbers, exact):** demotions 131,053 / 273,200,
promotions 894,941 / 2,709,722, digests `a287f479…`, `2109a2e0…`, `5e8c9e24…`, `bc8b489a…` —
all as published by e0f9/b9ae/760f.

**The hot set is N-independent:** cache hits are **identical (763,888) at 10⁴ and 10⁵** while
the belt grows 10×; the belt's own reads are ~1 per kick interval (they are the kick planning
itself), so its mints are already at the kick floor and it needs no retention — the entire
redundant read stream lives in the N-independent locals/fleet (~350 bodies, ~2.2k hits each).

## Predictions (predictions.md, written before the flights)

- Held: identity on every arm incl. the held-out seed (P1); with the shared cache, hits ≥ 85%
  at 10⁵ and promotions in [0.3, 1.5] × demotions — measured exactly 1.0× (P2, P3); retain
  wall within +15% of control (P4: +6.5% and +12.5%); the 10⁹ bill falls to ≤ ~16 cores
  (P6: 3.55×10⁻⁵ × 10⁹ × 100 × 4.4 µs ≈ 15.6 — equal to the shipped engine's own
  compile-per-kick, i.e. the seam's *extra* CPU bill is ~0 under retention).
- **Fired, and reported:** P2's first (cold-clone) build deleted only 39% — the store clones
  records, so a per-copy cache misses 65% of the repeat reads; fixed by sharing, and the miss
  is itself the finding that the read stream crosses clone boundaries. P5's memory branch
  held exactly as its "reads touch ~all bodies" arm: retained_now = 1.0–2.0 × bodies (the
  resolver reads every kicked body; retired history segments hold their filled caches too),
  rss returns to and slightly exceeds shipped (548–554 vs 538–539 MB).

## What would make it wrong

- The identity certificate is the canonical cut at rtf 1000, 1 thread, coast scenes; a
  budget-limited or threaded flight could expose ordering the digest does not see (40c0 makes
  that unlikely; e0f9's suite passes on the patched tree — re-run by the checker).
- Walls are shared-box order-of-magnitude; the counts, ratios and digests are deterministic.
- The hot-set claim is inferred from hits' N-independence (two rungs), not per-body tracing;
  a bounded-cache build (the proposed rule) is the named next experiment, not flown here.
- The 10⁹ composition uses the settled belt kick rate (3.55×10⁻⁵/body/game-s) and this box's
  4.4 µs compile; the M1 re-measures both.

## Cost of adopting, and fit

The seam + **a bounded retained-entry cache** (the locals; O(10²–10³) entries ≈ a few hundred
KB, not global retention): keeps the seam's 962 B/body standing store (the deletion e0f9
certified), keeps the promotion bill at the kick floor (= the shipped engine's own kick
compile, +0 extra), and avoids global retention's memory regression. Global retention as the
record names it should NOT be adopted as-is. PRINCIPLES: "Store the generator, not the
generated" (P6) — the rule keeps the generator-only store; "Compute only surprises" (P3) —
one mint per surprise (kick), hits free; the bounded amendment is via negativa on the cache
itself. ~30 lines over the seam; default-off; digest-identical (four scenes, both seeds).

## The lens

The quant lens prices tails and capacity, and may miss law-level structure: the finding that
the resolver's own planning is the reader (so retention and the kick compile are the same
bill) is a representation fact, not a pricing one — a law change (break #1, the cadence) moves
this bill by orders, and no cache sizes it away. Contacts stayed 0 on every arm (the
checker's open `same()` experiment remains open).
