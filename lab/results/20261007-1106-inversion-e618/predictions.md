# Predictions — inversion run 20261007-1106-inversion-e618

Written after the smoke test (nc=200, σ_e=0.001, which reproduces the gold: 232 encounters
vs their 233; dist-rank ≤ 2, lon-rank ≤ 3; grid instrument misses 0 pairs vs full O(nc²)
scan) but BEFORE the decisive sweep. All configs: a half-width 1e-5, ρ=1e-4, 2 orbits,
seed 7 unless said. Mechanism: at contact |Δθ|·r ≤ ρ always, so the partner is inside the
ρ-arc window; the number of bodies angularly interleaved between the pair is
~ nc·ρ/(√(2π)·σ_λ), linear in nc. The gold measured distance-rank (stays small) while the
certificate watches the longitude order.

## Cases not tuned on

1. **nc scaling at the gold's own fleet parameters** (σ_e=0.001, ϖ ±0.1, σ_λ=0.01):
   lon-rank p50 grows roughly linearly with nc; max lon-rank crosses k=4 between nc=800
   and nc=3200; frac(lon-rank > 4) ≈ 0 at nc ≤ 800, > 0.3 at 3200, > 0.8 at 12800.
   dist-rank max stays ≤ 4 at every nc (the gold's metric survives my instrument).
2. **e-spread at nc=3200** (σ_e = 0.003, 0.01; radial breathing 30× and 100× ρ):
   lon-rank distribution unchanged (angular occupancy is set by nc/σ_λ, not e);
   dist-rank unchanged (≤ 4); but the interleavers' median radial offset from the pair
   grows from ~ρ to ≫ ρ — the interleavers stop being contacts, so the inflated watch
   width is pure waste while distance-rank cannot see the failure.
3. **Bunch width** (σ_λ = 0.02, 0.005 at nc=3200, σ_e=0.01): lon-rank occupancy scales
   ~1/σ_λ (halves / doubles).
4. **Isotropic apsides** (ϖ uniform, nc=3200, σ_e=0.01): lon-rank inflation persists
   (mechanism is angular); encounter count drops.
5. **Seeds 8, 9** at the headline config (nc=3200, σ_e=0.01, σ_λ=0.01): same story,
   frac(lon-rank > 4) within ~±0.15 of seed 7.

## Kill criterion for my own claim

If lon-rank max stays ≤ 4 at nc=12800 (all other gold parameters), the train certificate
holds at every scale I can reach and my mechanism is wrong: the dossier then reports the
certificate as SURVIVING inversion, with the measured occupancy as the safety margin.

## Arithmetic consequence (checkable, not run)

k*(10⁶ fleet, σ_λ=0.01) ≈ nc·ρ/(√(2π)σ_λ) ≈ 4×10³: the gold's "nc·4 sections ≈ 300 MB"
becomes nc·k* ≈ 4×10⁹ sections ≈ 290 GB at 72 B/section — memory ruin at exactly the fleet
scale the certificate was adopted for; kept at k=4 it misses the contacts instead.
