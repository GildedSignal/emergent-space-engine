# Predictions — 20261010-2220-scout-9096 (written before the decisive run)

Question: does the player's growing light cone stay affordable, exactly, at c, in some representation?

Model (integer automaton, field-step news): one wildcard source emits action `a` units/tick; a cell at distance r gains staleness `δ_k = a >> 2k` per tick (dyadic mass-type dilution d^-2, band k = [2^k, 2^{k+1})). A cell recompiles (pays work C_r = 2πr apps) when staleness crosses its quantum. Three representations:

- L0 naive: every touched cell recompiles every tick (no quantum).
- L1 flat: quantum q = 1 per cell everywhere.
- L2 graded: quantum q_k = 2^k per cell (quantum ∝ distance, i.e. ∝ cell size; the sizing multipole validity already forces — Δg/g ≈ 2ℓ/d ⇒ ℓ ∝ d).

Predictions, held out (case not tuned: the a-sweep points, two-source, silence):

1. **P1 (the wall, L0):** work/tick = Θ(t²) — every cell inside the cone pays every tick. Quadratic; killed on sight.
2. **P2 (flat law shape):** L1 work/tick = 3πa·(#bands) = 3πa·log₂t → **linear in ln t, unbounded**. Every band pays equally (self-similar waste: no scale ever rests).
3. **P3 (graded law shape):** L2 work/tick = Σ_k 3πa·2^{-k} → 6πa, **saturating**. Signature: work/tick(t=2^14)/work/tick(t=2^7) ≥ 1.8 for L1, ≤ 1.02 for L2.
4. **P4 (memory):** pending staleness entries (rings with 0 < residue < q): L1 ≈ all rings beyond band ½log₂a → ∝ t (~15,300 at t=2^14, a=2^20); L2 = one per band → ∝ log₂t (~14). Ratio > 1000. (Per-cell anisotropic count is another factor 2πr per ring for L1 → Θ(t²); analytic, not simulated.)
5. **P5 (hot radius d*):** band where cells cross ≥ once per tick: L1 k* = ½log₂a (d* = a^{1/2}, fit exponent 0.50 ± 0.03); L2 k* = log₈a (d* = a^{1/3}, 0.333 ± 0.02), over a ∈ [2^6, 2^24].
6. **P6 (exactness):** per ring, integer identity Σ arrivals = apps·q + residue, no exception, any t.
7. **P7 (two sources):** work exactly additive (2× single, integer-exact); superposition adds deposits, never work.
8. **P8 (silence):** source stops → work/tick → 0 immediately (residues stay sub-quantum forever, bounded staleness: error type, not size); memory stays.
9. **P9 (smoothness probe):** L2 crossings are spatially coherent (whole bands fire together) → p99/mean of per-tick work > 5 unstaggered; a deterministic per-ring dyadic phase stagger brings p99/mean < 3.

Kill criteria for the candidate: L2 work/tick not saturating (P3 ratio > 1.1), memory not log (P4), any exactness break (P6), non-additive two-source work (P7), or stagger failing to flatten (P9).

What the falsifier cannot see: scalar isotropic news only (the real deposit is a rank-1 Kerr–Schild tensor — additivity is linear by construction but untested here in tensor form); recompile cost per crossing taken as O(1); no neighbor cascade simulated (a crossed cell's own change is sub-quantum to neighbors by the same law — argued, not measured).
