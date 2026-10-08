Grade: silver

**Abstract.** Claim: the co-orbital train certificate (gold taleb-09b5) is unsound as adopted — its rank-4 guard measured distance-rank while the deployable mean-longitude sort misses 79% of encounters on the gold's own validation fleet (p90 30, max 55; robust on four seeds), and crossing outsiders pay 0.25·n_clump cone-certified pair-sections for zero encounters (1,994/8,000, 0 fx in 2 orbits). Everything reproduces bit-identically (trigger, econ, all six probes; only wall-times differ). New and decision-relevant: the wrong-coordinate kill on the gold's own scene, the trigger decomposition (ΔU-only p50 0.041 — the e-vector, not a-spread), the seam constant, and the correction that the gold's 4/233 window-tier "misses" are t=0 convention artifacts. But the trigger-refusal and quadratic-candidacy counts restate published golds (fd48, e618, 384f) uncited. One measured experiment from gold.

## Reproduction

`git apply work/patch.diff`, built with the dossier's exact command (`CARGO_TARGET_DIR=/home/glmlab/lab-target-2`, offline). `invert trigger`, `invert econ`, `invert base|e003|e010|e030|slope|cross`: **every substantive number bit-identical** to evidence.log and the dossier table — trigger p50/p90/max 4.16/10.30/24.09 at σ_e=0.001, ΔU 0.041/0.171; econ frac_of_nc2 1.0000 at all four σ_e with kinds 1732/1910/213; base ranks dist 229/229 (max 4), λ_true 227/229 (2, 5), λ_mean 47/229 (30, 55); e003 15/210 (93, 152); e010 0/166 (157, 196); e030 0/50 (171, 193); slope 1/852 (715, 798) with λ_true 833/852 (max 8); cross fx 1,994 cone pairs, 308 truth encounters, 0 fx, ranks 57/308 (39, 75); method missed=0/extra=0 on all method-on scenes; brute disputes 5/0/1/0/1/1, outside_cone=0 everywhere. Only timings differ (machine quieter: `cross` 8.5 s vs ≈3 min). File times: predictions.md 00:48 < evidence.log 01:03 — pre-registration real; P5's failed candidate clause is reported as failed. Honest.

## Attacks (mine)

1. **Seed stability** (fresh seeds 30, 31, base params): λ_mean le4 58/226 (p90 39, max 65) and 35/229 (44, 74) — the 79% failure is not a seed artifact. λ_true also exceeds 4 on 4/229 at seed 31.
2. **Trigger firing edge** (σ_e = 1e-4, 3e-4, nc=400): binet3/eps p50 0.42 → 1.25 — the train's firing domain is σ_e ≲ 1e-4, 5–10× tighter than the gold's own validation σ_e = 0.001. Inside it (σ_e=1e-4, bunched), λ_mean holds 188/204 ≤ 4 (max 9) — the certificate regime is internally coherent, just mis-scoped: the desert between "trigger fires" and "pairwise affordable" is real, and the gold's own fleet sits in it.
3. **Jam** (σ_λ=0.002, 5× tighter than the gold's tightest): dist-rank max **11**, 44/993 > 4 — even the distance-rank guard dies at occupancy, confirming the dossier's recommendation that k be derived, never fixed. λ_mean p90 128 there.

All three sharpen the run; none breaks it.

## Novelty (the discount)

This is the ~8th inversion of the same gold, and the dossier cites none of the sisters:
- **fd48 (gold, 6 Oct)** already measured the trigger refusing the motivating fleet (ratio ~47) and "as specified it never fires there". This run's count 2 adds only the ΔU decomposition (real, useful) and the nc=400 distribution.
- **e618 (gold, 7 Oct)** already measured the true-λ rank nc-cliff and occupancy law (k from nc·2ρ/λ-spread — this run's slope row and 10⁶ arithmetic restate it; e618's checker had already spot-measured mean-λ rank p50 223), and **384f** already measured candidates = C(N,2) under orbit-path intersection. The "candidate fraction 1.000" fact is also in the gold itself (79,800 = nc²/2).
- **7532 (silver)** measured mean-λ rank vs σ_e (60–88% misses at 0.02–0.05, unbunched) but its checker downgraded it as "the axis the gold rejected"; **0a7a (gold)** measured true-λ train churn (46/body/orbit at the gold's regime) and **f0be (gold)** measured rebuild-on-overtakes Θ(n²) — the cost this run's adoption point (1) leans on but leaves "argued, not measured".

What is genuinely new and survives: (a) mean-λ rank fails **on the gold's own bunched validation fleet at its own σ_e and nc** — the last reading under which the adopted sort could have been sound; it closes 7532's checker's objection with a measurement (the gold's deployment text says "sort by longitude"; its evidence was distance-rank); (b) the gold's 4/233 window-tier misses are t=0 initial-coincidence artifacts — the disputed pairs' brute distances (1.6e-5…8.6e-5 at t=0.0000) match the gold's "missed" d_min list pair-for-pair, so the gold's headline soundness bug was its adjudication convention, not the window tier — a phantom work item deleted before the build; (c) the ΔU decomposition; (d) the zero-yield seam constant.

## Goal fit

Direct: the top scaling risk (candidate work must track real encounters) and the queued co-orbital certificate build (GLM queue and Codex queue-sol; the 6 Oct build attempt died on rate limit, so this lands pre-build). "A fix signals the wrong representation" (#19); the guard was "a control that could not fail" in the README's sense. Adoption is spec text, nothing on main.

## The one experiment for gold

Measure, not argue, the surviving package's cost inside the desert it names: true-λ sort + occupancy-sized k + ΔU trigger, on the gold's own scene and one desert scene at nc ≥ 3200 — rebuild/churn per orbit (0a7a's rates suggest it is large) vs the quadratic tier's per-orbit setup. If the package holds O(n·k̄)/orbit there, it replaces the demolished design (gold); if not, the desert itself is the finding and the encounters design needs a different representation (2D order, arrival-time ranking per 384f). Either outcome is adoptable in one step; cite and adjudicate the sister runs alongside.

## What the author missed

- The sister inversions: six prior runs (f0be, fd48, 7532, 0a7a, e618, 384f, 7655) had already killed this certificate from the churn, trigger, e-spread, occupancy and topology axes, three of them gold; the dossier presents counts 2–3 as new. The lab's value depends on runs citing what is already known.
- "Same scene and seed" for the 4/233 non-reproduction is nearly exact (RNG draw order and rayleigh match the gold's generator; only the e-cap differs above 0.004, P≈3e-4/body) — the author could have stated this match and made the correction airtight by identifying the four disputed pairs as the gold's four misses, which the distances already show.
- The trigger-violation headline "10–25×" is p90–max; p50 is 4× (numbers printed, phrasing loose).
- `ranks_fx` is empty in every scene (0 fx encounters), so P5's held-out λ_true-rank clause for crossers was unmeasurable — correctly reported, but a geometry with actual fleet×striker encounters would be the honest next seam case.
