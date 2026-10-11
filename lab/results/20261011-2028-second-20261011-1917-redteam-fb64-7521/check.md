Grade: silver

**Abstract.** All six result JSONs reproduce bit-identically; a third method (scipy DOP853 r-space rays) confirms the +414 M arrival-interpolation corruption, the r_e≥20 leak, and the prototype: the A_phi-keyed image-resolved memo reaches the floor at r_e=8 physically (worst frame ≤6.8e-4 rad), robustly across fresh phases, where per-family and b-keyed memos fail. But the headline adjudication is wrong: at the checker's published dφ=7.5e-4 **plus 4000 α**, their r_e=6 numbers reproduce exactly (delay 38.604, err_fix 9.55e-2), r_e=8's too; refinement 4k/8k/16kα stays at 38.6–40.9 M, and scipy root arbitration gives median delay 38.60. The silver's r_e=6/8 rows are under-resolved-image artifacts. Adoption cost unchanged: one memo column keyed by the sweep parameter.

## Reproduction
Every shipped number regenerates: `attack.py calibrate/sweep` and `attack2.py quad/sweep2/imgmemo/calibrate2` reproduce all six `results-*.json` **bit-identically** (md5, clean tree, 60.2/54/35 s). `results-quad.json` matches the dossier table (orig worst A_t 1.2/7.9/414 M at r_e=6/20/1000; fixed ≤5.8e-6 rel); `sweep2` matches (30.87/12.30/3.95 M delay; err_fix 9.93e-3/2.35e-2/7.83e-4); `imgmemo` matches (alpha-keyed 3.1e-5/7.6e-7/7.3e-7 rad med, 16/16 ≤ floor at 6/8/20; b-keyed 3.1e-2/4.2e-2/1.9e-2 — fails; jumps 4/16 at 8). Timeline consistent: predictions.md (20:31) precedes attack2.py's last save and every results file. Caveat: the dossier's three-table adjudication, the phi0 rows and the 13.7× order check have **no shipped mode** (I regenerated them myself; `sweep2` does not contain the comparison).

## Held-out predictions

Q2, S2, S3 held. S1 is the run's pivot and it is inverted: the author predicted the checker's corrections would reproduce ([REPRO]), found they "do not reproduce under ANY of the three tables", and reported that as a refutation — but their "checker-style" table used 2000 α, not the checker's published 4000 α (check.md: "dφ=7.5e-4, 4000 α"). At 4000 α the checker's numbers reproduce exactly at r_e=6 **and** 8. S4 failed as disclosed; S5's outcome ("P8 at 6 holds") is an artifact of the same 2000-α miss. I1–I3, I5 held; I4 failed sharper than predicted (b-keyed memo itself fails — confirmed).

## My attacks

1. **Third-method oracle** (scipy DOP853 r-space first-order null rays with events; different parameterization, rule and code path from both the RK4 tables and the GL quadrature). Confirms: fixed table A_t at imgmemo hero columns to ≤1.5e-2 M (r_e=8), ≤1e-2 M typical (6/20); original table's small-b corruption +368.8 M at (r_e=1000, b=21.6) against fixed +9.5e-3 M; halving dφ drops it 8.0× (dossier: 13.7× at the worst node — same order, unshipped number).
2. **The adjudication, redone at the checker's construction** (`scene_frames` on dφ=7.5e-4 linear, 4000 α): r_e=6 delay 38.604 / err_phase 0.166 / err_design 0.116 / err_fix 9.55e-2 — the checker's exact published numbers. On the author's own fixed tables at 4000/8000/16000 α: delay 38.60/40.94/38.60, err_fix 0.096/0.128/0.078 — the metric moves away from silver, not toward it; images_max 3→4; per-frame primary flips (t=72.72: err_fix 3.37e-1→4.82e-3).
3. **scipy root arbitration** (16k-α table candidates, closure refined ray-by-ray): the extra images are real (closure residuals 1e-5..1e-3 after refinement); the physically arbitrated median delay at r_e=6 is **38.60** — the checker's value. The quadrature "at every sampled b" cannot certify a root set; it validated dt at columns, and the author's mid-b argument answers the wrong question.
4. **phi0 adversarial** (2.7, 5.9 — unused by the author): the 20 M row stays above 1e-4 (3.8e-4–4.2e-4, P8 fail robust); the prototype at r_e=8 stays under floor (med 1.1e-5/8.5e-6; 100%/94%). But P8's r_e=6 "held" is fragile: err_fix/err_phase 0.070–0.117 across fresh phases at 2000 α, ~0.5 at ≥4000 α.
5. **Physical margin audit**: err_img_alpha is measured against the table's own truth. With scipy bounds on the table's dt at hero columns, r_e=8's worst frame is ≤6.8e-4 rad (2× under floor, median ~2e-5) — the floor claim holds physically at the named scene; at r_e=6/20 fold-edge winding frames the 2000-α table's dt interpolation is off by up to ~0.5–0.7 M (→ up to ~3e-3–3e-2 rad), so "16/16 ≤ floor" and the "1,900× margin" are shared-harness statements there, as the author's caveat (c) half-admits.

## Novelty

The A_phi-keyed memo and the fold diagnosis are new (law.md:24 Motion.6 indeed keys light by "b = L/E"; nothing in HISTORY.md or docs applies image-resolved arrival to the gather — H0183's Shapiro is the oracle, not the view). The adjudication's mechanism half (A_t corruption does not leak at 6/8 via scene queries) is correct and new. The image-set-resolution finding (scene medians at r_e=6 unconverged even at 16k α) is new and, unknown to the author, vindicates the first checker's numbers.

## Goal fit

Principle 30 (navigation/knowledge must be perfect) and principle 34 (oracles are guards): both cut both ways here — the run guards the quadrature but not its own root set. Principle 2 ("'Exact' means deterministic and reproducible"): the shipped record reproduces; the dossier's adjudication prose does not.

## The one experiment for gold

Rerun the adjudication at the checker's 4000-α construction plus the scipy root arbitration, and correct the record: the silver r_e=6/8 rows die (converged r_e=6 err_fix ~0.08–0.13, P8-at-6 fails or is coin-flip), the checker's numbers stand (mechanism: image-set resolution, not A_t interpolation), and restate the prototype's margins with the physical bound. The prototype itself needs no further experiment at r_e=8.

## What the author missed

- The checker's published alpha count (4000) — the single parameter that flips the run's headline; "do not reproduce under ANY of the three tables" was tested only against tables the checker never ran.
- Root-set convergence is a separate axis from A_t accuracy; no alpha-resolution scan was run on their own tables (three lines of code, ~2 min).
- The 1,900× margin is against the shared harness; a physical bound was computable from their own quadrature and changes the claim at 6 and 20.
- The adjudication, phi0 and order-check numbers are not regenerable from shipped modes — the exact gap that sank earlier silvers.
- P8-at-6 "held" reported as clean when it is grid- and phase-fragile (their own phi0 file omitted r_e=6).
