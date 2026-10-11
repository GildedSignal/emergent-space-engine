Grade: gold

**Abstract.** Claim: the plane's kick resolver costs ~75 µs/kick against a ~42 ns information floor (idiot index ~1,800×), and the cost is the per-kick rebind (tube refit + history + Arc), not physics. I reproduced everything from the dossier's commands in a clean tree: both digests identical, timings within 1% (median 75.2 vs 75.6 µs; sub-phases 3.7/4.3/0.27/67.3), floor 42–43 ns batched, 2.2 ns streamed, 126–128 ns causal-random, ~13.6 ns/source. My own probe (timing `rebind()` directly) confirms the attribution beyond the author's evidence: 63.8 of the 67.4 µs rest. Seeds 2 and 7 keep the structure invariant. Adoption is one builder item (deferred fit, additive invariants), acceptance B12–B17 + digests. Gain 10²–10³× per kick.

## Reproduction

Clean tree at `a838a284` + `work/patch.diff` applied with `git apply`. Build 30.7 s. (Note: the workspace target dir is `/home/glmlab/lab-target-2`; the dossier's `CARGO_TARGET_DIR=…` placeholder is right to keep. `gcc` needs `-lm` here.)

`xtask universe --kick-bench --seconds 30 --rtf 100` (seed 1):

| quantity | mine | author |
|---|---|---|
| digest / replay_digest | `eccc7f5a…` / `0e02bf0f…` | identical |
| frames / samples / refused | 1800 / 1158 / 0 | same |
| median all / made / leavers (µs) | 75.2 / 34.5 / 91.6 | 75.6 / 34.9 / 91.7 |
| p99 (µs) | 387 | 370 |
| read / field / kepler / rest (µs) | 3.69 / 4.29 / 0.265 / 67.25 | 3.74 / 4.32 / 0.266 / 67.62 |
| memo exact / quantized | 0.0 (1125 shapes) / 0.9547 | identical |

Floor (`gcc -O3 -march=native -lm`): 4 M bodies 64 MB stream+field **42.0–43.0 ns** (author 41.65); 16 M 256 MB stream no-field **2.22 ns** (2.22); 64 MB no-field 2.22; causal-random 256 MB+field **125.9–127.9 ns** (author 139–161 — same order, this box less loaded); causal-random cache-resident 51.6 ns (the random-order penalty is memory, as claimed). Field share (42.9−2.2)/3 = **13.6 ns/source** (author ~14). Idiot index 75.2 µs / 42 ns = **1,790×** (author ~1,800×).

Numbers that differ, all trivial: dossier says field 4.4 µs (JSON says 4.32); dossier's rest 67.3 is computed as total−sub-phases while the JSON's per-sample median is 67.6; the causal-order floor lines are absent from `work/floormatrix.txt` (the dossier's command regenerates them — I did); p99 387 vs 370 is machine noise.

## The attribution, independently verified

The author bounded "rest" only by subtraction and left open whether it hides Scalar step machinery rather than the fit ("this run did not" time `bind()`). I did: atomics around `rebind()` inside `step::process`, snapshotted per kick by the bench. Result: **rebind median 63.8 µs of rest 67.4 µs (94.7% of rest, 85% of the whole kick), fired on 1158/1158 kicks**. The lever is the refit, not the Scalar conversions. The author's worry is resolved in their favour.

## Adversarial cases

- **Seeds 2 and 7** (same config): medians 55.5 / 66.4 µs; physics (read+field+kepler) 8.2 µs on both; rebind 43.8/47.0 and 54.9/58.4 µs of rest (93–94%); exact memo hit 0% with 957/957 and 1485/1485 distinct shapes; quantized 95.1% / 96.9%. The claim is seed-invariant; seed 1's 75.6 µs is the high case (idiot index 1,300–1,800× across seeds).
- **Shorter window** (`--seconds 10`): rest 79.3–79.5 µs — early kicks are dearer; the decomposition direction is unaffected.
- **`kick()` source read**: the resolver is readout → secondaries+tide → field → sigma-delta → `rebind` (fit + history `Segment` + `Arc` entry); the plane's dolls hold ~3 sources (star system, three planets, a moon), so the floor's 3-source assumption matches the scene.

## Predictions

`predictions.md` (17:33:05) precedes both bench outputs (17:34:42 pre-instrumentation, 17:38:23 decomposed) and `floormatrix.txt` (17:38:29). P2 (rebind > 50%): held, 89% — and strengthened to 85% of the whole kick by my probe. P3 (floor): held (2.2 / 2.1 / 126–128 ns; the author's 161 ns case honestly reported above 150). P4 (index ≥ 100×): held, ~1,800×. P5 (exact hit < 5%): held, 0%. P1: held for made bodies (34.5 in [5, 60]), **missed** for leavers (91.7 > 60) and on p99/median (4.9 > 4) — both disclosed in the dossier, both in the direction that makes the bottleneck worse, so they cannot have oversold the claim. The digest-identity claim (instrumentation reads only) is verified by the two saved runs sharing both digests, which my run also matches. Immaterial: predictions named `--seconds 20`, the runs used 30.

## Novelty

H0210 records "kicks cost 29 µs" (M1, before motion law v2) and names kick cost as the next item; H0211–H0215 contain no decomposition and no floor. The memo result (exact 0%, quantized ~95% but a law change) matches the 5 October correction (H0212/H0213, board) and is cited by the dossier as corroboration, not novelty. `b-readout-cost` is the readout component (6.7 µs), not the resolver; the 6 October gold `components-4643` was encounter setup. The decomposition, the floor and the idiot index are new on the record.

## Goal fit

Board item 1 ("kicks dominate the engine's cost") and item 3 (cheaper events). The run kills the premise that the kick's cost is physics — the field is 6% — and redirects the lever from cadence and memoization (both already dead on the record) to the representation: delete the per-kick refit, which `docs/representation.md` line 67 already prescribes ("a kick updates the cycle by a multiply-add"; thesis 3). PRINCIPLES P1 ("the cheapest compute is compute not done"), P19 (bandaids signal the wrong representation — the memo was the bandaid). Both quotes verified in the docs.

## What the author missed

1. The read side was not measured (admitted): deferring the fit moves its cost to reads; at the goal's scale kicks dominate reads, but a watched fleet at rtf 1 could lose. The builder item must carry a read-side budget.
2. The floor assumes epoch batching (body-ordered streaming); today's causal queue pays the ~126 ns random-order price — a scheduler change the adoption cost does not include.
3. The tail: p99 is 5× the median (370–387 µs) and is not decomposed; P12 (p95/99 smoothness) will care at adoption.
4. One seed reported; the median varies 55–75 µs across seeds (I ran 2 and 7). Structure invariant, magnitude not.
5. `work/floormatrix.txt` does not contain the causal-order runs the dossier quotes; save every headline number's raw line next time.

The one experiment that would make this gold — timing `bind()` alone — is done (above, in the author's favour). The next experiment is the build itself: the deferred fit with additive integer invariants, judged by B12–B17 and the replay/tie digests.
