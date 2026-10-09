Grade: silver

**Abstract.** Claim: the tube ("gravity is news") read's energy error is second order in source kicks and bounded; naive retarded spirals. All 12 dossier runs reproduce bit for bit in a clean tree. My isolation control (candidate's sources slaved to truth, five lines of sed) proves the growth attribution directly: the read's own error stays flat — 3.3e-7 at μ=1e-3 and 5.1e-5 at μ=1e-2 over 30 reader orbits — so the free-run growth (3.4e-5, 2.3e-2) is inter-law source divergence, not the read. But the frozen kill criterion's letter fires on three un-run in-domain cases: a crossing reader (R=2, dE→1e-1, truth self-exchange 0.37), close sources (rJ=1.2rS, dS/rS→5e3), and μ=1e-2 R=5 monotone to 2.3e-2. Adopt as evidence for `b-news-gravity` (no acceleration term in tubes) after an encounter clause is added to the domain.

## Reproduction

Clean copy of `work/` (patch.diff is empty — no repo edits), `sh repro.sh`: **all 12 runs identical to `runs.txt` to the last digit** (machine line differs only), 53 s total. Every headline number in the dossier traces to a reproduced line: floor 2.12e-9 with dS/rS=0; naive 3.0e-3→1.2e-2→3.4e-2 (dS/rS=1.99 at 10); decisive 2.88e-7/3.43e-9/3.15e-11 (μ-decade ratios 83.9 and 108.9 ≈ 10², slope 2.0); 1.70e-4 at 100 P_T; Carlip 4.12e-5 transient decaying to 5.98e-7; E 1.80e-3 saturating vs truth's own 1.29e-2 (7.2×); solar 8.31e-9; G 2.18e-2 with dS/rS=1.08 at 1 P_T = 11.2 binary periods ("~11" ✓); dt-halving 2.88e-07 unchanged.

## Predictions

Frozen before the decisive runs as far as the folder can show: `predictions.md` mtime precedes `news.c` and `runs.txt` by 11+ minutes; `run.log` is empty, so order rests on mtimes plus the honest miss reporting. Held: floor (2.1e-9 vs ≤1e-9, factor 2), solar bound, naive spiral (slower than predicted), G failure, C's amplitude range. Misses disclosed, not hidden: boundedness at μ=1e-3, Carlip gain (it is 140× *worse*, a stronger deletion argument than predicted), E amplitude.

## My attacks (scratch `/tmp/check93a4/work`, regenerate: `sed 's|ring_push(&ring\[0\], Sl\[1\]\[0\]); ring_push(&ring\[1\], Sl\[1\]\[1\]);|for (int k = 0; k < 2; k++) { Sl[1][k] = Sl[0][k]; } ring_push(\&ring[0], Sl[1][0]); ring_push(\&ring[1], Sl[1][1]);|' news.c > news_iso.c`; close-J: `sed 's|2\.17\*rS|1.2*rS|; s|kappa/sqrt(2\.17)|kappa/sqrt(1.2)|'`)

1. **Isolation control (the experiment the dossier lacked).** With the candidate's sources overwritten by truth's each step (dS/rS printed 0), the pure read error is **flat: 3.32e-07 through 30 P_T** at μ=1e-3/R=5 (free run: 3.44e-5), and **2.17e-05 → 5.11e-05 bounded** at μ=1e-2/R=5 (free run: 2.32e-2, i.e. 99.8% of it was source divergence). This converts the author's circumstantial attribution (μ² at fixed t + μ-independent growth) into a direct measurement, and **confirms** the central claim.
2. **Crossing reader, R=2** (rT=22.2 inside rJ=24.1; in-domain: μ=1e-3, κ=0.3, R≤10): dE 1.0e-4 → 3.2e-4 → **9.95e-2**, monotone, ≥1e-3 within 30 P_T — the frozen kill criterion's letter fires. Physics: dEtruth(self)=0.37–0.49 and dT/rT=2.76 — T's own encounters with J are chaotic and the 1e-3 threshold sits 370× below the truth's self-oscillation (a control that cannot pass is a broken instrument). Still isolated-sources it explodes the same way, so this is metric saturation in the encounter regime, not read secular growth — but the author never ran it and the headline "survives in-domain" does not carry this qualifier.
3. **Close sources, rJ=1.2rS** (μ=1e-3, R=5): the sources' *mutual* tube read diverges (dS/rS 6.9 → 800 → 4960) while truth stays quiet (1.2e-3). Deep conjunctions at 0.2 rS are the encounter regime law.md assigns to changeovers/pair events, not tube reads — but nothing in the frozen criterion excludes them.
4. **μ=1e-2 at R=5**: 1.06e-4 → 4.62e-3 → 2.32e-2 monotone — trips the letter cleanly (the author's own E at R=10 was saved by saturation; dS/rS≈2 there shows the same chaos dominance, and by the letter E trips too).

## Novelty

`q-gravity-at-c` tested free-falling sources (`lenses/b-news-gravity.md`, opus-memo R5: free-fall/Laplace probes only); the kicked-source residual, the acceleration-term deletion, and the doll-boundary quantification are new measurements. Audit verified: `lab/rungs/` has no r5 or r6 files; no B-gate exercises retarded reads (B15 cost, B16 lensing); law.md's contact line says "in the frame of one of the two bodies" with no id rule (letter-level, as claimed). Minor: "Laplace ~1e-12/orbit at solar scale" is ~3 orders low (κ_J² ≈ 2e-9/orbit); the conclusion — a planted naive-retarded law passes today's gates — holds either way.

## Goal fit

Foundation risk retirement for `b-news-gravity` (queued), directly on "gravity must travel at c… can't construct layer upon a flawed foundation"; error type over size (principle 13): a bounded second-order read error whose apparent growth is chaos no law escapes. Not gold: no 10× bottleneck move, nothing built is deleted (the acceleration term was a candidate, never a component), the premise is confirmed rather than broken, and the in-domain survival claim needs the encounter qualifier my cases forced.

## The one experiment that would make it gold

Make the isolation control the decisive metric (sources slaved: the read error is *measured* flat at 3.3e-7 rather than inferred), add the encounter clause to the kill domain (no reader-source or source-source orbit crossings inside the test horizon, mirroring B12/B13's oracle-domain exclusions), and freeze the proposed two-sided rung (this scene, naive-retarded must fail, free-fall tube must pass). One step, ~30 s per case.

## What the author missed

- The five-line isolation control that proves their own attribution.
- The geometry dimension of their frozen domain: they attacked mass (E) but never reader radius or source separation; three in-domain-by-letter cases kill by the letter they froze. A red-team must attack its own instrument's domain — their criterion's positive control (truth self-exchange) exceeds its pass threshold in exactly those cases.
- Their case E already trips their own frozen criterion as written; the non-monotone rescue is a reading, not a rule.
- "μ-independent Lyapunov rate" is mislabeled: dS/rS ∝ μ·t² is diffusive (quadratic), not exponential.
- The Laplace solar-scale rate is off by ~3 orders (immaterial to the conclusion).
