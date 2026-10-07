# Predictions — inverting gold 20261006-0346-taleb-09b5 (co-orbital phase certificate)

The gold's claim: under a formation, every real encounter lies within partner rank 4 along the
orbit, so a phase-neighbour certificate at O(n·k) replaces the quadratic tier, triggered by one
dimensionless number. Nothing in the claim says what the fleet's element spread, shear, or
neighbouring populations may be. These predictions are written before any scene runs. All ranks
are measured with the encounters crate's own truth (`truth_pair`: every local distance minimum
< ρ, rigorous conservative advancement), planar, μ=1, a=1.

Definitions used here:
- **dynamic rank** of encounter (i,j) at time t_m: #{k≠i : circdist(λ_k(t_m), λ_i(t_m)) < circdist(λ_j(t_m), λ_i(t_m))}, λ = mean anomaly + ϖ.
- **static rank**: the same count at t=0 (what a certificate computed once would use).
- **lagged rank**: the count at t_m − 2π (one orbit), what a certificate refreshed once per orbit would use.

## P1 — control: the gold's own regime reproduces
Tight circular formation (n=600, a∈[1−1.2ρ, 1+1.2ρ], e≈0, ϖ=0, λ₀ uniform, ρ=1e-3, ~120 orbits).
Dynamic rank ≤ 4 for ≥ 95% of encounters.

## P2 — element spread breaks rank ≤ 4 (the silent assumption: phase coherence = element coherence)
Identical-period fleet (n=600, a=1 exactly, Rayleigh σ_e, ϖ spread half-width 0.2 rad, λ₀ uniform,
ρ=1e-3, 60 orbits), σ_e ∈ {0.005, 0.02, 0.05}. Because the equation of the centre is ~2e sin ν,
two bodies can be physically adjacent while their mean longitudes differ by up to ~4·max(e).
Prediction: median dynamic rank ≈ 4·σ_e·n/(2π) within a factor of 2 (≈2, 8, 19 at the three σ_e),
and at σ_e=0.05 a k=4 certificate misses > 50% of real encounters. Rank scales ~linearly in σ_e·n;
no phase-ordering certificate at fixed k survives σ_e ≫ 8πk/n.

## P3 — shear sets the refresh rate (the hidden cost factor of O(n·k))
Shearing formation (n=600, a∈[1±5e-3], σ_e=1e-2, ρ=1e-4, 100 orbits). Dynamic rank stays small
(partners are phase-adjacent at closest approach), but the ordering moves: differential precession
dn/n = −(3/2)da/a sweeps each body through ~1.5·(da/a)·n ranks per orbit.
Prediction: median lagged rank (one-orbit refresh) ≈ (3/2)·(δa/a)·n within a factor of 2
(δa/a=1e-2 → ~9); a k=4 certificate refreshed once per orbit misses > 20% of encounters here,
and static rank (no refresh) is unbounded (median ~ n/4). The certificate's cost is
O(n·k) × refreshes, and refreshes per orbit ~ (3/2)(δa/a)·n/(2k) — an O(n²·δa) term the gold's
cost statement omits.

## P4 — composition hole (a body-level trigger cannot route pairs)
Fleet (n=200, tight, a≈1) embedded in a belt (n=800, a∈[0.99,1.01], σ_e=1e-2), ρ=1e-3, 100 orbits.
Prediction: fleet×belt encounters are ≥ 30% of all encounters involving fleet bodies, and they are
not phase-neighbours under any ordering of the fleet. If the concentrated trigger replaces the
window tier for fleet bodies, those contacts are missed: tier routing must be per pair, not per body.

## Kill criteria for my own run
- If P1 fails (control ≠ rank ≤ 4), my harness or the gold's claim is misread: VOID my inversion, report the reconstruction gap.
- If P2's rank does not grow ~σ_e·n (say, flat in σ_e), the "equation of the centre" mechanism is wrong: the gold stands, my mechanism dies.
- If P3's lagged rank stays ≤ 4 at one-orbit refresh, shear is not a hidden cost: gold stands.
- If P4's cross fraction < 5%, the composition hole is negligible: gold stands.
