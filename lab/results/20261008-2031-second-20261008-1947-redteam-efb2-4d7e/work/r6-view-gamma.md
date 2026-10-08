# Rung r6: the view at gamma (one sample per pixel vs the received history)

Proposed by the second author of `20261008-1947-redteam-efb2` (its checker's named experiment).
Frozen before the decisive run. Design: [docs/representation.md](../../docs/representation.md) §2
("Observables"). If every candidate is killed, only those configurations die, never the method.

**Question.** At closing γ from 1 to 2×10⁶ (the queue's `b-high-gamma` lens targets γ = 10⁶), does
what the view renders for a periodic emitter equal the light the observer actually receives during
each frame — and does the design's own crossing solver ("Newton's method finds the crossing, starting
from the previous frame's") still find it, in the doll frame and in raw observer-frame magnitudes?

**Truth.** A frame is a 1/60 s exposure of observer proper time. What it records is the k-weighted
average of the emission over the light received in it, k = dt_arr/dt_emit the LOCAL arrival slope
from the crossing geometry (never a constant, never a global formula). With the line of sight fixed
through the window this average is closed-form in the window's edge phases (error O(R/D0) ≤ 2×10⁻³);
a quadrature truth would alias exactly in the high-k regime and is forbidden. Roots are bisected on
the monotone doll-frame arrival equation; the checker re-derives them by an independent contraction.

**Scene** (doll frame, c = 1, light-seconds). 32 emitters on a ring R = 0.2 ls at orbital speed
β_o, each a lighthouse b_j(t′) = 1 + cos(ωt′ + φ_j). Observer coasts toward the system at closing β;
200 frames at 60/s observer proper time; **D0 = 2.1·γ·N·Δτ + 100 ls so the observer never passes the
system** (no flyby: every frame approaches, D0 margin ≥ γ·N·Δτ). Ladder: γ ∈ {1, 2.24, 22.4, 70.7,
125, 250, 255, 2×10⁶} × β_o ∈ {0.05, 0.3} — the 255 row sits at ≈ 2.03 orbits/frame (near-integer:
the strobe band); 22.4 and below are below Nyquist (honest region). No random seed: the φ lattice
is fixed. Normalised profiles: the DC beaming factor (k⁴, additions in log form per the design) is
common to every law and cancels in every comparison.

**Configurations.**
- `kavg` (candidate): the k-averaged sprite — per frame i and emitter j, render
  1 + sinc(x)·cos(ω(t′ᵢ+t′ᵢ₋₁)/2 + φ_j) with x = ω(t′ᵢ − t′ᵢ₋₁)/2 from the two crossings the engine
  already solves (the doll-frame Newton). One memo per (spectral type, log k): sinc and the pose are
  table lookups, the additions are the frame's own. Below the resolvability boundary it degenerates
  to the instant sample (sinc → 1).
- `exact-exposure` (positive): the same law on the bisection truth's crossings — the ideal the
  criterion exists to keep passable. It must pass.
- `instant` (negative): the design as written — one sample per pixel: render 1 + cos(ωt′ᵢ + φ_j).
  It must fail.
- `raw-obs` (negative): the same emission event solved in raw observer-frame magnitudes (boosted
  worldline, float64 ulp ~10⁻² s on 10¹⁴ s terms at γ = 2×10⁶), rendered with the k-averaged sprite.
  It must fail on the solve, which is the design's number-form question.

**Metrics** (over all (frame, emitter) pairs of all 16 cases; per-emitter, never a median across
emitters — a median of wrapped positions is not an instrument):
- `solver_fail_frac`, `solver_wrong_roots`: Newton's non-converged fraction and converged-but-wrong
  roots (|t − truth| > 10⁻⁶·max(1, |truth|), truth = bisection).
- `iters_mean`: mean warm-started Newton iterations (doll solver for kavg/instant; raw for raw-obs;
  0 for exact-exposure).
- `bright_p99`: 99th percentile of |rendered − received average|, in units of the AC amplitude.
- Diagnostics (not criteria): `phase_below_p99` (below-Nyquist honesty of the rendered rotation,
  per emitter), `frozen_frac_above` (fraction of above-boundary pairs whose rendered advance is
  < 0.05 rad — the wagon wheel), per-case bright percentiles, and the `kavg-global` variant
  (sprite keyed by the global approaching k = √((1+β)/(1−β)) instead of local geometry).

**Output.** `metrics.json` (the five configs), `r6_results.json` (per-case detail), log lines.

```configs
kavg candidate
exact-exposure positive
instant negative
raw-obs negative
```

```criteria
solve-fail behaviour solver_fail_frac <= 0
wrong-roots behaviour solver_wrong_roots <= 0
iters cost iters_mean <= 12
bright behaviour bright_p99 <= 0.1
```
