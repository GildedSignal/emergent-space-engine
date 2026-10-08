# Predictions (written before the decisive runs)

Question: at 10⁹ bodies on the 8 GB M1, which budget term breaks first — static memory,
live distinctions (H_live), event throughput, or bandwidth — and by how many orders?

Numbers taken from the repo, not tuned by me: kick 29 µs (H0210), 32.5 kicks/orbit
(H0190 K1), 114× from averaging (K2), belt program 0.126 bits/body (gold components-98bc),
naive quantized state 157 bits/body, tube 16 B (law.md), r8 belt 427 encounters / 20 orbits
at N = 10⁴ (σ_e ~ 10⁻², ρ ~ 10⁻⁴, a ∈ [1, 1.5]).

Held-out cases and what I expect:

1. **Encounter-rate growth at fixed distribution** (probe A: σ_e = 10⁻², ρ = 10⁻⁴ fixed,
   N = 10³..8×10³, 20 orbits, exact truth from `crates/encounters`): per-body true
   encounter rate grows with exponent α ∈ [0.7, 1.3] (I predict ≈ 1: every added body is
   another perturber for all others; dilution does not save it).
2. **Anchor rate**: at N = 10⁴ the per-body rate lands within a factor 3 of r8's belt-0
   2.1×10⁻³ per orbit (different seed; same σ_e, ρ).
3. **Throughput check**: re-deriving the board's "190 cores for 10⁹" from the plane's own
   29 µs/kick and H0190's 32.5 kicks per LEO orbit (T ≈ 5400 s) lands within 25% of 190.
4. **Scar entropy** (probe B, analytic MC of flyby impulses at b < ρ, masses from 10⁶ kg
   ships to 10²¹ kg dwarf planets, element quantum ε_a ∈ {2⁻¹⁰, 2⁻²⁰, 2⁻³⁰} of a):
   for rock-and-smaller masses every single-encounter element change is far below any
   plausible quantum (Δa/a < 10⁻¹⁸ vs ε ≥ 10⁻⁹), so h = 0 per encounter and H_live grows
   only through accumulated sub-quantum walks (rate ∝ D/ε², D ∝ m²). For planet-mass
   perturbers h ≈ 20–60 bits per encounter.
5. **Fill times** (10⁹ bodies, T_orbit = 1.6×10⁸ s, h = 50 bits/scar):
   - all in one 0.5-AU belt (local N = 10⁹): H_live fills 8 GB in ~10⁶ s (days) —
     memory binds before throughput;
   - spread over ≥ 10³ sparse belts: ≥ 10⁸ s (years) — memory never binds;
   - LEO fleets: memory never binds; throughput needs ≥ 60–170× cheaper kicks
     (or 114× fewer via averaging).

Kill criterion for my own headline: if probe A shows α < 0.5 (per-body rate saturates),
the "one dense belt fills memory" branch dies and H_live is bounded everywhere; if the
measured anchor rate at N = 10⁴ is > 10× off r8's, my belt-units arithmetic is wrong and
the ledger must be re-derived before claiming anything.
