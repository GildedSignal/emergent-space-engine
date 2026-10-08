Grade: silver

**Abstract.** Claim: the SEM step (solve each step's α so K = H_D − U_P + p_t = 0; the motion memo's P8) is killed on the v2 clock — the per-step residual is one-signed in step size. Reproduced from the dossier's commands: plain k=8 exponent 0.064 / worst 4.97e-7, k=6 0.061 / 4.46e-6, dJ 5.55e-17, SEM k=8 fail-rate 1.0 / α-dev 2.5; my independent denser census (49 α points, α→0 included, unseen seed 99): one-signed 58.0% at k=8 (author's exact number), 39.8% at k=6, 63.7% unseen seed, α² slope median 2.0–2.5. The memo's 1% kill line is exceeded under every bracket reading. Gain: retires the exact-constraint closure; B12-v2 should certify a bounded state-function offset. Cost: none — a kill, one design-doc edit.

**Reproduction** (clean tree, `work/patch.diff` empty; Linux x86 shared, orders of magnitude only):
- `smoke`: dJ_per_step 5.55e-17 ✓.
- `b12 8 plain 200`: exponent 0.0642, worst 4.972e-7, 0 lost (99 s) ✓. `b12 6 plain 200`: 0.0606, 4.457e-6 ✓.
- `b12 8 sem 20` (short): fail_rate 1.0, α-dev 2.63, 5,532 steps / 27.6 s — scales to the author's 54,263 / 420 s ✓. `b12 6 sem 20`: fail_rate 1.0, α-dev 13.5 — fills the author's timeout-killed k=6 SEM run; k=6 fails too.
- Independent root census (my script, 300 steps × 16 ships): one-signed within the solver bracket [1/8, 8]: k=6 39.8%, k=8 58.0%, k=8 seed 99 (unseen) 63.7%; k=6 has more roots than k=8 (60.2% vs 42.0%), matching the author's encounter-concentration reading; α² slope 2.0–2.5 confirms the claimed mechanism; `nan` audit 0.0%.
- Novelty: no H entry or doc mentions SEM/KMO/P8; H0215 and the memo's open list leave P8 unanswered. Not a redo.

**Why silver, not gold.** The kill itself is solid — the pre-frozen criterion (memo P8: "a solution is missing at more than 1% of steps") is exceeded 3–60× under every reading, including an unseen seed — but the record has three named defects:
1. **"No solution at all" is overstated.** The author's census grid stopped at α = 4. Extending to [1/64, 64]: one-signed drops to 3.2–41%, i.e. solutions do exist for many steps — at first sign change α ≈ 8–23, where |K| has left the residual scale by 2–3 orders (K(α=8) ~ 1e-10, K(α=64) ~ 1e-7): degenerate runaway roots of a multi-orbit step (frozen-force kick over ~1 planet period), not usable solves. The honest claim is "no usable root near the nominal step"; the bracket sensitivity was not measured or disclosed.
2. **The decisive diagnostic is not regenerable from the run folder** ("Script in the transcript") — exactly the 5 October silver pattern: right physics, missing record. I regenerated it independently and it matched, so the result stands.
3. **The pre-registered rate prediction failed 30–50×** (0.01–2% predicted, 44–58% found) and the census was designed after the SEM runs died. The author reports the miss prominently and honestly, and the miss strengthens the kill — but "held-out predictions held" is not met on the letter.

Also corrected in passing: the SEM "fail rate 100%" is a fleet-batch artifact — `ok` requires all 16 ships to converge in the same batch step, so fleet failure is trivially certain at a 58% per-ship no-root rate; the per-ship number is the census's. The dossier's own framing already rests on the census, so the verdict is unaffected.

**The experiment that would make it gold.** Pre-register a usable-root census: freeze a usability band (root with α ∈ [1/2, 2], runaway roots classified out by the |K| scale), then sweep scenes — two planets, encounter-dominant, eccentric ensemble — plus probe the structural prediction the α² argument implies (below). If the usable-root fraction stays below 99% everywhere, the kill is structural and scene-independent.

**What the author missed.**
- The bracket effect (miss 1 above), and with it the sharpest form of their own argument: on a true SEM trajectory K(start) = 0, so K(end(α)) = α²C₂ds² + α³C₃ds³ has no nonzero root at all except where the cubic competes — success at step n nearly guarantees no-solution at step n+1. The census on plain trajectories (nonzero shadow offset) therefore *overstates* the roots available to SEM; the kill is stronger than the dossier claims.
- The Noether-identity check cited as "verified numerically" is not in the shipped commands (`du_dt` computed, never compared). Verified here independently: max rel 7.4e-15 — true, but not regenerable from the run.
- SEM cost multiplier measured ~2.6× per ship-step here, not the "~5×" quoted (both replica-scale numbers).
- B13/B14 arms of the kill line never measured (disclosed; unnecessary given arm 1).
- Scene coverage is one circular-restricted ensemble (the lens section says so); my unseen-seed census only varies the draw, not the regime.
