topic: scan-queue
status: open
closed-by:
valid-while:
updated: 20261018-0431-system-0e9c

# The player's scan queue: birth, service latch, and the ruin band

## Current best

**The fallback's domain is the universe, the certificate's is the doll, and the fix is one
bail path: on a bail the index answers the doll's own registered population, and nothing
else is ever read (20261018-0431-system-0e9c, system; `ES_LOCAL_BAIL` env-gated patch,
off-arm the pristine path; `SCAN_CENSUS` print-only counters in `encounter.rs::capture`;
`nladder` ported to Linux `/proc` for this run).** Measured on shipped code: the fallback
walk (`0..bodies.len()`, `encounter.rs`) pays a `binding_at` read for every body in the
universe and discards each one at the doll test (`other.doll != me.doll`, one line AFTER
the read) — **80.6% of every bail's walk is discarded after the read at the seam**
(`ladder_digest` N=3000 belt-crossing L10: 2,920 bails of 9,280 captures, 1,841 bodies
walked and 1,484 discarded per bail, 333 candidates kept), **67.1% in f102's fallback
regime** (N=10³ burn: 416 bails, 1,070 walked, 718 discarded, 344 kept) and **24.8% at
plane scale** (N=0: 383/384 captures bail — 604c's 100% confirmed — 72.7 walked, 18
discarded, 32.5 kept). With the fix: bails serve the doll population from the index
(`all_of`: unbounded + every bin, deduped), **the candidate set is identical to the body
at every scene** (belt-crossing 1,201,472 = 1,201,472; N=10³ burn 261,373 = 261,373; kept
per bail 333/344 unchanged), **total walked bodies −75.1% at the seam** (5.77M → 1.44M)
and −52.3% at 10³ burn, doll-discards 0 everywhere, and the frozen digest record
reproduces bit for bit (`ladder_digest` full 13-case set × 4 schedules, off vs on: one
digest per case per schedule in both arms; the N=3000 seam digest
`4995f38448103cc20232d292eb40a84b`, kicks 40106, encounters 789, contacts 0, identical).
Exactness is by construction, not luck: the caller's cheap tests already discard other
dolls' bodies, and the index is a superset of every retained binding per doll
(`note` widens, `rebuild` hulls), so the two walks keep the same candidates — the digest
record checks the construction. **What this deletes [corrected by the checker]:** the bail's
walk term WHERE BALES FIRE — O(doll) reads instead of O(universe). The bail's trigger,
however, is the doll's window bin-entries against `self.bodies/4 + 64` (the UNIVERSE'S
count), so the ladder's own bail regime is a mid-N window, not a scale law: at N=10⁴ on the
same seam flight it no longer fires at all (checker's arm: 0 of 1,152 captures, windows
~97 bodies, digest identical), and at 10⁹ with the belt in another doll the shipped
threshold already suppresses a small-doll bail (seam-doll bin-entries ~1.8×10³ against
2.5×10⁸) — the "10⁹ reads ≈ 100 s → 333" deletion describes a configuration the shipped
threshold cannot produce, and where bails DO fire at scale (3999's in-band regime) the doll
IS the belt, so the doll-local answer is as big as the walk (it saves ~314 of N there). The
fix's true scale role is ENABLING: both threshold outcomes are now O(doll), so the nonlocal
knob 604c flagged against PRINCIPLES 15 (`self.bodies/4`, the universe's count) can finally
be made LOCAL — 604c's own open direction — because without this fix a local threshold on a
333-body doll beside 10⁹ bodies would bail and walk the universe, while with it the same
bail serves 333: the 3×10⁶× saving is the composition's (fix + local threshold), not the
flag's alone. f102's ~44 µs fallback-regime capture keeps its kept-candidate term (333+
reads either way — the discarded reads were ~0.1 µs each, invisible at 10³: capture_ms
54.2 → 55.7, noise) and loses its walk term where bails fire. The threshold's DECISION
nonlocality (which path, not what a path costs) remains, now cost-free to fix. Domain:
seed 1, the frozen case set's scripts; checker-extended — chaotic key mashing at
N=100/1000/3000 (15,564 bails, candidates exactly equal 3,405,900 = 3,405,900, digests
identical), N=10⁴ burn (0 bails, counters identical both arms) and the N=10⁴ seam above;
unflown — a formation crowd (K beside a belt, 604c's bailing pair), other seeds' seam
crossings, and the composed local-threshold arm (the O(doll) serving law is
construction-invariant; the bail's TRIGGER is not, as the 10⁴ seam shows).

*[Prior best retained below: f102's reuse-walk entry, the read's inside price, the latch,
the λ-index and the ruin band — see the standing text on main's page; this entry is
additive and touches only the fallback's domain.]*

**[f102's entry retained verbatim on main's page: the reuse walk is the memo's proof, not
its overhead — 47.8% of burn captures are duplicates at ~44 µs; no change-signal coarser
than the candidate set certifies a duplicate; direction (d) dead as stated.]**

## Refuted

- **"The fallback walk is what it must be — when the filter gives up, every body is read,
   as it always was" (the shipped comment's own contract, and the premise under cdf0's
   N-relative rule and 3999's every-N reading): the walk's cross-doll majority is pure
   waste — 80.6%/67.1%/24.8% of it (seam / 10³ burn / plane) is discarded one line after
   the read, and the index serves the same candidate set at O(doll) with bit-identical
   digests on the frozen record (20261018-0431-system-0e9c).**
- **"Fixing the bail means re-deriving its threshold" (promotion's open-direction pricing,
   the bail made local in numerator and denominator), as a COST claim: with the doll-local
   fallback both of the threshold's outcomes cost O(doll), so no threshold setting can cost
   a scan its frame — the cost question dies (20261018-0431-system-0e9c). The DECISION
   nonlocality itself (PRINCIPLES 15) remains open and now free to take: making the
   threshold doll-local is the composed end state the fix enables [checker].**

*(the page's standing refutations stand: direction (d) as stated; the 50× cheaper reads;
the small-N scoping; the angular certificate's mean-vs-max; the tight-axis pre-read cut;
Kingman; the bigger budget; the root-doll seam; the missing-impulse class.)*

## Open directions

1. **Reopen the drain by the candidate set** — re-priced: the certificate half stands
   (1250, ab3d/1d54), and the fallback's domain half is now closed by this run (the bail
   serves the doll). What remains of direction 1 is the KEPT-candidate term at the seam
   (333 reads per capture in-doll): the two-stage angular pre-read cut and the
   population-level answer / phase-neighbour rank (f102's upstream lever), both unchanged
   by this run. The max-gated latch (`scan_ns`, 1250's finding) is untouched: the fix
   cuts the walk, not the Passage readouts that hold the max above room/2.
2. (unchanged) The λ-index at 10⁶ and the index's own maintenance.
3. (unchanged) The reuse traffic: every mint pushed twice.
4. (unchanged) The latch's escape.
5. New, small: fly the fix beside a formation crowd (604c's bailing population pair) —
   the O(doll) law is by construction, but the crowd's doll population is K-sized
   (1.00 candidates a ship), and the pin (candidates × 224 B, the memory page's fence)
   should be confirmed unchanged: the post-filter candidates were already doll-local.

## Contradictions

None new. 3999's "every-N disease" and this run's "O(doll) bail" measure the same
fallback on different axes (when it fires vs what a firing costs); reconciled, not in
conflict. f102's per-duplicate ~44 µs and this run's unchanged capture_ms at 10³ agree:
the price is the kept candidates and the tube solve (7343's 85–90%), not the discarded
reads — the discarded term only becomes the story at N where the belt is in another doll
(seam: −75.1% of walked bodies; the seam's capture_ms 500.9 → 329.8 over the same
window, −34%, the walk's share at last measurable there).

## Runs
- 20261016-0213-dynamics-69f3 (awaiting grade): the scan queue is a one-way latch at S = b/2 —
- 20261016-1120-components-cdf0 (this run, awaiting grade): the scan's candidate set censused —
- 20261016-1740-quant-1250 (this run, awaiting grade): the angular certificate built on the knot
- 20261016-1120-components-cdf0 (awaiting grade): the scan's candidate set censused —
- 20261016-1740-spacex-3999 (awaiting grade): the belt-bin regime measured — in-belt fallback at
- 20261016-1740-quant-1250 (awaiting grade): the angular certificate built on the knot
- 20261016-2229-quant-7343 (this run, awaiting grade): the in-belt read decomposed — 85–90%
- 20261016-2229-scout-ab3d (silver, checker): the two-stage angular certificate measured — sound in its domain (0 misses; checker: 27 all-seed scenes), the tight-axis pre-read cut exists at 35–50 ns; S(10⁵) 1.6–1.8 ms at the code-derived near (49-m ships; the run's 12,850-km "shipped radii" are a 2¹⁸ misread), 10⁶ marginal at ≈6.4 ms with the λ-index; querents e > 0.4 unsounded as coded.
- 20261016-2327-second-20261016-2229-scout-ab3d-1d54 (this run, awaiting grade): the certificate re-derived at the true shipped point (49-m ships, near 6.71×10⁻⁷ AU) — 0 misses in 32 all-seed scenes on a regenerating record, the closed-form margin fixes e > 0.4 querents (the clamped table provably missed), S(10⁵) 2.1 ms under the bar, 10⁶ marginal 6.9 ms, the bar holds to querent e ≈ 0.6.
- 20261018-0143-system-f102 (system, this run): the reuse walk is the memo's proof — 47.8% of burn captures are duplicates at ~44 µs (~0.5% wall), and global/binding-guarded/per-doll change-signals all miss every duplicate (0 hits at every measured grain); direction (d) unsound-or-empty; the lever is the re-timed pending kick. [checker2: clean reproduction — the author's exact digests (d976e91f/be73e0a8/81e5739a) and counts 460/220/240; seeds 3/11 → 48.6%/48.5%; 10⁵ seed 3 → 220/453, 0 hits, 28.4 µs/dup, 233 MB; the global-version arm reconstructed → 0/220; coast 10⁴ all fresh; sustained re-timing keeps the class at ~48% of captures over 4 s — it tracks burn duration, not input count.]
- 20261018-0431-system-0e9c (system, this run): the fallback's domain is the universe
