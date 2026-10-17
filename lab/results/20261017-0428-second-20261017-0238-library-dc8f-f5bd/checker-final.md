Working...
Check complete. `check.md` written; the author's page corrected in place where it overstated.

**Grade: gold.**

**Verification chain (all numbers re-derived, not trusted):**
- **Reproduction:** regen exit 0 on clean tree + patch. The 5,400-gs calibration is bit-for-bit (OFF 334/136/22,219/9,217; arm 131/26/6,580/1,382), T4 states identical, and — decisive — the arm's full 8×10⁶-gs flight regenerates its ledger exactly in the checker's own rerun (632,170 kicks / 1,263,346 events). Record probe 2.620×10⁻⁴° / 1.181×10⁻³°.
- **Independent recompute** of the debt curve from the raw traces with my own code: 0.698° @ 2.08×10⁵ gs, 2.18° @ 1.03×10⁶, 14.65° @ 7.41×10⁶ still rising; t^2.15 dead by 99×, linear-from-11k dead by 18× under; fits t^0.87/t^1.18/median t^2.01; crossings for every behavioural bar ≥ 10⁻²° measured inside the flown range (k\* = −0.1/+1.7/+3.7). Spared set 540/540, zero mismatches. No NaNs; the max genuinely switches bodies (17 owners).
- **The kill needs no extrapolation:** the published 2.6×10⁻⁴° at 5,400 gs sits 3,102× above the law's coarsest acting grid (the tube's 32-bit periapsis angle, 360°/2³², quote verified in docs/law.md). The fence and the 10⁷-gs constant die by arithmetic on published numbers; the flight adds the replacement law.

**Defects found (side claims, corrected on the page, none moves the verdict):** the tube-grid and 10⁻⁶° crossings are extrapolated below the first horizon (0.7–130 gs across fits), not "measured inside the flown range"; the 1,900-gs calibration ledger quoted in the dossier has no artifact anywhere in the run; the quoted bench ns come from a flight the regen overwrote (surviving runs: 0.57–0.6×, same verdict); the "6 late belt joins" are doll-2 in-situ bodies; analyze.py hardcodes the word-quantum ranges (I verified them from the dump: 2.50–5.63×10⁻¹⁷°) and its late-joins print subtracts an int set from strings.

**Predictions:** pre-registered before both decisive flights; 3/5 held outright, 2 wrong in magnitude but verdict-preserving with falsifiers that did not fire — honestly graded. Topic stays open (one gold, not three agreeing).
