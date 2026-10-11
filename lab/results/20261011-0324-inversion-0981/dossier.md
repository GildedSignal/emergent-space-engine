# Dossier — 20261011-0324-inversion-0981 (inversion lens)

## Claim

The gold's "every real encounter lies within partner rank 4 along the orbit" is a **density
artifact and a coordinate artifact**: the honest partner count is the ρ-window population
≈ 2ρn/w (linear in fleet size), and at e = 0.7 with pericentre spread the true encounter
partner sits permanently at mean-longitude rank ~n/2 while its true-longitude rank is ≤ 9 —
so the queued `b-coorbital-cert` build, as specified ("partner rank 4"), would drop ~92% of
intra-fleet encounters at n = 2000 (rising toward ~100% at the game's 10⁶-ship fleets) and
~95% on eccentric co-orbital formations, at any refresh cadence.

## Bottleneck

Board item "encounters at N / the co-orbital certificate" (top scaling risk). The gold
20261006-0346-taleb-09b5 replaced the quadratic window tier with an O(n·k) phase-neighbour
certificate at k = 4. Inverted: what is k a function of? If k must grow with n, the
certificate quietly reinstates the quadratic tier it was meant to kill. Gain: the build
spec is corrected **before** the build runs (it is still queued), one step early.

## Evidence

Truth: the crate's `truth_pair` (conservative advancement, Halley states — no shared solver
path with any certificate). Floats explore; the quantities judged (ranks, populations,
missed fractions) are what the certificate would see. All scenes in one run, 57 s wall,
6 threads, < 100 MB, load 1.3/8 vCPU (machine state recorded above).

Reproduce (from this tree, patch applied):

```
cargo run --release -p emergent-encounters --bin inversion   # → run-output.json (57 s)
```

