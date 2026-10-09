# Predictions (written before the decisive runs)

Calibration basis: one smoke run only (n=300, σ_e=1e-2, ρ=1e-3, a∈[1,1.5], 20 orbits, seed 7:
30 events ⇒ λ ≈ 5e-3 events/body/orbit). Nothing else tuned. All decisive configs below are
held out: longer horizons, other seeds, denser/narrower belts, an intruder.

Configs (truth = every local minimum of pair distance below ρ, shipped `truth_pair`):
- `long3`: 300, σ_e=1e-2, ρ=1e-3, [1,1.5], 1000 orbits, seeds 11/12/13 — main tail.
- `ultra`: 100, σ_e=1e-2, ρ=1e-3, [1,1.5], 10000 orbits, seed 15 — deep-time absorption.
- `dense`: 3000, σ_e=1e-2, ρ=3e-4, [1,1.5], 20 orbits, seed 14 — density scaling.
- `scale300/1000`: 300 and 1000, σ_e=1e-2, ρ=1e-3, 20 orbits, seeds 21/22 — λ vs n at fixed span.
- `storm`: 400, σ_e=0.025, ρ=3e-3, [1,1.0025], 20 orbits, seed 8 (shipped "narrow-adversarial").
- `intruder`: 300 bodies σ_e=1e-2 ρ=1e-3 [1,1.5] 50 orbits seed 9, body 299 replaced by e=0.9.

Model: an event scars both bodies permanently (pop.rs ladder semantics: kicked ⇒ leaves the
program; scars are exact absorbing deltas). First-event time per body ⇒ scarred fraction S(t).

- **P1 (across bodies):** on `long3`, events concentrate: top 1% of bodies hold >1%·(mean share)·10
  (Gini > 0.3); the max-body count exceeds the median body by >10×. Driver guess: eccentricity
  (wide radial span ⇒ more overlapping partners).
- **P2 (across time):** on `long3`, 1-orbit bins have Fano factor (var/mean) > 1.5 — clustering
  beyond Poisson — and max/median bin > 5.
- **P3 (trains):** on `long3`, >30% of events are same-pair returns: another event of the same pair
  within 1.5 synodic periods (2π/|n_i−n_j|) of a previous one.
- **P4 (absorption):** on `long3`, half the bodies take their first event inside 200 orbits
  (S(1000) > 0.9). Extrapolating the smoke λ naively gives T½ ≈ 139 orbits.
- **P5 (quantum sweep):** counting only events closer than 0.1ρ as scarring multiplies T½ by >3
  (kick size ∝ 1/d concentrates events near 0 misses), but S(1000) at q=0.1 still exceeds 0.5.
- **P6 (intruder):** the intruder's transit produces at least one 1-orbit bin >10× the median bin,
  and the intruder takes the top per-body event count by a factor >3.
- **P7 (storm belt):** `storm`'s per-body rate λ exceeds `long3`'s by >30× (density × ρ).
- **P8 (λ vs n):** at fixed span, σ_e and ρ, λ grows linearly in n (λ(1000)/λ(300) = 3.3 ± 30%).
- **P9 (determinism):** re-running any config reproduces the same hash2 and event count.

Failure of P2+P3 together would say the belt's distinction stream is Poisson-like (Mediocristan):
then mean-rate sizing is safe. Failure of P4/P5 would say programs survive a belt — also a result.
