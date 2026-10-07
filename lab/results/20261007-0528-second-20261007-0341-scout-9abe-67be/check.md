Grade: gold

**Abstract.** Claim: near first-order commensurabilities the kick layer is cadence-uncertifiable at every cadence (29/30 rows over ±2 W), the per-row oracle ceiling is 1.14× in tide evals / 1.24× in kicks (gate-robust 1.05–1.18×), and the scout run's "2:1 vs 3:2 inversion" was an operator-precedence artifact (S2c n_per = 0.6857, 2.29 W off a 3:2). Everything regenerates bit-identically: `cadence.py` 0 diffs vs both stored JSONs; `lattice.py full` 77.8 s, 0 diffs; oracle independently recomputed 466.8→409.6 = 1.140×. My probes confirm: truth converged at 4× resolution; fresh phases π/6, π/3 still nothing; μ=1e-4 zone rows fail identically (self-similar); 5:3 at e0=0.1 still only FIXED-64. Gain: deletes the cadence-law branch before the queued q-cadence spend; the frequency selector survives. Adoption cost zero.

## Reproduction (clean /tmp tree, no patch to apply — patch.diff empty)

- `python3 cadence.py S2c,S2d,S2c2,S3,S4` (7.7 s): **0 diffs** against this run's stored JSON and against the original scout run's stored JSON (branch `claude/lab-20261007-0341-scout-9abe`, commit 7e3053e); `cadence.py` is byte-identical to the original's.
- `python3 lattice.py full` (77.8 s): **0 diffs** vs `out_full.json` (wall fields aside). `analyze.py`: 17/62 certifiable; first-order 1/30 (the fluke `21_d+2.000_p2`, FIXED-64 only); baseline 466.8 evals/orbit, per-row oracle 409.6; no non-fixed policy holds all 17 (best TRIG-0.25 at 7/17; TRIG2G-2.0 holds nowhere; FIXED-64 holds everywhere but costs 0.42×). `gatesens.py`: 17/62, 1/30, 1.14×; absolute-e 25/62, 2/30, 1.18×; loose 38/62, 8/30, 1.05× — all as written.
- Oracle recomputed **independently** from the raw JSON with my own gate code: 1.140× evals, **1.237× kicks**, winners FIXED-16×6, TRIG-0.25×5, FIXED-64×4, TRIG2-0.5×1, AVG×1. The 4× bar is dead even under free-trigger engine accounting.
- The scene bug, from code reading and arithmetic alone: `2**(2/3)**1.5` parses right-associative → n_per = 0.68571 (intended 0.5); S2c sits +2.29 W from the 3:2 and +14.86 W from the true 2:1; S2d n_per = 0.48773 = 0.98 W from the true 2:1, 7.92 W from S2c. All four dossier numbers exact. The original checker's 3:2 probe (FIXED-64 epump 0.12) matches my `32_d+0.000` row, so its inversion really did contrast the mislabelled scene against a true 3:2 — no 2:1 was ever tested. Dissolved, as claimed.
- Instrumentation: `layer2` vs the shipped `layer` on precedence-clean S2d, 4 policies: kpo/epump/da_rel identical to 6 decimals.
- **Timing:** predictions.md 05:38:24; out_full.json 05:39:53 (a 78 s run, so it started after the predictions). The pilot (05:35:43) is disclosed calibration and is bit-equal to lattice row `21_d+0.000_p0`; `out_S1/out_extra.json` are pristine `cmp`-identical copies of the originals. Record honest.

## Adversarial cases (mine, `adv.py`)

1. **Truth convergence** at the 2:1 centre: ts = 1024/2048/4096 agree to 6 decimals at both horizons (e 0.100023 / 0.030800). The gate's reference is not the failure.
2. **Fresh phases** π/6 and π/3 at both first-order centres: nothing holds, consistent with the ±2 W sweep.
3. **μ = 1e-4** (the dossier's own caveat (ii)): centres, ±2/3 W, ±2 W rows still certify with nothing — and FIXED-64's margins are numerically the same as at μ=1e-3 (epump 0.681→0.121, da 0.032→0.053 vs 0.68→0.12, 0.0321→0.0526). The zone is self-similar in μ; only its frequency occupancy shrinks. This strengthens the run beyond what it claims.
4. **5:3 at e0 = 0.1**: centre still nothing; +2/3 W holds only FIXED-64. The e0 caveat does not reopen a cheap cadence.

## Novelty and goal fit

No prior H entry covers a resonance-lattice cadence study, an oracle-ceiling argument, or the precedence bug; this is literally the gold experiment the scout run's checker named. It correctly cites H0203 ("resonance kills averaging") as existing law, corrects the silver scout run's surviving rule at its root, and answers the queued q-cadence item (120 min) before it is spent — a deletion, plus "shows that a premise is wrong", twice. Board focus #1 (fewer kicks per orbit at held behaviour). PRINCIPLES 9 ("a failed experiment kills that configuration, never the method"), 13 (the near-resonance layer error is coherent and structural — exactly the compounding class), 22 (the selector is "the simulation tells us what's next"). Gates judge behaviours (e-ratio, a-drift), never trajectory identity. Adoption is a decision plus zero code.

## Why gold, not silver

Reproduced bit-identically end to end; predictions were pre-registered with real risk (P3 and P4 failed and are reported as failures); the negative result carries a ceiling (1.14×/1.24×), not just a null; it is gate-robust across three gate variants and survived four independent adversarial probes; and it corrects the predecessor's evidence base (the mislabelled scene) rather than merely adding a counterexample. The two slips below are factual prose errors that do not touch the claim, the numbers, or the adoption decision.

## What the author missed

- **"5:3 (15 rows): 0 certified" is contradicted by the run's own record:** `53_d+0.667_p2` and `53_d+2.000_p2` hold FIXED-64@66.1 evals/orbit under the pre-registered gate, and the oracle sum includes them. Should read 2/15, none cheap. Immaterial to the verdict.
- **P5 is self-scored "held" while half of it failed:** the predicted "1.5–3× eval cuts from de-phased coarse cadences" did not happen (DEPH-2.5 holds 1/17, GOLD 0/17). The dossier states the de-phased null elsewhere but does not score the miss.
- The centre-gate is endpoint-e on a librating truth, so a right-amplitude, wrong-phase libration also fails it. That is the right behavioural demand, but "uncertifiable" should be said to include libration phase, not only amplitude/quadrature error.
- The oracle is over the 14 policies tried; the claim "no real rule can exceed" is safe only because centres fail at any cost and the 4× bar dies even with free trigger evals — worth one sentence of scoping in the dossier.
- The float harness still cannot speak for the integer engine's anchors; correctly deferred, but the S1 quiet-scene trigger cut remains unmeasured there.
