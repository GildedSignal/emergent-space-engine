# Predictions — 20261020-1210-taleb-9ed1 (written 12:24 UTC, BEFORE any decisive flight)

Question: is 8365's birth-stagger freeze-kill (max 718–1231 → 40.6 ms at 1e5, fence off) a law of
the mechanism (flat arrivals ⇒ no mega-frame) or a coincidence of its birth rung? The Taleb test:
3× the bodies, another seed, external load, and 2× the horizon. Nobody has flown the stagger above
1e5 (nladder page, 8365 + both checkers; 0a46's higher rungs are all unstaggered).

Calibration already flown (before this file, disclosed): a0_anchor_1e5.csv, stagger off, fence off,
seed 1 — max_ms 714.9 at frame 2142 (14,362 events), kicks/body/gs 4.889e-5, end footprint 1,887 MB.
This is the record's family (8365: 718; 0a46 checker: 712.7). No other CSV flight has run.

Arms (all `nladder <N> burn <sec> 400 12 <seed>`, ES_FRAME_CSV=1; fence = ES_SCAN_TTL_S=16,
ca63's gate, a disclosed law change that deletes the held-scan memory channel; stagger =
ES_STAGGER_GS=14000, 8365's gate):

| arm | N | sec | seed | fence | stagger | tests |
|---|---|---|---|---|---|---|
| A1 | 1e5 | 150 | 1 | on | off | fence does not eat the freeze |
| A2 | 1e5 | 150 | 1 | on | 14k | kill replicates under fence |
| A3 | 2e5 | 130 | 1 | on | off | freeze grows at 2e5 |
| A4 | 2e5 | 130 | 1 | on | 14k | **DECISIVE: kill at 2×** |
| A5 | 3e5 | 120 | 1 | on | off | freeze grows at 3e5 |
| A6 | 3e5 | 120 | 1 | on | 14k | **DECISIVE: kill at 3×** |
| A7 | 2e5 | 130 | 2 | on | 14k | seed |
| A8 | 1e5 | 150 | 1 | on | 14k | + 16 busy loops: load |
| A9 | 1e5 | 300 | 1 | on | 14k | 120k gs: does the spread persist 8 eras? |

## Predictions, with kill bars

- **P1 (A1):** max_ms ≥ 400. The fence deletes the tail channel (ca63), not the era-1 crest; the
  freeze rides the kick comb (8365). Kill bar: < 400 ⇒ my 2e5/3e5 fence-on comparisons are
  fence-confounded and I must say so.
- **P2 (A2):** max_ms ≤ 120 (8365 got 40.6 fence-off; headroom for fence churn +4%/2e5... at 1e5
  ca63 measured +39% crest cost under fence, so headroom ×3). Kill bar: ≥ 300 ⇒ the kill does not
  survive the fence.
- **P3 (A3):** max_ms ≥ 900 (record family at 2e5 fence-off: 1,152–1,852; fence ≈ +4% cost there).
- **P4 (A4, decisive):** max_ms ≤ 250. Mechanism: staggered arrivals flat (~0.2 ev/body/bin) ⇒ the
  era-1 stream at 2e5 is ~250 kicks/frame × ~46 µs ≈ 12 ms/frame — at budget, no batch, no nested
  pull. **Kill bar: ≥ 500 ⇒ the freeze re-forms at 2× under the stagger — the fix is rung-bound or
  a second channel exists, and 8365's "identical stream ⇒ no freeze" premise is incomplete.**
- **P5 (A5):** max_ms ≥ 1,500 (record: cc9d 2,840.8, 476d 2,854 at 3e5 fence-off). **(A6):**
  max_ms ≤ 300 (3× stream ≈ 375 kicks/frame × 46 µs ≈ 17 ms + draw). Kill bar ≥ 800.
- **P6 (A7):** max_ms ≤ 250 on seed 2 (the spread is id-hash per ship; seed changes orbits/phases).
- **P7 (A8):** no single frame ≥ 300 ms under load-16 (476d's checker: unstaggered under load the
  burst still lands, ~16 s excess; over-frames and lag are allowed to grow). Kill bar: ≥ 600 ⇒ load
  re-concentrates the freeze under the stagger.
- **P8 (A9):** through gs 120k (eras 5–8), the hottest 1k-gs bin of any kick-comb era holds ≤ 30%
  of that era's kick arrivals, and max_ms ≤ 150. **Kill bar: any kick era with one bin ≥ 45% ⇒ the
  comb re-forms in time — the stagger is a delay, not a delete.**

## Secondary reads (no bars, reported either way)

- Convexity: era-1 µs/kick under stagger ≈ the sequential 45–46 µs (8365's price) rather than the
  nested ~86 µs the freeze pays — i.e. the stagger also avoids the convex per-event regime.
- End lag and peak footprint per arm (cap: kill any arm whose footprint passes 2,000 MB, disclose).

## What would make the whole run wrong

The stagger gate touches only ship first-clock synchronisation (8365, step.rs) — if it also
changes the stream (kick rate moves > 5% vs 4.889e-5), arms are not comparable. The fence drops
expired scans unanswered (a law change, ca63); A1 exists to price that on the freeze itself.
