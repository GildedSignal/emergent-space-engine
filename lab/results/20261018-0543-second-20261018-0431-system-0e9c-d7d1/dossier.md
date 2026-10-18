# Dossier — 20261018-0543-second-20261018-0431-system-0e9c-d7d1 (second author on 0e9c)

## Claim

The checker's named gold experiment is done: composing the doll-local bail (`ES_LOCAL_BAIL`, 0e9c) with a local threshold (`ES_LOCAL_THRESHOLD`: the doll's registered population in place of the universe's `self.bodies/4 + 64`, 604c's direction) leaves every outcome bit-identical — the frozen 13-case × 4-schedule digest in all three arms, 0e9c's seam census counters reproduced digit for digit, 3999's in-band probe at 10⁵ with `pass` identical — while the bail now fires at scale and answers O(doll): in-band at 10⁵ it walks the doll (99,715 of 100,028), and on 604c's formation pair (200 fleet ships in the player's doll beside a 10⁴ belt, flown here for the first time) the composed arm walks 551 bodies a capture against the pristine arm's ~9.5×10³ (94.6% of them discarded after the read), capture wall 350.9 → 33.7 ms (10.4×), digest identical — the shape that at a 10⁹ belt is the ~10⁶× the 10⁹ sentence needed. The composition is not a uniform win, and that is now measured too: where windows sit at the doll's quarter (the seam), the local threshold flips filtered captures to the doll list — candidates ×2.56 (1,201,472 → 3,073,824, all sound supersets; digests identical) — and the experiment's per-scan population recount costs more than the walk saves there; the threshold's setting is a priced read-mix knob, both sides O(doll), no longer a nonlocal coupling.

## Bottleneck

Board live question 1's read path (the scan), continuing 0e9c. The checker kept 0e9c silver for exactly one reason: its 10⁹ headline described a configuration the shipped nonlocal threshold cannot produce (the bail never fires at 10⁴+ on the ladder), and where bails do fire at scale (in-band) the doll is the belt, so the fix alone saves ~314 of N. The gain measured here is the composition's: the scan's walk term becomes doll-bounded at every N and every threshold setting (the 10⁶× class), and the nonlocal coupling 604c flagged against PRINCIPLES 15 — other dolls' populations deciding this doll's scan path — is gone at zero outcome cost.

## Evidence

