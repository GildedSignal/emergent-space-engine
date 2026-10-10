# Predictions (written before any run; scene parameters fixed here)

Inverting the adopted gold `20261006-0346-taleb-09b5` (phase-neighbour certificate, O(n·k), build
spec `lab/lenses/b-coorbital-cert.md`, tests = "the gold run's scenes and a dense ring").
Its silent assumption: the concentrated workload is **one** co-orbital population, so every real
partner is on *your* orbit. Held-out cases: **multi-population concentration** — two fleets, each
narrow in period (so any concentration trigger that fires on the gold's scene fires on each fleet),
whose orbits cross only through eccentricity spread.

All scenes: truth = the crate's conservative advancement (every radially overlapping pair, margin
2ρ, local minima below ρ), Kepler μ=1, ρ = 1e-3, 50 orbits, `emergent_encounters::belt::Rng`.
Encounter = one local minimum (pair, t) — distinct events by construction; I additionally check
zero duplicate (pair, t) within 1e-9. Rank = position of the partner in the body's phase order
(wrapped mean-longitude distance), evaluated either per co-orbital group (the adopted certificate)
or merged (the most favourable reading). k = 4 (the gold's number).

## Scenes

- **CTRL** (the gold's co-orbital belt, my seed 20261010): n = 300, σ_e = 3e-4, a ∈ [1, 1.0001].
- **FLEET2** (decisive): fleet A n = 300, a ∈ [1.0000, 1.0002]; fleet B n = 300, a ∈ [1.0600,
  1.0602]; both σ_e = 0.04 (Rayleigh, capped 0.5 as in the crate). Period spread per fleet
  Δa/a = 2e-4 — twice the gold's scene width, so any period-concentration trigger fires per fleet.
  Radial ranges overlap (A's apo ≥ 1.02, B's peri ≤ 1.10) exactly through the e-spread.
- **RETRO** (if time): FLEET2 with fleet B mirrored (counter-orbiting): head-on fleet meeting.

## Predictions

1. **CTRL:** truth encounters 1,500–3,000; per-group = merged rank at encounter time covers 100%
   at k = 4 (the gold's claim, independently reproduced); rank at a single 50-orbit window open
   covers ≥ 95%.
2. **FLEET2:** truth encounters 1,000–5,000; ≥ 95% of them cross-fleet (intra-fleet conjunctions
   are drift-starved: Δn_within·T ≈ 0.09 rad).
3. **FLEET2, the kill:** cross-fleet coverage of the per-group phase certificate = 0% at any
   window length (the partner is not in the group). Merged-rank coverage at window W = 1 orbit
   ≤ 10%. Coverage ≥ 99% needs W ≤ 0.05 orbits, which costs ≥ 10³ certificates per real encounter
   (n·k·windows/encounters), i.e. the same quadratic-tier blowup the certificate was adopted to
   delete.
4. **Kill criterion (fixed now):** the contract "zero misses at O(n·k)" is broken if, at every
   window length whose certificates-per-encounter stays ≤ 200 (the order of the quadratic tier's
   measured setup cost per encounter in the gold), FLEET2 coverage < 99% — dropping far more than
   the 4–6% the gold condemned the window tier for. **VOID condition:** CTRL rank-at-encounter
   coverage ≠ 100%, or duplicate (pair, t) events > 0 (the instrument, not the design, is broken).
5. **RETRO (weaker prior, honest guess):** cross coverage 0% per-group as in FLEET2; merged-rank
   coverage at W = 1 orbit ≤ 5% (relative longitude rate ≈ 2n re-orders ranks twice as fast, and
   head-on meetings are longitude-uniform, not conjunction-gated).
