# Predictions — belt as program (run 20261004-1525-components-98bc)

Written before the decisive run of `crates/shipmem/examples/belt.rs` (m = 2^20, default
keysets; nothing below was tuned on output — the code has not been run yet).

The belt: Darwin p ∈ [2048, 2560)·2^16 (27 bits of span), e Rayleigh σ = 0.07 through a
2^12-entry dyadic quantile table (12 bits), kind 6 bits, ω 32 bits, t_p uniform over 2^44
quanta (44 bits). Draw floor = 121 bits/body exactly (Rng-charged). This is the game's
10^9-scale content shape (belt/disc): smooth, correlated through Key::darwin, no majority
step, so today's form P rejects it and form B (packed blocks) holds it.

## Held-out cases and expectations

1. **Arm A (i.i.d. belt → Shelf blocks):** `blocks_bits` ∈ [1.0, 1.25] × floor (121 bits);
   round trip exact (`rt_bad` = 0). Its own KS vs the analytic law (positive control) ≤ 0.002.
2. **Arm B, counter-mix program:** total bits/body ≤ 0.5 at 2^20 (the description is
   5 keys + one 16 KB table + parameters), and at kick rate 1e-2 total ≤ 1.2 bits/body
   (scars: ~50 bits/kicked body + Elias–Fano ordinals ~2 + log2(1/rate) each).
3. **Fidelity of the mix program (behaviours, not sample identity):** KS on p, e, ω, t_p
   each ≤ 0.002 on both key sets (n = 2^20; α = 0.01 critical ≈ 0.0016); two-sample KS on
   the stored E, L columns vs arm A ≤ 0.004; nearest-neighbour median in the (p, t_p) plane
   within ±5% of arm A's, nn p1 within ±20% (tails are noisy at 1024 samples).
4. **The lattice program (the elegant form):** 1-D KS near-perfect (≤ 0.001) but the NN
   median deviates from i.i.d. by more than 10% — rank-1 lattice stripes in phase space.
   If this holds, the counter mix is the design, not the lattice.
5. **Cost:** program eval (mix + darwin + table) ≤ 200 ns/body; Shelf block decode
   ∈ [10, 100] ns/body. The program pays no memory traffic at all.
6. **Scaling:** program total bits/body ∝ 1/m (fixed description amortizes): at 2^18 it is
   4× the 2^20 value. At 10^9 bodies the description is < 10^-3 bits/body.

## The floor arithmetic (no measurement needed)

- Working precision: 121 bits/body → 15.1 GB at 10^9. Over 8 GB.
- Brutal player resolution (p 18 bits, e-table 8 bits, ω 16 bits, t_p 24 bits, kind 6):
  72 bits/body → 9.0 GB at 10^9. Still over 8 GB, before tubes, catalogues and events.
- Conclusion I expect the run to license: a lossless i.i.d. belt does not fit the machine
  at any resolution the game could accept; the generator form (PRINCIPLES 6) is not an
  optimization but the only representation that meets the goal. The 8 GB gate must be
  judged on birth populations as programs + scars, not on preserving a particular sample
  (which is what B18's Random/Traders floors currently measure).
