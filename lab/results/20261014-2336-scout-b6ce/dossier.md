# Dossier — the in-band scan's missing along-track key

**Claim.** The player-in-band scan ruin (OOM at ≥5×10⁴ under burn, 625b/d7e3/c481) is
structural — the shipped `Radial` index bins by octave of radius and a 2–3 AU belt is a
thin shell it cannot cut — and a kinetic bucket index on the law's own birth constants
(mean longitude L sorted within a×mean-anomaly×e buckets; every key exactly linear or
constant between kicks) answers the scan with **zero misses and a measured 24–53× cut**
on a float replica of the ladder belt at 10⁵ and 10⁶, with maintenance that piggybacks
the kick rebind.

## Bottleneck

Bodies in the flyable engine (the board's furthest gap; the at-Home record 10⁶). The
player-seam ruin stands: in-band under L8 burn every minted scan's `candidates` vector is
the whole retention (99,715 × 224 B = 29.4 MB per mint, c481), ~190 mints are held, and
the flight OOMs at N ≥ 5×10⁴ (d7e3). The gain: the standing term ÷24–53 today (measured),
capture 30.3 ms → 0.58–1.3 ms per mint at 10⁵; what it deletes at wiring is the in-band
walk-all path of `Radial::candidates` (and, with streaming capture, the held-candidates
retention itself — c481's named fix composes).

## Requirements (scout step 1)

| # | Requirement (number) | PRINCIPLES |
|---|---|---|
| R1 | Zero misses: the tier is a superset; the exact `hit` predicate decides | "Laws are versioned… floats never decide"; radial.rs's own contract |
| R2 | Capture O(window+log N), not O(N): 30.3 ms → ≤1 ms at 10⁵ | #3 compute only surprises; #1 |
| R3 | Standing per held mint ≤ KB-scale, not 29.4 MB | #24 the memory floor is information |
| R4 | Maintenance only at kicks (3.55×10⁻⁵/body/game-s, cf45) | #14 no work for no reason; #6 store the generator |
| R5 | Integer-portable keys (birth constants, exactly-linear clocks) | #16; the tube's own Q48/Q32 quanta |
| R6 | Arbitrary player windows under thrust, no reshaping per query | #5 the player is the wildcard |

## The survey, ranked by fit (scout steps 2–3)

1. **The engine's own certificate, transplanted to the seam** — 88ee's unified rule
   (cone ∧ wrap(Δλ₀) with exact mean-motion extremes) is the same certificate with
   horizon H; the player seam needs horizon h. **This run measures its player-seam form
   as a kinetic bucket index.** Law-native, integer-friendly, already proven on belts.
2. **Kinetic sorted list** (Basch–Guibas–Hershberger; CGAL Kinetic): sorted order of
   moving keys maintained at swap events. Our keys are *exactly linear between kicks*,
   queries are rare and updates rarer, so the swap event queue is unnecessary — a shear
   bound (n_max·age) covers it (measured 1.13×10⁻³ rad over the whole flight: a "lazy
   kinetic" reading). UNVERIFIED beyond the classic results.
3. **MOVIES** (Dittrich et al. 2010, throwaway snapshots): rebuild-a-static-index-per-
   epoch is exactly the re-epoch the shear bound prices (0 epochs needed per 16,000 game-s
   flight). UNVERIFIED specifics.
4. **TPR\*-tree** (Tao–Papadias–Sun, VLDB 2003): near-optimal predictive window queries,
   but tree nodes carry velocity envelopes that grow with time and need rebuilds; memory
   per body ≫ floor; float-shaped; designed for update rates ~10³× ours. UNVERIFIED.
5. **Sweep-and-prune** (game broadphase): per-frame incremental sort exploits coherence;
   pays per frame where we mint per 83 game-s; on radius alone it is the shipped index's
   failure; on longitude it reduces to candidate 2 without the event queue.
6. **Rotating-frame spatial hash**: same math in physical space; strictly worse than
   element space because keys there are exactly linear while positions need the Kepler
   solve per body per query.

The fish's water (bottleneck 0's idiom): the belt is thin in **element space** — (a, M, e)
constant, L exactly linear — and wide in none of them; the radial index fails because
radius is the one coordinate where a belt is *dense*.

## Evidence (scout step 4: the falsifier)

`work/scan_tier.py` (numpy; ~80 s): the ladder's own generator (a U[2,3) AU, e
Rayleigh(0.07) re-drawn >0.4, doll 0), player circular 2.5 AU in-band, 193 mints (one per
83 game-s, the 625b burn protocol), brute-force truth at every 4th (10⁵) / 16th (10⁶) mint.
Two window anchors: `R_code` = 2¹⁰·2·(34·2⁸ root units) = 0.176 AU (derived from
`ENCOUNTER_LOG2=10`, `scenario.rs` ladder_ship) and `R_count` = 0.037 AU (back-solved from
c481's ~21 encounters/mint). Controls both sides: the shipped shape (walk-all) and a naive
mean-longitude tier with no eccentric widening.

| arm | N | shipped cand/mint | tier cand/mint | cut | tier misses | naive misses | MB/mint | flight held | truth hits/mint |
|---|---|---|---|---|---|---|---|---|---|
| R_code | 10⁵ | 100,000 | 4,218 | 23.7× | **0** (49 truth mints) | 18,375 | 0.94 | 0.18 GB | 615 |
| R_code | 10⁶ | 1,000,000 | 42,051 | 23.8× | **0** (13) | 47,362 | 9.42 | 1.82 GB | 6,047 |
| R_count | 10⁵ | 100,000 | 1,899 | 52.7× | **0** (49) | 1,127 | 0.43 | 0.08 GB | 25.0 |
| R_count | 10⁶ | 1,000,000 | 19,050 | 52.5× | **0** (13) | 3,424 | 4.27 | 0.82 GB | 286 |

Supporting: apsidal fraction (the shipped radial filter's own keep fraction) is 0.51–0.76
at every mint — above the bodies/4+64 walk-all trigger, so the shipped shape reads every
body every mint, as c481 measured; the shear bound is 1.13×10⁻³ rad over the whole flight
(zero re-epochs; with per-body epoch-at-kick it is bounded by age-since-kick instead);
truth hits/mint at R_count = 25.0 vs the record's 4,032/193 = 20.9 (c481) — the anchor
closes to 20%. Composed at the record's conversions (224 B/candidate, 303 ns/candidate —
c481/625b, not re-measured here): capture 30.3 → 0.58 ms at 10⁵ (R_count); the flight's
held set 0.08–0.82 GB against the measured 11.2 GB plateau and the ≥5×10⁴ OOM. Maintenance:
every kick rebinds (a669: 1.00 compiles/kick), so re-slotting the body's bucket costs one
binary search inside the rebind — at 10⁹, 3.55×10⁴ re-slots/s ≈ 2–4% of one core
[INFERENCE].

Reproduce: `sh regen.sh` (≈90 s, needs numpy).

## Predictions (predictions.md, written before the run)

- P1 ✓ walk-all every mint at both N (apsidal fraction > trigger).
- P2 ✗→resolved: R_code predicts 615 truth hits/mint where the record counts ~21; the
  count-anchored 0.037 AU arm reproduces the record (25/mint). My ship-radius reading
  (34·2⁸ root units → a 0.176 AU near-window) is 30× the record's effective window: either
  the encounter path reads a smaller radius (doll units at wiring) or logged encounters
  dedupe. Both arms are reported; the cut's *shape* is R-linear either way.
- P3 half: zero misses ✓ at every arm; the cut is 24–53× where I predicted ≥50×/≥300×
  (tier candidates 4.2%/1.9% of N vs predicted ≤2%/≤0.3%) — my bucket-width estimate was
  2–6× optimistic. The dominant slop is the e-bucket granularity (geometric ratio 2 ⇒ the
  equation-of-center band ≈ 2Δe ≈ e per bucket), then the a-width (R_arc uses r_min =
  a_lo(1−e_hi)); both are knobs, both measured below.
- P4 ✓ the naive tier misses 61% (R_code) to 92% (R_count) of truth hits — the
  equation of center genuinely carries bodies ±2e rad off mean longitude; a longitude
  index without eccentric structure is dead.
- P5 ✓ shear 1.13×10⁻³ rad ≪ window; 0 re-epochs per flight.
- P6 ✓ held set 0.08–0.82 GB ≤ the box ceiling at both N (shipped: 5.7 GB at 10⁵ by the
  same accounting, 11.2 GB measured).

## What would make it wrong

- The replica is planar, unperturbed-Kepler between kicks. 3-D inclination adds a
  vertical excursion term (i·a) to the window — unmeasured; the ladder belt is planar, so
  the wired tier inherits this domain until a 3-D arm runs.
- The burn's player trajectory under thrust is not Kepler; I model the swept arc as
  (v+v_cap)·h (the shipped window's own term). At extreme burn levels the real slack
  could exceed it — the wiring must charge the same term the scan already charges.
- Misses were checked against 3-sample truth (a necessary condition: continuous closest
  approach ≤ sampled min; the sampling gap ~750 km ≪ R). A wrap-level integration bug in
  the exact predicate path would not show here — the tier never touches the predicate.
- The 224 B and 303 ns per-candidate conversions and the 29.4 MB/mint site are the
  record's (c481/625b), not re-measured on shipped code this run; the scan loop itself was
  read, not instrumented (code-reading + the record's counters carry the mechanism).
- At 10⁹ the single-level tier still touches ~1.9%·10⁹ = 1.9×10⁷ candidates per mint —
  the ruin's *shape* is fixed (O(window), not O(N)) but the constant needs the finer
  buckets named in Open directions (e-ratio 2→1.25 ≈ 4×; a-width 0.25→0.05; M 64→256)
  and/or streaming capture (standing O(answer), ~2.9×10³ at 10⁹) — both unmeasured.

## Cost of adoption

A second index beside `Radial` (or a widening of it into element space): keys are the
birth constants the tube already stores; re-slot rides the kick's rebind (a669: the rebind
already re-fits and re-stores every kick); the scan's capture loop reads buckets instead
of doll membership; window derivation re-done in doll units (the open anchor above). The
tier is a pure prefilter — the exact predicate, the digest and every gate are untouched
(the same contract `radial.rs` already states). PRINCIPLES fit: #3 "Nothing is evolved
that can be derived when looked at (clocks, redshift, views)"; #6 "Store the generator,
not the generated"; #15 "local laws… the goal is to reduce compute".

## The lens (scout)

What this lens may have missed: the survey's frontier half is marked UNVERIFIED (I cited
and ranked classics, not 2024–26 papers); no M1 numbers (Linux x86 float replica, orders
of magnitude only); no Rust prototype — the adoption cost is argued from the code read,
not built; and the scout's bias toward "the best solution anywhere" may undervalue the
simpler in-repo alternative (88ee's tier is the same certificate — wiring *it* to the
player seam may be cheaper than a new index class).
