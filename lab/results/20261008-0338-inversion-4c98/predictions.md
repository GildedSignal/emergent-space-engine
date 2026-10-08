# Predictions — inverting the co-orbital phase-neighbour certificate (gold 20261006-0346-taleb-09b5)

**Claim under test (board, verbatim):** "every real encounter lies within partner rank 4 along the orbit,
so a phase-neighbour certificate at O(n·k) replaces the quadratic tier, triggered by a dimensionless
number." Measured, per the board, **inside a lone formation** ("a fleet on one orbit").

**Inversion:** the claim silently assumes the encounter's partners co-rotate (same mean motion n, so
phase rank is frozen or slowly shearing). Any population with a different n — eccentric crossers, a
belt, an arriving fleet — slides through the phase ordering at rate Δn. Rank needed ≈ Δn · Δt_refresh ·
N/(2π). That is not a constant 4; it is cadence × differential rate.

**Scenes (2D plane, one star, Keplerian truth = every pair-local minimum of distance below ρ, the
crate's own `truth.rs` notion; certificate checked at refreshes over the window, an encounter caught
iff the partner is within rank k at the last refresh before its minimum):**

- `fleet` (control, the gold's scene): 600 ships, a = 1 AU, σ_a/a = 1e-4, e = 0, uniform phase.
- `fleet+crossers`: fleet + 60 eccentric crossers (a ∈ [0.7, 1.3], e ∈ [0.2, 0.5]) crossing 1 AU.
- `fleet+belt` (the game scene: a fleet inside a r8-style belt): fleet + 400 belt bodies, a ∈ [0.9, 1.1], e ≤ 0.2.
- `loose-fleet`: σ_a/a = 1e-2 (internal shear only).

ρ = 1e-3 AU, window 2 orbits, refresh cadence 1/16 orbit (and 1/8, 1/32 for the cadence coupling).
Two scopings of the certificate: **fleet-scope** (rank within the formation only — the natural reading
of "sort the fleet by phase") and **global-scope** (rank all bodies by longitude).

## Held-out predictions (not tuned on; written before the run)

- **P1 (control must pass, else the instrument is broken → VOID):** `fleet`: ≥ 99% of encounters lie
  within rank 4 at cadence 1/16 orbit. Reproduces the gold in its domain.
- **P2:** `fleet+crossers`, fleet-scope, k = 4: ≥ 95% of fleet×crosser encounters are missed
  (crossers are not in the fleet's phase ordering at all).
- **P3:** `fleet+crossers`, global-scope: the p99 required rank for cross encounters exceeds 20 at
  cadence 1/16 orbit.
- **P4:** `fleet+belt`, global-scope, k = 4: > 5% of fleet×belt encounters missed (belt edge Δa = 0.1
  gives Δn/n ≈ 15%, so rank ≈ Δn·Δt·N/2π ≈ 10).
- **P5:** `loose-fleet`: intra-fleet p99 required rank stays ≤ 4 even at σ_a/a = 1e-2 — internal
  shear is slow; k binds through cadence × shear, and intra-formation rank is not the failure.
- **P6 (cadence coupling):** halving the refresh interval halves the p99 required rank for cross
  encounters (ratio 0.5 ± 0.3); at cadence 1/64 orbit the cross-pair p99 rank is still > 8, i.e. no
  practical cadence brings different-n partners under k = 4.

**Kill rule:** any of P2, P3, P4 holding kills the universality of "rank 4 catches every real
encounter" beyond a lone formation, and forbids implementing the phase certificate as the whole
candidate tier of a concentrated scene. P1 failing voids the probe instead.

**What would make the kill unfair:** if the in-flight build already scopes the certificate
intra-formation AND keeps an orbit-geometric cross tier (Binet arcs) between populations, then P2/P3
confirm its necessity rather than kill anything — the kill target is the board's universal sentence
and any implementation that takes it literally.
