# Dossier — 20261008-0945-taleb-48e5 (Taleb lens): radial concentration vs the candidate tier

## Claim

Radial concentration does **not** break the encounters tier: across uniform belts, 100–1000×
density cusps (either edge) and a dense ring, per-body candidate work per real encounter
follows one profile-independent law **cpe ≈ 1.2·a^2.6/ρ** (candidates per encounter), the
degree tail is Mediocristan (**max/mean ≤ 3.9**, set by the Rayleigh e-tail, N-linear), and
the mean does not lie — but the law's a^2.6 says **outer belts overpay ~100× per encounter
at fixed absolute ρ**, so ρ must be carried as a relative (per-doll) quantity, and per-kick
setup is f·N pairs (f = 0.10–1.0 measured), the number the slack skin must absorb.

## Bottleneck

Board's top scaling risk ("candidate pairs per body grow with N; candidate work must track
real encounters") and risk "candidate work at scale". The untested axis was *density
contrast in radius* (the silvers tested fixed density; the 6 Oct gold tested phase
concentration). Taleb angle: find the workload where the mean per-body cost lies and the
worst cell ruins the allocator. Answer: no such workload exists along the radial axis; the
fragility is elsewhere (radius itself, and f·N per kick).

## Evidence

Harness: `crates/encounters` extended with `make_cusp` (dN/da ∝ a^γ belts; note γ>0
concentrates toward a_hi, γ<0 toward a_lo) and a `cusp` experiment: exact cone-test
per-body candidate degree for all bodies, plus real encounters by the crate's exact
per-pair checks over 500 orbits for 2 sampled bodies per radial bin. All runs ≤ 90 s,
JSON in `data/`.

Reproduce (from the repo root, after the run's patch or the commands below):
```
cargo build --release -p emergent-encounters
$CARGO_TARGET_DIR/release/encounters cusp 30000 0.05 1e-4 0.3 3.0 500 1 0 1 3 -2 -3   # profiles + truth
$CARGO_TARGET_DIR/release/encounters cusp 10000 0.05 1e-4 1.0 1.01 100 1 0            # dense ring
$CARGO_TARGET_DIR/release/encounters cusp 10000 0.05 1e-4 0.3 3.0 0 0 0 2             # N-ladder (also 30000, 100000; and gamma 0)
$CARGO_TARGET_DIR/release/encounters cusp 30000 0.05 1e-3 0.3 3.0 500 1 0             # rho control
```

1. **Tracking survives every radial profile.** cand_per_enc per radial bin fits
   a^2.32–2.69 for γ ∈ {0,1,3} (outer pile-up), γ ∈ {−2,−3} (inner cusp, 100×/1000×
   contrast), and the ring sits 1.2–1.5× above the same law at its a. Cusps run 1.1–1.4×
   *below* the law (denser ⇒ slightly better tracking). No sterile bin anywhere (max cpe
   2.2e5 ≪ my 1e7 kill line). At ρ=1e-3 every bin drops to 0.08–0.12× of its ρ=1e-4
   value: cpe ∝ 1/ρ, the encounter-cross-section mechanism, giving
   **cpe ≈ 1.2·a^2.6/ρ** (σ_e-dependence weak: 0.05→0.15 changes cpe 1.25×).
2. **The degree tail is Mediocristan.** max/mean = 3.9 (γ=0), 2.6 (γ=+3), 3.8 (γ=−2),
   3.3 (γ=−3), 1.0 (ring). The max-degree body is always a top-eccentricity body
   (deg_of_emax / deg_max = 0.59–1.0): the worst cell = Rayleigh e-tail (capped 0.5) at
   local density — budgetable from the e-cap, not a black swan.
3. **N-scaling is linear where it should be, quadratic where feared.** At fixed profile
   γ=0 and γ=2: deg_mean and deg_max ∝ N^0.99–1.05 (10k→100k). scanned/body grows as
   N^1.05–1.15, i.e. the U-scan is O(N²) total (0.34–0.48·N per body scanned) — the
   standing scan risk, now with constants.
4. **Per-kick setup = f·N pairs.** Candidate degree is a fixed fraction of N set by the
   belt's eccentricity spread: f = 0.10 (γ=0, decade-wide, σ_e 0.05), 0.23 (γ=+2), 0.16
   (γ=−3), 0.41 (σ_e 0.15), 1.00 (ring). One kick in a 10⁹ belt re-certifies ~10⁸ pairs
   unless the slack certificate absorbs it — quantifies why components-4643's deferral
   kill left the slack skin as the only lever.

## Predictions (predictions.md, written before the decisive runs)

- Held: P1 (cpe smooth, 10–100× outward rise; max/mean 3–8), P3 (e-driven max),
  P4 (linear deg_max in N; N² scan), P5 (ring: deg≈N, cpe within 3× of the same-a
  uniform, per-kick O(N)).
- Wrong, reported as wrong: P2's "deg_max/mean 10–30 at γ=3" (measured 2.6–3.9 — the
  mean does not lie along this axis) and its "tracking improves with density" as a
  strong effect (≤1.4×, second order).
- Disclosed error caught mid-run: my γ was inverted versus the doc comment (γ>0 piles
  at a_hi); the decisive grid was rerun with true inner cusps (γ=−2,−3). A first
  version of the bin table averaged degree over generation order (flat, artifact);
  fixed before any conclusion was drawn; the pairs/hits columns were always correct.

## What would make it wrong

The truth side samples 2 bodies per bin; cpe per bin carries Poisson noise (worst bin:
19 hits, ±23%). Bodies are Newtonian coplanar with Rayleigh e capped 0.5 and ρ absolute
— if the real belt is hot (e ~ 0.5 everywhere) or ρ is already relative in the engine,
the f constants change (f grows with σ_e: 0.10→0.41 measured) though the cpe ∝ a^2.6/ρ
law's mechanism does not. A 3-D (inclined) population can only widen crossing sets, so
f is a lower bound there. The scan constants are x86; the M1 re-measures.

## Cost of adoption, and fit with PRINCIPLES

Adoption is a design note for the encounters build (b-encounter-skin, b-coorbital-cert),
not code: (i) carry ρ relative to the doll (ρ ∝ a or per-doll quantum) so work per
encounter is radius-flat — principle 32 ("symmetry is found, not given": U-space is
scale-free, ρ was the asymmetry) and 33 (each scale resolves what matters at it);
(ii) budget the worst cell as ⟨deg⟩·2–4 with the e-cap known — no need to size by
maxima; (iii) f·N per kick is the number the slack skin must beat at 10⁹. "no
categories: regimes are chosen by dimensionless numbers" (4): the regime number is
a·⟨e⟩/ρ versus the cpe law, not density contrast. Deleting: any per-profile special
case (ring/cusp certificates) is unjustified — measured.

## The lens

Taleb's tail-hunt found no ruin along the radial axis — a real result (the mean does
not lie; Extremistan is absent; the f·N per-kick cost is the bounded worst case). The
lens almost hid the sharper find: the *smooth* a^2.6/ρ law is a representation defect
(ρ absolute in a scale-free space), which is a Feynman/representation observation, not
a tail observation. Blind spot as declared: "it says nothing about how to build fast."
