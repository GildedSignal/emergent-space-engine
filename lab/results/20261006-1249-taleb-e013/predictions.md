# Predictions — taleb-e013 (written before any run)

Target: gold `20261006-0346-taleb-09b5` — "every measured encounter sits within distance-rank 4 of its partner, so a phase-neighbor train certificate at O(n_c·k) replaces the quadratic tier". Its own dossier flags the untested edge: rank evidence is 234 encounters, one seed family, n_c ≤ 800.

## The premise under attack

The certificate watches the k≈4 nearest **in longitude-sorted order** ("sort by longitude, watch k≈4 neighbours, rebuild on overtakes"). The measured evidence is **distance-rank ≤ 4**. These two orders coincide only while the mean number of bodies inside a ρ-wide longitude window is ≪ 1. At a sub-ρ contact, |Δλ| ≤ ρ/a, and the bodies with λ between the two partners are ahead of i in the sorted list, not yet passed — they consume watch slots while being radially separated (radial spread a·e ≈ 14ρ ≫ ρ). So the train's required k should scale with the local longitude line density: E[λ-rank − 1] ≈ d_λ·E|Δλ| ~ ρ·n_c/(2π) for a uniform ring — linear in n_c, i.e. the O(n_c·k) cost is O(n_c²·ρ/a) and the k=4 constant is an artifact of small n_c.

## Held-out cases (all coplanar, a=1, e ~ Rayleigh(1e-3), ϖ ~ U(−0.1, 0.1), a_hw = 1e-5, ρ = 1e-4, same conventions as the gold's `taleb fleet`)

- **C0 anchor** (the gold's phalanx: n=200, mean-longitude bunch σ_λ = 0.01 rad, 1 orbit, S=512): 100–400 encounters; distance-rank max ≤ 4, median 1; λ-rank max ≤ 4. This must reproduce the gold or my instrument is wrong.
- **C1 uniform control** (n=800, λ uniform, 20 orbits, S=256): 40–250 encounters; both ranks ≤ 4, medians 1–2.
- **C2 density axis at fixed n=800** (σ_λ ∈ {0.004, 0.0015, 0.0005}, 3 orbits, S=256; expected interloper mean μ = 2ρ·d_λ ≈ {2–4, 8–15, 25–60}): λ-rank median grows roughly with μ/2 → ~{2–3, 4–8, 12–30}; **k=4 miss fraction ≈ {5–25%, 40–75%, 85–100%}**. Distance-rank stays ≤ 4 at the first two (radial decorrelation); at the tightest jam distance-rank may creep to 5–8 — held as uncertain (phase-aligned triples).
- **C3 scale axis, uniform ring** (n ∈ {12800, 51200}, 3 orbits, S=128; μ ≈ {0.8, 3.2}): λ-rank median ≈ 1 then 2–3; **k=4 miss fraction ≈ 0–3% then 5–20%**; distance-rank flat ≤ 4 throughout.
- **Scaling law**: median λ-rank grows ≈ linearly with n_c·ρ (fit across C1–C3 + theory); distance-rank does not.
- **Ruin arithmetic at the 10⁶ fleet that motivated the certificate** (μ = 2ρ·n/(2π) = 32): extrapolated k at p99 ≈ 25–50 → train store n_c·k·72 B ≈ 1.8–3.6 GB and setup work ×(k/4) vs the gold's "~4×10⁶ sections (~300 MB), setup falls 10⁵×". The gold's fleet arithmetic is ≳ 6× low on memory; the certificate is O(n_c²ρ/a) in n_c until the train is stratified by radial phase (the repair implied by the same invariant: contact needs radial alignment within ρ too, so sort within radial shells of width ρ).

## Instrument checks (registered in advance)

- Detection by 3D KD-tree per step (no longitude binning — the gold's checker lesson: its λ-binned brute missed 193/233).
- Relative motion per step < 0.5ρ so sampled dips resolve; C0 rerun at S=1024 must nest ≥ 99% of S=512 encounters.
- Encounter = sampled min distance < ρ (the gold's definition); ranks measured at the argmin step; both rank definitions computed for every encounter.

## Amendment (after C-series, before D-series and X1 — registered before those runs)

The pre-registered density axis was WRONG in its mechanism: bunching mean anomaly σ_λ does not raise contact-window crowding, because the ±0.1 rad perihelion spread ϖ dominates the true-longitude spread (C2a/b/c: μ̂ = 0.17/0.18/0.18 flat). The certificate's k is set by the TRUE-longitude line density d_λ, and |Δλ| ≤ d_min at contact puts d_λ·2d_min bodies between the partners in the sorted order. Measured scale axis (λ uniform, ϖ ±0.1 — the gold's own fleet workload): μ̂ = 0.089/0.383/0.951 at n = 12.8k/51.2k/128k (μ̂/n = 7.0–7.5e-6, linear), miss(k=4) = 0/0.24%/3.4%.

Held-out predictions for the runs below:
- **D1/D2/D3 aligned formation** (n=800, e~Rayleigh(1e-3), a_hw 1e-5, ϖ and M0 both Gaussian σ ∈ {0.012, 0.008, 0.004} rad, 3 orbits, S=256): true-λ density ≈ n/(2.5·σ√2) → μ̂ ≈ {1.5–3, 3–6, 8–15}; λ-rank p99 > 4 in D2, p50 ≥ 3 in D3; **miss(k=4) ≈ {5–30%, 30–70%, 80–99%}**; distance-rank stays ≤ 6 everywhere (radial spread 14ρ decorrelates 3D crowding). Encounter rate must stay ≤ ~3/body/orbit (else the workload is a contact swarm, out of the certificate's regime — if D3 exceeds it I report that and keep D1/D2).
- **X1 uniform 256k** (S=128, 2 orbits): μ̂ ≈ 1.8–2.0, λ-rank p50 = 2, p99 ≈ 7, **miss(k=4) ≈ 8–16%**, miss(k=8) ≈ 1–3%.
- **Extrapolation to the gold's motivating 10⁶ fleet** (same workload, μ̂ = 7.2–7.5): k=4 train misses most real encounters — Poisson-tail estimate ≈ 94%, empirical 2×Poisson calibration caps near 100%; honest k (p99.9) ≈ 16–24 → store ≈ 1.2–1.8 GB at 72 B/section vs the gold's "~4×10⁶ sections (~300 MB)", and setup work ×4–6 vs its "10⁵×" claim.
