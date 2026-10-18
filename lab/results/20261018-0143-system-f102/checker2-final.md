Working...
**Grade: gold** — written to `lab/results/20261018-0143-system-f102/check2.md`, with three overstatements corrected in the author's `wiki/scan-queue.md`.

**What I reproduced (all my own runs, patch applied by me, load 5–6):**
- Burn N=10³: 220/460 duplicates (47.8%), 43.3 µs each — the author's *exact* counts, and digests `d976e91f…`/`be73e0a8…`/`81e5739a…` bit-identical to the author's across off/on/verify modes.
- The two cells `regen.sh` cannot regenerate (the global-version arms, 0/209 and 0/217) I rebuilt behind an `ES_GLOBAL_KEY` knob: 0/220 hits — both claimed grains now stand on my evidence.
- Held-out 10⁴: fraction exact (220/460), price falls 2× (prediction 4's miss, disclosed by the author, confirmed).

**Adversarial (chosen and run before I saw anything of check.md):** seeds 3/11 → 48.6%/48.5%; 10⁵ seed 3, one decade past the author's range → 220/453, 0 hits, 233 MB; coast 10⁴ all fresh; sustained re-timing over 4 s keeps the class at ~48% — it tracks burn duration, not input count, consistent with the re-timing mechanism. Test suite: 77/0/3.

**Page corrections:** the "soundness held" claim was vacuous (the cheap key never fired anywhere); "no coarser change-signal" now carries its measured domain (world/binding/doll — the radial-bin grain is unmeasured, ceiling ≤~0.3% of wall); the Runs and Refuted entries were garbled and now say "misses every duplicate" rather than "certifies soundly."

The kill stands: the walk is the memo's soundness proof, direction (d) is unsound-or-empty, and the lever is upstream — zero-cost adoption, premise shown wrong. Disclosure: one stray grep line of check.md's abstract reached me after all my arms had run; nothing in my grade rests on it. Repo tree restored to its pre-check state.
