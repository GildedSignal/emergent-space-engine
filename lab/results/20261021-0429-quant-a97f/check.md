Grade: silver

**Abstract.** Claim: the calendar's post-mixing worst-window excess is neither shear-neighbourhood nor step lattice but the dues' marginal non-uniformity plus phase-locked pairs, both a ~10²-fire transient. Reproduced identically (clean-tree patch + regen; my independent iid floors 1.375/1.176; my own seed-1 flight bit-identical to the author's series through g=40). Held-out attacks: at seed 2 (2,700) the mechanism holds (excess 0.166, calibration 1.612/1.610, |Δa| −8%, 0 collisions) but the "+0.13 N-flat pairwise part" reads +0.00 — the split is seed-dependent; my engine flight to g=49 confirms the decay onset (plateau 1.59–2.11 through g≈37, then ≈1.44, p99 ≈ floor) but not the fire-100–120 floor endpoint. The N-growing-tail premise is dead; the 10⁹ worst-frame line may quote Poisson outside the priced epoch. Adoption cost: none (ledger text; stagger already flight-proven).

## Reasons

**1. Reproduction (clean tree).** Applied `work/patch.diff` to the restored tree, rebuilt, and confirmed the runner's regen numbers against the dossier, the JSONs and the logs: floor 1.375 [p10 1.280, p90 1.470] vs measured late 1.720; A6 1.564 / A0 1.707 / A1 1.588 / A5 1.564 / A2=A3 1.707 / A4 1.375 (control lands on the floor); 11,700: 2.230 / 1.904 / 2.035 / 1.182, and D5 reads 1.83 at g=20 — the 45c0 checker's number exactly. Calibration pred/meas 1.801/1.790 at 2,700. evolve.py reaches 1.304 by fire 120. My own iid-uniform floor recomputation (different rng) reproduces 1.375/1.176 exactly. evolve.py's 1.03·step_med spacing vs the flight's 1.03·step_max is immaterial: with ceil(spacing/s)=2 for the bulk, the per-fire relative slip is 2·(sᵢ−sⱼ), independent of the offset. The A6/A5 arms correctly isolate the dues marginal (bootstrap and permutation agree).

**2. Predictions.** Genuinely pre-registered: `predictions.md` (mtime) precedes `analyze.py`, the counterfactual outputs and the dossier; the flights were still running. P1/P5 held; P2/P4 failed and are reported as the finding (the author's own prior died — not post-hoc framing). P6 honestly revised.

**3. Attack (my cases).**
- *Seed 2, belt 2,700, g≤33 (outside the author's domain — one seed per N was the named hole):* the mechanism verdicts survive (marginal-dominant, no shear: cf|Δa| 0.2650 vs rnd 0.2875; no lattice: 0 exact collisions, jitter null; A4 on floor; calibration 1.612 vs 1.610), but the total excess halves (0.166) and **A6 = A0 = 1.541: the pairwise part is +0.00**, against the dossier's standing "+0.13". The split (57/43) is a seed-1 reading; only "never N-growing" is robust.
- *Engine flight, seed 1, to g=49 (half of the author's own named closing experiment):* plateau 1.59–2.11 flat through g≈37, then engine-side decay to median 1.44 at g=44–49 with p99 1.33–1.35 ≈ floor p99 — inside evolve's fire-matched band. Decay confirmed; **floor endpoint not reached by g=49 and stays model-extrapolated.**
- *Numbers differing from the dossier text:* persistent pairs "637k" vs 403,708 regenerated; cf |Δs|/s 3.9×10⁻⁴ vs 3.47×10⁻⁴ (ratio 40×, not 36×); "72% <10⁻³" vs 74.9%/87.5%; "C50(dues) 1.19–1.22 flat g=25–40" vs full range 1.06–1.25; evolve mid-band "1.47–1.66" vs 1.33–1.78 (the dossier's own caveats admit the last). Same orders, same verdicts; the page is corrected in place.

**4. Novelty.** The standing page's od 4 priced exactly this question (opened by 45c0's checker); no prior attribution of the excess exists in the wiki (grep: max/μ, worst-window, near-locked appear only on calendar.md) or docs/HISTORY.md. The instrument and the baseline flights are 45c0's, credited.

**5. Page.** Corrected in place: seed-scoped pairwise part, engine-decay note, the number fixes above, od 4 remainder updated; current best compiled to three blocks (≤15 lines; was ~99), total ~120 lines.

**6. Goal fit.** Prices the 10⁹ worst frame on the macro row and P12 ("i care about the p95/99 results i want the game to be smooth"); the epoch is derivable from the birth census — "Nothing is evolved that can be derived when looked at". Deletes the unbounded-tail caveat; no engine change to adopt.

## The one experiment for gold

The engine flight to g ≈ 120–145 at two seeds (~2×11 min): it closes the floor endpoint (the decay epoch past g=49 is model-extrapolated) and simultaneously re-splits marginal/pairwise at matched mixing depth, answering the seed-2 100/0 reading. Both halves of the headline then stand on engine evidence.

## What the author missed

- The split and the plateau's magnitude are seed-sensitive — one seed per N, and the "+0.13 pairwise" is presented as a standing component when a second seed reads zero.
- The named closing experiment (engine flight to g≈120, ~11 min) was left unflown while well inside the run's own wall budget.
- Dossier-text drift from the regenerated JSONs (637k, 3.9×10⁻⁴, 72%, C50 flatness) — each small, but the rules say the shipped code regenerates every number.
- The proposed page grew current best to ~99 lines against the 15-line budget instead of compiling the prior standings down.
