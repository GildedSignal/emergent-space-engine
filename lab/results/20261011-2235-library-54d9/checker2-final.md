Working...
`check2.md` written. **Grade: silver.**

**Reproduction:** exact, in a clean scratch tree — every table number regenerates (A: −2.42 fit, 14 evals for D=1e-5; B: 21668 evals = 1548×; behaviour 1.155 rad vs 0.017). Determinism witnessed: the author's surviving early `jA64b.json` is bit-identical to my fresh run, so the shipped code is the code that ran. Pre-registration holds on mtimes (predictions 22:40:45 < final sim.py 22:46:06 < first run < dossier); run.log is empty, so that evidence is mtime-only.

**Oracle:** sound — I re-derived that `jacobi1` is the exact CR3BP invariant (the barycentric-shift terms cancel: MUP·v_p − MUP·Ω×r_p = 0); the unshifted control sits flat at 3.93e-4 at every rate; Kepler drift is machine-exact (r error 2.3e-13, energy 4.0e-15).

**Adversarial (all beyond the author's, all confirming the kill):**
- Seeds 1 and 7: B/C walk (slopes 0.91–1.00), A/D flat.
- ±0.5-octave interval jitter does **not** cure the walk (slope 0.83) — the mechanism is the gate's weight allocation (long intervals at field extrema), not decorrelatable phase-lock; this answers the dossier's own untested caveat negatively.
- Narrow-clamp gate (clamps inert, matched rate): slope 1.00, 185× worse than fixed — the walk is state feedback itself, not clamp saturation.
- 5× horizon: A/D flat (D@8's flagged 0.37 slope resolves benignly), B/C keep walking.

**Why not gold:** the headline walk was already known (probe 1, 29 September, "energy exponent 0.47–0.98; fixed step flat"; Calvo–Sanz-Serna on the board); held-out predictions P1/P2/P5 failed (honestly reported); it is a float replica, not the engine's kick layer. The genuinely new parts — the state-dependent vs precomputed-from-constants split, the matched-cost quantification, and the B12 slope statistic aimed at queue-top `q-b12-design` — are real and adoptable now. Gold experiment named: wire the gate and the slope statistic into the plane's actual kick layer under q-b12-design.

Also flagged: fixed cadence has individual resonant walkers (maxSlope 0.55–0.71), so B12's slope statistic must judge the population median, not the worst body; and three small dossier overstatements (wake-ratio range 1.10–1.47 not 1.35–1.47; D@8's 0.37 outside the table's slope range; C's cost omits the derivative eval).
