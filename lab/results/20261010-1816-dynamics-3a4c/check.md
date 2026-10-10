Grade: silver

**Abstract.** Claim: kick cadence in belts is governed by behaviour unfolding within the certification horizon, not resonance proximity; no birth-element Chirikov scalar can rank it. All three simulations reproduce bit-identically from the dossier's commands; every histogram, rho and cost ratio regenerates, except: exp2's "honest 4.4x" is actually 2.7x, belt A is 2048 bodies (not 1024), and the FTLE shear formula is 44x off — though the mu-independence (ratio 1.00) is real. The pre-registered kill branch fired correctly (median K*(NEAR)=4). Checker probe: at K*=8, p90 apsidal-precession error 0.017 rad over 120 orbits — e-statistics miss what B14-class gates check. Adoptable now: redirect q-cadence away from a frequency oracle; 6.8x ceiling where behaviour unfolds.

## Reasons

**Reproduction (clean tree, /tmp).** `cadence.py A|B`, `exp2.py`: outputs bit-identical to the stored npz (8+6+5+5 cadence arrays). `analysis.py`, `exp2_analyze.py`, `conv.py` rerun and print the dossier's numbers: A median/p90 K*=4, never-sufficient 0%, uniform(p99=8)/scheduled 2.0x, rho(A)=+0.948; B rho=+0.488; C rho=0.980 (correctly discarded as rank noise on a constant); conv 512-vs-1024 ≤ 1.2e-5 of tolerance; exp2 near/far e_std and K* histograms exact; P9 89%; NEAR/FAR ratio 95x. Numbers analysis.py never prints, recomputed independently and confirmed: B histogram 8:1235,16:64,32:28,64:24,128:23,256:162 and 6.81x; C 8:1526/16:10; B zeta-strata endpoints 2.27→1.01 (tail not monotone: 0.79→1.01). The C FTLE median (6.878e-3, ratio 1.00) regenerates now but is absent from the stored analysis.json ("C FTLE file missing" — analysis ran 18:28, out_C_ftle.npz landed 18:29): a timing gap, not a fabrication.

**Errors found (none fatal, all reported):**
1. Exp2 "honest pooled savings vs uniform(p99=16): 4.4x" is wrong; under that exact definition it is 2.7x (8000/2960). Direction: overstates scheduling benefit — the corrected number *strengthens* the author's own kill branch (cadence barely bites; 85% at the floor).
2. Belt A is 2048 bodies; dossier says 1024.
3. The FTLE mechanism label is wrong: ln(1+s·6yr)/6yr with synodic shear s predicts median 0.30/yr vs measured 0.0069 (44x off), and measured lambda is nearly flat in a while shear varies 3x (corr≈0.29). The claim that survives — and it is the payload — is mu-independence: identical medians at mu and 3x mu, so the instrument cannot be reading chaos/libration. The "instrument warning" stands; the formula does not.
4. B/C histograms, strata and 6.8x are not printed by any shipped script; I had to re-derive them (they check out, but "the exact commands that reproduce them" is only partly met — the known silver-killer from 5 October).

**Predictions.** Addendum pre-registration verified by file times and log order (18:28 vs exp2 outputs 18:33/18:39). Base predictions (P1–P6) unverifiable from mtimes: predictions.md was last written 18:28, after the ladder outputs (18:23–18:26). No evidence of post-hoc writing — the failures (P1, P2, P8) are reported as failures and the pre-registered kill branch fired as written — but "written before the ladder runs" cannot be confirmed from the artifact.

**Adversarial cases (my own).**
- *Apsidal precession* (belt C physics, 400 bodies, K∈{4,8,512}, varpi tracked every Jupiter orbit): the K* metric (mean/std/max of e sampled every 4 orbits) is blind to precession. At K=4, p90 absolute error 0.052 rad over the 120-orbit horizon (~25% of the ~0.2 rad total secular precession; 2% of bodies exceed 0.3 rad); at K=8, p90 0.017 rad, median negligible. Boundary, not a kill: it materialises only if a gate tolerates precession more tightly than ~0.05 rad per century-scale horizon. B14-class gates are unmeasured here — this is the author's own admitted blind spot, now quantified.
- *FTLE structure*: lambda flat in a, mu-independent — see error 3.
- *Bit determinism*: three full reruns bit-identical.

**Novelty.** No HISTORY entry measures per-body cadence demand, per-body scheduling ceilings, or a resonance-scalar cadence ranker. Nearest is H0190 (kick *counts* per orbit, 32.5, low-orbit regime, cost side) — this run is the sufficiency and scheduler side, and it cites H0190 itself. The taste log's "the lever is cadence (q-cadence queued)" makes this the directly demanded measurement.

**Goal fit.** Board focus line 1 and q-cadence. It shows a premise is wrong (a birth-element frequency oracle cannot schedule kicks: rho sign-unstable, and resonance-proximal NEAR bodies need median K*=4) — PRINCIPLES 22, "the simulation tells us what's next not us": the scheduler must read measured unfolding, not predicted frequency. That deletion is adoptable within one step, before q-cadence is built. But the positive quantifications (4/orbit suffices; 2x quiet, 6.8x unfolding) are bound to the e-statistic behaviour metric, which my probe shows is not the engine's full certificate set — so the ceiling numbers are an upper bound on trust, not measured adoptions. Not gold: held-out predictions did not hold (the process worked, the mechanism died), the 6.8x ceiling is below the 10x bar until confirmed under the engine's own gates, and the regenerability dents (4.4x, unshipped analysis) are exactly the pattern that has capped silvers before.

## The one experiment to gold

Re-derive K* against the plane's own certificate set (B14 precession, B17-class resonance) and the real kick layer (orbit-averaged tides per H0190, not full-tide impulses), for belt B and the exp2 NEAR set. If the horizon-governed reading and the 6.8x ceiling survive gates the engine actually freezes, that is gold: it converts "e-statistics are cheap" into "the engine's certificates are cheap at measured cadence", and the precession boundary above either closes or becomes a real cost line.

## What the author missed

- The exp2 4.4x arithmetic (2.7x real) — the error favoured the interesting lever; the honest number is more negative, which is the finding.
- The FTLE "shear" formula was never checked against its own inputs; only the ratio was. A one-line print would have caught 0.30 vs 0.0069.
- Belt A body count misreported (1024 vs 2048) and B/C analysis numbers not regenerable by any shipped command — the 5 October lesson, repeated.
- The K* metric's blindness was named as a risk but never probed; 30 lines of varpi tracking (the probe above) quantify it and would have belonged in the dossier.
- "Spread 32x" for belt B conflates the p99 tail (256 needed by 162 bodies = 10.5%) with a scheduling win; those 162 bodies' share of scheduled work is 71%, so the tail dominates the bill — worth stating, since it is the actual q-cadence target population.
