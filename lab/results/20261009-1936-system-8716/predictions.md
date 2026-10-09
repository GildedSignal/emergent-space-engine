# Predictions (written before the decisive run)

Question: can ONE candidate structure — shape cells (Binet U-window) whose occupants are phase-sorted, with a single continuous phase-window formula — replace the two-tier cone certificate + the fleet phase-rank certificate + the concentration trigger?

The window formula, derived first order in e, phase = true longitude λ:

    w(cell) = min(2π, Δϖ_spread + (Δn_max + 2·n·e_spread)·H + b/a + skin)

with skin = 2·b/a, fixed a priori for all scenes. No scene-dependent parameter, no trigger.

Cases tuned on: none. I will tune nothing after seeing the sweep; if recall fails I report it as held.

## Held-out cases and what I expect there

1. **Tightness sweep** (fleet σ_shape from 1e-4 to 0.3, 7 log-spaced points, N=768):
   - unified recall = 1.0 at every point (the window formula is continuous in σ);
   - cone-only recall < 0.2 on truth for tight scenes is NOT expected — cone-only has perfect recall by construction (it emits all overlapping pairs); what breaks is work: cone-only pair-evals grow ~n_f²/2 on tight scenes (≥ 50× more pair-evals per true encounter than unified);
   - unified pair-evals per true candidate stay within 3× of the ideal-trigger (oracle two-structure) everywhere on the sweep.
2. **Mixed scene** (belt 1536 + embedded fleet 153 at σ=1e-3): unified recall = 1.0; realistic density-trigger (occupancy threshold τ) either melts (work > 5× unified) or misses (> 1% of true candidates) for at least one τ in {8, 32, 128} — the trigger is a repair with a failure mode; unified has no τ.
3. **Horizon doubling** (H: 8 → 16, same skin): unified recall stays 1.0 (window scales with H by construction); work roughly doubles in fleet-like cells only.
4. **e-distribution change** (Rayleigh → uniform e ∈ [0, 0.2], belt N=1024): recall 1.0 (belt windows saturate at 2π; e-skin term conservative).
5. **Scaling at fixed volume** (belt+mixed, N = 2k → 128k): pair-evals per true candidate ~constant (within 2×) for unified; cone-only also ~constant per candidate but candidates/body grow ~linearly in N — the quadratic risk the board names — unified's per-body growth is bounded by the phase window, i.e. candidates per body grow only as the phase-circle occupancy at fixed w, which is N-independent at fixed volume only if... held: unified candidates per body grow ≤ ~√N·log — weaker than cone-only's ~linear-in-N.

Honest failure criteria: any unified recall < 1.0 on any scene kills the window formula as written (a skin term missing); that is a real result, not a tuning knob.
