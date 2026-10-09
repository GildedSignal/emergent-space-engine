# Predictions — run 20261009-1345-system-136a (system lens)

Written before the decisive experiment. The claim under test: the cycle memo's key space
(quantized (periapsis, k), 11–12 bits per coordinate — `crates/space` `MEMO_SHAPE_BITS`/`MEMO_SCALE_BITS`)
is the encounters' Binet-cone candidate space, so the Catalogue the engine already keeps is the
candidate index, and per-pair section caches keyed by (bucket_i, bucket_j, Δϖ-band) amortize the
per-element-change setup (r8 v3's open cost, 2.5–24 µs per candidate pair per element change).

Held-out cases (not tuned on):

- **P1 misses (exactness).** On belt-0-like (n=4096, a∈[0.9,1.1], Rayleigh e σ=0.1), a keys=64 belt,
  a 512-ship formation on one orbit, and adversarial pairs placed at bucket corners with
  cone_gap − eps_u straddling the candidate boundary (−eps/2, 0, +eps/2), the bucket-envelope tier
  contains **100%** of the exact cone candidates. Any miss > 0 kills the unification's safety.
- **P2 overhead (superset factor).** Bucket-tier pass-through over the exact set: **≤ 8×** on the
  smooth belt, **≤ 3×** on the formation (one bucket by construction). If > 20×, tier-2 work
  explodes and the grouping buys nothing.
- **P3 residence under secular drift.** With a Jupiter-analog (μ=1e-3, circular, a_j = 2.08) over a
  belt at a≈1: absolute apsidal precession ~1e-3 rad/orbit (order), but candidate pairs are
  radially close, so **differential** dΔϖ/orbit is second order: ≤ 1% of absolute. Δϖ-band residence
  at a 2.4e-4 band: **≥ 50 orbits** per candidate pair. Radial (k, r_p) bucket residence: **≥ 20
  orbits** at belt e (the binding radial term is the forced-e oscillation, not a-drift, which is 0
  secular).
- **P4 setup amortization.** Re-sets of per-pair sections drop from kick cadence (0.3/orbit
  averaged, 32/orbit unaveraged, H0190) to ≤ 0.05/orbit on the belt: savings **≥ 6×** at the
  averaged cadence and **≥ 100×** at the unaveraged cadence.
- **P5 adversarial resonant drift.** At r4 v3's 2:1 pump scale (de/orbit ≈ 5e-5), k-bucket residence
  falls to ≈ 5–10 orbits: savings **≥ 100×** unaveraged but only **~2–3×** averaged. I expect this
  to be the honest shrink case; near resonance averaging is dead anyway (r4 v2), so the unaveraged
  number is the one that applies there.
- **P6 formation.** A formation shares one memo key exactly: **zero** cache invalidations absent
  drift (infinite residence).

What would make the claim wrong: any miss in P1; overhead > 20× in P2; differential precession NOT
second-order (then Δϖ bands flip faster than kicks and the averaged-cadence win disappears).
