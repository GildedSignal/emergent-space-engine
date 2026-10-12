Working...
Check complete. **Grade: gold** — written to `lab/results/20261012-0616-second-20261012-0358-scout-cdac-07b4/check.md` (only file added; author's folder otherwise untouched).

**What I did:**

1. **Reproduced bit-identical**: `python3 work/hlive_real.py` (189 s, exit 0, <0.5 GB) + `analyze.py` in a clean /tmp copy — `metrics-real.json`/`analysis.json` regenerate exactly (diff shows only machine load and wall-times). Positive control passes.

2. **Predictions**: `predictions.md` (06:44) precedes the decisive run (07:04); the disclosed post-prediction script edit is only the D(t) fix — I verified its load-bearing claim myself (kick-stream final cells ≡ propagated snapshots, D=295 both ways). 7/7 held, including the decisive matched-rate rows (2.78× at ε=1e-3, 8.69× at ε=1e-2, per kick-application — conventions checked).

3. **Physics verified independently**: `gauss()` against Cartesian impulses + independent element conversion (median rel. err 3×10⁻⁴); B18 store arithmetic recomputed (1.694/2.394 B/body confirmed).

4. **Three adversarial attacks**:
   - **Found an undisclosed detector hole**: the azimuth sort on `th ∈ (−π, 2π)` splits physical neighbours into interleaved blocks; brute force shows 12–16% of near pairs missed per step. One-line wrap fix → K 59.54→65.72 (**9.4% undercount**), s barely moves (2.56→2.35×10⁻⁴, down — consistent with the run's recycling story). No conclusion moves; anchor gap becomes 20–66×.
   - **Adversarial belts**: σ_e=0.15 → real 2.77× safer, σ_e=0.01 → 3.09× safer at matched rate; direction robust.
   - **One dossier sentence is false**: "zero single kicks reach a quarter cell" — actually 297/891,678 (0.03%) do, max 4.1 cells (deep-tail small-b, as the run's own ρ_b(0) story predicts). The real accumulation evidence (98–100% multi-kick escapes, median 158–420 kicks) stands.

5. **Novelty/goal fit**: no HISTORY entry covers H_live on real conjunction geometry; direct hit on the board's "fitting 10⁹ in 8 GB… distinctions per game-second"; PRINCIPLES 6 now measured on the real path.

Gold stands with four one-step amendments named in check.md: fold in the θ-wrap fix (K → ≈21.8–72.2), delete the "zero single kicks" sentence, relabel ρ_b(0) (6.2× absolute, not 2.7×), and note the dead-code inline α fixer (−0.817 regenerates from `analyze.py`).
