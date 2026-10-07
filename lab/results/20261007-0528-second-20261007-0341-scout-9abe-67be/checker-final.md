Working...
Check complete. `check.md` written to the run folder; nothing else in `lab/results/20261007-0528-…/` was touched (all work in `/tmp/chk`).

## Verdict: gold

**Reproduction (all bit-identical):**
- `cadence.py S2c,S2d,S2c2,S3,S4` (7.7 s): 0 diffs vs both this run's stored JSON and the original scout run's (commit 7e3053e); the script is byte-identical to the original's.
- `lattice.py full` (77.8 s): 0 diffs vs `out_full.json`. `analyze.py`/`gatesens.py` reproduce every headline: 17/62 certifiable, first-order 1/30, gate variants 1.05–1.18×.
- Oracle recomputed **independently** from raw JSON: 466.8 → 409.6 evals = 1.140×, 377.2 kicks = 1.237×, same winner counts. The 4× bar dies even with free trigger evals.
- The precedence bug verified from code + arithmetic alone: S2c n_per = 0.68571 (+2.29 W from 3:2, +14.86 W from 2:1), S2d 0.98 W from the true 2:1, 7.92 W separation — all four dossier numbers exact. The original "inversion" never tested a 2:1.
- predictions.md (05:38:24) predates out_full.json (05:39:53, a 78 s run); the pilot calibration is bit-equal to lattice row `21_d+0.000_p0`; calibration JSONs are pristine copies.

**Adversarial (4, all confirming):** truth converged to 6 decimals at 4× resolution; fresh phases π/6, π/3 at both centres still certify nothing; μ=1e-4 zone rows fail with *identical* margins (self-similar — stronger than claimed); 5:3 at e0=0.1 still only FIXED-64.

**Two slips found, neither material:** the dossier's "5:3: 0 certified" is contradicted by its own record (2/15 rows hold FIXED-64@66.1, and its oracle already counts them); P5 is self-scored "held" though its de-phased 1.5–3× sub-claim failed. Both go in "what the author missed."

The run deletes the cadence-law branch before the queued 120-minute q-cadence spend, corrects the silver predecessor's evidence at its root, and leaves only the frequency selector — adoptable in one step at zero code cost.
