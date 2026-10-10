# Predictions — 20261010-0814-dynamics-740f

Question: does the belt population's scar layer (H_live) walk to ruin or reach an
attractor? Measured as bytes/body vs kick events absorbed k, on the shipped
`crates/shipmem` store (`Program::seal_from`, exact integer grid), under four kick
generators: G1 collective (positive control), G2 independent Gaussian graininess,
G3 encounter-replay (impulse law, pairwise zero-sum, physical belt μ), G4 Cauchy
(extreme tail stress).

Held-out expectations, written before the decisive run (not tuned on):

1. **G1 (collective) ≈ 0 bytes/body at every k.** A kick shared by all bodies is a
   program/block constant; the shipped codec must absorb it (positive control). If
   it does not, the instrument is broken and the run is VOID.
2. **G2 action columns (a, ex, ey): bits/body ≈ Σ_f (½·log₂ k + c_f)** — a random
   walk's state entropy, not its history entropy. Slope ≈ 0.5 bit per column per
   doubling of k; **no linear ruin** (history storage would grow ∝ k).
3. **G3 follows the same ½-log law** while kicks stay bounded (finite variance),
   with a heavier additive constant from the tail (patched exceptions).
4. **The phase column (periapsis time) is the danger, not the actions.** Each
   action kick persists as a period error, so the phase deviation grows ~ k^1.5
   (integrated diffusion) → bits slope ≈ **1.5·log₂ k**, steeper than ½, until it
   wraps (saturates at log₂(period grid) bits — full decoherence of the birth
   bijection). The saturation horizon k* is the number that decides whether 10⁹
   bodies fit 8 GB.
5. **P1 (re-anchor the program at the ensemble mean each epoch) ≈ P0** for G2/G3:
   the mean of independent kicks is one vector against N bodies (variance 1/N);
   only G1 (correlated) is absorbed. The smooth tide is program-able; graininess
   is not. (If P1 bought a lot on G2, my zero-sum/collective split would be wrong.)
6. **N-independence:** bytes/body at N=2¹² vs 2¹⁴ agree within noise.
7. **Game-scale extrapolation:** at 1 AU, 1 h of play at RTF 100 (≈11.4 orbits,
   k ≈ 368 at 32 kicks/orbit), bytes/body stays in the single digits — orders
   below the 16 B full tube — and the belt at 10⁹ fits 8 GB unless k is near k*.

Kill criterion: if G2 bytes/body grows ≳ k^0.9·const (near-linear), the claim
"attractor not ruin" is dead and the run reports the ruin law instead.
