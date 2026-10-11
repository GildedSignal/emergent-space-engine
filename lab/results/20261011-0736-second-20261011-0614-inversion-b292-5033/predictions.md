# Predictions — second-author run on 20261011-0614-inversion-b292 (written before the fixed-instrument runs)

The checker (silver verdict) named the one experiment: the λ̄-rank instrument sorted raw
`mean_anomaly(t) + pom`, which spans more than 2π once ϖ is spread (mean_anomaly wraps to
[0, TAU), kepler.rs:73–76), so cross-block pairs' circular ranks were inflated. The fix is
modular ordering: `(m + pom).rem_euclid(TAU)` before `circ_rank`. Provenance honesty: the
checker's check.md already publishes corrected values for five scenes; my predictions below
are what the *fixed shipped instrument* must produce for the claim's record to be clean —
if my fixed instrument disagrees with them, either my fix or the checker's is wrong, and
that is itself a finding. Predictions for the scenes the checker did NOT correct (w1b, w1c,
c0b, e10b, and the new aspread/n1k/e5 geometry) are mine alone.

## P1 — the control is clean (c0, the gold's adj scene)

Modular λ̄-rank identical to the raw one: max 28, p50 ~9, p90 16, 61.1% > 4; enc 234,
k̂ 50.6, fracQ 0.254, method missed 5/234. Rationale: ϖ span 0.1 rad, so the raw range
exceeds 2π by only 0.1 and the duplicate zone holds at most the few members with mean
anomaly near the wrap; the checker measured raw = mod here. The headline claim (rank 28,
61% > 4 *in the gold's own scene*, no knob changed) is untouched by the bug.

## P2 — ϖ-spread scenes corrected (w1, w1b, w1c)

w1: λ̄-mod max 59 (raw 99), p90 32 (raw 92), >4 fraction 90.4% (raw 88.1%); distance-rank
stays ≤ 4. The "circular maximum (99 of 200) once apsides are spread" headline is FALSE for
ϖ-spread alone; the true max is ~30% of the cap. The worst-pair "diametrically opposite
(rank 99)" narrative is likewise false; the true worst w1 pair has λ̄-mod rank 59.
w1b/w1c (seeds 40/41, not corrected by the checker): I predict λ̄-mod max in 50–75,
>4 fraction 85–95% — the qualitative claim (apsidal spread alone defeats a ±4 watch)
survives on every seed.

## P3 — e-spread scenes corrected (e3, e10, e10b)

e3: λ̄-mod max 98, p90 82, 100% > 4 (raw 99/83/98%); e10: 98/94/100% (raw 99/86/100%).
Here the circular maximum IS genuinely reached (98 ≈ cap 99) — the correction does not
rescue the watch; it sharpened ϖ-spread and confirmed e-spread.

## P4 — s5 and d30 corrected

s5: λ̄-mod max 39, p90 27, 90.5% > 4 (raw 99/86/88%); d30: max 98, p90 92, 100% > 4
(raw 94/80/100%). k̂ numbers are untouched by the fix (the closed-form watch admission
already used modular wrap): k̂ 50.6 (c0/w1), 127.5 (e3), 195.3 (e10), 36.0 (s5), 198.7 (d30).

## P5 — seed-robustness of the control refutation (c0b = control geometry, seed 40)

enc ≈ 235, λ̄-mod max ≈ 44, p90 ≈ 26, ≈ 76% > 4: the control-scene refutation
(rank ≫ 4 with no knob changed) is not a seed-27 artifact.

## P6 — density kills the gold's own metric (n1k = control geometry, nc 1000)

The gold's distance-rank metric reaches max ≈ 10 and true-longitude rank ≈ 11 (vs 3 and 4
at nc 200): rank scales with local density, so k = 4 was never scale-free even on the gold's
own instrument. λ̄-mod max ≈ 218, ≈ 94% > 4; k̂/n_c ≈ 0.29 (scale-free, so the 3.6 GB
correction for the 10⁶ fleet stands). This closes the "watch k nearest by distance" door
the original dossier only asserted.

## P7 — a-spread makes the watch costlier, not kinder (aspread: a_hw 1e-3, ϖ π)

k̂/n_c ≈ 0.38 vs 0.25 in the control — the direction the original dossier guessed
("may be kinder") is wrong; differential drift widens the λ̄ window family's reach.
λ̄-mod max ≈ 64, ≈ 89% > 4.

## P8 — window soundness extends to e = 0.5 (e5: σ_e 5e-2, cap 0.5)

Exact-amplitude and 2-term windows both remain sound (max violation < 0; checker measured
−3.9e-3 / −6.9e-3), extending the soundness claim beyond the e ≈ 0.3 cap of d30.
λ̄-mod max ≈ 96, 100% > 4.

## P9 — the record regenerates

(a) Every stored original JSON line (incl. the previously missing c0) regenerates
byte-identically from the original instrument — verified for c0, w1, d30 here before
these predictions; the checker verified all eight.
(b) The fixed instrument reproduces the raw (buggy) λ̄ column byte-identically in a
side-by-side `lbar` field while adding the corrected `lbar_mod` field, so the shipped
record is self-auditing: one line carries both the contaminated and the corrected number.

## Kill criterion for the claim

If modular λ̄-rank in the control c0 drops to ≤ 4 (i.e. the bug manufactured the whole
control-scene refutation), the original run's thesis dies and this dossier reports the
gold's rank-4 premise as restored at 61%→0. The checker's values say it will not (28/61%
stand), but this run must show it from shipped code.
