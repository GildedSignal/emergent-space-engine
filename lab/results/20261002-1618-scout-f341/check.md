Grade: silver

**Abstract.** Claim: the 4× cut in kicks/orbit needs no new scheme in smooth regimes — plain leapfrog at 16 holds every gated behaviour — while higher-order splits and Gauss–Picard collocation are refuted there per kick; collocation wins only inside passages. I reproduced the whole suite **bit-identically** (33.5 s vs 36.2 s; `results.json` equal) and validated every truth with an independent RK4 (M2 precession agrees to 7×10⁻⁶; F1 ΔE to 1.2×10⁻⁴). Five adversarial cases — 500-orbit compounding, e₀=0.6, retrograde 0.45 R_H (inside B14), resonance at μ=10⁻³ (B17's edge), flyby at 3 radii — broke nothing: LF-16 precession 1.1–2.4%, pump 0.998 at μ=10⁻³, GP-4 0.14%/0.37% at 20 reads. Adopting LF-16 is one constant (`step_log2`), but the evidence is a float replica, single seed — one integer rung from gold.

## Reproduction

- `cd lab/results/20261002-1618-scout-f341 && python3 falsifier.py` in a clean copy: **every number in `run-log.txt` and `results.json` is bit-identical** (only `machine`/`elapsed_s` differ). 33.5 s on this 2-vCPU container vs the author's 36.2 s.
- `--smoke` reproduces the numbers recorded in predictions.md's pre-decisive amendment: GP-1-window 100.943% (killed), GP-3×4 0.668% at 49.00 kicks, Y4-12 1.219%/2.65e-2/3.9e-4 — all three match the recorded values.
- `work/patch.diff` is empty (0 B): the run edits nothing outside its folder; the falsifier is self-contained. Consistent with the rules.
- Implementations audited line by line: DKD with kick at interval midpoint and weight H in phase; GP charges s tide reads per sweep including the last, rebuild free; Y4 charges 3 kicks per macro; escape/e-dev/prec computed against an interpolated truth; B12-style Jacobi exponent is a log-fit of |J−J₀|. Accounting is honest throughout.

## Predictions

- `predictions.md` mtime 16:36:28 < decisive run 16:40:25 (`results.json`), with the smoke's kill recorded before the revised predictions. The ordering holds.
- Nit: `falsifier.py` mtime 16:39:45 — edited after predictions, before the decisive run (presumably the decisive case list; the file is untracked, so the pre-edit version is unrecoverable). The decisive artifacts reproduce from the shipped script and the scorecard matches, so I read this as the amendment's finalization, but it is not strictly provable.
- Scorecard verified against my reproduction: the four failed predictions fail exactly as recorded (GP-window-per-orbit 101%; LF-8 passes B14 at 5.6%; LF-8 stays inside B17; GP-3×8 costs 96 not 24–32) and the held ones held (flyby GP-4 ≤0.5%: 0.134%; Y4-12 <5% on M1: 4.43%) — except Y4-12 on M2 (5.79% vs <5%), which the author reported as "a hair over". Honest.

## Attacks (five)

1. **Independent RK4 truths.** The dossier claims a "dense RK4 cross-check" whose script is **absent from the folder** — so I built one. Correct RK4 on the same continuous ODE (planet term + direct + indirect tide): M2 truth precession +1.001901e-01 vs LF-2048's +1.001908e-01 (7×10⁻⁶ rel), e_max 0.303592 vs 0.303571, Jdrift 1.9e-7. F1: RK4 ΔE +1.560170e-01 vs LF-8192's +1.560362e-01 (1.2×10⁻⁴ rel). All truths are converged; every error in the dossier is against a valid reference.
2. **500-orbit compounding at LF-16 (M2).** Prec_err 2.36% (vs 0.89% at 120) — sub-linear, far under B14's 10%. Jacobi drift 3.5×10⁻⁴ with exponent +0.0017 (no secular growth) — but 3.5×10⁻⁴ exceeds the 10⁻⁴ B12 number if that clause were applied to this family. The e(t) deviation **grows steadily**: mean |Δe| 1.3×10⁻² (first fifth) → 5.0×10⁻² (last fifth), max 1.3×10⁻¹. Ungated, real, and it makes the queued correctors the natural companion at 16/orbit.
3. **Gate-envelope extremes.** e₀=0.6 at 0.3 R_H (beyond B14's births): LF-16 prec_err 1.12%. Retrograde e₀=0.3 at 0.45 R_H (**inside** B14's frozen envelope, untested by the author): LF-16 prec_err 1.62%, classification right; e_dev 0.126, Jdrift 1e-3. The margin survives both sides of the envelope.
4. **Resonance at B17's upper mass** μ=10⁻³, exact 2:1, 200 inner orbits: LF-16 pump ratio 0.998, amp ratio 1.016, regime matches — B17 holds at the strong edge, not just at μ=10⁻⁴ (even LF-8 scrapes in at 1.244). The author's caveat "seeds nearer the separatrix may need 32" is answered in the favourable direction at the mass edge.
5. **Sharper flyby, periapsis 3 radii.** Truth validated by ladder + RK4 (2.15343×10⁻¹, both converge). GP-4 at 20 reads: 0.136%/0.370% — B13-level; LF-16 fails (5.2%/5.8%), LF-64 passes. The passage result survives a sharper tide with sweeps still 5.

## Novelty

Nearest prior: H0190 (averaging tides cuts kicks 114×; 32.5 kicks/orbit unaveraged on low orbits) — a different mechanism and case family; it does not measure the plain split's step against B13/B14/B17. The board and HANDOFF pose this exact question ("the bigger lever is fewer kicks (GLM q-correctors)"), and nothing in HISTORY has measured the split at 16/orbit against the frozen gates, nor refuted higher-order splits per kick in the tide-cheap regime. GP-for-passages (IAS15's cousin, correctly cited) is new here. Not a redo.

