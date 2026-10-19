# Dossier — 20261019-1817-dynamics-45c0 (dynamics lens)

## Claim

The calendar page's "persistent ~2× dues tail" on the chained-clock belt is not persistent and not an attractor: it is the genesis train shearing into the birth step distribution's own shape (C50(dues) = C50(steps) to 1% while the census window fills, gens 1–7), which then phase-mixes to uniform (C50 2.02 at g=13, 1.64 at g=14, 1.05 at g=16, 1.3–1.5 at g=17–24, battalion 1 throughout) — and a genesis stagger deletes the whole phenomenon at birth (C50 1.03–1.07 flat to g=14, per-window load Poisson-level from genesis, no regrowth), so f82a's stagger lands the belt directly at its stationary load state.

The frame-load tail at 10⁹ (board: smoothness/allocator; the calendar page's od 3 consequence line reads the belt's load as "this decaying genesis wave … max/μ_span 94–144× at birth, p99/μ 7–12× at g = 8"). This run replaces a standing-tail reading with a priced transient: the wave is gone in ~16 fires (~16 × 28,140 game-s ≈ 5 game-days at the belt's cadence), and the mixing time is the inverse step spread (7.8% here; a design dial — the birth draw sets it, checker2's σ-28.5% [1,5) AU arm would mix ~3.6× faster). It deletes nothing in the engine; it deletes the worry and the need for any standing-tail mitigation at 10⁹, and it gives the stagger a stronger adopt statement than "flattens the train": it is exact in the stationary measure.

## Evidence

All numbers from `crates/universe/examples/genesis` (this run's patch: the example plus one added method `Universe::stagger_genesis`, print-only otherwise), shipped `plane_extra` law, seed 1 unless noted, belt 2,700 (extra 3000, the d520 arm), census at head + g·1.03·step_max, dues-span C50 (half-mass window over the dues' own span; equals the page's step-denominator C50 once the span saturates at one step, g ≳ 14). Logs: `ship_seed1_gens24.log`, `stagger_seed1_gens14.log`, `ship_seed2_gens14.log` (seed control); `analyze.py` recomputes the headline numbers from them.

- **Birth step law (no fires needed):** step median 5.714×10⁹ ticks, spread p1–p99 7.84% of median, C50_steps = 3.05. First-dues span at genesis 3.01×10⁸ = 5.3% of one step (the 58× genesis train, reproduced at the page's instrument).
- **Shear regime (gens 1–7):** C50(dues)/C50(steps) = 0.99–1.01 every census — dues(g) = due(0) + n·F is a monotone image of the step law, so the "plateau" is the birth step distribution showing through, computable at genesis.
- **Wrap + mixing (gens 8–24):** the dues span saturates at step_med (5.71→5.82×10⁹), the concentration breaks away from C50_steps (still 3.2–3.4) and decays: 2.15 (g=12), 1.64 (g=14), 1.05 (g=16), 1.27–1.53 (g=17–24). Mixing at g ≈ 1/0.078 ≈ 13 fires, as the spread predicts. Battalion = 1 at all 39 censuses on all arms.
- **Load (allocator's number):** per-window max/μ (64 windows per step, μ = 42) falls 18.9 → 1.85–2.11 late; p99/μ 17.4 → 1.56–1.75 (Poisson at μ = 42: max/μ ≈ 1.4, p99/μ ≈ 1.35). The belt's standing load is Poisson-plus-ε once mixed.
- **Stagger arm (span = one median step, hash(id)):** C50 1.05 at g=0, **1.04 at g=14, never above 1.07**; load_max 1.26–1.47 from genesis. No attractor re-grows the tail; the uniform stagger is invariant under the shear, as the phase picture requires.
- **Seed 2 (ship arm):** same curve (C50 2.90 at g=0 tracking C50_steps 2.91; 2.66 at g=9 = seed 1's 2.66 at g=9); drift p50 5.9×10⁻⁵/fire.
- **News rate (P4):** birth-data forecast (due ≡ d0 + k·s0) holds phase to fc_p50 ≤ 0.01 through g ≈ 19 (0.022 at g=24, ~25 fires; p90 0.048); per-fire step drift p50 6.0–6.9×10⁻⁵, p90 1.2–1.9×10⁻⁴.

Reproduce: `bash lab/results/20261019-1817-dynamics-45c0/regen.sh` (≈ 7 min: patch applies, the three flights rerun, analyze.py prints the numbers above).

## Predictions

`predictions.md` was written after a 300-body pilot, before these flights. P2 (stagger regrowth toward the plateau by g ≤ 12) **killed** — flat 1.03–1.07. P5 (C50 stays above 2.0 through g = 24) **killed** — crosses 2.0 at g = 13. P1 held exactly in its regime (0.99–1.01, gens 1–7) and then broke at the wrap, which is the finding. P3 held (battalion 1 everywhere; ship-arm load decays 18.9 → 1.85, stagger's same-g load never exceeded by > 2×). P4 held to g ≈ 19 and failed its letter at g ≥ 20 (fc_p50 0.022 > 0.01 at g = 24; the 0.05 threshold holds with p90 0.048).

## What would make it wrong

- My C50 denominator is the dues' own span, not the page's fixed step; the two coincide only after span saturation (g ≳ 14). If the page's late-g 2.2–3.0 reading is not a window artifact, the two instruments disagree at g = 14–16 (mine 1.64/1.35/1.05) and a checker should recompute half-mass both ways on one flight before adopting the refutation. The refutation's own evidence is instrument-internal: span saturation + C50 → 1 + stagger-invariance + battalion 1.
- The stagger arm's dues are shifted as a scene variant (exact drift until the first kick; `b.kick`'s partial-read word is not re-derived, unused on this census path) — if a checker finds the staggered belt's dynamics differ beyond the schedule (digest-level), the no-regrowth claim weakens to "no regrowth in dues shape".
- 2,700-body, one-draw belt, ≤ 25 fires, seed 1 + seed 2; no [1,5) AU wide-draw arm (faster mixing predicted, unflown), no 11,700 anchor.

Cost of adopting: none in engine code (the stagger exists as f82a's measured lever; this run only re-scopes what it buys). Fit with PRINCIPLES: "Compute only surprises. Cost follows change and entropy. Nothing is evolved that can be derived when looked at" — the load wave is derivable at birth (the step census prices it with zero fires), and the news per fire is 6×10⁻⁵.

## The lens

The attractor/transient dichotomy was the right lens but the transient hides two regimes, not one; the page's plateau was the shoulder of the second. What the lens may have missed: the load tail's residual excess over Poisson at g = 24 (max/μ 1.85–2.11 vs ~1.4) — a genuinely standing, if small, correlation that neither the shear nor the mixing picture prices; and the horizon is still only 25 fires against a 5.9 h game step (the belt's own century is unflown).
