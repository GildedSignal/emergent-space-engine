# Predictions (written before the decisive run)

Attack: the §6 cost table calls chaos "bursts" and prices tides as orbit-averaged. A belt
around a star with a planet has a third, *steady* population: the resonance-overlap band
(the Kirkwood regime), where orbit-averaging is dead (design admits), per-conjunction
first-order kicks are dead (r4 v2), and the single-resonance rotating doll does not apply
(two or more resonances comparable). No gate has a belt-with-planet scene (B18-belt is
planet-free, B15 has no belt, B17 tests two single resonances only).

Decisive experiment: 2-D circular restricted three-body (star + planet + massless test
particles), float64 leapfrog, dt = P_planet/140, T = 1200 P_planet, 800 particles uniform
in a ∈ [0.38, 0.75] a_planet (covers first-order resonances 2:1 through ~20:19), e0
Rayleigh, random angles. Chaos = Lyapunov exponent via renormalized shadow particle
(d0 = 1e-9, renormalized every 50 P_planet). `f_chaotic` = fraction with Lyapunov time
< 400 P_planet.

Held-out predictions (no tuning before running):

1. At μ = 9.54e-4 (Jupiter/Sun), e0 Rayleigh σ = 0.1: f_chaotic ∈ [5%, 25%].
   Additionally ≥ 10% of the belt librating in a single resonance (regular but
   un-averaged: the rotating-doll population).
2. μ scaling: f_chaotic(3e-5) ≤ f_chaotic(9.54e-4)/4; f_chaotic(1e-2) ≥ 2 × f_chaotic(9.54e-4).
3. Control μ = 1e-6: f_chaotic ≤ 1/800 ≈ 0.1% (overlap zones thinner than the sampling).
4. Cold belt (e0 Rayleigh σ = 0.01, μ = 9.54e-4): f_chaotic drops ≥ 3× versus σ = 0.1
   (first-order widths vanish with e; overlap needs it).
5. Conjunction rate of chaotic particles: 1–3 events per planet period per body
   (this is the rate of the missing cost row).
6. Least certain, run only if time allows: doubling T raises f_chaotic by ≥ 1.3×
   (islands break slowly; the measured f is a lower bound).

Numbers I will accept as killing the "bursts" premise: f_chaotic + f_librating ≥ 15% at
Jupiter μ sustained over the run (steady, not decaying with time).
