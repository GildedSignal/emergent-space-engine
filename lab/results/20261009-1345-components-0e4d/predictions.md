# Predictions — 20261009-1345-components-0e4d

Written before the held-out runs (belt C, the occupancy ladder at 2^21/2^22, and the
weak/strong crossover scan). Tuned on: belt A (p 2048–3072 M, σ_e 0.03) and belt B
(weak branch) at N ≤ 2^20, and the Part A error sweep.

1. **Hot belt C (σ_e 0.3, p 2048–3072, strong branch):** the gap axis spreads over
   ~7.6 octaves (e up to ~0.99 ⇒ gap down to ~0.005), so distinct codes at N = 2^20
   rise to ~0.9–1.0 M (vs 0.49 M for belt A), i.e. nearly every body its own key.
   Shape entries = distinct codes on the strong branch (verified equal on A at 2^18/2^20).

2. **Occupancy model (uniform Poisson saturation):** G = N / (−ln(1 − D/N)) fitted at
   belt A's D = 488 004 at N = 2^20 gives G ≈ 1.6–1.7 M cells. Predicts D(2^21) ≈ 1.15–1.20 M
   and D(2^22) ≈ 1.45–1.55 M. If measured D at 2^22 is outside [1.3, 1.7] M, the
   uniform-cell model is wrong (clustering or a structured grid) and I say so.

3. **Saturation at 10^9 bodies (belt A):** occupancy → G ≈ 1.7 M entries. At the measured
   ~12.6 KB per shape entry (124 knots × 88 B + 122 crossings × 8 B + 224 B struct +
   Arc + HashMap slot) the memo alone is **≈ 20–22 GB — 2.5× the whole 8 GB machine**,
   while the bodies themselves cost ~0.126 bits each (gold components-98bc) ≈ 16 MB.

4. **Crossover:** the weak branch (radius dropped from shape identity) turns on at
   compactness ≤ 2^−18 (p ≥ 262 144 M). Scan p0 ∈ {2^17, 2^18, 2^19} at N = 2^16:
   shape entries collapse from ~6×10^4 (strong) to ~10^3 (weak) between 2^17 and 2^18.
   Belt B (p 524288–786432) shape entries saturate ≤ ~1.1×10^3 ⇒ ≤ ~14 MB at any N.

5. **Floor (from Part A, already measured):** the 12-bit key is B2-tight on both axes
   (period error 3.5×10⁻⁴ at 12 bits; 1.03×10⁻³ at 11 scale bits fails 3/256; shape 11 bits
   ties 12; ≤ 10 fails broadly). B1 precession never binds (max 4.5×10⁻⁷, four decades of
   margin). So the grid cannot be coarsened to shrink the memo: the win must come from
   cheaper shape entries or a lower weak-branch threshold, not from fewer cells.

Kill criterion for the rung's premise: if occupancy at 2^22 comes in far below the model
(< 1.3 M) AND entries/bytes are far below 12.6 KB, the "memo is the bomb" claim weakens
to a strong-branch-only risk and I report it as scoped, not general.