All numbers from `regen.sh` (~14 min: build 45 s; three full digest runs ~10 min; seam censuses ~3 min; probes and formations ~40 s). Arms: `off` (pristine path), `LT` (`ES_LOCAL_THRESHOLD`), `LT+BAIL` (the composition). The patch = 0e9c's (census + bail + Linux `/proc` port) + the threshold gate in `radial.rs::candidates` + 604c's formation harness (`plane_formation`, lifted verbatim from 0552's patch) + 3999's `belt_scan_probe` (verbatim) + a `formprobe` flyer. Everything env-gated; off-arm is pristine.

**P1 — exactness (the frozen record, three arms).** Full `ladder_digest`, 13 cases × 4 schedules, off / LT / LT+BAIL: bit-identical after stripping per-case walls (the seam case `4995f38448103cc20232d292eb40a84b`, kicks 40,106, encounters 789, in every arm). The off-arm equals the shipped frozen record `artifacts/runs/nladder/ladder_digests_newpop.txt` on all **11** shared cases (0e9c's "12" was a miscount; the run set adds the two wave cases the record lacks). The construction: all three paths (filtered list, walk the universe, walk the doll) end in the same cheap tests; the index is a superset of every retained binding per doll; a bail's set (all same-doll alive bodies) equals `all_of`'s filtered form; a filtered set is a subset of it whose extras fail `hit` — the answer cannot move, and the digest checks it.

**P2 — the bail fires at scale, in-band (3999's probe at 10⁵, `belt_scan_probe 100000 1`).**

| arm | belt window (doll 0, r = 2.5 AU) | walked | pass |
|---|---|---|---|
| off | fallback (None) | 100,028 | 99,714 |
| LT | fallback still fires (occupancy ≥ doll/4 is doll-relative) | 100,028 | 99,714 |
| LT+BAIL | served, `kept=99,715` = the doll's population | 99,715 | 99,714 |

The player's home window (doll 2): identical in all arms (`kept=8 pass=7`). The answer half (`Scan::compute`'s loop): candidates 99,714, encounters 0, and the slack metrics (miss/arc over reach, min and p50) identical in all arms — the composition touches who is read, never what is computed. In-band the walk saving is the 313 cross-doll bodies only, as the checker said: the claim there is boundedness (the bail can never cost more than the doll), not saving.

**P3 — 604c's formation pair, flown (`formprobe 200 10000 20 100`: 200 fleet ships on the player's circle in the player's doll, the 10⁴ belt in the root doll; 1,375 frames, 192 captures).**

| arm | bails | walked/capture | discarded after read | candidates | capture_ms | digest |
|---|---|---|---|---|---|---|
| off | 177 (92%) | 9,489 | 9,718/bail (94.6% of the bail walk) | 98,940 | 350.9 | `e9043656…` |
| LT | 192 (100%) | 10,269 | 9,718/bail | 102,521 | 228.4 | `e9043656…` |
| LT+BAIL | 0 (all served) | **551.25** | **0** | 102,521 | **33.7** | `e9043656…` |

The off-arm reproduces 604c's census (78/84 bailed there, 9,549 `binding_at` a scan; here 177/192 and ~9.7×10³ discarded reads a bail — same law, longer flight). The composed arm walks exactly the doll (551 = its registered population), p99 frame 36.28 → 12.83 ms, kicks/encounters identical. This is the 10⁹ sentence at reachable scale: the player's scan's cost no longer sees the belt; at a 10⁹ belt the same two arms are ~10⁹ reads against 551.

**P4 — the seam census (`SCAN_CENSUS=1 … ladder_digest belt`, the command 0e9c's regen omitted).** Off-arm: `captures=9280 bails=2920 fb_walk=5374600 doll_discard=4336560 fb_cand=972248 filt_walk=399064 filt_cand=229224` — bit-equal to 0e9c's and its checker's numbers (80.7% of the bail walk discarded). Composed arm: `bails=0 doll_discard=0 filt_walk=3309456 filt_cand=3073824`; digests identical (`ef19d3de…`, `4995f384…`). Two honest costs, both new measurements: (1) **candidates ×2.56** — under the local threshold the belt doll's windows (bin-entries ~800, sitting between doll/4+64 = 790 and universe/4+64 = 821) flip from the filtered list (~36) to the doll list (~331); every extra candidate is a sound superset read for the answer loop (4.2 µs each — the answer term grows ~2.6× at the seam), never an outcome change. (2) **capture wall ×3.96** (550.3 → 2,177.9 ms): the env-gated implementation recomputes the doll population per scan (`population()` = an `all_of` build, plus another for the bail answer, ≈ +175 µs at a 2,905-body doll) — an experiment constant, removable by maintaining the count in `note`/`rebuild` (O(1) an event); the formation scene, where the doll is small, shows the walk saving dominating once the recount is not (33.7 ms there).

**The trade, stated once.** The threshold decides the read mix: filtered (window-sized, e.g. 36 at the seam) or doll-sized (331). A nonlocal threshold prices the mix by the universe's count (PRINCIPLES 15's coupling); the local threshold prices it by the doll, and both outcomes are O(doll) — so no setting can cost a scan its frame, and the knob's choice is now a measured dial, not a cliff. Where the mix should land is the page's standing angular-certificate work, unchanged by this run.

## Predictions

`predictions.md` was written before the decisive runs. **P1 held** (13/13 cases, three arms, one digest everywhere; 11 shared cases match the record). **P2 held** (the bail fires in-band under LT at 10⁵; the composed arm walks the doll with `pass` identical; in-band saves only the ~313 cross-doll bodies). **P3 held** (≥15× predicted, 17.2× measured on walked bodies 9,489 → 551.25; capture 10.4×; digest identical; 604c's off-arm census reproduced). **P5 held** (the answer half identical in every metric but wall). **P4 held in mechanism, failed in one letter, and the failure is informative**: I predicted the candidate total would be identical across arms; it is identical between walk-universe and `all_of` at a fixed threshold, but the local threshold flips filtered captures to the doll list, so the seam total grows ×2.56 (sound supersets; digests unchanged). My kill criterion ("a candidate total moves") was mis-specified: the invariant that guards the game is the digest/answer, and that never moved — the candidate total is the knob the threshold sets. Reported as held-out failure, not swept aside.

## What would make it wrong

A scene where a body's live binding at the scan's tick is absent from its doll's index (a registration gap outside the flown scenes) would let the doll-local bail drop a candidate the universe walk kept. The construction (`note` widens, `rebuild` hulls) plus 13 digest cases, 1,375 formation frames with handoffs and 129 encounters, and the checker's chaotic key-mashing bound it; 0e9c named a dedicated capture-stress case (rapid handouts at the edge) as the closer, and it remains unflown. Second: the seam's answer-term growth (×2.56) is measured at one scene — a belt-band window whose bin-entries sit between the two thresholds; scenes with entries below the local threshold keep the filtered mix, and where they sit is belt-occupancy (3999's law), so the mix at 10⁹ in-band is doll-sized either way (the doll is the belt). Third: census counters are seed 1 and the frozen scripts; other seeds share the law, not the letter.

## Cost of adoption, and fit

Adoption is 0e9c's bail plus a one-line threshold change and a per-doll population count maintained in `note`/`rebuild` (the env-gated probe recomputes it per scan; the shipped form pays O(1) an event — that constant is the seam's ×4 capture wall, measured and named). No law change, no B-gate refreeze (the answer set is digest-proven unchanged on every flown scene). The integrator re-measures on the M1 (Linux x86 here; reads are reads, the ratios carry, the constants do not). Fit — PRINCIPLES 15 ("local laws are great…": the scan's path choice becomes doll-local), PRINCIPLES 1 (the cheapest compute is compute not done: 89.9% of the formation scene's bail walk never needed doing) and 19 (the wrong representation was the threshold's denominator; the fix feels like cutting butter — the same rule with the doll's own count). The lens's own bar: the composition deletes the *cost class* of the bail, not the answer term — the seam's kept-candidate work (333 reads a capture) is still the page's open direction 1.

## The lens

The second-author lens (do the checker's named experiment, make the record regenerate) may have missed how the seam's read mix moves under the local threshold — I predicted the candidate total invariant and it is not, across thresholds; a formation-first author might have seen it. The seam's ×4 capture wall is my own implementation's constant (the per-scan recount), priced here rather than hidden. The formation harness is 604c's, lifted verbatim — the crowd scene's realism is its author's, not mine; and the in-band probe substitutes a belt body's window for a flown player-resident-in-belt session (3999's own caveat, inherited).
