Grade: silver

**Abstract.** Claim: the cone tier, the fleet phase-rank certificate and the concentration trigger are one rule — `cone ∧ wrap(Δλ₀) ≤ |Δn|(1+3ē²)H + 5(eᵢ+eⱼ) + skin` on one U-sorted scan. All shipped results reproduce bit-for-bit (`truth1`, `truth2`, `sweep`): recall 1.0 on every scene, candidates 20–40% below cone-only, no regime boundary; I regenerated the unshipped scale fractions (0.72 / 0.22 of C(N,2)). But the shipped index is falsified: on a constant-p, bimodal-e belt (H=16) it misses 66/495 true encounters (recall 0.867) while the naive per-pair rule keeps 1.0 — the U-bin drift window cannot see Δn from Δe at fixed U. Adopt the rule, not the index; the deletion of the trigger and fleet category is worth having before the crate builds them.

## Reproduction

- `python3 exp.py truth1|truth2|sweep` in the shipped tree (no patch to apply): all three jsonl files **diff-identical**. Times 26.9 / 41.9 / 94.9 s (the sweep exceeds the dossier's "≤ 80 s"; trivial).
- `work/patch.diff` is 0 bytes and `run.log` is 0 bytes; the folder is untracked in git. The dossier's claim that the falsifying run (the 3(eᵢ+eⱼ)→5(eᵢ+eⱼ) correction) "is preserved in git history of this folder's patch" is **false as shipped**. The correction itself is disclosed and derived (4e+2.5e² ≤ 5(eᵢ+eⱼ) for e ≤ 0.4), but the belt rows reporting it were produced after tuning on belt failures.
- `scale.jsonl` is regenerable by **no** shipped command: `exp.py scale` runs N=2500/10000 belt+mixed with different fields; `scale_quick.py` has no `e0` parameter and different fields again. I regenerated the rows myself (mk_fleet variant, e0 ∈ {0.02, 0.002}): cand fractions 0.718 and 0.223 of C(N,2) — the dossier's 0.70/0.22 are right, so the physics stands and only the record is broken. This is exactly the "numbers the shipped code cannot regenerate" defect the taste log demotes for.

## Predictions

`predictions.md` predates the results (mtimes: 24 m → 10/9/7 m). Held: recall 1.0 everywhere including held-out sweep points, mixed, uniform-e, H=16; the ideal-trigger collapse on fleets is a confirmed falsification of rank-4 portability. **Two failed predictions are not reported as failed:**
1. "unified pair-evals per true candidate stay within 3× of the ideal-trigger everywhere on the sweep" — measured 36–96× (unified 209k–293k evals vs ideal-trigger's constant 3,062).
2. Prediction 5: "unified candidates per body grow ≤ ~√N·log" — the author's own scale rows show **linear** per-body growth (185/body at N=512 → 752/body at N=2048, e0=0.02, fixed arc); the dossier reframes to "the fraction, not the exponent, is the gain" without flagging that the prediction said otherwise.

## Adversarial cases (mine)

1. **Index ≠ rule.** The naive per-pair rule brute-forced over all pairs vs `unified()`: the index **drops** 9 (belt), 11 (mixed), 0 (fleet) rule-passing pairs. The code's core claim — "the index is acceleration only; the emitted set equals the naive per-pair rule" — is false on the author's own scenes.
2. **Killer scene** (const-p belt: all bodies share p exactly, e ∈ {0.05, 0.35}, H=16, uniform ϖ/λ): `unified()` recall **0.867** (66/495 true encounters missed; every miss has dU = 0, Δn = 0.174, wrap(Δλ₀) ∈ (2.0, 2.9) — inside the per-pair sweep, outside the bin window). Naive rule recall 1.0 on the same scene. Cause: `n = (U(1−e²))^1.5`, so Δn has a Δe component that U-distance cannot bound; the bin drift term `2.4·d_bin·H/Ū` silently assumes Δn ∝ ΔU. A milder const-p/uniform-e/H=8 scene survives by luck (3,699 pairs dropped, none true; expected yield ~7 misses, got 0). The zero-miss certificate of the *shipped method* is therefore unsound; the *rule* is not implicated.
3. **The rule survives everything I threw at it:** belts e ∈ [0.25, 0.4] (edge of the claimed domain) and e ∈ [0.4, 0.55] (beyond it): recall 1.0. Apse-anti-aligned fleet, full-circle phase (the author's named unmeasured case): recall 1.0, and the one workload where unified genuinely wins (cand 22,487 vs cone 130,816, evals 30,681 vs 130,816). Truth at T=8192 vs 1024 (belt N=256): zero new true pairs; recall 1.0.
4. **Strawman check on ideal-trigger:** not a strawman. Oracle labels are given (the trigger is perfect), rank 4 is the constant the board actually adopted from taleb-09b5, and the argument that widening rank to stop missing converges to unified-plus-a-sort-and-trigger is sound, though unmeasured.

## Novelty and goal fit

- `docs/law.md`#39 (encounters crate design) has the Binet cone plus continued-fraction timing; the board carries the two-tier certificate (q-candidate-degree) and the phase-rank-plus-trigger (taleb-09b5, gold). The single continuous window replacing the trigger and the second structure is new; no HISTORY entry covers it.
- It targets the board's top scaling risk and deletes components before they are built ("prevents a component rather than replacing one" — the cheapest adoption). PRINCIPLES 4 ("no categories: regimes are chosen by dimensionless numbers") is genuinely better honoured by a per-pair inequality than by a trigger. But there is no 10× anywhere: candidate fractions 0.2–0.7× of the cone tier, evals 0.4–1.5×, and the O(N²) exponent at fixed distribution is unchanged (the dossier says so honestly).

## The one experiment that would make it gold

Repair the index so "acceleration only" is true: bound the bin-pair drift by Δn's full dependence, `|Δn| ≤ 1.5·n̄·max|Δ(U(1−e²))|` from (U, R) extremes of body and bin (or clamp per-bin e-spread), then show **emitted set = naive rule** on the const-p/e-spread adversarial class and re-run the pre-registered scenes with the corrected 5(eᵢ+eⱼ) constant fixed a priori on fresh seeds, plus one shipped command that regenerates `scale.jsonl`. Zero-miss must belong to the structure, not only to the formula.

## What the author missed

- The binned index is itself a second certificate with its own window — the very category the run set out to delete — and its window is unsound (Δn's e-component). The 9–11 dropped pairs on the author's own scenes were visible to a naive-equivalence check that was never run.
- Two failed predictions went unreported; the record carries a false provenance claim (git history) and an unregenerable evidence file. The work is better than its record, but here the record is the deliverable.
