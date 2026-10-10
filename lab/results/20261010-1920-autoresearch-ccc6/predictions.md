# Predictions (written before the decisive experiments)

Artifact: `crates/encounters` (r8 v2/v3 verified). Metric: `setup_ns_per_pair`
(the board's open item: re-certification setup per candidate pair per element
change; kick = the same setup on a kicked body's range). Behaviour held fixed:
`verify a|b|c|long` all `missed:0,false:0` (baseline confirmed 10 Oct).

Baseline (this Linux box, orders of magnitude only):
- scale n 10000 (σ=0.01, ρ=1e-4): setup 9165.8 ns/pair, 20.3 evals/pair.
- scale sigma σ=1e-3: 35592.9 ns/pair, 120.7 evals/pair (Wide sections dominate:
  ~600–2900 evals per Wide section, Cross ~0).
- kick: 7.2 ms/kick, 812.8 pairs/kick, 8.84 µs/pair.

## Tuned on
`scale sigma 0.001`, `scale n 10000`, `verify a|b|c|long`, `kick`.

## Held out (run once at the end, never tuned on)
- Behaviour: `verify d` (hot e=0.1 belt, mixed a 0.5–3, dense n=3000 ρ=3e-4).
- Cost: `scale sigma 0.003`, `scale n 30000`, `kick` (whole eps ladder), plus
  a 5-repeat median of `scale sigma 0.001`.

## Predictions
1. **R1 powf(1.5) → x·√x in the eval path** (rel_of ×2/eval, cross_window, rel):
   10–30% off ns/pair at both σ=1e-3 and σ=0.01; evals unchanged; all verifies
   stay missed:0. (powf is a slow libm call; the math is identical.)
2. **R2 Kepler Newton tolerance 1e-15 → 1e-12**: further 5–15%; a full extra
   iteration is spent polishing far below the ρ-scale margins; missed:0.
3. **R3 inner arc scan k=32 → 12** in `d_of_s`: 1.5–2.2× on Wide-heavy specs
   (σ ≤ 3e-3), ~1.2× at σ=0.03. Risk: a miss on hot belts (e = 0.1–0.2) where
   Δr·Δv wiggles more per orbit; any missed>0 on any verify set → revert.
4. **R4 arc-local Lipschitz** (max |v_i| over the arc's longitudes instead of
   global vmax): ≥ 1.5× on eccentric belts (e ≥ 0.03), ~1× on cold ones; the
   bound stays rigorous (|dD/ds| ≤ i's speed while crossing the arc).
5. **R5 slack skin** (store each silent certificate's drift budget; skip pairs
   whose kick drift is inside it): us_per_kick ~10–15× smaller at eps=1e-9,
   ~2× at 1e-7, ~1× at ≥1e-5. Soundness: the baseline's 1.5 slack factor shows
   5 skip violations at eps=1e-3, so the shipped skin needs a larger factor or
   a budget recomputed to be conservative; I predict violations = 0 for
   eps ≤ 1e-7 and > 0 at 1e-3 with the 1.5 factor as-is.

## What would make it wrong
Any missed>0 or false>0 on any verify set (behaviour), or a setup speedup that
only shows on the tuned σ (overfit). Cloud timings are x86 — orders of
magnitude only; the integrator re-measures on the M1.
