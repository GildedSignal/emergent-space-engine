# Dossier — run 20261009-1345-system-136a (system lens)

## Claim

The cycle memo's key space and the encounters' Binet cone are one structure: the quantized
(periapsis, k) buckets the engine already keeps (the Catalogue; 11–12 bits per coordinate,
`crates/space` `MEMO_SHAPE_BITS`/`MEMO_SCALE_BITS`) are a conservative candidate tier for the
encounter cone with **zero measured misses** and a **×1.0–1.2 superset** — deleting the encounters
crate's own candidate machinery and per-body element store — and per-pair section caches keyed by
(bucket, bucket, Δϖ-band) amortize the per-element-change setup by **×43–312 at the plane's
unaveraged kick cadence** (and by nothing at the averaged cadence: differential apsidal precession
flips any fine band at ~1/orbit — a boundary I predicted wrongly and report as held-out failed).

## Bottleneck

Board item "candidate work must track real encounters" (the 5 October top scaling risk) and
law.md's open cost from r8 v3: setup at 2.5–24 µs **per candidate pair per element change**. The
unification turns that cost from per-kick to per-cache-invalidation, and deletes the second index
the design was carrying (the crate's `Sorted` U-scan, `cone_pairs`, its `kepler::Body` element
store, and the co-orbital formation's dimensionless-number trigger). Expected gain: order of
magnitude on setup at the plane's cadence (the plane recompiles on ~99% of kicks — it is the
unaveraged regime), zero new per-body bytes (the 16-byte tube already carries the key index).

## Evidence (all from `python3 exp.py`, ~7 s, counts on fixed seeds; `metrics.json`)

**A. Exactness and overhead of the bucket tier** — buckets at relative width 2⁻¹¹ in ln r_p and
ln k (the memo's own granularity); bucket pair allowed iff worst case over the two boxes
(U-interval gap − (R₁max+R₂max) at Δϖ=π) < bucket-wide eps_u (the crate's own `eps_u`,
re-implemented); member pairs then get the exact `is_candidate` predicate:

| workload | n | exact cone pairs | tier-2 pairs | misses | superset | buckets |
|---|---|---|---|---|---|---|
| belt (a∈[0.9,1.1], Rayleigh e σ=0.1) | 4096 | 7,244,639 | 8,143,566 | **0** | ×1.12 | 4043 (1.01/bkt) |
| belt64 (a on 64 keys) | 4096 | 7,205,089 | 8,130,368 | **0** | ×1.13 | 3922 |
| formation (one orbit) | 512 | 130,816 (= C(512,2)) | 130,816 | **0** | ×1.0 | **1** |
| corners (bucket-corner pairs straddling cone_gap−eps_u = 0 at ±eps/2) | 1200 | 555,184 | 654,952 | **0** | ×1.18 | 792 |

The formation is the co-orbital gold's adversarial case (20261006-0346: window tier dropped 4–6%
of contacts, setup went quadratic): here it is **one bucket, all pairs tier-2, zero misses, no
trigger** — the bucket is the formation detector, and the phase-rank certificate works inside it
(timing, not geometry). Envelope instrument: `env_ok` true everywhere (after a last-ulp
conservative pad; before the pad the "violations" were 2e-16 roundoff).

**B. Cache residence under secular drift** (Jupiter analog μ=10⁻³, circular, a_j=2.08; free
apsidal precession + forced e; a fixed secularly):

