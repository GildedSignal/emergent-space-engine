# Predictions (written before the decisive runs)

Pilot (tuning) runs: none beyond the original run's numbers (this second author runs its first
real case only after this file). The instrument: `spacex_probe [cohort] [seed] [ticks] [threads]
[place]`, with `ESPACEX_PREFILTER` (the annulus pre-filter) and `ESPACEX_FASTDOLL` (the clone-free
doll test) as A/B switches; `place` 0 = star-doll belt (the original), 1 = home-doll belt at
alt 1.5–1.7 Home radii (separated annulus), 2 = home-doll belt at alt 1.08–1.12 (co-radial with
the player, the adversarial dense case the original never grew), 3 = home-doll belt with
e ∈ [0.05, 0.3] (wide annuli).

**Q1 — Safety (the invariant).** On every placement × seed {7, 42, 2026}, cohort 200, threads 1,
3e10 ticks: with `ESPACEX_PREFILTER` (and `ESPACEX_FASTDOLL`) on vs off, the universe digest, the
encounter count and the contact count are identical, and `PAIRS_SAME − PAIRS_REJECTED` (survivors)
≥ 0 everywhere. Any mismatch kills the pre-filter as unsafe.

**Q2 — Separated annulus (place 1).** The pre-filter rejects ≥ 99% of same-doll pairs, and the
player's scan µs/item drops ≥ 10× vs filter-off at the same cohort (the exact tier is deleted;
what remains is the clone + ~10 Scalar ops per pair). Per-pair exact cost for cohort-class tubes
(small compiled entries) is 0.5–4 µs — cheaper than the original ~4 µs average, which the moon's
big tube inflated.

**Q3 — Co-radial dense (place 2, the adversarial case).** The pre-filter rejects < 10% (the belt
brackets the player's own radius; the annuli overlap, and no radial test can separate them), and
the scan µs/item changes by < 1.2×: **the pre-filter fails here, by construction of the case.**
If instead it rejects > 90% here, my understanding of the geometry is wrong and that is a finding.

**Q4 — Wide annuli (place 3).** Rejection 10–60% (the player's |x| is inside the wide annuli for
part of each orbit); zero misses still required.

**Q5 — The foreign-doll slope (place 0, cohort 2000).** `ESPACEX_FASTDOLL` alone cuts the scan
µs/item by ≥ 3× at cohort 2000 (the 33 ns/body clone deleted, a field read left) with identical
digests. The original dossier's 33 ms/item at 10⁶ becomes ≈ 3 ms/item before any same-doll work.

**Q6 — The wall, stated honestly.** In place 2 the exact per-pair decode is the surviving cost at
~0.5–4 µs × same-doll population per player item; the scan seam cannot delete it by any per-pair
filter that refuses to decode, because the rejection information (phase at t) lives inside the
decode. The deletion belongs to the encounters seam (phase-neighbour certificates), not the scan.
