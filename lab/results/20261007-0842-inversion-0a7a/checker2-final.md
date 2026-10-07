Working...
Check complete. `check2.md` written; tree restored (patch reversed, scratch bin removed; only `lab/results/` untracked, as found; no commits, `check.md` untouched).

## Verdict: **Gold**

**Reproduction — exact.** Applied `work/patch.diff` to a clean tree, rebuilt, ran all 7 commands: every stored JSON matches field-for-field (churn 46/199/1373/1987 per body-orbit across the e-ladder, ev_p50=601, ratio 69.15, window_churn fractions, cone saturation 19900/19900, 0 missed; both O(n²) controls 64=64, 50=50). Only wall-times differ.

**Adversarial extremes (all confirmed the author):**
- e→10⁻⁹ at the same clump/bunch: churn **0.0** — the cost axis is eccentricity, isolated.
- nc ladder 100/200/400 (the author's dead nc=800 point): churn 26/46/82 → per-orbit work ~nc^1.8, upgrading their [INference] scaling to measured; the 69× ratio is nc-stable (66× at nc=100).
- The gold's actual uniform-λ fleet: churn 2.0/orbit — the gold's evidence was gathered where churn cannot appear; its bunched stress cases are the churning ones it never costed.
- Rank statistic stays ≤ 2 even at 234 encounters in a 5×-denser bunch — blindness is structural (Δλ ≲ ρ at contact).

**Fairness:** the churn×k×ev cost model is the gold's own spec ("rebuild on overtakes", n_c·k stored sections), not a strawman; my re-derivation of the cache escape gives 54 GB–7 TB at 10⁶ — the author's 0.9 TB is loose, but every reading is over the 8 GB machine. Novel: no HISTORY entry predates it; the adoption lives only in the taste log.

**Noted flaws (in the report):** the "244 encounters" tally is wrong (actual 203); P3's "marginal hold" is 0.017 vs a pre-registered ≥ 0.02; "the gold's own near-circular control" is really the gold's bunched stress config (its uniform-λ fleet is safe — conceded elsewhere in the dossier); and the unadjudicated tier-2 zero-window anomaly is flagged as the true first-in-queue experiment.
