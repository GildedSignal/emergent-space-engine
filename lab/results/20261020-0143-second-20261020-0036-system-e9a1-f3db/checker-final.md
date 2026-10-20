Working...
Check complete. `check.md` written with **Grade: gold**, and the author's wiki page corrected in place (additions only).

**What I verified:**

1. **Reproduction** — runner's regen (exit 0) matches every dossier digit within the disclosed wall-clock band (d1e5 871 ms/pull 866.7/105,486 root-pulled; cure arms 0 pulled, ≤16.3 ms). The `ES_ROOT_STREAM` hunks are ee4d's code verbatim (35/40 lines; the 5 differences are comments).

2. **The refutation is airtight — and I found the actual mechanism.** e9a1's committed branch logs pull 103k–204k ships at root in *every* burn arm (max 16,054/32,839/49,908-class), coast alone pulls 0. The real bug: e9a1's census awk did `split($4,a,"=")` then read `a["pulled"]` — split yields numeric subscripts, so every arm printed 0 whatever the logs said, and its *checker's* "fresh flights pull 0" ran through the same broken summary (the 5 October shared-harness lesson in miniature). The dossier's "coast census read onto the burn arms" was a correct-in-substance guess; the page now carries the proven mechanism.

3. **Adversarial cases** — (a) **3×10⁵**, a decade beyond both authors' item-probe range: worst frame 2,501 ms = one player item, pull 2,492.4 ms (99.7%), 49,908 ships nested; cure: 0 pulled, 13.1 ms. (b) **rtf 2000**, the dossier's own named failure mode: pull still the worst item (888/892 ms), and the scan wall is real and worse than recorded — 174 ms max. (c) branch log archaeology on all five e9a1 burn arms. Peaks 1.68 GB, under the cap.

4. **Predictions** — `predictions.md` (01:51) predates all flights; P2/P4 held; P1/P3 failed informatively with the failure handling pre-registered — the failures *are* the result (the pull was never empty).

5. **Novelty/goal fit** — cc9d attributed the gulp to the pull and ee4d's gold cured it, but the published page carried e9a1's "fleet loop" fix-target as current best with a checker's endorsement; this run deletes it with measurement, at zero adoption cost. Gold under "shows that a premise is wrong."

Misses noted in check.md: the misread-mechanism guess, one attribution slip ("ee4d's collapse against pulls = 0" — that claim is e9a1's, which post-dates ee4d), and "off = shipped bits" being not literal (unconditional timers, behavior-neutral).
