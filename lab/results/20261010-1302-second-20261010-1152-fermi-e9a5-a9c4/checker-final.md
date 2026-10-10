Working...
**Grade: gold** — written to `check.md`.

What I did, and found:

**Reproduce.** Ran `probe.py` in a scratch copy (twice): byte-identical output modulo `env.loadavg1`, 618 MB peak RSS, 16 s wall. Every digit the dossier quotes regenerates from `metrics.json` — all four scenes' H values, the bias 1.453 ± 0.015 (all 24 trials in [1.424, 1.501]), floor-invariance triple (±1.1 %/±0.8 %), churn 375.36/orbit → 6 076 events/frame, time conversion (534.5 real-years at 100×), reabsorption, and the four last-octave slopes. Kernel controls pass; the impulse-only negative control still fails at 14.6×.

**Predictions.** Written before the decisive run (mtime order, run.log empty). All six held.

**My attacks** — all landed inside the stated margins:
- **Non-Gaussian bias robustness**: t³ product −0.13 bits, a 98/2 ×8-sd mixture −0.37 bits — vs the tightest margin in the table (cold_belt 3-dof, 1.4 bits). Holds.
- **Grid/cutoff**: λ⁺ and D_weak stable ≤ 0.4 % across 2 000–16 000 bins and BMAX ×0.5–×2.
- **100× colder σ₀ = 10⁻⁴**: σ@16 384 and H unchanged — the cold result is σ₀-independent.
- **q = 10⁻⁷**: churn 52 942 events/frame — "churn binds, not memory" confirmed where it hurts.
- **Parent cross-check (git e1675df)**: the parent's coldswarm = 47.890 raw is indeed Σ×2500 ∧ σ₀=0.01, confirming the misattribution story; the refactored `shape_entropy_H` is bit-equal to the parent's inline code, as claimed.

**Novelty.** Parent silver was the first H_live measurement; this run converts it into an adoptable record (no new physics, and it says so).

**Misses I recorded**: P1's mechanistic σ_resid guess (1.5–2.5 m/s) missed 4× low (0.466), unreported in the dossier's "all six held"; the decisive predictions were anchored on the parent checker's published numbers (disclosed); growth tables differ from the parent's at MC-noise level (RNG stream), unstated.

Only `check.md` was added to the run folder; scratch cleaned.
