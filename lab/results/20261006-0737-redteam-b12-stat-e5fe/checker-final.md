Working...
Check complete — `lab/results/20261006-0737-redteam-b12-stat-e5fe/check.md` written, nothing else in the folder touched.

**Grade: silver.**

What I did, and found:

**Reproduced (clean tree, patch.diff empty):**
- Probe regenerates **byte-identically** (7/7 files, md5).
- `stats.py`: all 11 exponent rows of table 1 match exactly; draft-cell ratios match (bounded-e 1.75, r₂ 1.34); S* bounded-a 2.90 ✓.
- My independent implementation of frozen config A matches the dossier on **15/15 laws** and all four one-ulp ranges exactly.
- Real harness agrees: the ignored probe test fails today (leak 1.094 < bounded-a 1.103; walk control 3.1e5), planted laws read 1.355/0.353/0.416, and `behave --law echo --gates B12` fails on this box with "1 not converged, 1 inside; 0 of 14 judged" — §3 verbatim.

**Where it falls short of gold:**
- **Detector B has no shipped code.** Under six natural readings of "within-cell median spread" its table does not regenerate (compound 4.64 → 9.2–9817), and bounded-r2 flips across the 1.5 line between min-visits choices; under the pairwise reading the true leak passes *both* probes. Decisions match under MAD; the quoted margins don't.
- The true-leak A reads 1.17 in my faithful port vs 1.55 claimed (verdict identical), the fate triple {1,4,13} is not regenerable (14 ships flip in my run — the point is stronger, the specifics aren't), and the shipped fate command crashes.
- Predictions were pre-registered on time and qualitatively held, but P1/P2 numeric ranges missed and the dossier flags only some of that.

The premise-kill (B12's exponent is a level test that fails its own reference at every tolerance) is solid and answers the red-team the integrator queued in law.md. One experiment from gold: freeze detector B in code, regenerate its table with one-ulp replicas, and run one real law through A+B.
