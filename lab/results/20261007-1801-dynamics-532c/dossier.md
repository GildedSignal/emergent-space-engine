# Dossier — 20261007-1801-dynamics-532c (lens: dynamics and attractors)

**Claim.** For coplanar belt pairs the encounter tier is split by one dimensionless
number, the crossing fraction χ_t = Δa/(e₁a₁+e₂a₂): every pair that can physically
encounter has χ_t < 1, and in that whole regime the conjunction longitude advances
with jitter ψ = O((4/3)/χ_t) rad (measured std 1.9–2.5 rad) and conjunction-anchored
distance checks — raw radial or the Öpik perpendicular correction — miss 40–97 % of
true close approaches, so the continued-fraction certificate on the synodic rotation
is valid only in the sparse sub-tier ν = W·ε(R) ≪ 1 (events per orbit per pair),
and the deep-crossing tier (ν ≳ 1, ψ ~ 2π) must be scheduled by a phase-neighbour /
dense mechanism, not by per-pair synodic CF.

**Bottleneck.** Board: "finding encounters without work per orbit or per element
change" and the top scaling risk (candidate work must track real encounters). This
run says where per-pair certificates pay and where they cannot: it sizes the
payment schedule (events per conjunction ε, gap tail, cluster factor, drift
invalidation) rather than the tier's search cost. It also gives the structural cause
of r8 v2's "conjunction-less encounters" (0.5–6 %, 78 % adversarial): the encounter
is not anchored at the longitude conjunction when χ_t ≲ 1; it lives near the fixed
orbit-intersection points, whose timing is a Diophantine condition on the two
arrival-time sequences (a mean-motion commensurability clock), not on the synodic
phase.

**Evidence** (all commands ≤ 30 s, `python3 conjmap.py A|B|C`, numpy only, seeds
fixed in the script; outputs `results_A.json`, `results_B.json`, `results_C.json`,
plus `hit_B.npy`/`pairs_B.npy` for replay):

- **A (full Kepler, 256 pairs × 240 conjunctions × sweep):** conjunction-longitude
  step std ≈ 2.5 rad at χ_t = 0.05–0.5, 1.9 rad at e = 0.4 (theory: the
  equation-of-center wobble amplified by n/|s| ≈ (2/3)a/Δa, i.e. ψ ≲ (4/3)/χ_t,
  wrapped-uniform once χ_t ≲ 0.5). Leak of true window-minimum encounters
  (b_min < R) missed by the conjunction-radial test: 0.54–0.96; missed even by the
  Öpik perpendicular distance evaluated at conjunction: 0.41–0.77, worst at small
  χ_t and small R. The straight-line pass anchored at conjunction mis-sizes the
  true miss by b_min/b̃ with median 0.55–4.1 and p90 up to 100.
- **B (rotation statistics, 1304 crossing pairs, 65 536 conjunctions, R = 0.05a):**
  event fraction per conjunction ε_median = 0.199 (conjunction criterion; 0.40 with
  Öpik), median gap 3 conjunctions, gap CCDF slope −1.44 (−1.83 Öpik) — a heavy
  power-law tail, p99/p50 = 8.7; mean cluster 1.44 conjunctions, P(K ≥ 4) = 3.4 %;
  14 % of pairs are sticky (max cluster ≥ 4) and sticky pairs are 2.4× enriched in
  per-conjunction rotation numbers α/2π near small-denominator rationals p/q, q ≤ 8
  (18.7 % vs 7.8 %) — resonant returns, as suspected in r8 v2's "next".
- **C (element drift, 367 pairs × 16 384 conjunctions):** schedule statistics are
  flat in per-conjunction phase-drift σ up to 10⁻² rad (no mixing crossover —
  ε ≈ 0.2–0.4 windows are far wider than the walk); a frozen-α next-conjunction
  certificate is invalidated with probability ≈ σ^0.56 (4.3 % at 10⁻⁴, 14 % at
  10⁻³, 57 % at 10⁻²), median horizon 1–2 conjunctions at this ε.

**Predictions** (`predictions.md`, written before B and C): P2 held (slope −1.44 in
[1, 2]; p99/p50 = 8.7 against the predicted > 10 — borderline). P3 failed on
magnitude, held on mechanism (K̄ = 1.44 > 1.4 predicted; P(K ≥ 4) = 3.4 % > 2 %;
the small-q resonance attribution was confirmed, 2.4× enrichment). P1 partially
tested: the sweep's crossing condition keeps χ_t ≤ 0.5, so the grazing cells where
r8's 0.5–6 % band lives were never run (the patch that adds them did not apply — a
known defect of this run, the cells are one line in `sweep`); measured leaks are all
large, consistent with P1's direction but its low-e band is unverified. P4 partial:
no crossover was reached (needs σ ~ ε, far above the physical kick drift); the
invalidation exponent in T is untested because horizons collapsed to 1–2
conjunctions at ε ≈ 0.4. Other defects, stated plainly: the "events per orbit
window" statistic in B is broken (W computed from α wrapped mod 2π, so W = 1
always — the printed p50/p99/max = 1 is trivially wrong; correct W =
1/|1−(a₂/a₁)^1.5| ≈ 3–130 for this population, so events per orbit are ν = W·ε,
which is exactly the regime number above); and the first part-A implementation
compared radial differences only (its 60–98 % "leak" output was superseded by the
corrected full-2-D version whose numbers are those quoted).

**What would make it wrong.** The leak and jitter numbers come from equal-e,
coplanar, one-primary pairs with uniform angles; inclined pairs (3-D nodes) and
asymmetric e (χ_t near 1 with e₁ ≪ e₂) change the constants, not the structure, but
that is unchecked. The Öpik-at-conjunction failure could partly reflect my b̃ being
evaluated at the conjunction rather than at the nearest orbit-intersection passage;
an encounters-crate implementation that keys timing on crossing-point arrivals (the
Binet cone already computes the crossing longitudes) could restore a 1-D exact
rotation there — that prediction of mine is a derivation, not a measurement. B's
population weights all crossing pairs equally; a real belt's pair-weighting in χ_t
sets what fraction of candidate pairs actually sit in the broken tier.

**Cost of adopting / fit.** Adoption is a rule, not code: key the per-pair
certificate regime on χ_t (equivalently on ν = events per orbit): χ_t → 1 with
ν ≪ 1 keeps the CF certificate (law.md "Finding encounters" as written); χ_t ≲ 1
with ν ≳ 1 routes the pair to the phase-neighbour mechanism of the co-orbital gold
(20261006-0346-taleb-09b5) — the same trigger that gold run lacked a dimensionless
number for. Fits PRINCIPLES 4 ("regimes are chosen by dimensionless numbers"), 19
(one law at every scale; a fix signals the wrong representation — here the wrong
event anchor), 33 (each scale resolves only what matters at that scale), 3 (compute
only surprises: pay per cluster only where clusters exist). Cost: one comparison
per candidate pair against numbers the cone already has (Δa from U, e from (V,W)).

**The lens.** The dynamics lens looked for attractors and tails; what it found is a
regime boundary and a wrong anchor. It may have missed the allocation side: the
heavy gap tail (slope −1.44) with finite mean suggests certificate-queue occupancy
is well-behaved on average, but I did not measure the p99 of simultaneous live
certificates (Kingman), which is what the allocator actually feels; and the
resonant-return sticky pairs (14 %, K up to 6+) are exactly the burst source that
would show up there.
