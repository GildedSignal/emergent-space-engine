# Predictions (written before the decisive run)

**Claim under test.** The encounter finder needs one certificate, not three mechanisms. The cone
tier (dispersed pairs), the slack skin (setup amortization) and the phase-neighbour certificate
(formations, taleb-09b5 gold, with its dimensionless trigger) are readouts of one object: a pair's
Diophantine expiry, materialized only for phase-rank neighbours inside a frequency band whose width
is set by the certificate horizon T (|Δn| ≤ 2π/T), plus the cone for cross-band pairs. The section
classifier the crate already has (`Kind::Cross/Wide/Full`) is the same regime split.

**Scenes** (not tuned on): F1 fleet (N=800, a∈[1,1+3e-5], σ_e=3e-4, ρ=1e-4, 30 orbits);
F2 co-orbital swarm (N=1000, a∈[1,1.0001], σ_e=3e-3, ρ=3e-4, 20 orbits); X two crossing fleets
(2×400, radial ranges overlapping on [0.997,1.2], ρ=1e-3, 30 orbits); B belt control (N=1000,
σ_e=1e-2, ρ=1e-4, 100 orbits). Truth: the crate's own conservative advancement on every
radially-overlapping pair (independent solver: Halley vs the method's Newton).

**Predictions, held out:**

1. **P1 (exactness of the crate as-is in the degenerate regime).** `cone_pairs + pair_events`
   (the crate unchanged) misses **0** encounters on F1 and F2. The taleb gold's "the window tier
   drops 4–6% of contacts under a formation" was the plane's two-tier window, not this crate's
   sections machinery. If the crate misses contacts on F1/F2, the phase certificate is
   load-bearing and my unification is dead.
2. **P2 (where the formation cost sits).** On F1 the crate materializes ~n²/2 candidate pairs and
   the setup (window `evals`), not the exact checks, dominates: evals per real encounter > 10³
   (vs ≈ 10¹ on B).
3. **P3 (the unified certificate keeps exactness and prunes the setup).** Rank-pruning inside the
   horizon band (k=4 mean-longitude neighbours per body per renewal, renewals at T/8) with the
   cone kept for cross-band pairs: **0 misses on all four scenes**, and materialized pairs drop
   from ~n²/2 to ~n·k·R on F1 (R = renewals), i.e. setups per real encounter fall ≥ 10× vs P2.
4. **P4 (the boundary).** k=2 on F1 misses some encounters (the rank law has a real boundary
   between 2 and 4); k=4 holds. If k=2 also holds, the certificate is stronger than claimed and
   the rank law should be re-measured at k=1.
5. **P5 (negative control: the band is load-bearing).** Ranking by mean longitude **without** the
   band (all bodies in one ranking) **misses** cross-fleet encounters on X. If it misses nothing,
   the band structure is unnecessary and the certificate is just a global phase sort — a bigger
   simplification than claimed, to be re-derived before believing.
6. **P6 (no regression on the dispersed case).** On B, the unified certificate's work is within
   2× of the crate as-is (the band splits the belt; cross-band pairs dominate and go through the
   unchanged cone path).

**What would make the claim wrong even if all predictions hold:** a formation whose internal
e-spread makes most pairs *transversal* crossers (short arcs) rather than degenerate ones — then
rank-pruning is unjustified for them (their conjunctions are not phase-local), and P3's zero misses
would be luck of the scene. I will report the section-kind histogram on F1 to expose exactly this.
