Grade: gold

**Abstract.** Claim: with the four named defects fixed in shipped code, the exact-integer Allan rule (R1) catches a planted compounding per-kick bias on the law's cheap path (8/8 ships at 2^40, both draws; controls ≤ 1/8), B12's exponent inversion is confirmed (3/3 corrected model, 2/2 physical), and the multi-τ variants fail their pre-registered kill (K2: 2/8 control false flags). Everything reproduced bit for bit in a clean tree: the record (7 min), wh-output.txt, and the prior R1 record (25/25 identical). My attacks strengthen it: stochastic leaks caught 7/8, verdicts scale-invariant 2^32–2^48, a third draw 8/8 with clean control, a near-neutral tangential bias 0/8 under R1 (R2: 7/8). The queued q-b12-design build gets a validated statistic plus the measured window budget (T ≳ 32·τ_c). Cost: ~15 lines.

**Reasons.**

1. **Reproduction (clean /tmp copy; `work/patch.diff` is empty, nothing to apply).** `python3 exp.py all` → identical to `run-record.txt` line for line, the only difference the absolute path inside a numpy RuntimeWarning; ≈ 7 min as stated (7m08s). `wh-output.txt` regenerates identical, written by the shipped `wh()` itself. My independent reimplementation of `run_wh` reproduces the recorded diagnostics exactly (draw0 good/bias1/bias3: dJ med 7.8e-6 / 1.8e-3 / 5.6e-3, min_r2 0.3558 / 0.3044 / 0.3160). The prior-run claim also holds: `prior/exp.py controls` vs the current R1 column — 25/25 identical verdicts, same five deviations.

2. **The named gold experiment (K1) is delivered and passes.** bias3 (ε = 3e-2): 8/8 by R1, R2 and R3 in both draws; bias1 8/8; good controls R1 0/8 and 1/8, R3 0/8 and 0/8. The corrected saturating model inverts 3/3 with max|x| = 1.400 (the clamp — the prior divergence artifact is gone); physical-path inversion 2/2 (0.049 ≥ 0.021, 0.055 ≥ 0.009). Kepler roundtrip 7.93e-13, the honest number replacing the prior 3e-14.

3. **Predictions and kill criteria were honored as pre-registered.** `predictions.md` mtime 00:11:16, untouched afterwards; both decisive runs postdate it. K1 passed; K2 fired (R2 good control 2/8 draw 0) and is reported as a refutation of the multi-τ adoption, not buried — the process working as designed. K3 did not fire: in vitro the multi-τ rules do halve R1's OU false flags (T/16: 8/30 and 5/30 vs 17/30) — the checker's family is genuinely dented there, at in-vivo cost. Misses are reported, not hidden: R1 at 0.2A measured 0/3 (predicted ≥ 2/3), bias1 8/8 (predicted 2–7/8), τ_c = T/4 at 83/60/57% ("~all" predicted).

4. **Adversarial cases (mine, eight; all in /tmp, nothing in the run folder touched).**
   - *Scale:* verdicts identical at integerization 2^32–2^48 for good, bias1, bias3 — the 2^40 scale is not a hidden threshold.
   - *Stochastic-sign bias* (the dossier's admitted easy-leak weakness): R1 catches 7/8, 7/8, 7/8 at ε = 3e-2 across three scenes and 6/8 at ε = 1e-2 — the rule catches martingale leaks on the physical path too, beyond what the record shows.
   - *Third draw* (base 7777): good R1 0/8, bias3 8/8 by every rule.
   - *Same-scene contrast:* bias3 planted on the good control's own scene (seed 4247): 8/8.
   - *Encounter-rich good scene* (a = 0.965–1.035): R1 0/8; a second seed's scene died (NaN) — deep-encounter scenes are screened out by the pre-screen, see below.
   - *Alternating-sign bounded bias* with conjunction transients (Hill 22 steps): R1 1/8 — consistent with the conceded item 7.
   - *Inertial-tangential bias* (ε = 3e-2): dJ 1.7e-4 (30× below bias3), R1 0/8 — their C-near-neutral calibration claim holds — while **R2 flags it 7/8**: the multi-τ refutation is even stronger than the record's K2 line.

5. **Novelty.** No Allan/AVAR anywhere in docs, HISTORY.md or crates (grep over the whole checkout; only the two lab runs). Distinct from the killed recurrence ratio (taste log, 6 October — that one could not separate a slow leak from bounded error; this rule measurably can, on both synthetic and physical paths) and from H0215's already-known misranking. The B12 redesign is the top of the lab queue (`q-b12-design`) and HANDOFF "Headed next" §2 — this run is the instrument it was waiting for.

6. **Goal fit.** Unblocks the named instrument risk verbatim: "B12 cannot yet tell bounded from compounding error on chaotic ships; until it can, the motion law's stability is judged by probes, not a gate" (HANDOFF). Premises shown wrong by measurement: the multi-τ consistency fix (pre-registered kill, plus my 7/8 tangential false flags) and the prior run's window law (T ≥ 4·P_max does not extend to correlation times; T ≳ 16–32·τ_c). PRINCIPLES: "types of errors and not just errors" (OC#42) — the rule classifies error type, exactly the B5/B12 distinction; "exact means deterministic and reproducible" (P2) — integers decide, no thresholds, nothing compared across machines. The author is honest that this is an instrument unblock, not an engine-cost move.

**What the author missed.**

- The validated scene is encounter-poor *by construction*: the pre-screen (min_r2 ≥ 0.02, 0.5 < min_a < 2) rejects or kills deep-encounter scenes (my encounter-rich init either stayed clean or died), and B12's frozen scene is handoff-heavy (≥ 20 doll-edge crossings). The conjunction-transient screen (their item 7) is unbuilt and is the real adoption risk — the redesign must derive window and screen together, on the actual handoff scene.
- The fleet-level criterion (k of 8 ships) was reasoned about but never measured as a decision rule (admitted). Note the asymmetry it hides: false positives are scene-correlated (all ships share τ_c), so k-of-n can fail silently in exactly the regime the OU census flags.
- Hygiene: `exp.py` was edited at 00:19:36 — after a first full run (~00:11–00:19) and before the recorded second run — and the edit is not itemized. The final record regenerates bit for bit and the predictions/K-criteria predate both runs, so the held-out property stands; but "edits made after the run without saying so" is only half answered: say what changed.
- The corrected toy's bounded exponent (≈ 3.8) still calibrates the ordering, not the magnitude the gate will see (P2's 0.493) — inherited from the prior run.
- R1's estimator at τ = T/4 has 3 dof (non-overlapping, kept for bit-compatibility); my scale and draw attacks show it is adequate here, but a longer-τ octave should be sampled once the record-compatibility constraint is dropped.

**For the adopting step (not a gold condition):** R1 on the real B12 handoff scene with the encounter screen, the per-handoff-class invariant choice, and the fleet criterion measured.
