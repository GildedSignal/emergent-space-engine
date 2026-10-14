Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-0000-fermi-3071/check.md`, with two corrections applied to the author's `wiki/nladder.md` and the tree restored clean.

**Reproduction** (clean tree, patch applied by me): ho1rep digest `aca905ad7792…` is bit-identical to ea91's stored census (items, cut_tick equal); `analyze.py` regenerates every table; my own independent Gini/Zipf/Spearman code reproduces all quoted numbers (roster Gini 0.759, ρ 0.94–0.96, identical native counts across seeds 3/7/11 and m48/120/400, kicks 266 = 2·133, items 533 = 2·267−1, player 417→350, A 5/5, B's two misses).

**Adversarial cases** (three, two outside the author's domain — all *support* the adjudication):
- **rtf 300** (T≈16,500, one decade beyond): ladder bodies scale ×2.99–3.00 exactly; G_all keeps rising 0.737→0.753→0.764 toward the native ceiling, confirming the author's disclosed miss mechanism; player 1.64× (schedule-bound, not 3×).
- **m4 member floor**: native items bit-identical to m400's; G_all → G(nat) as members vanish.
- **Probe digest-neutrality**: probe-off digest equals probe-on.

**Why silver, not gold**: the core decomposition is real and adoptable (merge the resolved page), but the held-out record isn't clean — prediction 6 failed outright (G_all rose) and prediction 5's G(nat) band missed by 0.003 *inside the pre-registered kill list*, whose pre-registered consequence the author overrode post-hoc. My rtf-300 run independently confirms the override is scientifically right, but gold's letter ("the held-out predictions held") isn't met. Also caught: the "±0.013" model-accuracy claim is false for tune (0.017), the page's "266 = 2·133−1" arithmetic was garbled (fixed), and the measured G(nat) is not T-invariant (0.736→0.713→0.717) — only the ladder bodies' Gini is.

**Gold path named**: make the member/driver half arithmetic too (birth-burst formula + player count from the shipped decision schedule), pre-registered on fresh scenes — then no measured half remains.
