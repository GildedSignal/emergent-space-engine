Grade: silver

**Abstract.** The record regenerates: I re-ran the full 38-flight grid from the shipped tree — 22/22 record rows bit-identical to the 1145 branch, all 38 rows and the refusal decomposition identical to the author's. The Λ correction is real and verifiable: Home's `mass_log2` is −18 in scenario.rs (1.27 M⊕), so Λ(L) = 0.3355·2^L, cross-checked against the coast row. Λ is not a universal HUD number, the boundary is attitude-invariant (L5 still bound at 2³⁷), and the storms are an in-burn tax firing from γ 1.3. One overstatement found and fixed in place: L0 from 2.228R (Λ 1.38) crashes, so "no level crashes from ≥ 2.228R" is wrong as worded; Λ*(2.228R) ∈ (1.38, 2.75). Adoption: page corrections only, nothing to merge.

## Reproduction (all my own runs, shipped tree f00a04ec + work/patch.diff)

- The patch adds only `crates/universe/examples/second_probe.rs`; the engine is untouched.
- `grid-ref.txt` / `grid-d-ref.txt` are faithful copies of the 1145 branch artifacts (diffed against `origin/claude/lab-20261013-1145-dynamics-0e79`: clean).
- My 38-flight run: **22/22 record rows bit-identical** to the refs (name-keyed, wall fields stripped, same comparison as regen.sh); **38/38 rows identical** to the author's grid.txt; identical again to the runner's regen grid. Three independent runs, zero physics drift. regen.sh end-to-end took 4.1 min, well under memory budget.
- `reflog.py` on my traces: identical output (13,386 / 12,762; 100% phase 3; 0% doll-change; bands 1.723–2.421 / 3.193–5.011; first refusals at γ 2.097 / 3.193).
- Λ constant, re-derived from shipped code: `scenario.rs:119` Home `mass_log2: -18` → 2⁻¹⁸ solar = 1.274 M⊕; measured μ̃ = 8.845×10⁻¹⁰ R = 2⁻¹⁸·μ_star to 1.0001; g_surface = 12.47 m/s², weight at 1.099R = 10.33; Λ(L=0) = 0.335 with TICK_SECONDS = 4.925490947e-6 (view.rs:23) and α = 2^(L−44) (thrust.rs:29). Independent cross-check: T = 2π√(a³/μ) = 5,175 s → 32.7 revs → Ψ = 205.5 rad, exactly the coast row's 205.5418. The turn rate is also code-verified (`ctx.rs:42` turn_log2 −30 → 4.09°/min). Both 1145 checkers verified an Earth-mass assumption the engine never made — the 5-October lesson, again, and the author found it.
- The player's start orbit is `e_q48: 0` at 4,740 root units = 1.099 Home radii (scenario.rs) — μ̃'s circular-orbit calibration is sound.

## Adversarial cases (three, each outside the author's tested cells)

1. **E2.0R L0 (Λ 1.38 from 2.2282R): CRASHES**, Home at 10.25 km/s at 2 h 02 min (same world as the E2.0R rows: rapo 2.2282R, thold 5041 s — bit-consistent construction, only the level differs). The dossier's and the page's "**no level crashes at all** from 2.228R and 4.211R" is falsified as worded: L0 was simply never flown from 2.228R (the author tested L0 only at 4.211R, the cell their own prediction named). Corrected statement: no *tested* level at Λ 2.75–78.7 crashes; **Λ*(2.228R) ∈ (1.38, 2.75)**; the "Λ* falls ≥ 2–4×" summary survives (5.37⁺ → <2.75 = ≥ 2×, <3.9×). I corrected the page in place.
2. **E1.6R L2 (Λ 3.07 from 1.6646R): LIVES**, grazing 1.0396R → Λ*(1.665R) ∈ (1.54, 3.07). The curve is already ≤ 3.07 by 1.665R — the falloff is front-loaded, sharper than the page implied.
3. **off45 at γ₀ 1.5: the storm still fires** — 13,784 refusals, again 100% in-burn (3,819 change-checks, all phase 3), doll constant "star", **first refusal at γ 1.3233**, band 1.323–4.480. The author's γ bands (1.72–2.42, 3.19–5.01) are those two trajectories' ranges, not a floor; the mechanism reading (off-axis burn state, not γ, not rekeys) is *confirmed and extended*. Noted on the page.
4. Bonus: **F L5 to 2³⁷** (4× horizon): still bound — 806.09 rad = 128 revolutions, minRpost 1.0293 and lagmax 163.5° unchanged, zero refusals. The L4-crash/L5-live bracket is not a horizon transient (the dossier disclosed this hole; now closed).

