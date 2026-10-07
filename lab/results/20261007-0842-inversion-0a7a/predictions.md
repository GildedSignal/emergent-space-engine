# Predictions — inversion run 20261007-0842-inversion-0a7a

Written before any run of the probe (only the crate was read, no numbers measured).

**Question.** The gold 20261006-0346-taleb-09b5 replaced the quadratic candidate tier, inside an
a-concentrated clump, with a "train" certificate: sort by longitude, watch k≈4 neighbours, rebuild
on order changes (overtakes), trigger = clump Binet diameter vs eps_u (an a-space condition only).
The dossier itself names the untested invariant: radial spread ≲ ρ. I attack exactly that, at fixed
a-clump (trigger still fires): eccentricity spread σ_e ∈ {0.001 (control), 0.005, 0.02, 0.05} with
apsides spread accordingly (clustered for the control, uniform for e-spread fleets — a fleet after a
scatter or on transfer orbits).

**Measured quantities** (per scenario, nc=200, a=1±1e-5, λ bunch σ_λ=0.05, 2 orbits, ρ=1e-4):
- contact snapshot ranks (distance-rank and cyclic true-longitude rank at closest approach) — the gold's statistic;
- λ-train set churn: membership changes of each body's cyclic true-longitude 4-neighbour set, per body per orbit;
- continuous-presence lead: how long before contact the partner has stood within cyclic rank 4;
- section-setup evals per pair (the pairwise `sections` machinery) on e-spread pairs;
- real encounters per body per orbit (true-longitude-binned brute force, motion < ρ/2 per step).

**Pre-registered calls:**

- P1 (control, σ_e=0.001): contact ranks ≤ 4 everywhere; churn ≲ 20 per body per orbit; train work
  per real encounter well below the quadratic tier on the same scenario; lead p50 ≥ 0.01 orbit.
- P2 (the kill): churn grows roughly ∝ σ_e (equation-of-center wobble 2e sets the order-swap rate,
  not Δa). At σ_e = 0.05 I predict churn ≥ 100 per body per orbit, so train setup work per real
  encounter (churn × k × evals_per_section / encounters) exceeds the quadratic tier
  (nc²/2 × evals / encounters over the same horizon) by ≥ 3× at nc=200 — i.e., inside the trigger's
  own regime the adopted certificate costs more than the thing it replaced, and the gap grows with
  the rebuild horizon. The dimensionless trigger is missing the e dimension.
- P3 (non-vacuity): encounter rate at σ_e ∈ {0.02, 0.05} ≥ 0.02 per body per orbit (else the regime
  is dormant and the attack is moot — that would be a real negative result and I will report it).
- P4 (instrument): contact snapshot ranks stay ≤ 4 in every scenario, including where P2 fires —
  demonstrating the gold's headline statistic measures ρ-crowding, not certificate validity, and
  cannot falsify the watch by construction.
- P5 (secondary, throttling): at σ_e = 0.05 a material fraction (≥ 20%) of encounters have
  continuous-presence lead < 0.005 orbit; any budgeted/coalesced rebuild schedule that cannot
  react within that window misses them. (Under the maximally charitable reading — instant rebuild
  at every set change — nothing is missed; the cost in P2 is then the kill.)
