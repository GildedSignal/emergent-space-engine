Working...
Check complete. **Grade: silver** — written to `lab/results/20261012-0138-library-060f/check.md`.

**What held:**
- Reproduced bit-for-bit in a clean dir (4.6 s, deterministic, metrics JSON identical to the author's; empty patch.diff). The probe's "current B12" faithfully mirrors law.md's real gate — not a strawman.
- Zero per-seed calibration overlap verified on full seed distributions (bounded max 0.117 < compounding min 0.256); the quoted 0.009/0.38 margins and the 0.2-threshold-on-median (0.202) are exact.
- Pre-registration genuine (5/8 predictions failed with diagnoses — post-hoc documents don't contain that).
- Novel (no Hurst/range-scaling anywhere in docs or lab; the recurrence ratio was a different statistic), on a live HANDOFF risk, and all five lessons.md quotes verbatim in the Readwise cache.

**Why not gold:**
- The author's own pre-registered kill criterion ("any of 1, 2, 5 coming out opposite") **fired** on predictions 1 and 2; the dossier reframes to "the margin, not a misranking count" instead of declaring the configuration killed.
- My attacks found two unacknowledged false-alarm modes: **settle-to-bias** series (monotone rise to a constant, jitter < ~15% of the rise → Ĥ 0.5–1.08 "compounding" while the current statistic passes — a regular seed's exact signature, opposite-direction misranking to H0215's) and **slow oscillations** (period ≥ N/4 → 0.48).
- Not adoptable as built; nothing real measured (verified: no real Jacobi series exists in this runner's tree, so the plane test genuinely couldn't run here).

**What the author missed working in their favor:** the law's *actual* re-anchoring (frequent, small: ~0.05 compiles/kick) passes correctly (sawtooth → Ĥ 0.013) — their "what would make it wrong" overstates it; and H0215's misranking *is* synthetically reproducible (bounded staircase: current gE 0.26–0.41 fails, Ĥ 0.005 bounded) — their generator was just the wrong shape. Both recorded in the check; the gold step is a transient-robust range statistic plus the plane's real 16-seed series.
