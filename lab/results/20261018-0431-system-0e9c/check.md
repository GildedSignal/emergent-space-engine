Grade: silver

**Abstract.** The scan's fallback walk reads the universe and discards cross-doll bodies one `binding_at` read too late; an index-served bail (`ES_LOCAL_BAIL`) answers from the doll instead. Reproduced exactly: the seam census counters are bit-equal to the author's (2,920 bails, 5,374,600 walked, 4,336,560 discarded = 80.6%, 333 kept; on-arm candidates 1,201,472 identical, walked −75.1%, capture wall −34%), the 13-case digests are bit-identical in both arms and equal to the frozen record, and chaotic key mashing (15,564 bails) matches exactly. But the 10⁹ headline fails: the trigger (window bin-entries vs `bodies/4+64`) kills the bail by N=10⁴ on the ladder's own seam (checker: 0 of 1,152), and in-band bails at scale answer O(doll) = O(walk). The fix's real scale role is enabling 604c's local threshold. ~40 lines, no law change, adoptable now.

## Reproduction

- The runner's `regen.sh` exited 0; I re-applied `work/patch.diff` to the restored pristine tree (it applies cleanly; off-arm digests equal the shipped frozen record on every shared line, so flags-off is pristine), rebuilt, and re-ran.
- **Seam, both arms, reconstructed command** `SCAN_CENSUS=1 [ES_LOCAL_BAIL=1] ladder_digest belt` (NOT in regen.sh — see "missed"): off `captures=9280 bails=2920 fb_walk=5,374,600 doll_discard=4,336,560 fb_cand=972,248 filt_walk=399,064 filt_cand=229,224`, on `bails=0 doll_discard=0 filt_walk=1,437,104 filt_cand=1,201,472` — every counter bit-equal to the author's logs; candidates 1,201,472 = 1,201,472; walked −75.1%; capture_ms 642.7 → 337.4 (−47% under this box's load; the author's 500.9 → 329.8, −34%). Digest `4995f384…` identical in all four runs.
- **Census arms** (my regen): all digest-anchored cells exact; wall-paced nladder cells wobble ≤ 0.5% (bails 414 vs the author's 416 at 10³ burn; walked 568,192 → 270,940 vs 570,958 → 272,270 — the −52.3% ratio identical). The 10³ capture_ms "noise" claim is inconclusive here (67.3 → 94.2 under load); the seam wall gain reproduces.
- **Frozen record**: the off-arm matches `artifacts/runs/nladder/ladder_digests_newpop.txt` on every shared case line — which are **11**, not the dossier's "12 shared cases" (trivial miscount).

## Predictions

`predictions.md` (19 m) predates the decisive belt logs (15 m) and the census arms. P3 held exactly (13/13 cases, 4 schedules, both arms). P1 held at the seam (80.6%) with the 10⁴-coast domain gap honestly reported. P2's belt-arm letter ("~all captures bail") is 31% (2,920/9,280; per case 38%/25%) — only the in-band phase is ~all-bail, and a cumulative census cannot show the split; the dossier glosses this as "the seam ~all-bail regime". P4 held. P5 was properly flagged as inference.

## Adversarial cases (3, one outside the author's range)

1. **Chaotic key mashing** (N=100/1000/3000, both arms, census): 15,564 bails, 1,743,552 cross-doll discards (49.7% of the bail walk), candidates **exactly** equal (3,405,900 = 3,405,900), all three digests identical to the frozen record. The registration-superset construction survives a handoff-heavy chaotic scene — the author's own "what would make it wrong" case.
2. **N=10⁴ burn** (one decade past the author's 10³ burn, the fallback regime): 0 bails both arms, counters identical — the fix is inert where nothing bails, and the fallback regime does not extend to 10⁴ burn.
3. **N=10⁴ belt crossing L10** (one decade past the author's headline seam; single-schedule throwaway, since deleted): **0 of 1,152 captures bail**, windows ~97 bodies, digest identical both arms (`c43de364…`). The bail regime on the ladder's own seam flight ends between 3×10³ and 10⁴: the trigger is the doll's window bin-entries against `self.bodies/4 + 64` (the universe's count, ~1.8×10³ entries against a threshold of 2,571 at 10⁴), so the universe outgrows the doll's window.

**Consequence for the claim.** The 10⁹ headline ("a bail goes from ~10⁹ reads ≈ 100 s to ~333") describes a configuration the shipped threshold cannot produce: at 10⁹ a small-doll scan never bails, and where bails do fire at scale (3999's in-band regime) the doll IS the belt, so the doll-local answer is as big as the walk (~314 of N saved). The fix's genuine scale role is enabling: with both threshold outcomes O(doll), 604c's local-threshold direction can be taken without creating the 10⁹ walk — the 3×10⁶× saving belongs to that composition. I corrected the proposed page in place (the "what this deletes" passage, the second Refuted entry, and the domain line).

## Novelty

Real. scan-queue's open direction 1(c) is exactly "the capture fallback … still walks and clones every body"; cdf0 priced the O(N) term, 3999 the belt-band occupancy, 604c the threshold's nonlocality and a threshold-local fix; f102 the duplicates. No run built the doll-local bail, and neither docs/HISTORY.md nor git log carries it. The waste itself was known (cdf0); the run's novelty is the waste's exact decomposition (the doll test one read too late), the index-served fix, and the bit-identical proof.

## Goal fit

Board live question 1 (which term breaks first as the plane grows): this run answers it for the scan's walk term — it is a mid-N disease on the ladder (fires N ≈ 10³–8×10³), not a scale law; the fix deletes it where it fires and unblocks the principled threshold. PRINCIPLES 1 ("the cheapest compute is compute not done"), 15 ("local laws are great…"), 19 (the walk's domain was the representation defect). No gate touched, no law changed, no B-gate refreeze needed — the candidate set is provably and measurably unchanged.

## Why silver, and the one experiment for gold

Everything measured reproduces bit for bit and the deletion is adoption-ready, but the headline scale claim is wrong as stated and the standalone measured gain is confined to the ladder's mid-N (−75% of walked bodies at a 3×10³ seam, −34% of capture wall there; nothing at 10⁴+ standalone). **The gold experiment:** compose with the local threshold — change `self.bodies/4 + 64` to the doll's registered population (604c's direction), fly the frozen 13-case digest both arms plus 3999's in-band probe at 10⁵; bit-identical exactness plus an O(doll) bail in the regime where bails actually fire at scale earns the 10⁹ sentence this run currently borrows.

## What the author missed

- The trigger law bounds the bail regime to a mid-N window; the author's own 10⁴-coast row (0 bails) was read as "the filter stays on" without asking whether the seam regime survives 10⁴. It does not (my arm 3), which re-frames the whole 10⁹ paragraph.
- `regen.sh` omits the command behind the headline number (the seam census); I reconstructed it and it reproduces exactly — add it (`SCAN_CENSUS=1 [ES_LOCAL_BAIL=1] ladder_digest belt`).
- "All 12 shared cases" is 11; P2's belt-arm prediction is 31% bailed, not ~all (phase split invisible to a cumulative census).
- The formation crowd stays unflown — no shipped harness builds 604c's pair (checked `scenario.rs` and `examples/`); the page's direction 5 should name that as a harness gap, not just an unflown case.
- The 10³ capture_ms cross-arm comparison ("noise") is fragile on a loaded box; the seam wall comparison is the load-bearing one and it reproduces.
