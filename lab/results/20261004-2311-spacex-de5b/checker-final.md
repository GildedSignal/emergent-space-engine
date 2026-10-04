Working...
Check complete. `check.md` written; nothing else in the run folder touched; no git commands run.

**Grade: silver.**

**Reproduced:** `results.jsonl` byte-identical on rerun (6.2 s, one command); predictions predate the decisive run by mtime order (…446 → …463); patch empty; corrector round-trips exact to 1e-16 with REBOUND's published coefficients; euler control fails everywhere; novelty clean (`lab/queue.txt:6` queues exactly this).

**What stands:** the corrector kill (0× — gate outcomes identical everywhere, J slightly *worsened*), the mechanism (no O(ε·dt²) term in these observables), y4's ~dt⁴⁸ J scaling, precession-not-J binding on s1, and the cadence deletion surviving my 4×-horizon probe.

**Why not gold, in three findings:**
1. The frozen S3 element gate is silently absent from `summarize.py`. Under it, **dkd fails the close-pass scene at every K ≤ 64** (final-a error 1.6–5.3% vs a 1% gate with a 0.008% reference floor) while **y4@16 passes** — the dossier's "y4 3× worse on the close pass" is inverted under the author's own frozen criteria.
2. "J alone passes at 16/orbit on every s1/s2 moon" is contradicted by the author's own shipped table: ho-e30-0.4 needs K=32 (j_max 2.33e-4 at 16). Deletion is 2×, not 4×, at e ≈ 0.3.
3. The retro-0.6 precession gate is estimator-fragile at the 40% level (my probe: full-fit 2.17e-2 vs second-half 1.30e-2 on the *same* reference trajectory) against a 10% tolerance. My K=128 probe confirms the scheme difference is real, so the finding survives — the gate as frozen doesn't measure what it claims.

**Gold path named:** one ~10 s rerun with the S3 gate implemented and a secular-frequency P estimator.
