Working...
Check complete. `lab/results/20261009-1858-redteam-075b/check.md` written — **Grade: silver**.

**Reproduced (clean tree, all < 5 s):** every dossier number, bit-for-bit, including the held-out (8.0, 0.8) row (0.071 / 81 / 21 / 1.35 rad / 3.1e-9) and the unlogged (20, 0.5, ε=1e-5, systematic) row I reconstructed a command for (0.317844 / 3.7e-4 / 3.4e-5). Predictions predate the run; failed predictions (P2, P5) are reported as failures.

**Three findings from my attacks:**

1. **Novelty is partially pre-empted.** `docs/law.md` line 35 (5 October, citing lab run df81) already records the same C·drift² curvature bias, rejects the quantized memo, and re-anchors the jet at √(floor/C) at ~0.05 compiles/kick. The dossier's "never measured" and the fresh-premise-kill framing overstate; what's new is the regime where that mitigation's economy collapses (per-kick recompiles near the separatrix, cost parity with the 350–700 fixed-step control) plus the bucket-phase gate flaw (27.3 rad vs 4.4e-5 at the same orbit and kicks — verified).

2. **The `curv` column is measurement artifact.** The estimator differences drifted-C against stale-K0 and the base F0. Clean ε=1e-9 probes: (20, 0.5) → 3.9e3 (logged 7.8e6), (8.0, 0.8) → 7.9e7 (logged −2.6e10). The "1e7–1e8 at p=20", "non-monotone in e", and "4e10 along the walk" claims fall — but the mechanism survives: curvature is nearly flat in e and grows ~10⁴× toward the separatrix, and the bias arithmetic closes on the measured errors with clean values.

3. **Locality confirmed adversarially:** p=1000 with a 20% systematic C-drift keeps bucketed error ≤ 3e-8 rad — the kill is genuinely confined to the separatrix skin, as the author's lens section conceded.

**Gold path named:** emulate the design's actual jet+√(floor/C) policy on a separatrix ladder with bucket-phase-swept seeds; if anchors/orbit ≳ 32 within (p−6−2e)/p ≲ 0.1, the cost premise dies on the design's own mechanism and the dimensionless trigger + r-kick-absorb freeze adopt in one step.