Source: `crates/encounters/src/bin/inversion.rs` (this run's patch; restores with the tree).

**S1 — near-circular fleet** (a = 1 ± 1e-3, e ~ Rayleigh(5e-4), ϖ uniform, λ in a 0.1 rad
window, ρ = 2e-3, 10 orbits; only n grows — the fleet densifies, the game's scaling):

| n | enc/body/orbit | λ-rank at dip p99 (max) | frac rank>4 | **perm-miss rank-4** | perm-miss ρ-window | ρ-window pop (honest k) | rank-4 catchable (orbits) | ρ-window catchable (orbits) |
|---|---|---|---|---|---|---|---|---|
| 125 | 4.2 | 13 (21) | 30% | 30% | 30% | 4 | 0.165 | 0.24 |
| 250 | 8.9 | 26 (41) | 57% | 57% | 32% | 8 | 0.064 | 0.24 |
| 500 | 17.3 | 52 (77) | 73% | 73% | 30% | 17 | 0.027 | 0.24 |
| 1000 | 33.6 | 94 (150) | 85% | 85% | 30% | 33 | 0.015 | 0.25 |
| 2000 | 66.7 | 175 (274) | 92% | 92% | 29% | 65 | 0.0063 | 0.24 |

Laws, as predicted: p99 rank ≈ 0.09n; honest k = window population ≈ 2ρn/w (0.033n;
predicted 5→80, measured 4→65); rank-4 catchable duration ∝ 1/n (26× down for 16× n);
**ρ-window catchable duration is n-invariant** (0.24 orbits at every n). Missed fraction at
64 refreshes/orbit: rank-4 rises 0.43 → 0.96; the ρ-window stays flat (0.30). At the game's
10⁶-ship fleet (w = 0.1, ρ = 2e-3) the honest k ≈ 4×10⁴: "rank 4" was the window population
of the gold's own fleet size, not a law.

**S3 — eccentric co-orbital groups** (e = 0.7 fixed, a = 1 ± 1e-3, ρ = 2e-3, 20 orbits):

| scene | n | encounters | λ-rank p50/p99/max | φ-rank (true longitude) p50/p99/max | λ-sep at dip p50 |
|---|---|---|---|---|---|
| ring (ϖ ± 0.3, λ uniform) | 200 | 714 | 28 / 96 / 104 | 1 / 2 / 3 | 0.44 rad |
| formation (ϖ ± 0.15, λ at apoapsis) | 200 | 5831 | 83 / 197 / 199 | 1 / 5 / 9 | 0.045 rad |

Mean-longitude separation is nearly **constant in time** (equal periods), so 89–95% of real
encounters have a partner that is *never* within λ-rank 4 (nor within the λ-ρ-window:
98%) — no cadence fixes it; it is the wrong coordinate, not a timing problem. True-longitude
rank is ≤ 9 (2.6% above 4) on the same encounters. The mechanism: at a crossing, equal true
longitude maps to mean longitudes differing by ≈ (1 + dM/dφ)·δϖ, amplified up to ~5× near
apoapsis at e = 0.7.

**Residual in S1:** the ρ-window's flat ~30% permanent miss is the orientation channel
(λ-offset at the dip ~ e·δϖ, p50 1.2e-3 vs ρ = 2e-3, from ϖ uniform × σ_e = 5e-4); a
true-longitude window closes it (measured at e = 0.7: φ-rank ≤ 3 on the ring). A mean-
longitude window is safe only for near-circular or ϖ-aligned fleets.

## Predictions

Written before the run (`predictions.md`). P1 held (window population ∝ 2ρn/w, rank-4
duration ∝ 1/n, window duration n-invariant, rank-4 missed fraction rising to 96% at c64 —
stronger than predicted); its "ρ-window missed ~0 at ≥4/orbit" **failed**: 46% at 4/orbit,
30% permanent — the orientation channel, which S3 then isolated and fixed by changing
coordinate. P2 held (rank p99 crosses 4 by n = 500). P3 held (λ-rank p99 = 96 ≫ 10; φ-rank
p99 = 2; the formation's φ p99 = 5 grazed the predicted ≤ 4). P4 (dip duration ≪ 1/64 orbit)
was not measured: the backward-difference rate instrument under-resolved the dip (bogus
3×10⁸ orbits; the clamp fired) — analytic estimate 2ρ/v_rel ≈ 10⁻³ orbits stands as untested.

## What would make it wrong, cost of adoption, fit

Wrong if: the gold's certificate ranks in **true longitude already** (then only the density
axis stands, and it still kills k = 4 at scale); or if the concentration trigger never fires
on dense/eccentric formations (then the two-tier certificate covers them — but the build
spec's test scenes, "the gold run's scenes and a dense ring", include exactly a dense ring,
so the k question is live); or if fleets in the game are capped near the gold's n ( Julien's
words say 10⁶-ship fleets and "billions of entities": no). Cost of adoption: the certificate
watches a **true-longitude ρ-window** (all bodies within angular distance ρ — population
2ρn/w, ~4×10⁴ slots at 10⁶, tracking the physical encounter rate, which is what the board
demands: "candidate work must track real encounters") instead of a fixed rank-k list; the
trigger must additionally gate on ϖ-alignment/e before any mean-longitude shortcut. No
quadratic tier returns: window work per body per refresh is the honest encounter-rate
density, and catchability is n-invariant. Fit: principle 32 ("symmetry is found, not given":
rank was a symmetry of the gold's n, not of the physics); principle 18 (the right
representation: the window in the coordinate the encounter actually constrains);
`avoid stupidity before seeking brilliance` — this run removes a mistake from a spec before
it is built.

## The lens

Inversion attacked the newest gold's silent assumptions (its fleet's density and its
circularity) instead of building the certificate. What it may have missed: the gold run's
actual rank definition (not in this checkout — its branch is not merged here; I tested the
claim as the build spec states it), and the certificate's interaction with the Diophantine
timing layer, which can predict conjunctions from orbit geometry alone and might make the
neighbourhood watch unnecessary for slow lappers — though not for the S3 equal-period case,
where geometry (crossing + arrival times) is the only predictor. One number here is
instrument-broken (tin_phi_w) and reported as such.
