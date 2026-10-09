Working...
Check complete. **Grade: silver** — written to `lab/results/20261009-1210-constraint-c10d/check.md`; the tree is restored (patch reverted, no tracked files modified, nothing else in the run folder touched).

What I did:

- **Reproduced** in a clean tree with `work/patch.diff` applied: the 240-hauler run matched the author's **digest exactly** (195e4f72…), crossings 8.79 ms/frame at 299 bodies (author 6.51; inside their declared 4× box variance), engine share 5.2%, readouts 466 vs 465. Default run: body crossings 94.7% of the gather (the dossier's "97%" is 95.3% by its own totals — minor overstatement).
- **Predictions verified as pre-registered**: `predictions.md` mtime 12:22:46 precedes every sweep JSON (12:24:07+); the claims held (linear slope, ~0.1 µs/member, 1–2 warm readouts).
- **Three adversarial cases**: 960 haulers (1019 bodies — linearity holds at 4× the sweep, 17.4 vs 18.4 ms predicted, engine share falls to 3%); 240 haulers at rtf 1 (view cost rtf-independent, engine 1.2% with 0 kicks); 400 members (0.11 µs/member reproduces, but engine share is 28.7% from leaver rebinding — a workload counterpoint the dossier's "falls to 6%" omits).
- **Code read** confirms the mechanism: no dim/distance cull in the body loop, ≥1 readout per body per frame even warm, `ViewCache` already carries root + arrival-rate slope.
- **Novelty**: H0210 already recorded the gather at 83% of a light frame, and the b-readout-cost brief already noted growth with body count — so the premise-level dominance is prior knowledge. The new, reproduced delta is the decomposition, slope, ~10³-body ceiling, 150× members contrast, and the carry-the-crossing fix direction.

**Why silver, not gold**: the 10× gain from the proposed arrival-rate-carried crossing certificate is an estimate — nothing was built and its exactness is admitted unproven. The named gold experiment: build the carried crossing behind a flag, prove identical views across rtf/N, and show readouts per frame drop to ~per-change.
