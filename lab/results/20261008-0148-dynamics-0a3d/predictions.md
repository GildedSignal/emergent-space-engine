# Predictions (written before the decisive runs)

Question: is the belt's encounter (surprise) stream memoryless, and do encounters cascade?

Exact truth: the repo's `truth_pair` (rigorous conservative advancement, every local minimum of
pair distance below ρ), run over radially overlapping pairs of `make_belt` populations. All
stream statistics measured on that exact event list; no candidate tier involved.

## Held-out cases (not tuned on)

1. **λ(σ_e) shape** (aggregate encounters per body per orbit vs Rayleigh σ_e; belts N=1000,
   a∈[1,1.5], ρ=1e-4, 100 orbits): I predict λ is *peaked*, not monotone: for σ_e ≫ ρ/a the
   conjunction miss-distance spread (∝ a σ_e) caps P(miss<ρ) and λ falls like σ_e^{-1};
   for σ_e ≲ ρ/a the partner-overlap width ∝ σ_e limits λ and it rises. So across
   σ_e ∈ {1e-3, 3e-3, 1e-2} I predict λ(1e-3) > λ(3e-3) > λ(1e-2), roughly 3 : 1 : 0.3,
   with the peak near σ_e ≈ ρ/a = 1e-4.
2. **Stream clustering (cold belt, σ_e=3e-3)**: the aggregate stream is a superposition of
   per-pair quasi-periodic trains (synodic period T_syn). Predict: Fano factor F(T) > 1.3 at
   windows T near the median T_syn of encountering pairs, F(T) → 1 (±0.1) for T ≫ spread of
   T_syn; a majority (>50%) of events are repeats from pairs that already met before
   (≥2 events per pair).
3. **Warm belt (σ_e=1e-2)**: wider e-spread thins per-pair trains (fewer conjunctions qualify)
   and shortens T_syn mixing; predict F(1-orbit windows) strictly lower than the cold belt's.
4. **Concentrated formation** (belt squeezed into a∈[1,1.01], 50× surface density, the fleet
   regime of gold 20261006-0346): predict "seasons" — F(1-orbit windows) ≥ 5 and the p99
   window count ≥ 10× the Poisson prediction at the same mean.
5. **Branching sign (reduced model, parameters anchored to the measured λ slope)**: encounters
   pump e (viscous stirring) and the measured λ falls in σ_e, so the feedback loop
   e↑ → λ↓ is *negative*: no avalanche at belt scale; the belt self-regulates toward the λ
   peak (σ_e*). I predict the estimated branching magnitude |R| < 1 everywhere in the sweep,
   with R changing sign only below σ_e*.

Kill criterion for the headline ("no cascade gate needed at belt scale; smoothness must be sized
on trains, not on the mean rate"): if F(1-orbit) < 1.2 for the cold belt AND the concentrated
belt, the clustering claim dies (the mean rate suffices). Controls: Poissonized resample of each
stream (same count, uniform times) must give F ≈ 1 within ±0.07 — else the instrument is broken.
