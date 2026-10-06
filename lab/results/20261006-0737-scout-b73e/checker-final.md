Working...
Check complete: `lab/results/20261006-0737-scout-b73e/check.md` written, **Grade: silver**. Tree restored, nothing else touched.

**What I did (19 min of 30):**
- Applied `work/patch.diff` in the clean tree, built (`release`, 26 s), re-ran the dossier's five core commands serially, then 10 parallel adversarial benches and 5 serial knee/held-out benches — 20 runs total, all ≤ 30 s, ~1 core each.
- Read the engine (`frame_to`, `advance`, `Dash`) to judge the v2 transplant's faithfulness and the metrics.

**Reproduced:** digest `87f51de403a46799` bit-identical across all policies (also seed 7 → `0c9bbe61…`, members 200 → `c0e6a443…`, rtf 1 → `b411cce8…`); overflow counts match the author within load noise; the knee direction holds everywhere.

**Adversarial findings:**
- The knee's interior (7/9/11 ms — the author only measured endpoints 5 and 13): 0 hitches at 7 ms with lo1 0.023, 5 hitches at 9 ms with lo1 2.9 — "no constant meets both halves" survives and is now measured in between.
- Held-out rows the author never reached (seed 7, members 200, patched rtf 1) all hold; prediction 6 was shipped untested (stock binary, disclosed) — I tested it, it holds.
- Two defects: the tables' "hitches/h" column is raw frame counts (×120 off), and ahead's RTF median (4.28 > 4.0) is a pre-clamp frontier metric artifact — both recorded; neither flips a conclusion.

**Why silver, not gold:** real, reproduced, honest about failed predictions — but no 10× move, nothing deleted from `main`, and the structural mechanism (cascades longer than any rebuildable lead) is inferred, never measured. The gold-making experiment: log cascade length vs rebuildable lead on the plane's own bursts.
