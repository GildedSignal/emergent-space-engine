Working...
Check complete. `check2.md` written to the run folder; nothing else in `lab/results/20261011-0006-second-…-2b8e/` was touched, no git operations.

## Verdict: **Grade: gold**

**Reproduction — exact, every link re-run independently:**
- `hlive2.py` belt_s1 (seed 1): JSON bit-identical to the author's (sole diff: my `tag` string); naive16 117.33 = 90.5% of the 129.5 ceiling, smoothed med 23.14, p99/med 4.07, secular med 0.550/P_p
- W2048 (verified to be exactly the `sed` of `hlive2.py`): med 12.10 ✓; 1200-P_p long run: secular 0.556, fit 1.00147 ✓
- `entropy.py`+`analyze2.py` regenerate `metrics2.json` byte-for-byte; shipped-code record differs only in `wall_s_max`; the nats/bits ψ(N)−ψ(k) correction reproduces the stored 10⁶-run samples exactly (−8.492/−6.932)

**Adversarial (my own):** unseen seed 4 replicates every mechanism including tail structure (100% inner band, swept ratios 15.2/16.0/16.0); a 2:1 resonance ring — the author's declared weak spot — keeps the phase-lock linear (fit 1.013) with no libration blow-up; k-NN passes a uniform box (3.887 vs 3.878 true) and an independently generated birth ridge (−8.484 vs −8.492); bandwidth arithmetic re-derived (861 → 1.8×10⁵ events/wall-s; the parent's 2–4×10⁸ was 3–5 orders high).

**Predictions:** registered 00:10:39, before all runs. P1/P3/P4b/P8 — the load-bearing ones — held; P2/P5a/P6/P7 failed, each diagnosed into a mechanism and reported as failures (the honest-prediction discipline the lab demands).

**Gold rationale:** three premises of the parent silver shown wrong (window-dependent "13/P_p", the bandwidth arithmetic error, the log₂N-pinned "12.7-bit floor" — I confirmed 12.69 = log₂4000+0.72), a ~840× program-quality span quantified, and a measured 20.7→22.1 bits/ship mature footprint feeding the 10⁹-in-8-GB bottleneck; adoptable in one step, zero engine code.

**Flagged for the integrator:** the 10⁶-run full-sample k-NN is analytically corrected rather than re-run (verified exact on the two storable subsets; one 21-min re-run would harden it); near-exact-resonance and multi-stirrer cases remain open; 22.1 bits/ship is not yet a game-timescale number.
