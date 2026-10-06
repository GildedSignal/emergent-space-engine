Working...
Check complete. Verdict written to `lab/results/20261006-0030-library-39a2/check.md`: **Grade: lead**.

What I did:

**Reproduction — clean.** Ran the dossier's commands: the three greps land at exactly :15802, :190, :2653. My own fresh Gutenberg fetches match the cached texts byte-for-byte (md5 `f476f74e…`, `12742dc1…`); the texts are genuine (Halsted omnibus #39713, "SCIENCE AND METHOD" part at :14323, "CHANCE" chapter at :15687–89; Lefèvre #60979), and the quotes are verbatim in context. All five books are on `goodreads.csv`.

**Pre-registration — held.** mtimes: predictions 00:34:16 < fetches 00:36:37 < dossier 00:38:35; patch.diff empty.

**Why lead, not silver:**
- The only decisive prediction, P1 (≥ 4 of 5 quotes verbatim-retrievable), **failed 2/5** — honestly reported, but the lens charter's "verbatim highlight per lesson" is met for only 2 of 5 lessons.
- P2–P6 are untested proposals. Every load-bearing change is already owned elsewhere: least-slack cadence is board #4 verbatim plus the queued `q-cadence` lens; setup-by-predicted-conjunction is r8 v3's recorded next step plus the adopted dormant-pair deferral; frame scripts are plane.md §7; gravity-is-news with thrust-arrival tests is the queued `q-gravity-at-c` spec; doll clocks are law.md's open simultaneity item. The deltas are three small sharpenings, none measured.
- No engine number was measured; the claimed gain (B12 exponent 0.8 → ≤ 0.2) is the board's target quoted back. Precedent: `71a7` (30 Sept) graded lead with a real Readwise export and five verified quotes and no measured gain — this run has less library evidence and the same zero measurement.

**Attack that stuck:** lesson 5 ("the root clock is a derived calendar") reopens plane.md §2's "The root clock is canonical" without acknowledging the conflict.

Nothing else in the run folder was touched; no git operations run.
