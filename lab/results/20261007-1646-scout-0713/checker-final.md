Working...
Check complete. `check.md` written to the run folder; nothing else touched.

**Grade: gold.**

**What I verified:**
- **Reproduction, bit-identical.** All seven stored outputs regenerate exactly from the dossier's commands: selftest (split verified second order, 88× error drop for 8× kicks; truth convergence 1.1e-5), singles cal/h1/h2/h3 (with the stored full-precision eps_v the rows compare `==` in Python), ruleP singles, and the decisive 192-body mixed scene — every field equal (ladder 7.8%/0%/37.5%/100%, global fixed 8, totals 47714/75279, cuts 1.0301/0.6529). The pre-registered kill criterion (< 2×) fired at 1.03×.
- **Predictions.** The kill criterion predates all held-out runs; P7/P10/P11/P12 held; P2/P3/P4/P8/P9 failed against the candidate rules and are reported as failures. The wrong-direction predictions self-certify pre-registration despite the mtime caveat (addenda moved the file's write time past the A/B runs — noted in check.md).
- **Adversarial (4 of my own):** a fifth scene (e=0.2, D=60) confirms transfer-and-no-cut (PB 12.5 vs robust minimum 4); h2 at 96 orbits confirms the non-monotone ladder and shows the robust minimum itself is horizon-dependent (8→4); e=0.9 exceeds the harness's truth convergence (39% slope drift) — the probe's honest boundary, never measured by the author; the A/B calibration boundary is ~2× above the claimed eps* (immaterial: larger eps fails h2/h3 harder).

**Why gold:** everything regenerates, the kill was pre-registered and fired, my held-out cases confirm rather than weaken it, and it redirects the queued q-cadence lens before build spend plus installs the robust-minimum evaluation warning — adoptable at zero cost. **Misses recorded:** horizon-dependence of robust minima, unmeasured truth-convergence boundary per scene, calibration overstatement, the uncited Calvo–Sanz-Serna board lead, and the loose e=0 budget behind the 30× figure.
