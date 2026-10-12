Working...
Check complete. `lab/results/20261012-1227-dynamics-bd4e/check.md` written, first line `Grade: silver`; tree reverted to HEAD; nothing else in the run folder touched; no commits.

**What I did:**
- **Reproduced bit-for-bit.** Applied `work/patch.diff`, ran the dossier's command: `b12type.csv` and `b12traces.csv` regenerate identical; all medians match; β/z independently recomputed from the trace CSV match to 3 decimals. Predictions (12:33) predate the data (12:42). Step 7 is the plane's genuine default, not cherry-picked.
- **Attacked.** (1) Plane at step 9: different 8 ships answer, β median 0.000, max 8e-8 — the bounded verdict survives cadence and subset. (2) The slow 1e-12-per-period leak that killed the recurrence ratio: this instrument reads β 0.176, z 0.10 → **bounded, would pass** — the same hole, and today's exponent catches it. (3) Ensembles: true random walks read β ≈ 0.4 at any horizon (0.46/0.38/0.42 at 200/600/2000 periods) and bounded AR(1) ρ=0.9999 reads 0.434 — no threshold separates the classes at playable horizons, refuting the dossier's "longer horizon" fix.
- **Novelty/goal fit.** Structure function is new in the repo; real bottleneck (HANDOFF line 71, `q-b12-design`); the plane adjudication — B12's exponent convicting a bounded error on the shipped engine — is adoptable now.

**Verdict: silver.** The plane adjudication holds and reproduces; the proposed statistic does not — it fails the exact control that killed its predecessor, so the next run must combine type-by-β with a leak control before any freeze.
