Working...
Check complete. `check2.md` written to `lab/results/20261010-1544-components-986b/` (only file I added or changed; build artifacts kept in `/tmp`, author files untouched).

**Grade: gold**

**Evidence basis:**

- **Reproduction exact.** All 8 `out-s-*.jsonl` regenerate **byte-identical** from the dossier's commands (fixed seeds, empty patch.diff); selftest floor 4.02e-13, conjunction wrap 0.0, μ=0 control exactly 0.0 bits at all 24 checkpoints. Timings match the dossier's claim (~190 s for the set, contended).
- **Predictions pre-registered** (mtimes: predictions.md → final code edit → outputs → dossier) and honestly reported: the three failures (mass ×3.8 not ×10/decade; N-flat, not −1 bit/doubling; Coulomb 0.11 bits, not ~2) are real in the data and are the result. Prediction 1's ">1 bit/doubling" threshold was self-inconsistent (four diffusive columns already sum to ~2), but its substance holds — per-doubling increments are constant in time, no linear-in-t term.
- **Five adversarial cases of mine, all supportive:** strong-regime N-scaling flat to 0.5 bits (μ=3e-5, N=128/512); ×4 horizon with independent seed (cross-seed stable; σ_E ×2.56 ≈ t^0.68); heavy hot lane μ=3e-5/σ_e=0.05/200 orbits — sub-diffusive, no coherent onset; crossing belt (σ_e=0.25) quieter, zero ejections; μ=3e-4 row re-verified (σ_E 7.8e-2@6.25 orbits vs their 6.9e-2@6, entropy saturated at the 4·log₂N cap from ck1).
- **Novel:** first H_live rate measurement (board: "not measured yet"); corrects shipmem's per-kick premise (62 bits × kicks → log₂ of accumulated spread; 7×–1000× idiot index). Prior art (9fd9b33, a2b777c, b8e910d, 88c8660) priced only static sizes.
- **Two findings that strengthen it:** σ_λ wraps and saturates at 1/√12 once phase-mixed, bounding the dominant column at ~19 bits (q=1e-6) — the long-horizon fit is safer than claimed.

Caveats named in the check: the ~25±10-bit physical-belt central value at q=1e-6 leans ~10 bits optimistic (flat μ^0.7 on all columns gives ~36–40 bits; the adoptable q≤1e-5 conclusion survives either way), the 2.07 shape constant understates the E/L columns by ~2–3 bits, and a true mean-motion resonance remains unmeasurable in this probe.
