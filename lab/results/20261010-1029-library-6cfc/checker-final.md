Working...
Check complete. `check.md` written to the run folder; nothing else touched there.

**Grade: silver.**

**What I did:**
- **Reproduced** both probes in a clean tree (empty `patch.diff`): every number bit-for-bit — skin table (metric formation 300–809 pair-evals/kick/body vs belt 2.5–16; phase k=4 flat at 3.0) and B12 table (mean AUC 0.967 vs max 0.920 at T=1000; both ≈0.50 at T=100). Both scripts run in 13 s total, far inside the 60 s rule.
- **Verified pre-registration** by mtimes: `predictions.md` 10:34, probe outputs 10:50; predictions describe the v1 design (N=2,000, m≤5), the shipped probe differs — no retrofit. All six practitioner quotes found verbatim in `readwise.json`.
- **Attacked** with 9 skin + 6 B12 cases. Every one *supports* the claim: a station-kept formation saturates the metric skin at **996–999** pair-evals (the author's 300–809 is a transient average — their fleet shears apart mid-run); mild 5× packing already saturates; phase-rank holds at 3.0 even under 10× rate churn; mean-slope beat max in all six B12 variants, including the rare-large-jump case built to flip it.
- **Novelty:** HISTORY's "Verlet" hits are unrelated integration experiments; no prior phase-rank/slack-skin/window-mean entry. But the board's 6 Oct gold (taleb-09b5) already adopted the phase-neighbour rank-4 certificate for the window tier — this run measures the same disease one layer down, plus the m-insensitivity sweep and the B12 statistic choice.

**Why silver:** the remedy is an adopted certificate transplanted one layer down, measured only on a synthetic 1-D ring; two registered predictions were falsified (honestly reported, but gold's bar is that they held); the B12 half never touches the plane's real error trace. The gold experiment: the same comparison in `crates/encounters`' own harness on a station-kept taleb-09b5 formation, counting setups and pair-evals end-to-end.
