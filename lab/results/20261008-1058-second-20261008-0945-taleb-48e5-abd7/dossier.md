# Dossier — 20261008-1058-second-…-abd7 (second author on 20261008-0945-taleb-48e5)

## Claim

The silver's radial result stands and is now **radius-flat in per-doll units**: candidate work per
real encounter is `cpe ≈ 1.2–1.3·a^2.53/ρ` (hit-weighted; the silver's 2.6 was an unweighted-fit
overstatement), the a-exponent decomposes exactly as **a^1.5 local clock × a^1.0 relative-ρ**
(degree cancels in cpe by construction — not "degree growth"), so carrying **ρ ∝ a and per-doll
(local-orbit) time** makes work per encounter radius-flat with measured residual exponent
**0.000 over a 100× scale ladder** — an exact self-similarity of the shipped cone/sections
machinery, not a bound. The record regenerates from shipped code except `CE.jsonl`'s per-bin degree
columns (the author's disclosed pre-fix artifact, left stale; belt-level fields are bit-identical),
and the three misreported numbers are corrected below.

## Bottleneck

The board's top scaling risk (candidate work must track real encounters) — radial axis, and the
checker's named experiment: the per-doll accounting that makes work per encounter radius-flat.
Deletes: any per-radius special-casing in the encounters build, and sizing the allocator's worst
cell from maxima rather than ⟨deg⟩·2–4 with the e-cap known.

## Evidence

Commands in `run-log.txt`; binary `$T = $(cargo metadata …)/release/encounters` after
`git apply work/author-patch.diff && git apply work/second-patch.diff` (second patch adds `doll`,
exposes the e-cap; `cusp` output verified unchanged). Belts 5–8 s, rings 3 s, γ=−3 ladder 8 s/belt.

1. **Record regenerates.** A2 grid, ring, ρ-control: bit-for-bit (all fields, ex `wall_s`).
   `CE.jsonl` (N-ladder): `pairs`, `scanned`, `scanned_per_body`, all degree stats bit-for-bit;
   the per-bin `deg` columns alone differ — they are the flat pre-fix artifact the author
   disclosed (the shipped patch gives rising bins); regenerated as `data/CE-fixed.jsonl`
   (only `bins` differs in every line). The checker's "exactly" held only for the fields it used.
2. **Misreports corrected** (from the silver's own data): `deg_of_emax/deg_max` = **0.42–1.00**
   (inner cusps 0.42/0.43), not "0.59–1.0"; scanned/body N-exponent = **1.00–1.05** (0.998–1.050),
   not "1.05–1.15"; inner cusps sit **0.75–1.44 around the γ=0 law (mean 1.15–1.18, i.e. slightly
   above)**, all profiles incl. ring within 0.75–1.47 — "±40% of one law", not "1.1–1.4× below".
3. **The named experiment (`doll`, `data/doll-all.jsonl`).** Scaled belts (a,ρ,t)→(s·a, s·ρ,
   s^1.5·t), same N/seed/profile, horizon 500 local orbits at a=s, 8 sampled bodies/bin:
   - γ=0, s ∈ {1, 3.16, 10, 31.6, 100}: degree stats **bit-identical** across s (f = 0.1040);
     hits-weighted `cpe_perloc = cpe/a^1.5` geomean 9919.5→9922.3 (+0.03%); **ladder exponent
     0.0001**; every matched-bin exponent 0.000; hits 5564 vs 5563 (one encounter in 5.6k —
     tick rounding).
   - Ring (deg ≈ N): exponent −0.0000, deg stats and hits identical across s = 1…100.
   - **γ=−3 cusp, the checker's own attack profile: per-local-orbit ratio 1.0000** — its 27×
     at fixed clock was entirely the a^1.5 clock.
   - Within one belt at absolute ρ: raw cpe exponent **2.530** (hit-weighted), `cpe_perloc`
     exponent **1.030** — that 1.0 is the ρ/a term itself, which the per-doll transform removes
     across dolls. Prefactor 1.17–1.30 ≈ the silver's 1.2.
   - Mechanism: cpe = deg/(deg·per-pair rate) — degree cancels identically; per-pair rate ≈
     ρ·n/a (synodic Δa·a^−2.5 × P(hit|conjunction) ∝ ρ/Δa). Evidence beyond the construction:
     γ=−3's degree falls 9.2× outward while its cpe still rises ≈ a^2.0; γ=+3's rises 8.6× with
     cpe ≈ a^2.42 — opposite degree gradients, same law within ±40%. This corrects the checker's
     "1.0 is degree growth (a per-doll population question)": it is the relative-ρ term.
4. **e-cap probe** (`data/ecap.jsonl`, σ_e 0.3): cap 0.5 → max/mean 1.49, f = 0.464 (matches the
   checker's 1.5); cap 0.9 → max/mean **1.84**, f = 0.544, p99 ≈ N−1 (the 1.1% of bodies with
   e ∈ (0.5, 0.9] each see nearly everyone). Still Mediocristan; hot populations push f up, not
   the tail ratio.

## Predictions (`predictions.md`, written before the decisive runs)

Held: P1 (0.00% drift — bit-identical, stronger than the <2% I allowed), P2 (|β| = 0.0001 ≤ 0.1;
the checker's 0.14 alternative refuted), P4 (ring flat; ±0.3% not ±25%), P5 (1.84 ≤ 10).
**Wrong, reported as wrong: P3** — I predicted within-belt `cpe_perloc` exponent 0.0–0.15, measured
1.030. Cause: a single belt at absolute ρ cannot have ρ ∝ a; the within-belt 1.03 *is* the
relative-ρ term, measurable only there, while the per-doll residual is only defined across dolls
(ladder: 0.000). The miss was in my prediction's framing, not the mechanism; stating it plainly.

## What would make it wrong

The flatness is structural equivariance (Newtonian Kepler + a cone test with no absolute scale +
dimensionless SAFETY), so it fails only where the integer tick clock's absolute quantum (2^−32
time units) or u64 period overflow binds: period ticks overflow near a ≈ 7×10^5 — the doll domain
has a hard outer edge far beyond game scales. Population is still Newtonian, coplanar,
Rayleigh-capped: 3-D widens candidate sets (f is a lower bound), and the f constants are
e-cap-dependent (0.10 → 0.46 → 0.54 measured). Ladder used one seed; equivariance is seed-free and
three profiles (uniform, ring, γ=−3) agree, but the *level* 9922 carries that seed's Poisson noise
(±1% at 5.6k hits). The checker's heavier alternative (relative ρ + per-doll clocks wired into the
two-tier certificate at 10^6) was not run — the scaled-belt ladder is the cheapest decisive part,
per my brief.

## Cost of adoption, and fit with PRINCIPLES

Design note for the encounters build, no code: carry ρ per-doll (ρ ∝ a) **and** charge setup in
local-orbit time; then work per encounter is radius-flat by symmetry and the allocator needs no
radial balancing; budget the worst cell as ⟨deg⟩·2–4 from the e-cap; f·N per kick (f = 0.10–0.54 by
temperature) remains the number the slack skin must beat. "Symmetry is found, not given" (32): the
(a, ρ, t) equivariance was always there — absolute ρ and the a=1 clock were hiding it; "regimes are
chosen by dimensionless numbers" (4): the number is ρ/a; "each scale resolves only what matters at
that scale" (33). The cheapest compute is compute not done (1): radius-flat deletes per-radius
cases outright.

## The lens

The second-author lens did the named experiment exactly and little else; it nearly missed two
things. A mid-job binary swap forced a field-level diff, which is the only reason the stale CE bin
columns surfaced (a checker that compares only the numbers it cites will pass them again). And my
own P3 prediction conflated within-belt and across-doll residuals — caught only because I computed
the within-belt fit before writing the dossier. Blind spot as declared: no 10^6-scale wiring, one
ladder seed, and the e-cap probe caps at 0.9 because e ≥ 1 leaves the crate's elliptic Kepler.
