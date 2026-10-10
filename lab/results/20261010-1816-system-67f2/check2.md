Grade: silver

**Abstract.** Claim: deferring a kick's application into an exact accumulator is killed — it converts bounded magnitude error into secular timing error (energy exponent ≈ 1.0 vs 0.07) — so the renewal quantum belongs only on the derived-structure side. Every number reproduces exactly from the dossier's commands (7 s). The kill is real and robust: under my corrected-time replica the walk survives off resonance (exp 1.01), at e = 0.3 (1.19) and at the true 2:1 resonance (exp 1.29, then hyperbolic ejection at larger q); a quantize-and-carry control I added (same quantum, exact timing) stays bounded (−0.01–0.44). But the replica mistimes the perturber (clock advances 1.5 H per kick), so Scene B is not the 2:1 it names and the discard control's boundedness is an artifact. Adoption: zero code; one clean rerun from gold.

## Reasons

1. **Reproduction: exact.** `python3 deferral.py` regenerates every table entry (max|dE|, exponents, renewal counts, pumps, ψ windings); the convergence probes match (8.23e-7/0.07, 5.82e-6/0.21, 1.14e-4/0.56). The exact-Kepler-drift premise verified (E error exactly 0.0 over 1000 periods). `patch.diff` empty; predictions.md predates the script and results (mtime order).

2. **Bug found (adversarial 1).** The loop advances `t` by 1.5·H per kick (three 0.5·H increments) while the body advances H: final t = 1.494 × body time; the perturber phase used in the force leads the ship by 119 revolutions — the effective perturber rate is 1.5·N_J. Consequences: (a) Scene B is a 4:3 commensurability, not the named 2:1; ψ = 2N_J·t − λ − ω is not the actual resonant angle, so the pump/ψ-winding numbers describe an unintended scene. (b) All configurations, truth included, share the identical mistimed force, so the deferral-vs-immediate comparison is internally fair; Scene A is off resonance w.r.t. either rate and unaffected in kind.

3. **The core kill survives every attack.** Corrected-time replica (`kick_acc` at body time): Scene A deferred q=3.45e-5 → max|dE| 8.52e-3, exp 1.01; e = 0.3 → exp 0.96/1.19; true 2:1 (a = 5.2·2^(−2/3), correct phasing) → exp 1.29, max|dE| 2.03e-2 at 7.4 renewals/orbit, pump 1.87× at mild q, and at q = 8·dvr the body is **ejected hyperbolic** — stronger than the author's distortion claim. Prediction 4's substance (deferral distorts resonant response) holds, non-monotonically in q; the "2:1" label and ψ sign-flip numbers do not.

4. **The split rule is right, but the author's evidence for it was an artifact.** New control: apply every kick on time, rounded to the same q grid, residue carried (quantize-and-carry — pure magnitude error): exp −0.01 to 0.44, error 46× below deferral at equal q; flat at e = 0.3. Meanwhile the author's "discard stays bounded" surprise (exp 0.06) inverts under corrected phasing (0.73–0.98): the dossier's reported surprise rests on the mistimed force. The timing-vs-magnitude conclusion is correct; the discard control was the wrong instrument for it.

5. **Novelty.** No H-entry tests impulse-application deferral; the author correctly cites the rejected quantized (E,L) memo as the discard control's origin and H0190's averaging as the correct-variables form. Uncited adjacent prior art: r4 v1 / H0203–H0205 — instantaneous conjunction kicks over-pump resonances 2–9× — the same phase-error-in-kick-application family; this run adds the accumulator/threshold mechanism and the error-type split, which is new.

6. **Honesty.** Predictions 1–3 pre-registered, failed by the author's own kill criterion, and reported as failed — the record is clean. Fit: principle 2 (error type over size), principle 9, engine.md's "secular drift: forbidden" — now measured, not assumed.

## The one experiment to gold

Fix the clock (t += H per kick, force at body time), add the quantize-and-carry control, and rerun both scenes with Scene B at the true 2:1. My probes indicate all three claims then hold with clean evidence (walk exponents ~1.0 everywhere for deferral, bounded quantize-and-carry, ejection at the resonance's large q).

## What the author missed

The 1.5·H clock bug and its two consequences (mislabeled resonance scene; artifact-bounded discard control). The quantize-and-carry control that actually isolates magnitude error from timing error. The hyperbolic ejection at the true resonance — a catastrophic, more persuasive failure than pump distortion. The r4-v1/H0205 prior art on kick phase errors.

Probe script (corrected-time replica, all numbers above): replaces `t` accounting with `tau += H` and `kick_acc(rx, ry, tau)`; quantcarry mode: `dv += residue; applied = q*round(dv/q); residue = dv − applied; apply immediately`. Rebuilt from the author's unmodified `kepler_drift`/`kick_acc` in ~50 lines; ~12 s total.
