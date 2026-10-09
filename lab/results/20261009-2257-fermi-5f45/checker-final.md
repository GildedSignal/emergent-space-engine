Working...
Check complete. `lab/results/20261009-2257-fermi-5f45/check.md` written; nothing else in the run folder touched (the author's `opik_out.json` restored byte-identical after reproduction), no git operations.

**Grade: lead.**

**What held:** reproduction is bit-exact and fast; predictions.md verifiably predates the decisive run (23:02:32 < 23:05:12 < 23:05:18); bits/outcome ≈ 48–50; the "orbit period in game-seconds is the gating unmeasured constant" point; μ-tuning honestly disclosed; novelty confirmed (the H_live question is live, `b-h-live` unstarted).

**What killed it:** the central quantity is wrong by ~10³. `rate = np.mean(1.5·|da|·hit)` is the hit expectation of **one** sampled neighbour — the neighbour count/surface density is never multiplied in. At fixed density the estimator falls as 1/N (4.8×10⁻⁵ → 7.9×10⁻⁷ for N=1500→150,000), while the corrected rate is N-independent: ~0.13/orbit (ρ=10⁻⁴), ~1.25 (ρ=10⁻³) by density quadrature, and **0.68/orbit** by a fully independent direct Kepler simulation (two seeds, no Öpik algebra) — 1,440× the reported number. Everything downstream inherits it: the "275–1,600 h memory margin" becomes ~2–18 orbits (minutes at hour-scale, hours at day-scale); P3's "held" flips to failing by 10³.

**Two secondary faults:** (1) the P1 "narrow-belt uplift / two regimes" finding — reported as a mechanism and linked to the board's dilution flag — is purely the estimator's 1/N normalization (one regime: rate ∝ sd·ρ·σ_e); the author's own prediction of N-independence should have triggered instrument suspicion. (2) The compute ranges (2–4 / 47–104 machines) don't re-derive from their own cited constants (verified against law.md's 2.5–24 µs): the full range gives 3–63 / 71–1,500 — the "re-setup is the wall" verdict survives and strengthens, but the printed numbers are low-corner only.

Adversarial cases run: direct simulation (2 seeds), 1/N scaling at three N, 3D inclinations (rate ÷22, still ≥65× the reported number), 10⁶-ship formation (~30/orbit — the real memory hotspot). Peak checker memory ~250 MB, well under the 2 GB budget.
