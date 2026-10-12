# Lens: red-team of B12 v2 before it freezes (premise first)

B12 judges "errors never compound" on ships that cross a planet's sphere of influence many times. Its first statistic (a Jacobi growth exponent) ranked a bounded error above a compounding one, so it was rebuilt. Codex's candidate is on branch `origin/wt/cx-b12-v2`: `xtask/src/behave/b12_stat.rs`, `b12_corpus.json`, `handoff.rs`, and its receipt under `artifacts/evidence/cx-b12-v2/`. Its own result:
- echo and scaled pass;
- planted-bounded now passes;
- planted-compound, leak, planted-drift and planted-kick fail, as they must;
- the plane is UNSUPPORTED (sensitivity), over a horizon of 200 periods with 16 ships;
- the tested leak is 2e-10 per horizon.

Its author asked for a red-team of the correlated-return calibration and of the surface-domain proposal. Read the wiki page `lab/wiki/b12-statistic.md` first.

Attack the premise first, against PRINCIPLES: does this statistic measure compounding, the behaviour the player would see as drift, and is it calibrated where it decides, near its threshold? Then attack the letter, building in your folder (`git worktree add` the branch; never edit the crates, the gates or main). Plant at least three laws of your own, with your own errors, chosen to sit near the threshold:
- a slowly compounding error;
- a large but bounded one;
- a correlated-return artifact.

Report the statistic's verdict on each, with the distribution over seeds (n, worst, median), never a mean.

Gold: either a statistic that separates every planted pair with margin and that you could not fool, with the cheapest probe that would still fool it if one exists; or a clean break, the planted law it misgrades and why.
