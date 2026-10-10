Grade: gold

**Abstract (for the integrator).** Claim: H_live, the rate at which a program-born belt accumulates distinguishing bits (Kepler tubes + hyperbolic conjunction kicks), is measured for the first time and grows diffusively (σ ∝ t^0.55; the phase column ∝ t^1.6), so the storage quantum q, not the encounter rate, is the memory lever. Reproduced: all 8 stored JSONLs **bit-for-bit** from the dossier's commands (191 s); μ=0 control exactly 0.0 bits; kernel exactness is a trig identity (verified: 2·atan(μ/bv²) ≡ 2·asin(1/e), 2e-16). My adversarial cases: fresh seeds ±20%; a 2:1 resonant two-ring stays sub-diffusive (exponent 0.37); N-flatness holds to N=1024; high-e and μ=3e-4 behave. Gain: kills the per-body-store premise (7×–1000× off the floor); adoption is one rule. One erratum: the entropy constant is 4.13, not 2.07 (+4 bits); "fits at q ≤ 1e-5" survives.

## Reproduction

- Applied nothing (patch.diff is empty; the probe is self-contained in the run folder). Copied the tree, built, ran the dossier's exact command set: **all eight `out-s-*.jsonl` regenerate byte-identical** (deterministic seeds). Wall time 191 s vs the author's 192 s.
- Selftests: Kepler round trip 4.02e-13; conjunction wrap 0.0; hyperbola conserves speed to machine precision; kernel grid `deflect_imp == delta_hyp` at every point. The claimed identity is exact: with e² = 1 + (bv²/μ)², 2·asin(1/e) = 2·atan(μ/bv²) (worst rel err 2.3e-16 over the whole grid) — I verified this independently of the author's code.
- Every table cell in the dossier matches the author's JSONLs and my reruns (σ's, kicks/body 135.5, strong 10, contacts 59 at μ=3e-7; exponents 0.55/0.54/1.59).
- The one row without a stored artifact (μ=3e-4, "saturated") reproduces at a fresh seed: σ_E 7.8e-2 @6 orbits vs the author's 6.9e-2, then saturation — as disclosed.

## Predictions

Timeline is clean: `predictions.md` 15:52, `main.rs` final 16:19, all JSONLs 16:26–16:29. Eight pre-registered predictions, none tuned. Five held (control exactly 0 — stronger than the promised <0.05; kernel exact — stronger than "a few percent"). Three failed and the failures are the informative content (mass ×3.8–7 per decade, not ×10; N-flat, not −1 bit/doubling; Coulomb cost 0.11 bits, not 2) — each failure is reported as a result with a mechanism (rare strong encounters dominate). This is the lab's ethos done right.

## Attack (my cases)

1. **Fresh seeds** (belt 777, lane 555): all headline numbers within ~20% (σ_E 2.05e-3 vs 1.69e-3; lane σ_E flat 6.5e-4, σ_ϖ 1.35e-1); exponent 0.57 — no seed artifact.
2. **The author's named hole, resonance**: two rings at exact 2:1 (a, 2^(2/3)a), μ=3e-5 (heavy), random and aligned periapsides. Both stay **sub-diffusive** (σ_E exp 0.37, σ_ϖ 0.27, σ_λ 0.16–0.23): no coherent linear pumping at belt masses. The diffusive claim survives its most likely counterexample. (A massive resonant secondary remains outside this probe's two-body-kick physics — and outside a belt's self-scattering.)
3. **N=1024** (4× the author's range, same μ=3e-7): σ_E 1.58e-3 vs 1.91/1.69/1.67e-3 at N=128/256/512 — flat-to-declining, exponents 0.68/0.68/1.67 still sub-linear. The conservative flat extrapolation to 10⁹ is supported, not just asserted.
4. **High-e crossing belt** (σ_e 0.25, width 0.05, μ=3e-6): no pathology; σ_E exp 0.49, σ_λ 1.13, zero singletons. Extremes do not break the finder or the rate law.

## Novelty and fit

HANDOFF line 70: H_live "not measured yet" — this is the first measurement, and it is the named decider for the 10⁹-in-8 GB question (board focus item). Distinct from gold components-98bc (birth-program statics, 0.126 bits): this measures the live rate law beyond birth. PRINCIPLES #24: "The memory floor is information" — now it is a measured rate, with a zero-noise control. #6's "influences below one quantum accumulate" is measured to accumulate diffusively and to cost log₂ of the spread. Adoption is a rule (one line in law.md's Populations plus the allocator's budget), two design consequences (tight screening; program recompilation on mixing), and no code — one step.

## What is wrong in it (none of it breaks the verdict)

- **Entropy-constant slip.** Gaussian differential entropy per column is log₂(σ·√(2πe)/q) = log₂(σ·4.13/q); the dossier's σ·2.07 undercounts by 1 bit/column, 4 bits total, in the favourable direction. Corrected, a physical belt (μ~1e-9) after 100 orbits lands at roughly 31–43 bits at q=1e-6 against the 34.4 budget — marginal, not "25±10 fits". The actionable verdict is unaffected: at q=1e-5 it fits with ~2× headroom, which is what the dossier actually recommends. The −13 bits/decade-of-q lever is exact (4·log₂10 = 13.3).
- Every q=1e-6 empirical "bits" number in the logs is saturated at log₂N per column for μ ≥ 3e-7 — a cap, not a measurement. Disclosed by the author; the integrator should read only the σ columns.
- `kernel_scene`'s `rel_ang_err` diagnostic column is miscomputed (acos of a normalised cross product is not an angle error) — cosmetic; the claim rests on the two deflection columns, which agree exactly.
- Prediction 8 (centered ≪ raw) is verified only through drift magnitudes; the instrument never records uncentred entropy, so the ratio itself is unmeasured.

## What the author missed

The entropy constant (above) is the one real miss, and it thins the stated q=1e-6 margin for a physical belt. They also named the resonance hole but did not run it (I did: closed at belt masses); left the μ=3e-4 row without a stored artifact; and the σ_λ column — the dominant cost, t^1.6 — is exactly where the engine's phase re-anchoring at program updates would pay, which they note but do not quantify. The follow-up worth queueing: H_live under a *massive* resonant secondary (the Kirkwood case), where this probe's pairwise kernel does not apply.

First check, blind: reproduced bit-for-bit, held-out predictions pre-registered and adjudicated honestly, adversarial cases (resonance, N=1024, high-e, fresh seeds, μ=3e-4) all confirm or bound the claim. Gold.
