Working...
Check complete — `check.md` written, tree restored, build dir removed.

**Grade: gold.**

**What I reproduced in a clean tree** (patch applied via `git apply`, fresh target dir, test-binary hash identical to the author's):

- **B14 cost split (the run's new harness), N=1..4:** verdict integers exact — classification 187/243/243/242 of 255, apsides 0/0/2/11 of 53 — with walls within 2% of the author's (law 26.3/47.7/86.1/164.5 s vs 26.4/48.8/86.9/167.0; oracle 11.8–15.2 s vs 12.9). The original author's unlogged N=2 line regenerates exactly; the load-coin-flip gap is closed by a timeout-free record.
- **Traces bit-identical:** lost 49/9/11/13, kick totals 323,694/766,103/1,514,060/3,026,047 — the same integers to the digit. From the trace: exactly one refusal event in the whole B14 sweep (so lost moons carry none), two of thirteen N=7 losses at 0.36 periods < 0.4, µs/kick converging to ≈53.6.
- **B13 bit-for-bit:** the N=7 failing draw set with all magnitudes, and the refused state at draw #40 N=8 to the last printed digit.
- **B17:** N=1/3 FAIL and N=4 PASS with bit-identical floats — the pass band is real.

**Adversarial cases:** B13 at N=10, never run by anyone — 53/64 (worse than N=9), 11 failing draws all `NoBoundOrbit`, refusals multiplied to 2,578, confirming the dossier's "refinement makes it worse" extrapolation at the first point beyond the sweep. Trace arithmetic makes the classification cap airtight (lost ≥ 9 at every N≥2 ⇒ ≤ 246 < 253). My own split independently confirms the law-dominated correction (oracle ~13 s vs law 26 s already at N=1).

**Predictions:** pre-dated every decisive log (09:31:08 vs 09:32:48+); the load-bearing behavioural claims held exactly; the two missed Fermi cost priors were honestly reported and constitute the correction itself.

The silver's named gold experiment is done and verified on both pillars; adoption is a q-cadence re-aim with zero code cost. The misses I recorded are minor (the "confirmed in situ" wording is +24%, the 1.78 ratio, N=6's one flip, B17's N=7 being budget-only).
