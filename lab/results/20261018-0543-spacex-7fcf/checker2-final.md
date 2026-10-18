Working...
Done. `check2.md` written with `Grade: gold`. Summary of the blind second check:

**Reproduction** — Applied `work/patch.diff` to pristine `5597227` myself; verified its composition (step.rs/nladder.rs hunks = f134 verbatim, probe = 87fd verbatim + 12 disclosed print-only lines), rebuilt, flew: `off_110` and `both_110` bit-identical to the author's `flights_ref`, which is itself bit-identical to the runner's regen — three independent executions, zero differing numbers. Arming controls match 87fd's frozen records (corroborated from its published branch: 2.0→19.8e-6, 7.4→19.4e-6, 1.28e-3, the 251 collapse).

**Predictions** — `predictions.md` predates the flights; P1–P4/P6 hold exactly, K1–K3 never fire; P5 failed as worded (frac<1e-12 = 0.096–0.21 vs ≥0.5), disclosed honestly, and my runs confirm both the miss and the substitute witness (p25 separation 1.9×10⁵).

**Adversarial (one beyond the flown range)** — 22,000 gs (2× the worst flown horizon): composed median flat 5.4e-11 vs OFF 5.2e-5, spared tail again bit-identical to chain+stagger's; seed 3 holds; N=10⁴ clean; `ES_SECULAR_RES=1` leaves the tail bit-identical (the tail is the in-situ illegal set, not the resonant quarter).

**Novelty/goal** — Closes the live page's direction 1, the explicitly named single remaining adoption debt of the composed law (−89 % ledger at the worst horizon) on the furthest-gap bottleneck. Page fold is faithful (its multipliers are the correct ones); I added one bracketed checker-2 note with my held-out evidence and letter corrections.

**Blemishes recorded**: the dossier's ratio column has two 10× slips and "424×/820×" understate by ~10³ (page is correct); OFF's "×10 per doubling" is horizon-local (×2.2 from 11k→22k); the frac witness decays with horizon; N is a dead axis for this legality probe. Tree left pristine; no commits; flights untouched (my runs in `/tmp/check2`).
