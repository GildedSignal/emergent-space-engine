# Dossier — H_live measured: the belt's scar rate, and the quantum that decides 10⁹ in 8 GB

## Claim

The allocator's missing input — H_live, the live distinction (scar-creation)
rate that `docs/law.md` names as its memory budget — is measured for a B18b-style
belt, and its verdict inverts the comfortable reading: at the tube's native
32-bit quantum the belt is **not** free (10⁹ bodies write 180 GB per played
hour at rtf 100), and the 4 GiB/hour budget is met only if the scar quantum is
coarser than ~2×10⁻⁷ rad (~2⁻²¹); memory binds where surface density is
(a 10⁴-ship battle in a 10 km disc writes 92 GB/hour at 10⁶ ships), never where
body count is.

## Bottleneck

Board risk "H_live: distinctions per game-second — not measured yet"; focus
item 5 (10⁹ in 8 GB). Storage component, lens `components`. The floor of the
store is the scar rate (PRINCIPLES #6 "Store the generator, not the generated";
#24 "the memory floor is information-theoretic"). The design consumed this
number (`law.md`: "The allocator reads H_live as its memory budget") before it
existed; this run supplies it and shows which single constant — the scar
quantum — moves it by 10⁶.

## Evidence

`python3 hlive.py` (43 s, numpy 1.26, 8 vCPU, loadavg 0.10/0.19/0.68, 15.6 GB;
output `hlive-out.json`, seed 20261012). Monte-Carlo over 15,000 iid pairs from
the belt program (a ∈ [2.1, 3.3] AU, Rayleigh e σ = 0.1, uniform angles,
coplanar; D log-uniform 1–100 km, ρ 2500 kg/m³, 1 M☉ host), both members
propagated as exact 2-D Kepler orbits for 40 yr at dt = 3 d; local minima of
pair separation are conjunction approaches, each with its own (b, v_rel, μ).
Rate per body = (N−1)·⟨rate per pair⟩, N = 2²⁰.

- Approach rate: 2,005/body/yr within 0.05 AU; 11,456 within 0.25 AU; fitted
  R ∝ b^1.079 (**P2 holds**, the 2-D kinetic law).
- Upper-bound scar rate (every conjunction with deflection 2μ/(bv²) > q counts):
  q = 2π/2³² → 1,979/yr/body = 6.27×10⁻⁵/game-s → **180.6 GB/hour** for 10⁹
  bodies (8 B/scar); q = 10⁻⁷ → 6.4 GB/h; q = 10⁻⁵ → 0.80 GB/h; q = 10⁻³ →
  0.16 GB/h; physical contacts (25 km) → 0.23 MB/h. Median event deflection is
  2.5×10⁻¹¹ rad (sub-quantum even at q32); the q32 rate is the big-body tail
  (deflection ∝ D³).
- Budget crossover: 4 GiB/hour at q ≈ 2.4–7.3×10⁻⁷ rad (local vs global fit);
  20 GiB/hour at q ≈ 2–3×10⁻⁸.
- Drive: mean 2.68×10⁻⁸ rad/s/body (0.85 rad/yr), dominated by slow conjunctions
  between near-twin orbits — the co-orbital channel of gold taleb-09b5.
- Cluster (kinetic 2-D, H0173's scene family): 10⁴ ships, 10 km disc, 10 m
  ships, 50 m/s → 3.18×10⁻² events/body/game-s → 91.7 GB/hour at 10⁶ ships;
  the same fleet dispersed over 10⁴ km → 92 kB/hour. **P4 holds**: H_live
  spans ~9 orders between belt and battle at fixed body count.
- Resonant fraction under a Jupiter analog: 6.8% (crude bound, see below).

## Predictions (`predictions.md`, written before the run)

P2 ✓ (α = 1.079). P4 ✓ (0.0318 > 10⁻²). **P1 ✗ and P3 ✗ at q32** — the
informative failure: I expected distant conjunctions to be sub-quantum, but
deflection ∝ D³ makes 100-km neighbours' 0.05-AU conjunctions exceed q32, and
17% of all conjunctions then scar (6.3×10⁻⁵/s vs predicted <10⁻⁸; 180 GB/h vs
<1 MB). P3's "<1 MB" holds only at contact scale (0.23 MB/h). P5 ✗ marginal:
6.8% vs <5% (the per-MMR width share was a crude sixth of Wisdom's zone).

## What would make it wrong

- The count is an **upper bound**: successive conjunctions with the same
  neighbour are quasi-periodic (r8 v2), so sub-quantum deflections partially
  cancel instead of walking; the true rate at q32 could be far lower, flipping
  that verdict to "fits". The correlation structure on this same event stream
  is the named next run.
- The size law drives everything (rate ∝ ⟨D³⟩): a belt without 100-km bodies
  scars ~10³× less. The game's belt size law is undecided (B18b freezes shape,
  not sizes).
- The cluster number is kinetic theory, not the lattice's measured entropy
  (H0173); rtf and the 8 B/scar width are design choices — rescale linearly.

## Cost of adoption

One constant (the scar quantum, decoupled from the tube's 32-bit regeneration
angle: 32 bits is storage precision, not the distinction threshold) plus an
allocator rule: budget a region's scar memory by n₂D·2b_c·v — the same
dimensionless encounter number that already picks sparse vs dense order. No new
component; `shipmem`'s Form P already stores sparse scars.

## Fit with PRINCIPLES

#3 "Cost follows change and entropy" — H_live is the store's entropy rate.
#6 "Store the generator, not the generated" — measured: what the generator
cannot hold. #33 "An ant cares about a raindrop but the lion does not" — the
same conjunction is a scar for a 1-km body and nothing for a planet; the
quantum is per-scale, not global. #24 the floor is information-theoretic: the
floor moved 10⁶ with one constant, so the constant is the design decision.

## The lens (what it may have missed)

One component, one scene family: the gravitational channel of sparse scenes
only. The player/AI decision channel — the actual wildcard (#5) — is
unmeasured, as is the resonant-diffusion channel (6.8% bounded crudely).
Neighbour effects: measuring the belt alone says nothing about what fleets do
to each other's programs at the phase-neighbour certificate's own scale.
