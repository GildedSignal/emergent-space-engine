Grade: silver

**Abstract.** Claim: plain fixed-phase DKD holds B14 apsidal precession at 4–6 kicks/moon-orbit through 0.4 R_H, and correctors/higher-order compositions do not extend the frontier. Reproduced bit-identically (102/102 rows; 112 s shared container). Reference validated independently: RK4 and nk=1024/2048 agree ≤ 7.5e-4. r9's averaging kill and the n=0-multipole mechanism both reproduce. Adversarial correction: at f=0.4 the nk=6 frontier holds only on the author's sun-phase seed (4/5 seeds escape or err 40%); robust frontier there is nk≈16 (2× cut). Through 0.3 R_H, nk=6 is robust across 5 seeds and e0=0.05–0.3 (5–8× cut). Corrector kill confirmed. Cost to adopt: near zero; cadence must be phase-aware and conservative.

## Reproduction

- `python3 falsifier.py` in an isolated copy (output path redirected; run folder untouched): **102/102 rows bit-identical** to `results.json`/`decisive.log`. Runtime 112 s on the shared container (author: 53 s).
- Every dossier table number re-derived from my run: plain 0.807%@nk=4 / 306%@nk=3 (f=0.2); 0.972%@nk=4 / 175%@nk=3, escapes ≤2 (f=0.3); 0.747%@nk=6 / 29.7%@nk=4, escapes ≤3 (f=0.4); avg 7.5/20.7/38.9%; corr3 f=0.3 nk=4 = 123%; corr fine-step win 8.1e-5 vs 3.0e-4 (3.7×); corr5 f=0.4 escapes nk=6; fr4 loses to plain at equal 32 evals/orbit everywhere.
- Robustness bullets verified: 50-po horizon f=0.3 nk=4 → 0.74% (mine: 0.739%); second seed at nk=4 → 4.7% (author: 5.5%, seed value unspecified).
- Determinism: identical rates on repeat runs.
- Timing/log order: predictions.md 15:43:01 < falsifier.py 15:43:04 < decisive.log 15:43:58. Consistent with predictions-before-decisive-run.

## Held-out predictions

P2 (correctors don't extend the frontier; win only ≥ nk=16), P3 (fr4 never pays at equal evals), P4 (avg passes 0.2, fails beyond — r9's threshold independently reproduced): **held**. P1 off by one kick-step (predicted nk≈2 at f≤0.3, actual 4) — disclosed by the author. P5 mixed, as disclosed. P6 (slope ≈ −2) **not held as stated**: my fits give −1.36 (f=0.2) and −1.63 (f=0.3); the series is non-monotone (nk=8 ≈ nk=32 at f=0.2), so "within noise" is generous. A control, not load-bearing.

## Attack (beyond the rung's cases)

1. **Reference soundness.** Independent RK4 (4000 steps/sun-orbit, full dynamics) agrees with plain-512 to 4–8e-4; nk=1024/2048 to ~1e-5. Fit-window sensitivity: 0.88–1.3% across discard 10–40%. The 10% verdicts do not hinge on the fit or the self-referential reference.
2. **Seed spread (the hit).** Five sun-phase seeds at 20 po: f=0.3 nk=4 → 1.0/7.2/4.7/1.8/7.0% (all pass). f=0.4 nk=6 → 0.7%, ESC, 40.5%, ESC, ESC; even nk=8 breaks (ESC/18%/67%). nk=16 is the first all-seed pass (worst 5%). So "through ≥0.4 R_H" is seed-luck; the honest claim is **5–8× through ~0.3 R_H, 2× at 0.4 R_H**.
3. **B14 eccentric births.** e0=0.3 at f=0.3: nk=4 fails (16.8%), nk=6 passes (0.30%). e0=0.05/0.2 pass at nk=4 (2.8%/7.0%). A uniform nk=6 covers births; the frontier does.
4. **Non-monotone cadence.** f=0.4 nk=5 → 70.7% (worse than nk=4's 29.7%); nk=16 beats nk=32 on the worst seed. Direct, unreported evidence for the author's own aliasing mechanism — and for "the schedule is the lever, not the integrator".
5. **Extreme f=0.5:** the converged reference itself escapes (nk=512/1024, and e0=0.05) — Hill instability, physics not method. The domain edge at 0.4 R_H is where the claim lives; fair.
6. **Mechanism (A6).** Double average of the tide over both angles: constant to 3e-10 across (e, ϖ) — the "only n=0 survives" claim verified numerically.

## Novelty

No prior entry measures the plain-map kick-cadence frontier or the corrector/composition transplant. H0190 K1 set the 32.5-kicks/orbit baseline; K2's averaging was killed by r9 (precession beyond ~0.17 R_H), reproduced here as the avg control. Focus item 1 queued "correctors, higher-order splits"; this run measures that direction dead for moving perturbers and redirects to the schedule. New; cites its lineage.

## Goal fit

Board focus 1 verbatim. Judged on behaviour (precession rate, e, class) across seeds and horizons, never trajectory identity (PRINCIPLES 2/20). "The simulation tells us what's next not us" (22): the binding constraint is the source's synodic phase, and the measured non-monotonicity in nk makes the schedule-not-integrator conclusion stronger than the author's own evidence.

## Why silver, not gold

Gold needs a 10×+ bottleneck move, a deletion, or a killed premise adoptable in one step. The robust gain here is 5–8× (≤0.3 R_H) and 2× (0.4 R_H); the corrector-kill is measured in a planar single-perturber toy with the static-B case open, and the headline boundary (0.4 R_H) needed my correction. Real, reproduced, redirecting — one experiment short.

**The gold experiment:** lock the kick grid to the parent's synodic phase (or continued-fraction conjunction timing, r8 v3's skin), and measure whether behaviour holds below ~1 kick/moon-orbit across seeds, horizons, e0 births at 0.2–0.4 R_H. If it holds, that is >10× and gold; if aliasing persists even then, the cliff is physical and the cadence rule is the frontier.

## What the author missed

- **Seed fragility at f=0.4**: the robustness check ran a second seed only at f=0.3 nk=4, never at the claimed f=0.4 frontier; 4/5 seeds break it, and the robust frontier there is nk≈16. The dossier's "through at least 0.4 Hill radii" should be corrected before the integrator reads it.
- The non-monotone cadence (nk=5, nk=16-vs-32), which is free evidence for the stated mechanism and strengthens the PRINCIPLES-22 story.
- B14's e0≤0.3 births were one 10-second run away (nk=6 passes at 0.3%); "untested" undersells a frontier that in fact holds.
- P6's "≈ −2 held within noise": fitted slopes are −1.4/−1.6; the oscillatory error makes the exponent a weak control and the claim an overstatement.
- No independent cross-check of the plain-512 reference inside the decisive run itself (I supplied RK4; it passes, so the conclusion stands).
