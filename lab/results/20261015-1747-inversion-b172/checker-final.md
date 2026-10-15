Working...
Check complete. Verdict written to `lab/results/20261015-1747-inversion-b172/check.md`, author's wiki page corrected in place, tree restored to the runner's clean state.

**Grade: silver** — the run's numbers are all real, but its headline adoption claim dies on the one axis it didn't fly.

**Reproduced bit-exact:** runner's regen (all anchors + identity OK); I re-applied `work/patch.diff` in a clean tree and verified the instrument is f55d's verbatim — belt ctl digests `5caeb1b6…`/`d3542eea…` match f55d's published branch, and the 7.226/6.953/1.000, 810,531-deficit anchors regenerate. `ES_LADDER_FORM` is env-gated; the belt path is untouched.

**My 12 adversarial flights (all digest-identical to their scene ctl):**
- K=1 mega-fleet (the author's own named counter-example): **1.004** at cap 4,096 — collapse holds, stronger.
- Seed 5: 1.016, bill 132,755 = f55d's belt seed-5 bill.
- N=2×10⁵ at matched cut: 1.011 at cap 4,096 — the collapse extends a decade in N.
- **Depth, 48k game-s (the un-flown edge): the claim inverts.** Formation reads **29.3×dem** at cap 4,096 (belt 48.5), promote compile 28.6 s vs 0.54 s, wall +106% over ctl — and the formation's 48k knee is the mint bill exactly (cap 273,200 → 1.000, 0 evictions). The registered expectation ("stays window-local at any depth") is falsified: past one wave period (~27k game-s) the wave recurrence re-imposes the one-demotion-wave reuse distance scene-invariantly, so "a few MB instead of 1.4 TB" holds only for concentrated episodes shorter than one wave recurrence. A fleet battle is a long-horizon workload.

Prediction audit: pre-registration credible (honest "lives, weakly" divergence), but P1's hit-fraction clause (≥0.85) failed silently at 0.786, and "26 flights" is 23 arms.

Page corrections: checker bracket with the depth numbers under the run's entry; the Refuted line scoped to "matched cut only"; open direction 5(a) marked measured-and-failed. Gold path: fold the depth arms into the run's own regen and re-scope the claim to the now-complete law — knee = re-read reuse distance, window-local under concentration within one wave, mint bill at depth in every scene.
