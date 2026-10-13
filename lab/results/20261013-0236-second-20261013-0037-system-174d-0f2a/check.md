Grade: gold

**Abstract.** The silver's named experiment is done and the lever survives it. Re-priced with the law's own tide cadence (`plan_interval`'s `want` before the thrust clamp; probe verified — `clock_full` equals `step` on every coast kick), the tide behind a burn costs 0–24 events against 377–1,085 burst kicks (45–377×): paced 8 s L8 6 / L12 23 / L15 24 / brake 5 / turn 1, reproduced digit-for-digit in demand mode (3/16/24; worst frames 42/579/1,036) and on seeds 7 and 3. The fixed-granularity inversion was the coast divisor's artifact: on the dive the burned conic is an escape passage and the law's cadence coarsens to ~2³² ticks. Gain: burst items drop ~45× at every level. Adoption: the integrator's carry-the-burn build, priced.

## Reproduction

- Clean tree, `git apply work/patch.diff`, build (~10 s), re-ran the batteries myself (the runner's regen.log: exit 0).
- Demand 4 s bit-stable: law-cadence 3/16/24; worst frames 42 (frame 62) / 579 / 1,036; fixed-granularity 30,721; closest approach 9.680×10⁷. Paced 8 s seed 1: 6/23/24/5/1 events vs 636/897/1,084/404/377 kicks (author's 1,085 at L15 — the disclosed ±1 wall-clock variance of paced counts); per-window budgets median 8.687×10⁶, max 1.490×10¹³ at L15, identical across seeds 1/7/3.
- Derived numbers not printed by regen.sh, recomputed from a fresh full kick record: tide/burn ratio medians 4.49×10⁻¹⁰ / 2.82×10⁻¹¹ / 3.52×10⁻¹² (L8/L12/L15) ✓; plunge tail max 1.517×10⁻⁴ ✓; top-149 tide kicks = 100.0% of the 1.558×10¹³ sum ✓; γ at the dive 1.027, r 9.375×10⁷ ✓; dive clocks ~5.5×10⁹ ≈ 2³²·³ (step_for's `Passage` duration branch) ✓.
- Probe is counters-only (env-gated; `probe_clock_full` is a pure `step_for` recompute); `plan_interval` clamps exactly as the dossier describes.
- `predictions.md` (02:53) predates all four saved records (02:55–02:56) and the dossier (03:01); the smoke-test familiarity of the 4 s counts (2/11/24) is disclosed. P1–P5 all held; P1 at 100% (law-bound kicks 0 in every flight, every run I made).

## Adversarial cases (mine)

1. **Paced 16 s seed 1** (2× the author's longest flight, outside the tested range): forward L15 still 24 events vs 1,167 kicks (49×); reverse L15 brake 23 vs 969 (42×); the count saturates after the dive, as the escape-transit reading predicts. L8 grows 6→24 over 16 s (the burn keeps running; events accrue at the coarse cadence) — still 29×. No inversion anywhere.
2. **Reverse L15 brake paced 8 s** (untested level×direction, deepest dive): 23 events vs 969 thrust kicks, max window 1.87×10¹³, law-bound 0. Holds.
3. **Keys re-asserted every frame** (the real-client pattern, previously tested only at L8 demand): forward L15 composition unchanged (kick0 1090 / boundary 1089 / open 0; 24 events vs 1,085 kicks — decides add 421, outside the burst). The brake-to-plunge path under re-assertion opens deeper dolls (kick1+ 1328, open 483) and still prices 23 events vs 2,200 kicks.
4. **Seed 3**: 24/23/7 events, budgets identical to 3 digits.

## Novelty

docs/HISTORY.md has no waterfall or law-cadence entry; the frame-cost page held the silver's fixed-granularity counterfactual with the checker's inversion. This run does exactly the previous checker's named experiment and corrects the standing record: the plunge-adjacent strong-tide kicks — which the silver's lens called "exactly where a tide-carry law must keep its own events" — are where the law's own cadence is *coarsest*. That is a premise correction, not a repetition.

## The page

Fold-in faithful: the re-priced counterfactual replaces the inversion with the mechanism, the tide/burn range is honestly re-scoped (median 10⁻¹⁰…10⁻¹², plunge tail 1.5×10⁻⁴), direction 2 now names the adoption residues (word margin at readout, the ~10¹³-quantum periapsis window against the B-series gates, the read side), the seven publish conflicts are resolved keeping main's superseding text, and the new run line is appended. I corrected one defect in place: a literal `({RUN})` placeholder at the end of the waterfall block (now the run id). The 32ab/64e4 run-line dedup removes only exact duplicates, no run id dropped. Not three agreeing golds — topic stays open.

## Goal fit

Moves `frame-cost` open direction 2 and prices the lever the integrator's item 2/3 builds target. PRINCIPLES: "Compute only surprises … Nothing is evolved that can be derived when looked at" (3) — the burst is the burn's own solvable ramp chopped into word-sized rebinds; "you don't advance a ship tick by tick you just map where it wants to go" (14); "Store the generator, not the generated" (6).

## What the author missed

- The "149 deep kicks contribute 0.02 of the 24 law events" number is definition-dependent: under the per-kick integral the same kicks contribute 0.39 (one transitional mid-flight kick with a momentarily fine clock, dt/clock 0.375); 0.02 is the plunge-window share (tick span 1.0×10⁸ over the 5.5×10⁹ window). Both ≪ 1 event, so the conclusion stands, but the dossier presents one definition as the number.
- regen.sh's `grep -v "^kick tick"` strips the record the two derived numbers (ratio medians, 149-kick decomposition) come from; they regenerate only if the grep is dropped (I did). Everything else regenerates from the summary alone.
- The scoped claim "~0–25 tide events per burn, set by the dive" holds for the tested ≤8 s flights; at 16 s an L8 burn accrues 24 (linear in burn duration, not dive-set) — the page's domain line (2–8 s) already covers this honestly, but the phrasing invites over-reading.
