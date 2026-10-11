# Dossier — B12's statistic read as an attractor: memory and mean are the two ways error compounds

**Claim.** The Jacobi error's attractor class is not readable from its level (the frozen growth
exponent passes a bounded chaotic law nowhere and ranks laws by their running maxima), but it is
readable from its increments as two orthogonal statistics: the persistent share VR(τ) =
Var(e_{t+τ}−e_t)/(τ·Var(Δe)) — the walk test, blind by construction to deterministic drift, with
**no amplitude floor** — and the OLS slope of e on t with Newey–West errors — the drift test,
whose floor is amplitude/√samples, three orders below amplitude/horizon; together they pass every
positive plant and fail every negative plant on chaotic ships, with derived thresholds (VR: 1/2 ±
3 pooled se; trend: t > 3) and a derived lag (τ* = min(T/8, measured inter-event gap)).

**Bottleneck.** HANDOFF's first risk: "B12 cannot yet tell bounded from compounding error on
chaotic ships." Upstream of every physics merge this week (`q-b12-design`, Codex `b12-v2`,
Sonnet's `wt/b12-v2` all in flight). Expected gain: unblocks a frozen gate with ~40 lines; deletes
the magic 1e-12 floor (replaced by two positive controls: `noise-1e-11` and `planted-bounded`).

## Evidence

One command, this folder: `python3 b12attractor.py metrics.json` (76 s warm: `shipsbase.npz`
cached; 5–6 min cold). Scene: CR3BP rotating frame, μ = 1e-3, sep = 1, R_SOI = μ^0.4, R_H =
(μ/3)^{1/3}; 12 chaotic ships (of 80 drawn), 16–35 three-Hill entries each over 200 planet
periods, 1601 samples; reference DOP853 rtol 1e-13; the series is the gate's own
e_j = |C(t_j) − C(0)|/|C(0)| (`handoff.rs`). Full table in `metrics.json`; the decisive rows
(VR at the registered τ* = 200, sensitivity at 100 and 320; trend = median across ships):

| law (class) | EXP (frozen, ≤0.2) | VR(200) | VR(100) | trend t | VR+trend verdict |
|---|---|---|---|---|---|
| echo-conserving (bounded) | 0.000 pass | 0.000 | 0.000 | 0.0 | **PASS** |
| planted-bounded (bounded chaos) | 0.224 **FAIL** | 0.172±0.064 | 0.276 | 2.0 | **PASS** (+5.1σ) |
| noise-1e-11 (bounded) | 0.123 pass | 0.005 | 0.010 | 1.2 | **PASS** |
| scaled-1e-11 (bounded) | 0.224 **FAIL** | 0.172 | 0.276 | 2.0 | **PASS** |
| planted-compound (walk) | 0.520 FAIL | 0.620±0.061 | **0.810** | 3.3 | **FAIL** |
| planted-drift (drift) | 1.001 FAIL | **0.005** | 0.010 | 1e17 | **FAIL** (trend only) |
| planted-kick (multiplicative) | 1.058 FAIL | 1.583 | 1.439 | 11.4 | **FAIL** |
| float11 / float12 / echo-float13 (reference paths) | 1.29 / 2.07 / 2.09 FAIL | 0.277 / 0.993 / 0.976 | 0.37 / 0.87 / 0.90 | 9.8 / 10.5 / 7.7 | **FAIL** |
| leak 1e-13/period on 1e-11 noise | 0.297 FAIL | 0.005 | 0.010 | 41 | **FAIL** (trend) |

- Separation bounded vs compound at the registered τ*: **7.0 pooled σ** (kill criterion ≥3σ met).
- Mechanism, measured twice: VR(200) = 0.005 = 1/τ for a pure ramp (variance drops constants), and
  VR stays 0.005 for every leak in the sweep — VR is exactly drift-blind; conversely a signed walk
  has trend ~0 and is caught only by VR. The gate needs both; each is the other's negative control.
- **Walk floor (no amplitude term):** FAIL iff persistent share π = σ²_walk/Var(Δe) > 1/2 + 3·se
  (se_null = 0.064 measured) → a walk is caught when its step variance rivals the bounded
  increment variance, at ANY amplitude — where the exponent needs the walk's amplitude σ√T to
  rival the bounded amplitude A. That is the "compounding invisible to the level" class.
