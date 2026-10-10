# Predictions — inverting the co-orbital certificate premise (run 20261010-1706-inversion-3775)

Question: gold 20261006-0346 says concentration = a fleet in formation: "every real encounter lies
within partner rank 4 along the orbit"; fix = phase-neighbour certificate O(n·k), triggered by a
dimensionless concentration number; build brief `lab/lenses/b-coorbital-cert.md` (queued, unbuilt).
The untested scene: the **breakup cloud** — one event, N fragments, one point P. Every collision,
wreck and battle produces these by default; the game's own dynamics seed them.

Derived before any run (coplanar Kepler, μ=1, breakup at P=(r0, θP), Binet point
(U,V,W)=(1/p, e·cosϖ/p, e·sinϖ/p)). v1 of this file had d_min ≈ v_rel·Δt and "rank size grows
with N"; working out the exact two-crossing truth machinery corrected both before the decisive
run. The corrections are part of the result (noted inline).

- **D1 (null plane — unchanged).** An orbit through P satisfies r0·(U + V cosθP + W sinθP) = 1.
  The plane's normal (1, cosθP, sinθP) is null in the cone metric. By Cauchy–Schwarz every pair on
  the plane has ΔU² ≤ ΔV² + ΔW²: *every* fragment pair passes the Binet cone. In fact the cone
  condition is literally the crossing condition (two orbits cross iff their radii agree at some
  sky angle θ: (ΔV)cosθ + (ΔW)sinθ = ΔU has a solution iff ΔU² ≤ ΔV²+ΔW²). So the tier built to
  remove the N² candidate set retains ~100% of it, permanently: orbits do not decay, and every
  kick re-set of any fragment's candidates stays O(N).
- **D2 (trigger blindness — unchanged).** A breakup with dispersion σv has σ_a/a ≈ 2σv/v0 —
  belt-like element spread, not a point. An element-space concentration number classifies the aged
  cloud as diffuse while its candidate set is still 100%. A per-body cone-probe (fraction of K
  random others inside one's cone) does separate the cloud (~1) from a belt (small).
- **D3 (corrected: churn, not rank size).** At a co-passage through P both bodies transit the
  same point at ~v0 (relative direction change ~σv/v0), so miss distance d_min ≈ v0·|Δt|
  (exactly d_min = |Δt|·|v_i×v_j|/|v_i−v_j| ≤ v0|Δt|). The timing window is therefore b/v0 for
  every pair — no slow tail. Encounter partners at conjunction are λ-adjacent (only bodies
  physically near P can be λ-near θP), so *rank size stays small at all N*. What breaks is
  **cadence**: the λ-order at θP turns over at the passage rate N/T, so the partner set is fully
  replaced every ~4k/N of an orbit. A formation's λ-order is invariant forever (equal periods);
  the cloud's is stale after a fraction of 1% of an orbit. The certificate as specified (one
  O(n·k) pass, partners = static phase neighbours) either misses or must re-sort ~N/4k times per
  orbit.
- **D4 (corrected: two foci).** Every crossing pair has a second crossing point Q_ij (the second
  root of the same equation), and its conjunction timing is uniformly random, so encounters split
  ~50/50 between the shared focus P (one point for all N² pairs → one epoch-stream sort covers
  it, O(N log N) per orbit, work per at-P encounter ≈ 2τc/τb constant in N) and per-pair foci
  Q_ij (no shared structure → per-pair timing work on 100% of pairs, the exact quadratic the
  design's continued-fraction tier pays on the full candidate set).

Held-out predictions for the decisive run (N=300/1000/4000, σv/v0=1e-3, b/r0=1e-4, mixed ages
4–256 orbits; formation (train lattice) and Rayleigh-belt controls on both sides):

- **P1.** Cloud cone retention > 99% of pairs; belt < 10%. (Belt at ~100% voids my reading.)
- **P2.** Cloud Binet points fit the null plane to < 1e-12 relative residual.
- **P3.** At per-orbit evaluation cadence (the belt tier's cadence), λ-rank-4 miss fraction on
  true cloud encounters > 80%, and λ-sort refreshes needed per orbit to keep rank-k valid grow
  like N/(4k); formation control: zero misses at the same cadence. Partner λ-rank at conjunction
  time itself stays ≤ ~8 even at N=4000 (adjacency real; churn is the killer).
- **P4.** Co-arrival certificate at P (sort the passage-epoch stream, window 3b/v0): zero at-P
  misses at every N, work per at-P encounter ≈ window/encounter ratio, flat in N (within ~2×
  between N=300 and N=4000).
- **P5.** Aged cloud element spread (σ_a/a, mean e, ϖ resultant) within ~3× of the belt's and
  ≫ the formation's; per-body cone-probe retention ~1 for cloud, belt-like small for belt.
- **P6.** At-Q_ij encounter count within a factor 2 of the at-P count (measured on a random pair
  subsample, extrapolated with its CI) → per-pair tier work stays Ω(N²) per breakup no matter
  what the at-P certificate does.
- **P7 (validation, not held out).** The analytic d_min formula agrees with direct Kepler
  propagation to < 5% on sampled true encounters (curvature over the b-window is second order).

Kill criterion for the inversion: if cloud encounters at mixed age DO lie within λ-rank 4 at the
per-orbit cadence (churn irrelevant), or the belt control retains ~100%, or at-Q encounters are
< 10% of at-P, the gold's premise survives this scene and the dossier reports a negative result.
