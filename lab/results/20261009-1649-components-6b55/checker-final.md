Working...
Check complete. `check.md` written to the run folder; nothing else touched, no commits.

**Grade: silver.**

What I did and found:

**Reproduced (clean tree, empty patch.diff):**
- Crate `scale n`: enc_per_body_orbit = 0.0413/0.0394/0.0396/0.0388/0.0404 — exact match; N-independence in the ρ∝1/N regime is the crate's own measurement.
- `hlive.py` regenerated `metrics.json` **byte-identical** (fixed seeds, 30 s).
- Controls pass both ways: heavy belt scars 100%; diffusion ratio 0.886 ∈ [0.7, 1.4] (and I verified analytically the MC's |δa| construction predicts ≈0.91, so the control is self-consistent).
- Key τ values regenerate from the shipped code + the disclosed 22× rate correction (4.2×10³ / 4.2×10⁷ orbits); the 22× is anchored at a fixed-ρ point (N=10⁴, ρ=10⁻⁴: 0.86 analytic vs 0.0396 measured) and structurally explained (~18× from the omitted Gaussian tail decay).
- Adversarial `scale sigma`: rate linear in σ_e, matching the model; cross-checks `scale n` at the same spec (0.0403 vs 0.0396).
- Novelty: H_live is HANDOFF's "not measured yet" risk; no prior H entry.

**Why not gold — the record, not the physics:**
1. The headline constraint `Q_e ≳ 2×10⁻⁹·(M_belt/10⁻⁷)·(10⁹/N)^½` is the **one-orbit** boundary (missing √10⁴), ~77× too permissive — contradicted by the dossier's own table (Q_e=10⁻⁷ crosses at 4.2×10³ < 10⁴ orbits at the anchor mass).
2. "Destroys the store at any mass" fails at the run's own M_belt=10⁻⁹, Q_e=10⁻⁵ row (τ = 1.8×10⁷ orbits, 0.15% scarred). Correct law: ρ∝1/N scars iff M_belt ≳ Q_e.
3. **P6 misreported as held**: the analytic boundary is ~6.5×10⁻⁸ M⋆, two orders below the predicted bracket [10⁻⁵, 10⁻³]; only the biased MC (|δa| sums, uncorrected rates) lands near the edge.
4. Key-table row Q_e=10⁻⁹ has wrong σ and τ (σ is Q-independent; 1.6×10⁻¹¹ belongs to the M_belt=10⁻⁹ row); σ column header and "ρN=10⁻⁴" are also mislabeled.
5. P5 failed (honestly reported) — gold requires held-out predictions held.

Gold path named: measure the fixed-ρ rate's N-scaling (Γ ∝ N is analytic-only), then re-derive the headline constraint and P6 boundary from the shipped model. The qualitative design consequence — the encounters skin must aggregate at a physical ρ, never one shrinking with N — stands for game-relevant masses.
