Grade: silver

**Abstract.** The run inverts adopted gold `20261006-0346-taleb-09b5` (phase-neighbour rank-4 certificate at O(n·k) "replaces" the quadratic tier). The author session aborted on memory before any measured result or dossier; the patch builds and runs, and my reproduction confirms the mechanism: on the gold's own scene, setup-time k=4 coverage falls 1.00→0.93→0.56→0.27 over 50→5000 orbits (seed-robust: 0.55 at seed 777), erodes at fleet scale (1.00/0.96/0.83 at n=300/1000/2000 at T=50; k_needed 4→13→21, ≈ linear in n), and at-encounter rank stays ≤3 (a trivial control). Cross-group coverage 11.6%. Gain: an adopted certificate's premise is horizon- and scale-broken. Cost: none to keep, k must be churn-derived and scoped per group. Not gold: no dossier; four quantitative predictions missed.

## Reproduction

No dossier exists (`author-final.md` is `Working...` + `cannot allocate memory for thread-local data: ABORT`), so there were no author numbers to compare against; I reproduced from the patch:

```
git apply lab/results/20261011-2235-inversion-3477/work/patch.diff
cargo build --release --bin rank --bin rank-detail --manifest-path crates/encounters/Cargo.toml
/home/glmlab/lab-target-3/release/rank        # 9 scenes, 21 s total
/home/glmlab/lab-target-3/release/rank-detail # 4 s
```

