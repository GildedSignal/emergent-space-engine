Grade: silver

**Abstract.** Claim: WHFast correctors buy 0× and Yoshida-4 only 1.33× for the plane's 64/orbit DKD; the binding gate is apsidal precession, and a per-observable cadence (16/orbit for energy-only bodies) is a free deletion. Reproduced bit-identically, 6.2 s, one command. The corrector kill is solid: identical gate outcomes everywhere (J slightly worsened), REBOUND coefficients, round-trip exact to 1e-16; dkd needs K=128 on retro-0.6 (my probe). But the frozen S3 element gate is missing from `summarize.py`: under it dkd fails the close pass at every K ≤ 64 (final-a error 1.6–5.3% vs a 1% gate whose reference floor is 0.008%) while y4@16 passes — the s3 row ("y4 3× worse") is inverted. And "J passes at 16 everywhere" is contradicted by the author's own table (ho-e30-0.4 needs 32). Adopt: delete q-correctors; the cadence deletion is 2×, not 4×, at e ≈ 0.3.

## Reproduction

- `rustc -O -o kickcorr kickcorr.rs && ./kickcorr && python3 summarize.py`: byte-identical `results.jsonl` (cmp), 6.2 s, m20 = 4.5600. Table matches the dossier, including the quoted e10-0.4 precession errors 0.26/1.42/0.49/0.00 and "y4 locks at 32 on retro-0.6" (rel 0.0000).
- Timing: `kickcorr.rs` (…420) → `predictions.md` (…446) → `results.jsonl` (…463). Predictions predate the decisive run. `work/patch.diff` empty; no tree edits.
- Corrector: coefficients A1…B52 match Rein & Tamayo's published WHFast corrector constants; apply/un-apply round-trip exact to 1e-16 (probe). Displacement at K=8 measured 2.1e-5, not the dossier's 5.7e-5 — same order, immaterial.
- Negative control: euler fails every scene at every K (as shipped, with the disclosed softening that easy moons pass J).
- Novelty: no H entry tests correctors or higher-order splits; `lab/queue.txt:6` (`start q-correctors 90`) and HISTORY.md:3121 queue exactly this. Direct hit on board #1.

## What holds

- **Correctors 0×, reproduced.** dkd3/dkd5 gate outcomes are identical to dkd on every (scene, moon, K) except ret0.5 (32 vs 8 — the corrector *hurts*). The mechanism claim is consistent with the data: corrector rows' j_max are slightly worse than dkd's (e.g. retro-0.6 at K=16: 3.6e-5 → 7.4e-5), as expected when the repaired O(ε·dt²) term is absent and the corrector only adds its own ε-noise.
- **Precession, not J, binds on s1:** e10-0.4 at K=32 fails P (+0.49 rel) with j_max 2.6e-6. Verified.
- **y4's J error is ~dt⁴⁸** (×27–28 per halving measured) and buys little where J binds — verified.
- **The cadence idea survives a 4× horizon** (my probe, 200 planet orbits): j_max at K=16 = 1.8e-5 (e10-0.4), 7.1e-5 (ret0.7, near the edge), 9.6e-6 at K=32 (ho-e30-0.4); bound classes match their references.

## What fails

1. **A frozen gate was silently dropped.** `predictions.md` froze "S3: final osculating a and e within 1% / 10%"; `summarize.py` never implements it, and the dossier's s3 row (dkd=16, y4=48, "3× worse") comes from the gate-less summarizer. Under the frozen gate: dkd fails s3 at every K ∈ [2..64] (K=8: passes elements 0.85%/4.8% but fails P at 0.37; K=16/32/64: final-a error 4.3%/5.3%/1.6% > 1%), while y4 passes at K=16 (0.27%/3.2%). The reference floor is ref512-vs-ref2048 = 0.008%/0.04%, so the gate is passable, not noise. This inverts the s3 conclusion and weakens "64/orbit is already near its own minimum": on the pass scene no dkd cadence swept holds its own frozen tolerance, and y4 — not dkd — is the admissible scheme. Not disclosed anywhere; the r4-v2 failure mode.
2. **"J alone passes at 16/orbit for dkd on every s1/s2 moon" is false in the author's own shipped data**: ho-e30-0.4 has j_max 2.33e-4 > 1e-4 at K=16 (the summarizer's own J-only row says 32; there J, not precession, binds). The deletion is 2× on that moon, not 4×.
3. **The retro-0.6 P gate is estimator-fragile far beyond the 10% tolerance.** The reference's LSQ rate on the *same* ref512 trajectory is 2.17e-2 (full fit) vs 1.30e-2 (second-half fit): a 40% ambiguity, ~4× the tolerance; e10-0.4's is 8%. The s2 "y4 admissible where dkd is not" row compares schemes under one estimator whose self-agreement is worse than the gate. My probe confirms the underlying scheme difference is real (dkd K=128 locks to rel −0.007), so the finding survives — but the frozen gate as written measures estimator agreement, not behaviour. r9's Clairaut lesson, again; the dossier names the fix but not the magnitude.
4. Minor: `COST` ignores the corrector's 8/16 kicks per output epoch (favors correctors slightly; conclusion unaffected); pro0.45's reference flips bound/escape between K=512 and 2048, so its class-gate column is decided by a chaotic reference (the "<0.05% on every bound moon" sentence is technically true and hides this).

## The one experiment for gold

Re-run the sweep with the gates as frozen: implement the S3 element gate in the summarizer and replace the LSQ apse slope with a secular-frequency estimator (fit ω from the e-vector, or FFT of the apse series; report the estimator's own ambiguity as the floor). Expected: dkd fails s3 ≤ 64, y4@16 passes; retro-0.6's wall survives but at a wider tolerance. That either kills dkd's "near-minimal" claim on hard scenes outright (strengthening the finding past the dossier's version) or dissolves the wall — both publishable, one run, ~10 s. Fix the cadence sentence to "16 on low-e moons, 32 at e ≈ 0.3" while at it.

## What the author missed

The two defects are both in the reporting layer, not the physics: a dropped frozen gate that inverts the strongest held-out scene, and a headline sentence ("16/orbit for every s1/s2 moon") contradicted by the author's own printed table. The P-gate fragility was named as a risk but its measured magnitude (40% on retro-0.6) was checkable from the shipped data in minutes. The physics work — corrector implementation, y4 scaling, negative control, pre-registration, honest scoring of three failed predictions — is clean and is why this is silver, not lead.
