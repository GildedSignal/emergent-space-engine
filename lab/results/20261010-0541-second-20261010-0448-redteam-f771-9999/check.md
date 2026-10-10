Grade: gold

**Abstract.** Claim: the re-frozen r1 (r1w) runs end-to-end — binet-m16 killed by the widened envelope on two frozen criteria (period 0.9766, precession 0.9883), binet-m32 passing every r1 criterion. Everything reproduces bit-for-bit (41 s, 38 MB; metrics sha256 stable across re-runs; controls match). My independent attacks all agree: a fresh 256-seed draw kills m16 again (0.9766) and m32 passes (0.9961, one per-seed fail — the Fermi hedge); m=70 at (7,0.99) measured 9.8e-4 at 1070 crossings, so 0.1% per-seed is unreachable in the 512 budget; moderate-e r_p<6M bands pass with margin; the old landing nudge loses 50% of deflection; m8 measured dead (0.918). Adoption: freeze r1w from the draft; integrator re-runs the shipped harness.

## Reasons

**1. Reproduction: exact, all three commands.** Clean scratch tree, shipped scripts, no patch (`work/patch.diff` is empty). `binet_probe.py` regenerates the shipped record (identical except the host line, 2.8 s); `r1w_run.py` regenerates `r1w-output.txt` identically and `metrics.json` sha256-for-sha256 (`ad519e7b…`), stable across a second run (determinism claim held); `controls.py` matches controls.txt's C4 (Gauss-8 vs 16: 4.81e-6, 1000× below the 4.75e-3 model error) and C5 (slopes −2.68/−2.70). The quick tie-out matches the shipped row exactly (4.45e-4 / 1.93e-2 / 246). Record arithmetic is consistent: 6/256 = 0.9765625 and 3/256 = 0.98828125, fail lists and e* table in metrics.json match the printed output. Timing honest (43.5 s, 38 MB).

**2. Predictions: written before the decisive run, honestly scored.** File order: predictions.md (t−27 min) precedes the last code edit (t−5 min) and the final outputs (t−4/−3 min); the two mid-run bug fixes are disclosed in the dossier and visible in the trail. 7/10 held (P1 0.9766 in [0.94,0.99]; P3 6/6 and 9.94e-4; P4 slopes −1.96 to −2.02; P5 hyperbolic bound; P8 6.7e-5; P10 0.95→0.99). The three misses are all held, disclosed, and in the safe direction: P6 and P9 predicted failures that did not occur (m32 more robust than predicted; the frozen repeat reading passes at 6.8e-16), P7 was the author's own amplitude-landing bug, fixed and re-verified. No predicted pass failed.

**3. My adversarial cases (six).**
- **Fresh draw, Random(20261011), 256 seeds:** m16 period fraction 0.9766 again (6 fails, worst 1.6e-2 at (5.8, 0.984)) — the kill is not draw-specific. m32 = 0.9961 with exactly one per-seed fail (4.1e-3 at (5.8, 0.984)), still ≥ 0.99 — the Fermi hedge ("1–2 fails, still passing") is exactly what happens.
- **The m≈70 extrapolation, measured:** at (7, 0.99), m=64 fails per-seed (1.176e-3), m=70 passes (9.785e-4) at 1070 crossings/cycle, m=96 at 1466. The "per-seed 0.1% needs ~1100 crossings, 2× the 512 budget" claim was a law; it is now a measurement, and it holds.
- **Moderate-e hyperbolic periapsides** (r_p<6M at e = 0.3–0.7, gate-legal; the author's grid only had e ≥ 0.95): five cases, all bound, period errors ≤ 7.7e-4 (m16) / ≤ 2.0e-4 (m32), precession ≤ 1.5e-3 — the hyperbolic branch is robust beyond the measured grid.
- **binet-m8** (candidate config in the draft, never measured by the author): period fraction 0.9180, low-e grid 8.5e-3–1.4e-2 — dead, as the m⁻² law asserted.
- **Invariant 2 counterfactual:** reverting the landing nudge to the shipped multiplicative `u·(1±1e-12)` loses 50.1% of the deflection at every b tested (err 5.1e-1) vs 3.5e-5 with the fix — the disclosed first-run bug story is real and the invariant is necessary.
- **Below the e floor:** at e = 0.005, r_p = 11, m32 fails per-seed (1.43e-3) — see missed item 3.

**4. Novelty: yes.** H0205 records r1 DISPUTED, "needs a clean PASS"; no HISTORY entry or doc covers the widened envelope, the low-e axis, hyperbolic bands, or the e*(r_p) table. This run completes precisely the experiment the f771 checker named as the gold deliverable ("run the re-frozen r1 end-to-end… that run *is* the gold deliverable"), and supersedes that checker's probe-level numbers (0.967 at 128 seeds) with the rung-level result.

**5. Goal fit and principles.** Shows H0205's "m16 passes every criterion" was envelope/fraction luck — a premise correction — and kills configurations binet-m8 and binet-m16, never the method ("A failed experiment kills that configuration, never the method", 9). The surviving m32 error is a fixed bias per (E, L), retrace-verified, scaling m⁻² ("Errors never compound", 13). Every threshold is r1's frozen number unchanged; only the seed envelope widened, in the harder direction — the fix the f771 author proposed and its checker endorsed. Controls on both sides (m32/m64 pass on identical machinery; quadrature and oracle sensitivities 3+ orders below every decided band). The decided quantity is arrival-time accuracy near compact masses (principle 30). Cost: one rung file (draft included), then the integrator's clean re-run in the shipped harness.

## The experiment that would make it gold

Not applicable — but gold stands only together with the integrator's shipped-harness re-run of r1w (the lab cannot freeze rungs); the physics facts that decision needs are all measured here and survived my independent checks.

## What the author missed

1. **binet-m8 has no metrics** yet is a candidate config in the r1w draft; its death was asserted from the m⁻² law. I measured it: 0.9180 fraction, low-e grid up to 1.4e-2 — dead. The draft should carry the measurement (or drop m8 from configs) so the rung re-run has a verdict for every config.
2. **Long runs deviate from both r1 and the draft:** r1 froze 10⁴ cycles; the run measures 12 cycles plus two 100-cycle confirms, while r1w-rings.md still says "long runs: unchanged cases". Bit-identity locking (cycle ≤ 4) makes the physics conclusion safe, but the frozen text must state what is actually judged.
3. **The e floor 0.01 is load-bearing and undocumented as such:** at e = 0.005, r_p ≈ 11, m32 already fails per-seed (1.43e-3), and the worst grid point at the floor (9.94e-4) is marginal. The draft should record that the low-e margin is thin and the floor is a domain choice, not a convenience.
4. river-m16/32, square, tiltonly are not re-run (disclosed in the lens section only) — the shipped-harness re-run must cover them for a complete r1w verdict.
5. r1's frozen Output picture (orbit trace p = 20, e = 0.5; five light paths) was not produced.
6. controls.txt C1 points to the banded-vs-shipped tie-out as "inside r1w-output.txt"; it only prints in the `--quick` path (I reproduced it there: exact). The number is real; the pointer is wrong.