- absolute dϖ = 4.0×10⁻³ rad/orbit; **differential dΔϖ = 1.8×10⁻⁴ rad/orbit = 4.4% of absolute**
  (median over the belt's exact candidate pairs);
- residence per candidate pair: Δϖ-band 2.4×10⁻⁴ → **1 orbit**; Δϖ-band 1.5×10⁻² → **84 orbits**;
  radial (k, r_p) buckets → **1,243 orbits** (the e-oscillation; a-drift is 0 secular);
- resonant adversarial (r4 v3's 2:1 pump, de/orbit = 5×10⁻⁵): k-residence **10 orbits**;
- savings vs per-kick section re-set (invalidations vs kicks, per pair per orbit): averaged
  cadence (0.3 kicks/orbit) **×0** at the fine band, ×25 at the 1.5×10⁻² band; unaveraged
  (32/orbit) **×43** / ×2705; resonant: ×312 unaveraged, ×3 averaged.

The plane is unaveraged (it recompiles on ~99% of distinct kicks), so the measured ×43–312 is the
regime it flies in; the averaged path (stable hierarchical orbits) gains nothing at fine bands and
its wide-band gain is conditional (below).

## Predictions (`predictions.md`, written before the run)

Held: P1 (zero misses on all four workloads incl. boundary-straddlers), P2 (superset ≤ 8×,
measured ≤ 1.2×), P5's unaveraged half (×312 ≥ 100 at the resonant pump), P6 (formation: one
bucket, zero invalidations absent drift). **Failed, and reported as failed:** P3's "differential
precession ≤ 1% of absolute, band residence ≥ 50 orbits" — it is 4.4% and 1 orbit. The reason:
apsidal precession varies at first order in a, and the cone admits pairs with Δa/a up to ~10% at
belt e (their radial ranges overlap), so candidate pairs are not nearly-identical orbits. P4's
"≥ 6× at the averaged cadence" failed with it. This failure is the useful boundary: **fine-grained
section caching buys nothing at the averaged cadence; only the wide band does, and only if the
sections' safety margin absorbs a 1.5×10⁻² rad rotation** — unmeasured, the named next experiment.

## What would make it wrong

1. The shipped quantizer is fixed-point chop (MemoCode: 11-bit gap + 6-bit exponent), my grid is
   the log-grid of the same relative width; if the shipped buckets' envelopes are not conservative
   under their exact chop rule, misses could appear (re-check with `crates/space`'s own quantizer).
2. The Δϖ-band width the windows tolerate: the linear window is ~ρ wide, so the absorbable
   rotation may be ~10⁻⁴ rad, not 1.5×10⁻² — then the averaged-cadence gain is zero and only the
   unaveraged ×43 stands. Must be measured on the crate's `sections()` with drifted ϖ.
3. Everything is planar (the crate and the plane are 2-D). Inclination adds a second Binet angle;
   the identity survives but the ϖ-neighbour structure becomes a 2-torus and is unmeasured.
4. Drift rates are Newtonian-secular orders for a Jupiter analog in belt units; the game's
   weak-field scenes (sep 5.27×10⁸ M) precess far less, which only widens residence.

## Cost of adopting, and fit with PRINCIPLES

Adoption is one step on the plane's seams (plane.md §6 already reserves the encounters interface):
the candidate index becomes the Catalogue's key adjacency (occupied keys + their Binet envelopes,
one small record per occupied key), the crate's `Sorted`/`cone_pairs`/element-store are deleted,
`dioph.rs` timing is kept per kick, `sections()` gains a (bucket, bucket, Δϖ-band) cache. Zero new
per-body state. Risk: the band-width question above; mitigate by keeping the per-kick timing
recompute unconditional (it is exact integers) so a too-wide band can only cost, never miss.
PRINCIPLES: "there are many kinds of symmetries… under the right representation many symmetries
can appear" (32) — the symmetry the cone found is the memo's compression, one space for both;
"the cheapest compute is compute not done" (1) — the second index is not built at all;
"we know we have a fish, we need to find its water" — the water was Binet space, for storage and
discovery alike.

## The lens (what it may have made me miss)

The whole-system lens went looking for one unification and may over-trust it: the identity is
proven only at the tier boundary (candidates, misses), not through the crate's full pipeline
(sections → Diophantine → checks) on the evolved belt; the ×43–312 are drift counts, not
wall-clock sections recomputes. Elegant unifications hide a hard special case — here it is the
**eccentric, differentially-precessing pair** (large Δa overlap, fast Δϖ drift), which is exactly
the case my failed prediction P3 exposed. A second blind spot: hierarchy — bodies in different
dolls never meet, but handoffs move tubes between catalogues; the bucket tier must be rebuilt per
doll at handoff, unmeasured here.
