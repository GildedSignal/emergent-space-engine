# Predictions (written before the decisive runs)

The diagnosis so far (measured, probes only, no fix applied yet):
- P0: a level-15 burn from the plane's start refuses at γ ≈ 1.76e3 with `NoBoundOrbit` from the weak-passage validation: the timelike margin D = r_p/L² = 1/(L²q) (by Vieta on the radial cubic) falls below the Q48 quantum of the shape word k (2^-48), so the floored word lands on/past the null boundary k = q(4k²−2k+1). Predicted break γ = √(r_p·2^48)/b ≈ 1753 at r_p = 1 AU; observed 1762.
- With that check hacked open, the next refusal is `Range` around γ ≈ 6.5e4 (source to be identified), and the flight would be lost at the leave edge 2^40 at γ ≈ 2049.

## Predictions for the fix (margin-carried passages, proper-velocity thrust step, leave edge 2^54)

1. **The γ = 10⁶ flight completes**: a level-15 burn from the plane's start reaches γ ≥ 10^6 with zero refusals and no loss, and the engine's events keep up (the flight takes ~10^5–10^6 events, most of them past γ ≈ 400 where the clock's far-field step, not the thrust step, binds). If the clock's far-field step (P_D·f'(c/8)/f'(c), about 3·10^9 ticks) makes the flight need more than ~5·10^6 events, the test will show it as slowness, not refusal.
2. **Replay identity**: the burn to γ = 10^6 and back (reverse at the top, brake to rest) gives one digest under any frame/budget/thread split, and the digest differs if the reverse decision moves (control).
3. **Work at every level**: the burn's work test (ΔE vs ∫α·v dt, 3%) holds at every throttle level 0–15 on the sub-relativistic spans it has always covered; I do NOT expect the existing levels' numbers to move at all (the margin path only activates where main refuses).
4. **Proper-time rate**: at the top of the flight the view's rate is within ~1% of 1/γ (the τ numerator now uses the exact D; the weak-τ Taylor is bypassed by keeping the real compactness in margin-carried shapes). If the second-order weak-τ term were still in play I would expect rate off by ~10% near the top — that is the falsifier for choosing the exact-q path.
5. **Gates unchanged**: B13, G1–G6, B16 pass with the same detail lines as on main (the margin path is dormant for every orbit that compiles today: same bits, because `margin: None` preserves the old arithmetic bit for bit).
6. **Held-out**: a level-8 burn (about 45 g) run out past the old γ ≈ 1762 wall should now pass through it smoothly: γ grows monotonically with no refusal, and the r(γ) relation follows r ≈ (γ−1)·c²/a within a few % (the relativistic rocket equation in the flat far field).

## What would make it wrong

- If the coordinate-time readout of a margin-carried passage accumulates errors above the position word's quantum per step (the t numerator still uses the 21-bit word k, good to ~2.4·10^-7 relative), the work test (3%) or the replay identity would fail at high γ. The falsifier is the work test run at the top throttle over the whole flight, not just the start.
- If the catalogue ever shares a margin-carried entry between two different exact D at the same word key, replay identity across budgets would break (the memo must key on the margin).
