# Predictions — 20261008-1058-second (written before the decisive per-doll runs)

The checker's named experiment: re-derive the radius-flat rule in **per-doll units**
and measure it — scaled belts at several a, local-orbit accounting, ρ/a fixed —
then state the true residual exponent. (Reproduction of the silver's record already
ran before this file; it regenerates bit-for-bit, no tuning freedom there.)

Setup: `doll` extends the run's own `cusp` (same seed, same cone scan, same exact
per-pair truth). Belt (n=30000, σ_e 0.05, γ=0) on [0.3·s, 3·s] for s ∈ {1, √10, 10,
10^1.5, 100}; ρ = 1e-4·s (ρ/a fixed); horizon = 500·s^1.5 a=1-orbits (= 500 orbits
at a = s), so every belt runs the same *local* coverage per unit s; 8 sampled bodies
per radial bin (the silver used 2 — the per-bin noise it was dinged for). Ring
(n=10000, [1, 1.01]·s), 100 local orbits, same ladder. Per bin I report
cpe_perloc = cand_per_enc / a^1.5 (candidates per encounter per local orbit — the
per-doll work-per-encounter: the a^1.5 mean-motion clock divided out).

Mechanism to discriminate (from the silver's own law cpe ≈ 1.2·a^2.6/ρ):
per-pair encounter rate ∝ ρ·n/a = ρ·a^(-2.5) predicts exponent 2.5, i.e. residual
2.5 − 1.5 (clock) − 1.0 (ρ/a) = **0**; the fitted 2.642 predicts residual **0.14**
(10^0.28 ≈ 1.9× across the 100× ladder).

## P1 — structure is scale-free
deg_mean, deg_p99, deg_max and f = deg_mean/n are constant across s to within float
and sampling noise (< 2% drift over s = 1→100); the candidate geometry (cone test in
Binet u with ρ ∝ a) has no absolute scale.

## P2 — the named question (ladder)
cpe_perloc at matched relative bins is flat in s: fitted residual exponent |β| ≤ 0.1
end-to-end over 100× (≤ 1.6× total drift, within the bins' Poisson noise). If
β ≈ 0.14 holds instead, that is the true residual and the adoption note must carry it
(ρ relative alone leaves a mild a^0.14); if β ≈ 0.5–0.6 the checker's a^1.5-with-ρ∝a
reading wins and radius-flat fails even in per-doll units.

## P3 — within-belt residual
Fitting log cpe_perloc vs log a inside one belt (10 bins, 8 samples each) gives
exponent 0.0–0.15, consistent with P2's ladder value at far better cost; the inner
bins (denser local coverage, more hits) anchor it.

## P4 — ring (pure clock, deg = N−1 by construction)
cpe_perloc flat in s within ±25% (hits/belt ~130, Poisson); deg stays N−1 at every s.

## P5 — e-cap tail (checker's side note, cheapest form)
With the population's e-cap raised 0.5 → 0.9 at σ_e 0.3 (24.9% of bodies were pinned
at 0.5 in the silver's hot case; 1.1% land in (0.5, 0.9] now), deg_max/deg_mean stays
≤ 10 (still Mediocristan: the Rayleigh body of the tail sets the worst cell, no
blow-up), though larger than the capped 1.5 the checker measured.

Kill criteria: any bin sterile at 8 samples where the silver had hits; deg drifting
> 2% with s (scale leak in the cone test); β outside [−0.1, 0.2] (then I report which
mechanism the residual favors and radius-flat is refuted as stated).
