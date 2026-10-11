# Predictions (written before the decisive run)

Question: is H_live (bits of live distinguishing information per body) bounded in steady
play for a kicked belt, under (A) a frozen birth program, and (B) periodic generator
re-fit (re-emit the program as a bijection over the current ensemble)? And what is the
true information birth per kick, against the law draft's "+62 bits per kick"?

Model (not tuned on these cases): N = 2^20 bodies, 1 element column, belt of W = N cells
(one body per cell), diffusion s = 1 cell/orbit, close-encounter jumps at
r = 2.1e-3/body/orbit (r8 v2 belt 0: 427 encounters / 10^4 bodies / 20 orbits) with
jump std J = 100 cells, T = 2^13 orbits (main).

Held-out cases (I will not retune the model for these):

1. **Frozen program, scar entropy vs t:** grows ~ (1/2)log2(t) + log2(4.13·s) bits/body;
   crosses 8 bits/body near t ≈ (2^8/(4.13·s))^2 orbits. For s = 1: t ≈ 3.8e3.
   For the held-out s = 0.1 and s = 10, same law, 100x shifted in t.
2. **Re-fit program (m = 256-knot quantile bijection, sorted matching):** residual entropy
   stays <= 2 bits/body at every checkpoint t, for every s in {0.1, 1, 10} and both
   densities (W = N and W = N/32).
3. **Label permutation (rank displacement d):** entropy(d) ≈ (1/2)log2(2πe·2·s²·t·λ²)
   with λ = bodies per cell; crosses 16 bits/body at t ≈ 2.5e8 orbits for s = 1, λ = 1
   (correction at 00:16, before any checkpoint output was read: the first draft said
   "> 10^9 orbits", inconsistent with the formula quoted above by ~4x; ~2.5e6 orbits at
   s = 10). A 3-column law (U, e cos ϖ, e sin ϖ) pays this per walking column.
4. **Claim check ("+62 bits per kick"):** the net information birth per body per orbit is
   the differential entropy of the kick delta, ≈ log2(4.13·s) ≈ 2 bits at s = 1 (plus
   jump contributions r·H(jump) ≈ 2.1e-3 × 9 ≈ 0.02 bits) — i.e. ~1.5 orders of
   magnitude below the 62-bit scar-record cost the law draft budgets. 62 bits is the cost
   of an *un-reabsorbed scar record* (Elias–Fano rank + zigzag deltas), not of the
   information created.
5. **Encounter survivors:** under re-fit, ever-hit bodies (88% by t = 10^3 at the stated
   r) leave no permanent trace in the element columns; their news is exchangeable and the
   re-fit absorbs it. The surviving growth is only the label permutation (+ player-pinned
   distinctions, not modelled here).
