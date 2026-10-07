Working...
Check complete. **Grade: gold** — written to `lab/results/20261007-1550-dynamics-71a5/check.md`; nothing else in the run folder touched.

**Verification summary:**

- **Reproduction (exact, different host):** `cert2.py` regenerated `results2.json` identical to the author's minus the machine block; `cert.py`'s log matched `run1.log` line-for-line including the disclosed end crash; the `results3` snippet reproduced all 12 `first_below` values bit-for-bit. Wall times match the dossier (220 s / 72 s / 61 s).
- **Predictions:** written before the decisive runs (file-time order verified). Controls (1) and engine scaling (5) held on both sides; 3 failed as written but its pre-registered fallback was honored and the corrected t_tang = travel/Δϖ̇ law confirmed by exact halving + brute force; 2 and 4 honestly reported unresolvable/skipped.
- **Adversarial (3 own cases):** the untested *toward*-tangency direction still realizes every encounter after t_tang (now 14/14 both directions); independent bisection reproduces Δϖ\* = 0.7269, near/far travel 0.0269/1.4269; at e = 0.7 the controls stay exact and differential precession produces real misses — mechanism confirmed in the regime the author admitted untested.
- **Novelty:** holds. `crates/encounters` genuinely models a static `pom`; no HISTORY/board entry couples Δϖ̇ to section aging (r8 v2/v3, q-candidate-degree, taleb-09b5 are all fixed-element). Corollary recorded for the board: the phase-neighbour certificate is immune (equal p ⇒ rigid rotation).
- **Gold basis:** a premise in adopted law.md ("valid until a kick … no work per orbit") is shown wrong in the law's native strong-field regime (40–400 orbits at p ≈ 50 M, 4×10⁸ weak-field), measured against the design's own tube dynamics, adoptable in one design step (co-precessing sections).

Recorded flaws: the 6×10⁻⁴ rad/orbit parenthetical is ~10× off, the stored B2/results3 t_cross columns encode the wrong-direction tangency, the snippet doesn't regenerate results3.json exactly, and the miss-rate evidence at G6 is one event.
