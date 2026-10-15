# Dossier — 20261015-1615-quant-0619 (quant)

**Claim.** The burn knee of the bounded retained-entry cache is not a working set but a
cumulative count — `WS(N) = demotions(N) = N + 30,187` exactly (integer-exact at every N,
seed and cut) — so **no bounded cap holds the promotion floor on burn below ~N entries**;
the only sub-knee rule is a priced trade with an exact integer price law
(`promotions − demotions = hits_sat − hits_cap`, 7/7 arms), and a fixed default cap
(S=16,384) degrades with N (1.24× → 7.23× → 8.50× demotions at 10⁴→10⁵→2×10⁵).

## Bottleneck

The board's first gap (bodies 28 → 10⁹). The two 1450 runs built the bounded cache and
left one decision open: the burn-safe cap rule (b0ed's checker named this "the gold
experiment": fly the burn ladder with a pre-registered knee). Expected gain: closes the
adoption decision (or deletes the cache on burn) — a decision worth 10³ at 10⁹ (either
~1.4 TB of retained entries or the re-mint bill).

## Evidence (21 flights, one frozen binary, 8 vCPU x86 shared; counts/digests/ratios deterministic, walls OoM)

Same build as 0757 (`work/patch.diff` = e0f9's seam + 1d52's retention + the `ES_RETAIN_HOT`
FIFO ring), reproduced bit-for-bit first (10⁴ burn ctl/hot65536 = 0757's numbers exactly;
10⁵ sat retained_now = 130,187 = 0757's checker's cap-262,144 point). Commands:
`bash knee.sh` then `python3 knee_table.py` (regen: `bash regen.sh`, ~11 min).

| N (burn/20k/s1) | ctl digest | demotions | **WS = sat retained_now** | WS−N | sat vs glob hits | sat rss | glob rss | ctl rss |
|---|---|---|---|---|---|---|---|---|
| 10⁴ (0757 + smoke) | `5caeb1b6…` | 40,187 | **40,187** | 30,187 | = (=584,807) | 125 | 72 | 71 |
| 3×10⁴ | `665e2ad0…` | 60,187 | **60,187** | 30,187 | = (795,107) | 234 | 194 | 191 |
| 10⁵ | `d3542eea…` | 130,187 | **130,187** | 30,187 | = (1,528,451) | 642 | 591 | 582 |
| 2×10⁵ | `1a76696e…` | 230,187 | **230,187** | 30,187 | = (2,573,307) | 1,222 | 1,171 | 1,151 |

1. **The knee is the demotion count.** Every saturating arm (cap 2²⁰, 0 evictions) ends
   with `retained_now = demotions` exactly; `demotions = N + 30,187` at all four N (seed 7:
   128,593 = N + 28,593; 48k cut: 270,979 = its demotions, ratio 2.08). Nothing dies before
   eviction: the ring is an **archive truncated at cap, not a cache over a concurrent
   working set** — refuting 0757's "the wave's concurrently re-read bodies" mechanism
   (right numbers, wrong reading: "≈40k at 10⁴" was simply demotions at 10⁴).
2. **The price law is exact.** At all 7 below-knee arms:
   `promotions − demotions = hits_sat − hits_cap` to the integer (e.g. 10⁵/65,536:
   775,010 = 775,010; 2×10⁵/131,072: 1,538,196 = 1,538,196). The read stream is
   cap-invariant (`hits+promotions` constant per scene: 1,658,638 at 10⁵), so every miss
   costs exactly one re-mint and the cache only moves the hit/miss split.
3. **A fixed cap degrades with N.** ×demotions at cap 16,384: 1.24 (10⁴, 0757) → 7.23
   (10⁵) → 8.50 (2×10⁵); at half the knee: 6.95 (10⁵, cap 65,536) → 7.68 (2×10⁵, cap
   131,072). The hit curve is a cliff at the knee, not a working-set slope: hits 43.3% /
   45.4% / 92.1% at 10⁵ for cap 16,384 / 65,536 / 130,187. Compile bill at 10⁵/16,384:
   4.83 s per 20k game-s = **3.4 ms/frame** (8.5× the 0.40 ms burning frame budget);
   at 2×10⁵: 10.05 s, wall 43.1 vs 34.5 s (+25%).
4. **The ring at the knee holds more than global retention.** `sat retained_now − glob
   retained_now = +27,911` at every N (constant): FIFO pins read-once non-belt fills the
   store already released. Same hits as global, +8-9% rss (642 vs 591 at 10⁵). Above the
   knee the cap is free (rss 642 at caps 131k/262k/2²⁰). Global's live-now = N + 2,276 on
   burn — every floor-holding rule stores ~N entries.
5. **Identity held everywhere**: 21/21 flights digest-identical per scene across
   ctl/glob/sat/caps (6 arms at 10⁵ and 2×10⁵, 5 at 3×10⁴, 3 at seed 7 incl. ctl).
6. **10⁹ composition**: knee ≈ N per 20k game-s ⇒ cap ≈ 10⁹ entries ≈ 1.4 TB — the
   bounded cache cannot hold the burn floor at 10⁹, exactly like global (2 TB, b0ed).
   The shipping rules on burn are only: (a) pay the priced re-mints (the identity prices
   any cap exactly), or (b) delete the reads — the resolver's kick-planning re-reads
   (~15 reads/body per 20k at 10⁵), the page's open direction #2.

## Predictions (predictions.md, written before the flights)

P2 (identity) 21/21 ✓; P3 (containment at the knee) ✓ incl. hits = global's exactly;
P4 (price law) 7/7 exact ✓; P5 (seed 7 WS ∈ [0.5×, 2×]: 0.988) ✓; P6 (WS(48k) ∈ [1.3×,
2.5×]: 2.08) ✓; P1's point ranges held (60,187 ∈ [55k, 85k]; 230,187 ∈ [160k, 260k]) but
**P1's law is refuted as stated**: the "sub-linear exponent" was an artifact of fitting a
power law through an additive constant — the truth is linear with offset (WS = N + 30,187),
asymptotically ∝N (the 0757 two-point α = 0.51 and my four-point α = 0.58 both → 1).
P7 half-failed: caps above the knee are free ✓, but rss(sat) ≤ rss(glob) FAILED (+8-9%,
the pinned 27,911 zombies, diagnosed and constant at every N). Two failures, both
sharper than the predictions they replaced.

## What would make it wrong, cost, fit

Wrong if: a scene exists whose burn re-reads are temporally local (a formation/battle —
b0ed's named falsifier — where reuse distances collapse below a constant cap); the knee
there would be ≪ demotions and the archive reading dies. Cost of adopting: none for the
decision — this run closes a rule rather than adding code; the integrator keeps coast's
bounded cache (0757: saturates ~4k) and must not ship a fixed burn cap. Fit: "Compute
only surprises" (the re-reads that never change anything are the bill); "The simulation
decides" (the cap curve is the law's read pattern — now measured as a cumulative count);
"a gate tuned on the data it grades is a control" (the price identity is integer-exact,
not a fit). Lens: Quant priced capacity and got a cliff; what it may miss — whether the
reads themselves (the true cost, ~15/body) are deletable by representation rather than
payable, and whether promote_us tails (p99 9-16 µs, max 338 µs at 2×10⁵/16,384) hurt F1
more than the mean compile bill.
