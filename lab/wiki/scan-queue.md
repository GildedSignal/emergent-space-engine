topic: scan-queue
status: open
closed-by:
valid-while:
updated: 20261018-0543-second-20261018-0431-system-0e9c-d7d1

# The player's scan queue: birth, service latch, and the ruin band

## Current best

**The composition is flown and the doll bound is earned at every scale flown [checker2: the "10⁹
sentence" is conditional — see the bail-gating note below]: the doll-local bail (0e9c) composed with a
local threshold (`ES_LOCAL_THRESHOLD`: the doll's registered population in place of the universe's
`self.bodies/4 + 64`, 604c's direction) moves no outcome anywhere — the frozen 13-case × 4-schedule
digest bit-identical in all three arms, the off-arm equal to the shipped record on all 11 shared
cases, the seam census reproduced digit for digit, 3999's in-band probe at 10⁵ with `pass` identical
— while the bail now fires at scale and answers O(doll) (20261018-0543-second-…-d7d1, second author
on 0e9c; everything env-gated, off-arm pristine; `regen.sh` regenerates all of it in ~14 min).**
In-band at 10⁵ the bail fires under the local threshold (occupancy ≥ doll/4 is doll-relative) and
walks the doll: 99,715 of 100,028, candidates identical — boundedness, not saving (the doll IS the
belt there). On 604c's formation pair, flown for the first time (200 fleet ships in the player's
doll beside a 10⁴ belt, harness lifted verbatim from 0552's patch): the pristine arm bails on 92% of
captures and discards 9,718 read bodies a bail (94.6% of the bail walk — 604c's census reproduced:
78/84, 9,549 `binding_at`); the composed arm walks exactly the doll (551.25 a capture, −94.2%),
discards 0, digest identical. [checker2: the wall numbers do not regenerate — the run's own regen prints
capture 117→28 ms on a quiet machine and p99 12.1→11.8 ms unchanged; three reproductions (author loaded,
runner, checker) scatter 3× on capture wall and show no p99 effect (the dossier's 350.9→33.7, 10.4×, and
p99 36.3→12.8 were machine load); the walked ratio 9,491→551.25 (17.2×) is the structural fact.] The
shape at a 10⁹ belt is ~10⁹ reads against 551 **only when a bail fires** [checker2: conditioned — at a
10⁵ belt in the same harness the pristine arm bails 0/192 and walks 394 a capture (its 10⁴ bails are
bin-span bails, threshold-independent, incidental to the locals' redraw); what holds at both 10⁴ and 10⁵
is the composed arm's doll bound, 551.25]. **The trade the composition buys, measured:
the threshold sets a read mix, and locality makes both sides O(doll).** At the seam the belt doll's
windows (bin-entries ~800, between doll/4+64 = 790 and universe/4+64 = 821) flip from the filtered
list (~36 candidates) to the doll list (~331): candidates ×2.56 (1,201,472 → 3,073,824, all sound
supersets — the extra bodies fail `hit`, digests unchanged), so the answer term grows ~2.6× there;
and the env-gated probe's per-scan population recount (two `all_of` builds ≈ +175 µs at a
2,905-body doll) puts the seam's census-measured capture wall at ×1.9–2.2 across the checker's
reproductions (the author's ×3.96 was a loaded flight) — an experiment constant
removable by maintaining the count in `note`/`rebuild` (O(1) an event); the formation scene, small
doll, shows the walk saving dominating once the recount is not. No threshold setting can cost a
scan its frame any more: the nonlocal coupling 604c flagged against PRINCIPLES 15 is gone, at zero
outcome cost, and where the mix should land is the standing angular-certificate work (direction 1),
now a dial rather than a cliff.

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
flag's alone. **[The composed arm is now flown — see the entry above: digests identical in
all three arms, the formation pair measured end to end.]** f102's ~44 µs fallback-regime
capture keeps its kept-candidate term (333+ reads either way — the discarded reads were
~0.1 µs each, invisible at 10³: capture_ms 54.2 → 55.7, noise) and loses its walk term
where bails fire. The threshold's DECISION nonlocality (which path, not what a path costs)
is closed by the composition above. Domain: seed 1, the frozen case set's scripts;
checker-extended — chaotic key mashing at N=100/1000/3000 (15,564 bails, candidates
exactly equal 3,405,900 = 3,405,900, digests identical), N=10⁴ burn (0 bails, counters
identical both arms) and the N=10⁴ seam above; second-author flight — the formation crowd
and the composed arm (this page's former unflown list), other seeds' seam crossings still
unflown.

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
   nonlocality itself (PRINCIPLES 15) is closed by the second-author flight: the local
   threshold taken, every digest identical, the formation pair's 10⁶×-shape measured
   (20261018-0543-second-…-d7d1).**
- **"The candidate total is invariant across thresholds" (the second author's own
   prediction): false — a threshold flip moves captures between the filtered list
   (window-sized) and the doll list (population-sized); what is invariant is the ANSWER
   (digests identical everywhere). The candidate total is the knob the threshold sets, and
   its price is measured: ×2.56 answer reads at the seam, 0 outcome change
   (20261018-0543-second-…-d7d1).**

*(the page's standing refutations stand: direction (d) as stated; the 50× cheaper reads;
the small-N scoping; the angular certificate's mean-vs-max; the tight-axis pre-read cut;
Kingman; the bigger budget; the root-doll seam; the missing-impulse class.)*

## Open directions

1. **Reopen the drain by the candidate set** — re-priced twice: the certificate half stands
   (1250, ab3d/1d54), the fallback's domain half is closed (0e9c), and the composition makes
   the bail's cost doll-bounded at every setting (d7d1) — so ALL of direction 1 now aims at
   one term: the KEPT candidates (331 a capture at the seam's doll list, 333 at its bail,
   ~534 at the formation's), i.e. the two-stage angular pre-read cut and the
   population-level answer / phase-neighbour rank (f102's upstream lever), which now price
   the read mix for both threshold outcomes at once. The max-gated latch (`scan_ns`, 1250's
   finding) is untouched: neither fix cuts the Passage readouts that hold the max above
   room/2.
2. (unchanged) The λ-index at 10⁶ and the index's own maintenance — now also the per-doll
   population count the local threshold reads (O(1) an event in `note`/`rebuild`; the
   env-gated probe's per-scan recount is the experiment's constant, priced at the seam).
3. (unchanged) The reuse traffic: every mint pushed twice.
4. (unchanged) The latch's escape.
5. **Done by d7d1:** the formation crowd flown (604c's pair, harness verbatim from 0552's
   patch): the composed arm walks the K-sized doll (551 at form=200), discards 0, digest
   identical — the pin's per-scan worst case is the doll list (≤ population × 216 B,
   K-sized for a fleet doll; the filtered captures keep their window-sized lists). Left:
   the harness itself is a run patch until the integrator merges it (the shipped tree
   builds no formation — the gap stands), and a capture-stress case (rapid doll handouts at
   the edge, 0e9c's own named closer) is still the registration-superset construction's
   unflown corner.

## Contradictions

None new. 3999's "every-N disease" and 0e9c's "O(doll) bail" measure the same fallback on
different axes (when it fires vs what a firing costs); the composition reconciles them: the
bail fires wherever occupancy says (doll-relative, so still every-N in-band) and costs the
doll wherever it fires. The seam's ×2.56 candidate growth under the local threshold and the
formation's −94.2% walked are the same knob read at two occupancies — a priced dial, not a
conflict. f102's per-duplicate ~44 µs and 0e9c's unchanged capture_ms at 10³ stand (the
price is the kept candidates and the tube solve, 7343's 85–90%).

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
- 20261018-0543-second-20261018-0431-system-0e9c-d7d1 (this run, awaiting grade): the composed
