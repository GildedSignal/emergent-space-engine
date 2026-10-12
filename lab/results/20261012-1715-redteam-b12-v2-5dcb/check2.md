Grade: gold

Abstract: The B12 v2 pooled statistic is broken as a fleet gate and must not freeze. Reproduced independently (regen.sh exit 0, 178 s; anchored rows — slab, hump, creep, quad arrows, echo, planted-bounded, planted-compound, all four official gate lines — byte-identical to the author's captured log): a law leaking at the declared 2e-10/horizon on 5 of 16 ships with a bounded mid-horizon blip on the rest passes officially (+3.127; author's blip shape −18.796; both PASS). Second-checker amplifications through the official gate: a 5-ship leak at 50,000× the declared rate passes identically (+3.152 at 1e-5); the window extends to 3 leakers (+4.365 PASS); a fleet-wide 1e-10 blip with no leak passes at −13.570 with "RESOLVED" sensitivity; pure 1/2-ship leaks correctly fail (+17.7/+22.1). Adoption cost: none — reject the freeze; redesign is the per-ship verdict with a calibrated per-ship null.

## Reproduction

- `bash regen.sh` in a clean tree: exit 0, 7/7 tests pass, 102 s of test time. Every anchored number matches `work/rt-all.author.log` exactly (slab +22.667/+50.969, hump +8.634/+8.611/+8.864/+8.762, creep 0.000×4 → +39.084 → +55.492, quad +9.579/+9.598/+9.665, echo 0.000/inj +55.491, planted-bounded +0.812/inj +50.473, planted-compound +20.560, all official PASS/FAIL verdicts and detail strings). The blip-involving rows differ exactly as `fix-note.md` discloses (the sin² window was inferred after the author's patch was lost); every verdict is identical in both runs. sha256 of corpus/b12_stat/handoff match `artifacts/evidence/cx-b12-v2/receipt.json` on `wt/cx-b12-v2`, and the receipt's planted-bounded arrow −2.806 grounds the platform-noise claim's other side.
- The break is through the real gate, not the probe's replica: `rt_minority_leaks_at_the_declared_rate` calls `handoff::b12` and asserts the official detail string contains the probe's own conditional arrow (+3.127), official PASS, 0 unresolved, 0 bad, worst 1e-9. The per-ship table shows the gate's own dt-coefficient fit at −2.00e-10/horizon on all five leaking ships (0, 1, 6, 11, 12 — a₀/sep > 1.13) in both runs: the deciding statistic discards a correct per-ship detection.

## My adversarial cases (independent code, official gate path)

Fresh worktree of `wt/cx-b12-v2` + the run's patch + my own `check2` tests (`fn`-pointer error shapes, `Events` law, `b12(&law)`):

1. **Rate-blindness (outside the author's tested range):** the 5/16 split leak at λ = 1e-5/horizon — 5×10⁴× the declared detectable rate — passes officially at +3.152, sensitivity RESOLVED; λ = 2e-9 passes at +3.127. The leaking ships' z saturates; the pooled mean decides nothing about rate.
2. **Window width (outside the author's tested range):** 3 leakers + blip majority → official PASS +4.365; 4 leakers → +2.999. The hole is not an artifact of the a₀/sep > 1.13 boundary; it spans at least 3–5 leakers of 16.
3. **Fleet-wide blip, no leak:** a = 1e-10, w = 0.1 on all 16 ships → official PASS at −13.570 with sensitivity RESOLVED (+43.168); the identical shape at a = 1e-6 fails only because its own residual masks the injection (same arrow −13.638, UNSUPPORTED). `arrow <= 5` has no lower bound, and the "RESOLVED" label certifies power the gate does not have. (These verify the page's check-amplified lines to the third decimal.)
4. **Controls:** a pure 1-ship leak (+17.741) and 2-ship leak (+22.131) with a below-floor majority FAIL officially — the cancelling majority must be above-floor with negative z; the page says exactly this.
5. **Determinism:** planted-bounded twice in one process is bit-stable (+0.812/+50.473 both passes), so the ±3.6 swing against the receipt is platform (libm), not run-to-run noise — consistent with "floats never decide them" being violated near the 5 cutoff.

## Predictions

`predictions.md` (49 min mark) predates the captured decisive output `work/rt-all.author.log` (23 min mark) and the dossier; its content shows genuine misses (slab τ=5 predicted PASS-side, landed +22.7 FAIL — the author reports it wrong and names the mechanism: pairs are always first-half × second-half). Held-out scoring in the dossier matches the logs (quad held at +9.6, hump median +1.9 in (−25, +10); the 5/11 minority variant is disclosed as post-prediction).

## Novelty

Only B12 run in `lab/results/`; the published wiki topic `b12-statistic` has 0 prior runs. The v1 exponent kill (taste log, 6 October) is a different mechanism; this run refutes the v2 pooled rank score, whose own doc demands exactly this red-team before freeze ("MUST NOT be called a validated certificate until the red-team addresses this premise"). The candidate's shipped controls (fleet-wide leak, leak+bounded, small bounded offset) do not cover a minority leak with a shaped above-floor majority — the break is new, not a repetition.

## Page

Every number in `wiki/b12-statistic.md` checks against the logs or my runs (−13.570/+43.2, +17.7/+22.1, +3.13 at 2e-9–1e-5, quad +9.6 scale-free, creep cliff, receipt −2.806 vs +0.812, slab +22.7/+51, hump +8.6–8.9, author's blip −32.7). I added one line for my window results (3/4-leaker PASS). Not closed: one run, not three golds.

## Goal fit

Pre-freeze red-team the integrator queued ("B12 is being redesigned from the requirement, then red-teamed again"); it shows the candidate's premise is wrong before it freezes — the gold path. PRINCIPLES: "Gates are frozen before the first run and never weakened after" and "Floats never decide them" (the ±3.6 platform swing at a 5 cutoff); a player's ship drifts or it does not — P2 "behaviours matter": the pooled fleet mean answers a different question than any ship's drift.

## What the author missed

- The original patch was lost (run.sh captured 0 bytes) and the shipped probe is a reconstruction; anchored rows reproduce byte-identical and the author's captured log preserves the originals, but the author's session left no reproducible artifact by itself.
- Rate-blindness (passes at 5×10⁴× the declared rate) and the fleet-wide no-leak PASS at −13.570 with "RESOLVED" sensitivity — both stronger and simpler than the minority split; found in the page's check-amplified lines and re-verified here.
- The window's lower edge (3 leakers of 16 suffice) was unmapped.
- The proposed per-ship fix (permutation-calibrated per-ship null) is designed but unbuilt — the next step, not this run's.
