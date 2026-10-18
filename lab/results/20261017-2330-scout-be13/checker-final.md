Working...
Check complete. **Grade: silver** — written to `lab/results/20261017-2330-scout-be13/check.md`, with the author's wiki page corrected in place.

**What held:**
- **Reproduction:** both scripts rerun in a clean tree — outputs bit-identical to the shipped `.out` files (and to the runner's regen).
- **The headline:** the galaxy Φ program genuinely passes at 256×1024 (smooth med 0.0028/p90 0.0062 vs the 0.008 bar), ~h² convergence, N-weak residual, 2.6×10⁵ numbers flat in N. Novel: the handoff page itself named this the "unmeasured half"; HISTORY's galaxy work is another era and question.
- **My probes extended it:** the clustered lab-scene shape — the run's own named open experiment, unrun by the author — **passes** at 256×1024 (0.0014/0.0031); 3 fresh seeds all pass; the eps–grid coupling survives with corrected constants.

**What broke (why silver, not gold):**
1. **A third, uncaught instrument bug inverts a shipped claim.** `confirm.py:21` sets the COM program's radial extent to `R_MAX` (5.0) instead of `log(R_MAX)` (1.61) — 1.61× coarser bins on 62% of the rings, visible in the author's own output as the cells_used mismatch (148599 vs 221937). On matched bins, COM centring is **better at every grid** (0.0372/0.0087/0.00094 vs 0.0388/0.0115/0.0028; p90 passes at 256×1024). The adoptable sentence "mass at the geometric centre, never the COM" is backwards — adopting it gives away 3×.
2. **"m ≤ 4" overstates:** at the passing grid m≤4 is median-only (0.0077, 4% headroom) with p90 ≈ 2× the bar; the measured pass is the full-azimuth program.
3. Two of four held-out predictions failed (honestly reported); inner-disc p90 (0.013) is over the bar — the tested annulus was the easy middle.

**Page fixes:** Domain sentence corrected, Open-directions 5 rewritten with the inverted-claim correction and checker evidence, and the accidentally **deleted** `f666` Runs entry restored (append-only violation). The one experiment to gold: rerun the dials on the one-line-fixed instrument and fold in the clustered/seed cases — everything I measured says it lands favorable.