## Goal fit

Board focus #1 verbatim. The 4× (8× if today's default `step_log2: 7` — 128/orbit — is the real baseline; `step.rs`'s doc says 1/64, `ctx.rs` default says 7) comes from deleting margin, not adding a component: "The cheapest compute is compute not done. Delete before optimizing" (P1); "A failed experiment kills that configuration, never the method" (P9 — the killed GP/Y4 configurations are recorded with their mechanisms). Kicks at 29 µs (HANDOFF) are the engine's dominant per-body cost, so this is the right lever.

## Why silver, not gold

- Real, reproduced, and adversarially robust — but the gold bar needs 10×, a deleted component, or a one-step adoption. This is a measured 4× (possibly 8×) on a **float replica**: single seed per case, 2D, Newtonian tide, no rebinding, no integer rounding, no changeover. The author says so and names the exact missing rung. The premise refutation ("a better scheme is needed" → wrong for smooth regimes) is genuinely valuable, but adopting it on the engine is one frozen-criteria rung away, not done.
- One revised held-out prediction failed (Y4-12 <5% on M2: 5.79%) — reported, but "the held-out predictions held" is not strictly true.

**The one experiment for gold:** the integer rung — B13/B14/B17 (and the B12 Jacobi clause) run on the engine at `step_log2` 4 and 5 on its own scenes, frozen criteria first, planted negatives included. If 16 passes on the integer law, gold and adoptable in the same step.

## What the author missed

- **The claimed RK4 cross-check has no script in the folder.** I re-did it; it holds (attack 1). Claimed evidence must be in the dossier's commands.
- **The secular e-walk at 16/orbit**: mean |Δe| quadruples from 120 to 500 orbits (attack 2). The dossier flags e_dev as a risk; measuring its growth was one cheap run and turns "risk" into a number — and into the precise case for the queued `q-correctors` at 16 rather than a return to 32.
- **Jacobi at long horizons**: 3.5×10⁻⁴ over 500 orbits exceeds the 10⁻⁴ the dossier itself quotes, though with a flat exponent (0.0017). Should be on the rung's watch list.
- **Retrograde births**: B14's envelope is half retrograde; all the author's moons are prograde. Mine passes at 0.45 R_H, but the rung's 256 seeds must include them (they will, if the gate is run as frozen).
- **The baseline ambiguity**: `ctx.rs` defaults to `step_log2: 7` (128/orbit) while `step.rs`'s doc comment says 1/64. If the plane truly runs 128, the cut is 8× and understated; either way the repo should say one thing.
- The M1 precession metric is degenerate (e crosses ~0.002; ladder non-monotone: LF-8 "beats" LF-16). Correctly demoted to smoke, but worth a sentence so nobody reuses it.