Clean tree at `a838a284`; build 5.7 s; every process well under 2 GB. Key numbers (mine, not the author's — the author has none):

| scene | T | enc | cov_k4 | max_rank0 | max_rank_at |
|---|---|---|---|---|---|
| gold (n=300) | 50 | 2093 | **1.0000** | 4 | 2 |
| gold | 200 | 7579 | 0.9251 | 12 | 2 |
| gold | 1000 | 37190 | 0.5642 | 47 | 2 |
| gold | 5000 | 189629 | 0.2696 | 161 | 3 |
| spread Δa=3e-4 | 200 | 8174 | 0.7224 | 29 | 2 |
| spread Δa=1e-3 | 200 | 7401 | 0.4535 | 91 | 2 |
| spread Δa=1e-2 | 200 | 1478 | 0.3031 | 150 | 1 |
| hot (σ_e=3e-2) | 200 | 6181 | 0.5404 | 17 | **17** |
| cross (A↔B) | 200 | 2602 AB | 0.1157 (AB) | — | 63 |

`rank-detail` (gold, T=5000): conjunction-driven encounters (pairs with ≤16 events) have mean setup-rank 56.8; top pairs start at Δλ₀≈0 and first meet after 4k–20k orbits of synodic drift. That is the churn mechanism observed directly.

## Predictions (pre-registered; file exists with no run-order log to prove timing — the patch and predictions are the only survivors of the abort)

- **P1 direction held, thresholds missed.** k=4 holds at T=50 (cov 1.000, k_needed exactly 4) ✓; falls with T ✓; but <50% is reached only at T≈1000–5000 (predicted 200–400), and T=5000 coverage is 27%, not <10% ✗ (k_needed 161 ≥ 100 ✓). Growth ≈1.5–1.6 rank/50 orbits vs predicted 1.1 — right order.
- **P2 direction held, thresholds missed.** ≳90% at Δa=1e-4 ✓ (0.925); monotone collapse ✓; but Δa≥1e-3 gives 45%/32%/30%, not <10% ✗. Deferral saving falls 105×→3.4×, not ≳30×→≈1× ✗ (right sign, ~3× off at the end).
- **P3 failed in sign.** Conjunctions do NOT outnumber encounters (438 conj pairs vs 6181 encounters): hot-ring encounters mostly occur with no Δλ crossing, so a swap/conjunction-triggered certificate *misses* them rather than overpaying. `sec_none`=0 contradicts "sections() rejects most hot pairs". And measured cov_k4=0.54 hot vs 0.93 cold at same Δa, T: temperature IS part of the certificate's problem (max_rank_at=17), contradicting P3's conclusion. The author's own kill criterion did not trigger (k_needed=4 at T=50; coverage falls with T and Δa), so the churn model stands in direction.
- **P4 held in direction.** AB coverage 11.6% (predicted <5%) ✗ on the number, ✓ on the conclusion (88% missed); within-A 86.5% covered ✓. Per-group scoping and a churn number Θ follow.

## Attack (my cases)

1. **Seed:** gold scene T=1000, seed 777 → cov 0.5487 (vs 0.5642): the collapse is not a seed artifact.
2. **Fleet scale — the case the author left unrun and the one that matters:** the gold's motivation was a 10⁶-ship fleet. n=1000: cov 0.957 (T=50), 0.688 (T=200); n=2000: cov 0.832 at T=50 — k=4 already misses 17% at the gold's own horizon. k_needed 4→13→21 tracks the churn model's n·T·Δa; extrapolated to 10⁶ the certificate is dead within one orbit. This is stronger than anything in predictions.md.
3. **The counter-case the dossier should have faced:** at short horizons the deferral is large (deferral_saving 392–453× at T=50) and the lazy channel is tiny (lazy_eager_per_enc ≈ 0.05–0.06, all scenes) — most encounters are repeats of few near-resonant pairs. So the inversion kills *k=4 pinned at setup time*, not phase ordering per se: a certificate that re-sorts on the conjunction channel may still win. The work measures the failure but not the repair.

## Novelty

`docs/HISTORY.md` and the docs carry no horizon-stability or synodic-churn critique of the phase-neighbour certificate; HISTORY's "rank 4" hits are SVD ranks, unrelated. `docs/HANDOFF.md:69` and the board's taste log carry the gold's claim with no horizon qualifier. The original gold's run folder is not on this branch (results publish on `claude/lab-*`), so I could not check whether it measured rank at encounter time — but my max_rank_at ≤3 at all T on its scene shows at-encounter adjacency is trivially true for cold rings (bodies at an encounter share λ up to the equation of center), and cov_k4=1.0 at T=50 shows a short setup horizon also yields k=4. Either reading leaves the adopted claim horizon-broken. Novel on the record.

## Goal fit

Encounters without work per orbit is a live board focus item and the O(N²) candidate term is "the top scaling risk". This shows an adopted answer to it has a premise that breaks exactly at fleet scale. PRINCIPLES: "Measure before claiming, and never strawman" (10) — the gold's rank-4 claim went in unmeasured against horizon and n. The inversion obeys "A failed experiment kills that configuration, never the method" (9): it kills the fixed-rank configuration, and names the churn number as the replacement trigger.

## The one experiment that would make it gold

Measure the repair on the design's cheap path (the premise red-team's rule): a λ-order certificate that re-sorts and re-certifies on the conjunction channel, with k derived from Θ = n·⟨|δn|⟩·T/(2πk) per group, run at n=2000, T=200, on the cold, hot and cross scenes — coverage must stay 1.0 with work per real encounter bounded (the lazy channel suggests ≈0.05 lazy pairs per encounter is reachable), against the eager cone tier. Plus re-derived collapse thresholds (the current model over-predicts the collapse rate by ~2–5×).

## What the author missed

- The run aborted before any result: no dossier, no commands of record, no claim. By the lab's own precedent that alone caps the grade.
- P3 inverted: hot-ring encounters outnumber conjunctions 14×, `sec_none`=0, and temperature does halve coverage — both the mechanism and the conclusion of P3 are wrong as written.
- Quantitative thresholds off by ~2–5× across P1/P2/P4 (the churn constant is ~1.5–1.6, not 1.1, and the coverage floor is ~27–30%, not <10%).
- The fleet-scale n sweep — the gold's own motivating scene — was the obvious adversarial case and was not in the scene list.
- No engagement with the repair the numbers imply (conjunction-channel re-sort, per-group scope), so the work shows the premise broken but leaves "replaces" unrefuted in its defensible form.
