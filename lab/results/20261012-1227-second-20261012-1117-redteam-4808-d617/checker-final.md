Working...
Check complete. **Grade: gold** — written to `lab/results/20261012-1227-second-20261012-1117-redteam-4808-d617/check.md`; nothing else in the folder touched, no git operations.

**Verification performed:**

- **Reproduction (bit-for-bit, all four scripts):** `check_instrument.py`, `kickgate.py`, `scatter.py` (1–2 s) and `linger.py` (6 m 12 s) each match `run.log` exactly — all 15 gate cells, random-sign rows, 30 scatter cells, all four linger blocks. Patch was empty; controls behave (positive μ=2 passes, negative μ=0.03 fails), so not VOID.
- **Holdout:** `predictions.md` predates every decisive script by 9–28 min (mtimes); the scorecard discloses its own misses rather than burying them.
- **Five adversarial cases:** (1) δL² scaling re-measured — 1.840e−4/1.840e−2/1.841e0, matching the dossier's unt-eed numbers; (2) low-e band cells (e=0.1, 0.25) fail *harder* (up to 21 rad/10³ kicks) — the failure spans all eccentricities where the band exists; (3) six scatter bodies re-integrated as geodesics — band/bound/plunge classifications all correct; (4) the prior checker's two disputed refs shown to be its own artifacts (its ODE sides with this run's quadrature to 7 digits); (5) the family instrument's domain (r_p < 6) covers every band cell.
- **Novelty/fit:** no HISTORY or docs entry covers this; it amends law.md's live jet entry by showing the 730-quanta re-anchor trigger watches the wrong quantity on a fed domain — adoptable in one step (domain rule + drift counter, ≈0.01 compiles/kick).

**Flaws named in check.md (none decisive):** the δL sweep wasn't regenerable from shipped scripts as-is (I verified it); the claim line overstates budget A ("fails both budgets" — A passes by 4% at (0.99, 0.3), disclosed only in the scorecard); the e=0.99 degeneracy is blamed on μ=0.53 (that's e=0.9's value; e=0.99's family ends at 0.32); the dossier cites only the four prior-checker values it matches, silent on the two rows that disagree.
