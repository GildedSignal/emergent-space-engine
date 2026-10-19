# Predictions (written before the decisive flights)

Question: what share p of the belt's resolved kick items actually fire a velocity quantum (rebind = a static compact certificate cannot sleep through them)? This is budget-1e9's open direction 2, the residency dial's multiplier.

## Fermi estimate first

- Item rate λ: the root doll steps every ship 2^step_log2 times per Cinder period (88 d ≈ 3.53e6 game-s), one step ≈ 27.6e3 game-s ⇒ λ ≈ 3.6e-5 items/body/game-s — exactly a9d7's measured 3.55–3.64e-5 fired-kick rate (memory-h-live L200). So a9d7's "fired kicks" count ITEMS (stats.kicks counts resolved items), not quantum fires.
- Per item, dv = a·h with a the secondaries' differential pull on a belt body at 2–3 AU and h = Δs-mapped time. The velocity word's quantum is fixed at birth (2^velocity_exponent). Sigma-delta carries the sub-quantum part, so p ≈ E[|dv|]/quantum (up to correlation).
- The code carries sub-quantum kicks by design ("A sub-quantum kick fires nothing"), so the designer's intent is p < 1; but the belt's h is one whole doll step (large), so I estimate p is NOT tiny: **p(belt) ∈ [0.1, 0.7]**, most fired kicks |dvq| = 1–2 quanta, max ≤ 16.
- The locals (300 bodies about Home/Moon, short periods, strong tides): **p(locals) ≈ 1** (their dv per step exceeds the quantum most items).
- Player/fleet (clock law with thrust): excluded from the belt dial; counted separately.

## Pre-registered predictions for the held-out arms (K = 1e4, and wave 2 at K = 3e4)

1. P1: clock-census fired fraction (non-thrusting) at the 3e4 belt through wave 1 is in [0.05, 0.8]. Kill criterion for the "never promotes" hope: if p > 0.5, the residency dial τ = 43.6/p gs improves less than 2× and the compact store's value must come from absorbing quantized kicks (a law change), not from kicks sleeping.
2. P2: p is K-flat (1e4 vs 3e4 within a factor 2): the belt's per-body perturbation does not scale with belt size (no belt-belt channel in the plane).
3. P3: Σ|dvq| / fired ≈ 1–2 quanta per fired kick (sigma-delta keeps fires single-quantum).
4. P4: wave 2 (41–43.5e3 gs) has the same p as wave 1 (steady cadence, not a birth transient).
5. P5 (control, both sides): the census OFF runs bit-identical `ladder:` digests to the shipped binary (the probe is counters only); with ES_KICKCENSUS on, kicks/events totals in `ladder:` still match the stats line (census counts the same items).

## What would make the dial close

τ(8 GB) = 43.6/p game-s at 5.1 KB/live-body; at p = 0.1 → 436 gs; p = 0.01 → 4,360 gs ≈ 0.13 Cinder orbit. The SOI arm (4b55) is τ ≤ 0.12 orbit regardless; if p·λ_promote still exceeds Γ_SOI the belt cadence owns the dial.
