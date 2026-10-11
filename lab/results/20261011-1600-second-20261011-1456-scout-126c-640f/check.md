Grade: gold

**Abstract.** Second author on silver 20261011-1456-scout-126c; the prior checker's named gold experiment is done. `python3 falsifier.py` (27 s) now regenerates every metrics key bit-for-bit (verified twice; E1–E6 bit-identical to the prior record; both orphaned keys live). The near-separatrix valley holds on the law's fixed dyadic cuts (base 32 + rungs to σ/2, σ from the complex root pair): oracle-verified ≤ 1e-6 for δ ≥ 1e-8 at ≤ 75 panels (m=2), log(1/δ) growth against adaptive bisection's 43→3765; valley kicks at δ = 1e-8 held ≤ 1.1e-7 where uniform panels fail by up to 0.25. My probes extend the claim: whole outer-plunge family L̃² 12.1–15.9, near-separatrix kicks, deeper endpoints — all hold. Cost: one sector extension of `crates/space` (b-plunge-tubes), endpoint trap documented in code.

## Reproduction

Clean scratch tree (the run folder's `work/patch.diff` is empty — no tree edits). I ran the falsifier from a copy in `/tmp` so the stored `metrics.json` was not overwritten.

- `python3 falsifier.py`: 27.4 s, exit 0 (then 27.2 s, 28.2 s). Every physics key **bit-identical** to the stored `metrics.json`; consecutive runs differ only in `machine`/`wall_seconds`. The only stderr is the recorded L=0 divide-by-zero (`degenerate f=inf A=inf`, stored in metrics).
- Prior-record identity, by the dossier's own command: `git show origin/claude/lab-20261011-1456-scout-126c:…/metrics.json` vs regenerated → `[]` (every prior physics key bit-identical: classification 730/0 with the same 40 undecided, all six accuracy sectors, negative control, near-radial incl. the L=0 refusal, horizon slopes, 24/24 kicks). `separatrix_valley_panels_to_1e-11` regenerates exactly (43/83/133/205/3765), now called from `main()`. `bound_control_apo_to_peri` is a live path (3 seeds); its old stored values were dead-path orphans (prior checker's finding, confirmed: the old block's `ev_plunge` at `r_end = r₂` can never fire on a tangential touch).
- Every number in the dossier's E7 table, E8 block and bound-control paragraph matches the stored metrics exactly (m=1: 32/41/47/55/61 panels at 5.0e-12/4.1e-8/1.7e-7/3.0e-7/6.5e-6; m=2: 32/47/59/75/87 at 5.0e-12/3.6e-8/2.8e-8/5.3e-8/7.0e-6; m=2 vs rtol-1e-13 truth 4.8e-12/3.6e-8/2.9e-8/4.1e-9/2.9e-6; kicks uniform 7.5e-4…2.5e-1 at δ ≤ 1e-6 vs ladder m=1 ≤ 4.9e-7 at ≤ 53, m=2 ≤ 1.1e-7 at ≤ 71; bound control 4.6e-10/8.1e-10/5.5e-8@8→4.4e-11@16, floor predicted 4.2e-7 vs measured 3.7e-7).

## Predictions

`predictions.md` mtime 16:16:36 precedes `falsifier.py` 16:46:12 and `metrics.json` 16:48:00. P-D held fully (the record). P-C held. P-A panel counts held approximately (32/41/47/55/61 vs ≈ 32/38/44/52/58 — the prediction missed the exact rung-count formula, `2(J+1)+1` not `2J`). P-A/P-B's ≤ 1e-9 accuracy targets **failed by ~2.5 decades** and are reported as failures with exact numbers; the pre-registered kill lines (≤ 1e-6 at δ ≥ 1e-8, ≤ 96 panels, valley-kick ≤ 1e-6) held everywhere. The m=2 measurement is marked post-prediction in the code. The failed accuracy targets are themselves evidence of genuine pre-registration: tuned predictions would have matched. This is the honest-failure pattern, not the 1-October pattern (a failure reported as held).

## Adversarial cases (mine)

1. **The whole outer-plunge family, not just L̃² = 13.** L̃² ∈ {12.1, 14.5, 15.9} at δ ∈ {1e-4, 1e-8, 1e-10}: m=1 ≤ 3.2e-7 at ≤ 63 panels, m=2 ≤ 3.0e-7 at ≤ 91 panels; at δ = 1e-10 the candidate tracks the oracle's own rtol-1e-13 shift (truth-limited, as claimed). L̃² ≥ 16 has no outer-plunge sector (Vmax ≥ 1) — physical, not a gap. The near-cusp L̃² = 12.1 is the tightest case: 8.4e-7 (m=1, δ = 1e-10), still under the kill line. The claim generalizes across the sector.
2. **Below the claimed domain.** δ = 1e-12/1e-14: candidate 5.6e-4/3.2e-2 vs oracle shift 2.6e-4/1.4e-2 — same order, confirming the dossier's "unfalsifiable below 1e-10"; m=2 panels 99/115 exceed 96 only below the claimed domain.
3. **Valley kicks from a near-separatrix bound orbit** (E²b = Vmax(1−1e-6)) at extreme phases f ∈ {0.05, 0.5, 0.95}, δ ∈ {1e-6, 1e-8}: uniform64 fails (4.0e-4…2.1e-1); ladder m=1 ≤ 4.2e-7 at ≤ 53 panels, m=2 ≤ 1.7e-7 at ≤ 71 panels. P7's domain statement survives a harder case than shipped.
4. **Deeper plunge endpoint** (r_end = 2.1): identical panel counts, errors 1.9e-7/6.3e-8 at δ = 1e-6/1e-8.
5. **Robustness claims**: m=4 gives 5.5e-8 at 115 panels (no gain over m=2's 5.3e-8 — "adds nothing" confirmed); safety=4 unchanged (3.02e-7); base=64 no gain (2.1e-7/6.8e-8). Rfun vs factored R agree to 2–3 digits through δ = 1e-10 — the predicted Rfun floor is indeed not the limiter.

## Novelty

The representation is the prior run's (not yet in HISTORY; standing limitation H-line "plunge orbits have no tube"; law.md's Darwin cos is bound-only; the prior acosh uses are Shapiro quadrature). New here and absent from the docs: the **fixed dyadic rung ladder** — B9's band pattern applied to distance-to-barrier-top in η, σ from the complex root pair, η(r_U) from the critical radius — replacing the prior run's adaptive float bisection (43→3765 panels, integrand-probing, not law-native) with a fixed function of (E, L). Plus the arccos/arccosh endpoint trap (η = −π, 0 by construction), a real finding for the b-plunge-tubes builder.

## Goal fit

HANDOFF names the live player-facing defect: "braking to rest above a planet gives `NoBoundOrbit` (plunge tubes, `b-plunge-tubes`)" — motion law v2 item 3, builder branch queued. This run also deletes the taste log's named silver-killer (5 October: "results that the shipped code could not regenerate") for this representation. Principle 19 holds in the strong direction: the valley fix is the law's own geometric bands on a new variable, not a new category; principle 13: same cuts ⇒ same error every evaluation — fixed by construction, not compounding. The 10× bar: 87 fixed panels vs 3765 adaptive at δ = 1e-10 (43×), and the adaptive method is unadoptable in principle (floats probing the integrand decide the cuts); the killed uniform-panel configuration is replaced, not patched.

## What the author missed

- The m=2 rung count is measured, not derived (self-flagged). Adoption does not hinge on it — m=1 clears every kill line across the whole family — but the builder should re-derive m from the panel-error budget as the dossier says.
- Author-final's "41–87 panels for δ = 1e-4…1e-10" silently spans the m=1 and m=2 columns; the dossier table is exact, the summary line is loose.
- Everything remains Schwarzschild, single-well; Kerr, γ ≫ 1 direct plunges and the L = 0 radial path stay outside, and the integer-side claims (bit-reversible carries, exact roots, no float floor in integer arithmetic) remain inference — the valley's δ ≤ 1e-10 behaviour can only be settled there.
- The valley evidence all starts at the turning point (`at_turn=True`); a plunge already in motion mid-valley (a kick landing below the barrier top) is covered by E8 only for kicks from bound orbits — the deep-flyby analogue is untested.