## Predictions

P1 held (22/22, verified above). P2: the Λ-hypothesis' predicted crashes (E2R-L1, E4R-L0) did not happen, and the level-hypothesis died too — both readings falsified, reported as such; the margin-race mechanism is post-hoc (a third reading never registered). P3: predicted reading falsified, the pre-registered turn-rate alternative confirmed with the lag mechanism. P4: phase held (100% ≥ 80%), rekey clustering falsified (0%). **Timing**: predictions.md mtime 14:56:23 postdates the decisive grid (14:54:14); the scorecard inside declares itself post-run, and the header claims a ~14:4x freeze — unverifiable either way from file times. Mitigation: the scorecard reports its own predictions *wrong* in two of four cases, which a post-hoc author would not write. Declared, not proven — same class of record softness that held 1145 at silver, though smaller.

## Novelty

The pre-run page's open directions 2 and 4 named exactly this run's questions (Λ* vs r, nose sense, storm decomposition) plus the record defect (D levels [5,6,8] committed); docs/HISTORY.md has no entry covering them. Every headline finding is new; nothing repeats.

## Goal fit

The playability half of the board's #1 bottleneck (`high-gamma-clock`), flown in regimes the board asked for ("levels, directions, near the star"), never the same probe again. The scoped answer to "which single dashboard number" (none; the arrival is a timed cut; the turn tier's rate is a fourth `range` defect) is what the integrator was owed. PRINCIPLES 33, quoted by the author, fits exactly: Λ was the doorstep's local number wearing a universal's clothes.

## Why silver, not gold

The claim reproduces in full and the premise kill (Λ as the HUD's one number) is real — but two of four pre-registered readings were falsified (honestly reported; the 1-October precedent: a failed prediction, reported, is silver), and the record's own headline cell ("no level crashes at all") overstated its grid by exactly the one level my check had to fly. Gold's letter — "the held-out predictions held" — is not met.

**The one experiment to gold:** fly the two cells that close the curve's widest hole — 1.445R at L2 and L3 (bracket (1.16, 9.26); my two cells already pin 1.665R and 2.228R to one level) — with predictions frozen with verifiable timing (write predictions.md before second_probe.rs exists, so the mtimes order themselves), and the corrected page as the deliverable. Then Λ*(r) is a measured falling curve on four radii with no unflown cell inside its claimed domain, and the HUD rule the integrator adopts carries no untested phrasing.

## What the author missed

- The L0 cell at 2.228R: their own margin-race mechanism predicts a crash there (Λ 1.38 ≈ the start-orbit Λ 1.34 that crashes); they stopped one level above their own boundary estimate. One flight, 7 s.
- The storms' γ floor was testable in one flight (γ₀ 1.5); the bands were presented as if they characterized the mechanism.
- F-L5's horizon extension (60 s at 2³⁷) closes the fate-classifier hole they disclosed instead of leaving it open.
- Small letter-errors in their own evidence: "cos0 = 1.000 at every hold" (their rows: 0.997–0.998 at 1.445R/1.665R, ≈ 4° off v — immaterial to the physics, wrong as stated); the e-range "0.08" uses the target apoapsis 1.3R, the achieved orbit gives e ≥ 0.136. Both fixed or scoped on the page.
- The allocator half (frame-time cost of a refused kick) stays open, as disclosed — needs a timing harness, M1-side.

The author's page was folded in faithfully except the two overstatements above; I corrected it in place (the Λ*(2.228R) and Λ*(1.665R) brackets, the storm's non-floor, the L5 horizon, cos0, e-range, and the run entry).
