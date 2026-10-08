Working...
Check written to `lab/results/20261008-1058-inversion-6534/check.md`. **Grade: silver.**

**Reproduced** — bit-identical on every deterministic number via the dossier's own `run.sh` in a clean tree (patch.diff empty; standalone crate over `crates/encounters`): zero-miss 124/124; ab-block hits 189→49 574 (exponent re-fits to 2.016), evals 7 545→1 912 173 (2.003), 0.5 evals/pair; cone and radial candidate sets exactly m²; corridor d_max 0.029–0.030 rad with 0 beyond 0.15; belt contrast 14 951 vs 39 evals/hit. Predictions pre-dated the outputs; the failed prediction 3 is honestly disclosed and does strengthen the claim.

**Attacks run** (independent scenes built on a copy of the harness, since removed):
- Fresh seeds: 129/129 zero-miss — soundness holds.
- Steep incidence γ≈19.8°: zero-miss, all-Cross sections, cone still m² — product structure is incidence-independent.
- Near-tangent γ≈0.6°: zero-miss 304/304, but all sections go Wide — 518.6 evals/pair (72×), 15 497 evals/hit (1000×), corridor bound breaks (d_max 0.249, 292/8363 beyond 0.15). The author's disclosed kill case is real and much larger than measured.

**Why silver, not gold** — two dossier numbers its own log contradicts:
1. The extrapolation divides by 4 twice: 0.79 µs/pair is already 4-thread wall, so 10¹⁰ pairs ≈ 2.2 h (not 30 min), 10¹² ≈ 9 days (not 2 days). Conclusion survives — the error understates the cost.
2. The corridor mechanism is misattributed: my steep control (ρ/sin γ four times smaller) leaves d50 unchanged at 0.0106, so the width is set by the lane's ϖ dispersion, not ρ/sin γ; the dossier's numerology was a scene coincidence.

**Gold experiment:** build the crossing-time rank-window exit on the frozen scene, verify zero-miss vs truth at m≥500, and measure its work per real encounter — the selectivity side of the O((n_A+n_B)·log n) claim, plus the corrected extrapolation. Novelty checked against HISTORY and the board (H0156, 25 Sept, is the pre-pivot ancestor of the symptom); the routing gap, the metric inversion and the corridor invariant are new and on the board's top scaling risk.