- **Drift floor:** with an iid background σ = 1e-11, the smallest swept leak (1e-13/period, total
  2e-11 = 2σ) fails at t = 41; measured floor therefore ~2 orders below amplitude/horizon (the
  endpoint estimator's floor, which P5 parroted); doubling the background amplitude doubles the
  boundary (t: 41→20.4 at the same leak), i.e. linear in amplitude as OLS predicts. With a chaotic
  background, HAC inflates se by √(2κ_eff), κ_eff ≈ 17 samples here (from planted-bounded's
  VR(200) = 0.172 ≈ 2κ/τ): floor ≈ 6e-13/period at amplitude 1e-11. **The horizon B12 certifies:
  200 periods, 1601 samples, and the drift floor it can promise at bounded amplitude A is about
  A·10⁻² per period.**
- Lag: the registered τ* = 200 leaves a sparse walk (inter-entry gap 61 samples, measured) in the
  indeterminate band (0.62); the derived rule τ* = min(T/8, inter-event gap) = 61 → reads 0.81 at
  τ = 100: FAIL. τ* is set by the scene's event cadence, not chosen.
- Machine independence: one-ulp nudge of every ship's birth state — all 12 re-kept, every verdict
  stable except planted-compound moves INDETERMINATE→FAIL (0.62→0.76), i.e. never toward a pass.
  The reference itself fails at every tolerance (echo-float13: VR 0.976, EXP 2.09) — confirmed on
  this box, so B12's law-vs-reference amplitude clause must keep the convergence exclusions.

## Predictions

`predictions.md` written before the decisive run. Held: P2 (reference compounds at every
tolerance), P7 (kick super-unit VR 1.58), P8 (se_null 0.064 ∈ [0.08, 0.25] predicted — just
under), P3's separation (7σ) and P6's verdict stability. Failed, each teaching the mechanism:
P1's direction (my ships rank bounded 0.224 < compound 0.520; the frozen ships' inversion 0.49 >
0.31 is the documented case — three harnesses now agree the exponent cannot pass a bounded
chaotic law); P4 (VR marginal for the 1e-12 leak — instead VR is exactly 0.005: drift-blind by
construction); P5's boundary (amplitude/horizon is the ENDPOINT estimator's floor; OLS beats it
by ~2 orders; the amplitude-scaling half held).

## What would make it wrong

- My ships are not the gate's frozen 16 (`sample::HANDOFF_KEPT`); the directed `q-b12-design` run
  must repeat this on the real harness (`handoff.rs`, `fit.rs`). The inversion direction differs
  between my ships and the frozen ones (both fail the exponent) — the exponent's ranking is
  scene-dependent, which is itself the miscalibration.
- VR assumes the error is sampled at uniform cadence; the gate samples uniformly in time, so a
  law whose event rate changes systematically converts event-walks into time-series with drifting
  rate. The trend test catches that case; the class label (walk) may be misread as drift.
- The folded |·| series (the gate reads absolute error) gives walks a spurious positive trend
  (spread grows: compound's t = 3.3): harmless for FAILing, but it means trend alone cannot
  certify "no walk"; VR must be primary for the class.
- Chaos-sensitive fates (ulp flips inside/outside, the redteam's finding) remain outside both
  statistics; the convergence exclusion stays load-bearing.

## Cost of adopting, and fit with PRINCIPLES

~40 lines: `fit.rs` gains `variance_ratio` and `drift_t` (OLS + HAC, lags 50); B12 judges
median-VR(τ*) ≤ 1/2 − 3·se AND median t ≤ 3 on the judged ships; positives `noise-1e-11` and
`planted-bounded` must pass, negatives `planted-compound`, `planted-drift`, `planted-kick` must
fail (law.md line 81: controls on both sides). Principle 13 ("errors never compound") and 2
("error type over error size"): VR and t are type statistics — scale-free or floor-stated.
Principle 26: unit-root/variance-ratio and HAC regression are the quant-trade tools for exactly
this question (is a series integrated?), stolen from people who paid for being wrong. Principle
18: the level was the wrong observable; its increments are the water.

## The lens

Attractor classification delivered: bounded (echo, state-only laws), random walk (compound,
float reference paths), drift (deterministic leaks), multiplicative (kick) — plus the conserved
structure the level statistic missed. What the lens may have missed: my horizon is the gate's
200 periods (a law decorrelating only at 10⁴ periods reads VR≈1 and fails — honest at this
horizon, but the verdict must carry its horizon and floor, as stated above). The lens brief's
cascades, allocator tails and cell-tree hysteresis were not touched.
