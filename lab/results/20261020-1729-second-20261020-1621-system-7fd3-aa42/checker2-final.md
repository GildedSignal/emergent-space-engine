Working...
**Grade: gold** — written to `check2.md`, blind to the first checker.

**What I did:**

1. **Reproduced from a clean tree**: applied `work/patch.diff` myself at base `30860cea`, rebuilt, reran `regen.sh` end to end. Every dossier number lands inside the stated spread (bench wall 0.366–0.430 vs 0.367–0.427; stages 0.845–0.866 vs 0.842–0.861; belt wall 0.257/0.264; scaffolding 41–57%). Bench counters and digests bit-identical across author/runner/my runs — the census doesn't perturb the bench.

2. **Verified the crux at the source**: a765's stored table on its branch computes to 0.894/0.882/0.876, and its "rebind mean" column (60–71 µs) is exactly the `from_state` total (my fs_total 62.8–75.3) — so its 85–90% was compile/of-stages all along. The contradiction genuinely dissolves into denominator × scene. Verified the outside-from_state code reading line by line (bind.rs L274–294, word retry L238–254, step.rs L363–372).

3. **Four adversarial arms, two outside the author's swept ranges**: bench seed 1234, `--seconds 30`, rtf 300 (all: wall 0.405–0.409, stage 0.844–0.846, scaffolding ~52%), and belt 3×10⁴ **burn** (wall 0.297, compile 8.8 µs/mint, scaffolding 39.9%). All hold the cell structure; the burn belt refines "scene" to the population's e, not the activity.

4. **Predictions timing confirmed** (17:33:21 < runs 17:38 < dossier 17:39); honest kills of the pre-registered fork.

5. **Corrected the author's page in place**: the scaffolding was called "second-largest on the belt" but it beats the compile there too (11.5–12.7 vs 7.3–8.2 µs) — now "largest measured term on BOTH walls"; folded my arms into the domain sentence.

**Why gold**: the named experiment that gated 7fd3's silver, run whole, both standing numbers reproduced from their own cells, the new largest wall term measured for the first time, and both redirect premises (7fd3's "next 10× is the fit", a765's "compile-bound rebind") shown mis-scoped — adoptable in one step (print-only). Named misses: the belt ranking slip, the mints>rebinds attribution bias (makes 41–57% a floor), the two non-identity JSON fields the patch drops against its "print-only" claim, and the unpriced scaffolding internals (the next run's first hour).
