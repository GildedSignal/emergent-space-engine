Working...
`check.md` written: **Grade: gold**, 120-word abstract. Full check summary:

**Reproduction.** Clean tree, patch applied, batteries re-run myself (runner's regen.sh: exit 0). Demand mode bit-stable (events 3/16/24, worst frames 42/579/1,036, fixed-granularity 30,721); paced 8 s gives 6/23/24/5/1 events vs 636/897/1,084/404/377 kicks — the author's ±1 kick is the disclosed wall-clock variance of paced counts. Per-window budgets (median 8.687×10⁶, max 1.490×10¹³ at L15) identical across seeds 1/7/3.

**Derived numbers** (not printed by regen.sh's summary) recomputed from a fresh full kick record: ratio medians 4.49×10⁻¹⁰/2.82×10⁻¹¹/3.52×10⁻¹² ✓, plunge tail 1.517×10⁻⁴ ✓, top-149 kicks = 100.0% of the 1.558×10¹³ tide sum ✓, dive clocks ≈2³²·³ from `step_for`'s Passage branch ✓.

**Instrument.** All 39 coast kicks have `clock_full == step`; source reading confirms `plan_interval`'s `want = step_for(...)` then `.min(thrust_step)` — the probe measures exactly the pre-clamp law cadence, counters-only.

**Adversarial (4, one outside range).** Paced 16 s (2× longest tested): L15 still 24 events vs 1,167 kicks; reverse L15 brake (untested level×direction, deepest dive): 23 vs 969; keys re-asserted every frame at L15 (real-client pattern): composition unchanged, 24 vs 1,085; seed 3 agrees. Law-bound kicks 0 in every flight of every run. No inversion anywhere.

**Predictions.** `predictions.md` (02:53) predates all records (02:55+) and the dossier (03:01); smoke-test familiarity of the 4 s counts disclosed; P1–P5 all held.

**Page.** Conflict resolution faithful, fold-in honest; I corrected one defect in place — a literal `({RUN})` placeholder, now the run id.

**Residuals named in check.md:** the "0.02 of 24 events" is the plunge-window share (the per-kick integral gives 0.39, dominated by one transitional kick — both ≪ 1, conclusion unaffected); regen.sh's grep strips the kick lines the two derived numbers come from; "~0–25 events per burn, dive-set" holds only for ≤8 s flights (16 s L8 accrues 24, linearly).
