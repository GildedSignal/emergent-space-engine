Working...
Check complete. Summary of what I did and found:

**Reproduction** — clean tree at base `d0ccab00`, applied `work/patch.diff` myself, rebuilt, reran all four bench commands. Every deterministic counter is bit-identical (calls, agree/disagree, distinct keys, passages, `disagree_quantum = 0`). I also built the **unpatched** tree and proved the clean-path claim: digests `e622722a…`/`58127f4c…` and the memo block equal the stored audit-off run; made/leaver medians 35.4/201.3 µs vs the dossier's 35.7/203.3.

**Attack** — five arms outside the author's range: fresh seeds 3, 11, 12345; **rtf 300** (a held-out arm named in `predictions.md` but never reported — it changes the population itself, 2,536 calls); and a 3× longer flight. All hold: 14,278 audited rebinds total, zero quantum disagreements, zero proto errors, compile share 82–87%.

**Grade: gold** (`check.md` written). The measurement layer is exact and the premise correction is board-level: the "~50 ns floor" in board bottleneck #3 is the *write* floor, the fit is 6% of the rebind (inverting the priority under 71 runs), and the deletion (Carlson compile) is pre-verified with the population share now measured. Dead predictions were pre-registered, honestly booked as deaths, and didn't carry the headline.

**Blemishes found, documented, and corrected in the page** (reporting layer only, all visible in the run's own raw JSONs):
- regen.sh's tail understates by the prototype's 2.3 µs (subtracts `ns_proto` from a timer that already excludes it): true tail 5.3–5.6 µs, rebind mean 62.6–75.4 µs, compile share 84–87% — every conclusion survives.
- The dossier's passage arithmetic (66 × ~350 µs / 1,467 calls ≈ 16 µs, not 1.3–1.6) doesn't follow from its own counters; the cycle-compile split stands by residual.
- The floor's tail term (~1 µs) is asserted — at the shipped tail the gap is ~6–7×, not 10–12×; the write≠arithmetic reconciliation survives any tail price.
- The proposed page had dropped the `c3a5` and `ec9d` run lines (Runs is append-only) — restored, plus my reproduction note added.

Working tree restored to base; only `check.md` and `wiki/kick-jet.md` touched in the run folder.
