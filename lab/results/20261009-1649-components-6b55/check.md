Grade: silver

**Abstract.** First measured H_live-side constraint for the belt store, and it reproduces bit-identically: the crate's `scale n` gives enc_per_body_orbit 0.0412/0.0394/0.0396/0.0388/0.0404 (N-independent in ρ∝1/N), `hlive.py` regenerates `metrics.json` exactly, controls pass both ways (heavy belt scars 100%, diffusion ratio 0.886 ∈ [0.7,1.4]), and the key τ values (4×10³ orbits at Q_e=10⁻⁷, 4×10⁷ at 10⁻⁵, Kuiper mass, N=10⁹, fixed ρ) follow from the shipped code plus the disclosed, measured 22× rate correction. But the headline constraint Q_e ≳ 2×10⁻⁹·(M_belt/10⁻⁷)·(10⁹/N)^½ contradicts the run's own table by ~77× (it is the one-orbit boundary, missing √10⁴), "destroys the store at any mass" fails at M_belt=10⁻⁹/Q_e=10⁻⁵ (its own τ=1.8×10⁷), and P6 is misreported as held. Gold-worthy physics, broken headline arithmetic.

**Reasons.**

*Reproduced (clean tree, empty patch.diff — the crate ran unmodified):*
- `cargo run --release -p emergent-encounters -- scale n`: enc_per_body_orbit = 4.128e-2, 3.938e-2, 3.957e-2, 3.878e-2, 4.038e-2 — exact match; N-independence of the per-body rate in the ρ∝1/N regime is the crate's own measurement, as claimed.
- `python3 hlive.py` → byte-identical to the stored `metrics.json` (fixed seeds; 30 s vs claimed 23 s).
- Controls: heavy belt (10⁻³, Q=10⁻⁹) scars 100% ✓; MC/analytic diffusion ratio 0.886 ∈ [0.7,1.4] ✓. I verified analytically that the MC's |δa|-accumulation predicts ratio ≈0.91, so the control is self-consistent.
- τ arithmetic: stored τ(N=10⁹, M=10⁻⁷, fixed ρ) = 1.911e2/1.911e6; ×22 → 4.2×10³ / 4.2×10⁷ — the dossier's key rows 2–3 regenerate. The 22× itself is anchored at a fixed-ρ point (N=10⁴, ρ=10⁻⁴: analytic 0.86 vs crate 0.0396 → 21.7×) and is structurally explained (the analytic integrand omits the Gaussian decay of p(miss<ρ|x): ≈18× by hand).
- Adversarial `scale sigma` (fixed ρ): rate linear in σ_e (0.0041→0.0403 for σ×10), matching the model's σ-scaling, and 0.0403 vs 0.0396 cross-checks `scale n` at the same spec.
- Player cone: 3213 bodies/s → 1.03×10⁵ bits/s = 8.6% of the 4 GiB/h budget ✓.
- Novelty: H_live is HANDOFF line 70's "not measured yet"; no HISTORY entry measures it. The queued lens b-h-live asks for the engine instrument (`xtask universe --bench`), which this run does not build — it is the physics-side bound, complementary, and the first number.

*What breaks the record (none of it flips the qualitative conclusion):*
1. **The headline constraint is wrong by ~77×.** From the shipped model, a 10⁴-orbit session needs Q_e ≳ σ₁·√10⁴ = 1.5×10⁻⁷·(M_belt/10⁻⁷)·(10⁹/N)^½. The dossier's 2×10⁻⁹ is σ₁ without the √10⁴ session factor. The dossier's own table proves it: Q_e=10⁻⁷ at the anchor mass crosses at 4.2×10³ < 10⁴ orbits, yet the formula says 2×10⁻⁹ suffices. The error is permissive — the direction that flatters the premise.
2. **"Destroys the program store at any mass" is false at the run's own lightest mass.** M_belt=10⁻⁹, ρ∝1/N, Q_e=10⁻⁵: τ = 1.8×10⁷ orbits (corrected), MC scarred 0.15% — no destruction. Correct statement: ρ∝1/N scars immediately iff M_belt ≳ Q_e (per-event impulse ≈ M_belt, relative); true for Kuiper-and-heavier at behaviour-plausible quanta, which are the game-relevant masses.
3. **P6 misreported as held.** The prediction: lightest M_belt crossing Q_e=10⁻⁷ within 10⁴ orbits lies in [10⁻⁵,10⁻³]. The decisive analytic measure puts the boundary at ~6.5×10⁻⁸ M⋆ (τ∝M⁻²: τ(10⁻⁷)=4.2×10³<10⁴, τ(10⁻⁹)=4.2×10⁷>10⁴) — two orders below the bracket. Only the biased MC (|δa| sums, uncorrected 22× rate) lands near 10⁻⁵. A held-out prediction that failed should be reported as failed.
4. **Key-table row Q_e=10⁻⁹ is not regenerable:** σ_walk 1.6×10⁻¹¹ belongs to the M_belt=10⁻⁹ row (σ is Q-independent; rows 2–3 correctly say 1.6×10⁻⁹), and τ should be 0.42, not 4. Same conclusion (crossed), wrong numbers. Also the column header "σ_walk(10⁴ orbr)" holds per-orbit values (the 10⁴-orbit σ is 1.5×10⁻⁷); and "ρN = 10⁻⁴" for the scale-n regime should be ρN = 1 (ρ = 10⁻⁴·10⁴/N).
5. P5 failed and was prominently, honestly reported — correct behaviour, but gold requires held-out predictions held.

*Fit.* Moves a named top risk (board bottleneck 5 / H_live) from "not measured" to measured; PRINCIPLES P6 ("Store the generator, not the generated") and P16 ("the biggest quantization we can get away with") now have a memory-side number; the ρ-regime tension is a real, new constraint on the encounters design.

**The one experiment that would make it gold.** Measure the fixed-ρ per-body rate's N-scaling (Γ ∝ N is analytic-only; one run of the crate's `steady` at fixed ρ=10⁻⁴, N=10⁵–10⁶, or a thinned-belt variant), then re-derive the headline constraint and the P6 boundary from the shipped model, correct the "any mass" claim and the bad table row. The τ numbers then stand on measurement at every factor.

**What the author missed.**
- The √T session factor in their own headline formula — the one number the integrator would quote.
- P6's outcome was judged on the MC (which accumulates |δa|, i.e. cumulative variation, not net offset, and uses uncorrected 22× rates for every "measured" column) instead of the analytic crossing time the conclusions rest on; neither bias is disclosed.
- The 22× correction is applied to τ but not to the MC/session bits columns; session bits are ~Q-independent of the correction at the anchor, but scarred fractions are not.
- The player-cone bound counts a 1-light-second disk's population; a light cone sweeping outward touches fresh bodies on an annulus that grows with radius — the constant 3.2×10³/s is the t=1 s value, not a session-scale bound.
- The correlation risk (quasi-periodic conjunctions, their own top disclosure) has a cheap falsifier they did not run: sample consecutive conjunction phases of a single pair (r8's continued-fraction structure) and compare coherent vs diffusive crossing; coherent repetition can cross a quantum in τ ≪ τ_diffusive.
- The lens brief (b-h-live) asked for the engine instrument in `xtask universe --bench`; that queue item remains open — this run bounds the physics but does not close it.
