# Predictions — run 20261007-2344-taleb-6f01

Written BEFORE the decisive sweeps (`cert.py wscan`, `cert.py escan`). Tuned only on
the pilot control (aligned formation, seed 11), which reproduced the gold's domain:
149 contacts, max partner rank 3, 0 misses, brute-force subsample agreement true.

Model behind the numbers: partner rank in a sort ≈ N·(sort-key gap)/(2π).
For mean-anomaly (M) order the key gap between encounter partners is ≈ |Δϖ| (they are at
the same true longitude, so their anomalies differ by the pericentre offset), so
miss_M(D, N) ≈ max(0, 1 − 8π/(N·D)) with D the pericentre-spread extent, k = 4.
For true-longitude (λ) order, static Δϖ is absorbed; the residual is drift within the
window plus the epicyclic wiggle (~2Δe), so λ-miss ≈ 0 while N·(1.5·da·T + 2Δe)/(2π) ≲ k.

## wscan (D-sweep at N=300; Δϖ* = 8π/N = 0.084 rad)

| case | miss_M (pred) | miss_λ (pred) |
|---|---|---|
| D=0.05 | ≈ 0 (< 2%) | ≈ 0 |
| D=0.2 | ≈ 58% | ≈ 0 |
| D=0.5 | ≈ 83% | ≈ 0 |
| D=1.0 | ≈ 92% | ≈ 0 |
| D=π | ≈ 97% | ≈ 0 |
| N=150, D=0.5 | ≈ 66% | ≈ 0 |
| N=600, D=0.5 | ≈ 92% | ≈ 0 |
| wide-belt (da=0.1, D=π) | ≈ 97% (tier invalid here) | ≈ 97% too (no shared orbit; both meaningless) |
| D=0.5, ρ=3e-4 | within ±5 pp of 83% | ≈ 0 |
| D=0.5, ρ=3e-3 | within ±5 pp of 83% | ≈ 0 |

Scaling line: miss_M(D=0.5) linear in 1/N (66/83/92% at N=150/300/600) → allowed extent
D* = 8π/N. At N=10⁶: D* ≈ 2.5×10⁻⁵ rad (~5 arcsec) for zero misses at k=4.

## escan (station-keeping e-vector scatter, e0=3e-4, N=300 unless said)

| case | miss_M (pred) | miss_λ (pred) |
|---|---|---|
| dvec=1e-4 | > 50% (ϖ spread ~±dvec/e0 ≈ ±0.3 rad) | ≈ 0 |
| dvec=1e-3 | ≈ 96–98% (ϖ random) | ≈ 0 |
| dvec=3e-3 | ≈ 96–98% | ≈ 0 |
| e0=0.02, dvec=0.02, N=600 | ≈ 98% | > 10% (first λ cracks: S_λ = N·2Δe/2π ≈ 4–6) |
| e0=0.02, dvec=0.005, N=600 | high | < 2% (S_λ ≈ 1) |
| e0=0.02, dvec=0.02, N=300 | ≈ 97% | < 10% (S_λ ≈ 2; smaller than the N=600 case) |

## Trigger blindness (the silent part)

Across the whole D/dvec sweep at fixed da=1e-4 and N: dn_rel stays ≈ 1.5e-4 (±10%) and
phase density is exactly N/2π, while miss_M goes 0 → ~97%. A trigger built on period
spread or phase density cannot see the breakage. binet_radius grows monotonically
(~5e-5 aligned → ~e-scale at full scatter), so a Binet-cluster trigger does move.

## Held out for the checker

- Fresh seeds: same miss fractions within ±5 pp.
- Other k: miss_M(k) ≈ max(0, 1 − 2πk/(N·D)) while positive.
- The pilot control must stay 0-miss (it is the gold's domain; a miss there voids the
  instrument or the gold).
- Kill criterion for my claim: if miss_M does not track 1 − 8π/(N·D) within ~±10 pp
  across the sweep, or λ-miss is not ≈ 0 on the wscan family, the safety-number law is
  wrong and the run reports that, not the law.
