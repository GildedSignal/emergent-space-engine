Working...
Check complete. `check2.md` written: **Grade: gold**.

**What I did** (45-min budget, clean tree, `work/patch.diff` applied by me, then reverted):

**Reproduced exactly** — every integer matches:
- **B14 harness** (the run's only code): oracle 11.6 s; law 24.7/47.8/86.2/167.8 s at N=1..4; classification 187/243/243/242 of 255, apsides 0/0/2/11 of 53 — identical to the dossier's table. My trace regenerates the author's exact integers (kicks/moon 1300/3013/5952/11905; lost 49/9/11/13; zero refusals). Steps 5–7 are arithmetically forced: exact kick counts × measured ≈53 µs/kick reproduce the logged 330/645/1292 s within 1.5%.
- **B13**: N=7 and N=9 bit-for-bit, plus **my own sweep of every cadence this run never logged** — 0, 0, 1, 3, 15, 41 of 64 at N=1..6. The claim "fails at every N=1..9" now verified across the entire range; the "3–41/64 in B17's pass band" is exactly the measured 3/15/41 at N=4/5/6.
- **B17**: F/F/F/P/P/P at N=1..6 with pump ratios identical to six digits.
- **CLI**: N=1 FAIL 35.89 s; N=2 FAIL 59.19 s (the 60 s straddle is real).

**Adversarial cases** (all supported the claim): the refusals probe on the *worst* draw #68 at N=9 (not the author's example #40) — bound, nearly radial, same-tick re-refusals, `NoBoundOrbit`, and I read the raise at kicks.rs:157–176 myself; trace forensics (two of thirteen lost at 0.36 periods; lost moons refusal-free); the law-dominance correction quantified (80% law at N=2, 93% at N=4 — machine-independent since kicks are cadence-linear by construction).

**Integrity**: predictions.md (09:31:08) predates every decisive log; the two missed cost predictions were reported as misses — and they *are* the correction (honest failure, unlike the 1 October precedent that lost gold for reporting a miss as held).

**Gold rationale**: reproduced everywhere executed; pre-registered behaviour predictions held; two premises shown wrong by measurement (the passing-fixed-cadence premise behind q-cadence, and the oracle-dominated budget reading); adoptable in one step (brief rewrite, no code). Novelty checked against HISTORY.md (ends at H0215) and law.md — B17's band was already cited (disclosed by the author); the flyby-tube mechanism, B14's per-cadence record, and the correction are new.
