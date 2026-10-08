Working...
`check2.md` written: **Grade: gold.**

Check summary:

**Reproduced bit-exact** — all four dossier commands in a clean tree (`patch.diff` is empty): A_gold_T4_s1 (1122 encounters, miss@4 35.1%→0% with P/4 rebuilds), B_e06_s1 (27, 96.3%, max rank 202), D_battle_s1 (inter-cluster miss@4 100%, max rank 129), geo correlations 0.994/0.998/0.998 — every number identical to the author's JSONs, controls PASS both ways.

**Truth independently validated** — my own oracle (dense all-pairs sampling, golden-section refinement, no KD-tree/ternary) finds exactly the probe's 27 sub-ρ pairs on B_e06_s1, dmin agreeing to 4.5×10⁻¹⁵; 2× finer slicing gives an identical pair set.

**Predictions held out and held** — `predictions.md` (20:02:04) precedes every result file (20:03+); P1–P4 all verified against raw data, kill criteria untriggered.

**Three adversarial cases** — all confirm and sharpen the claim:
- Aligned apsides at e=0.8: miss@4 = 0, max rank 3 → the fragility driver is **apsidal scatter, not eccentricity**;
- σ_ϖ sweep at fixed sig_a=10⁻⁴: miss@4 = 39% already at σ_ϖ = 0.02 rad → the safe domain is razor-thin and the a-concentration trigger stays blind at every point;
- the oracle cross-check above.

**Novelty** — the gold is recorded regime-free in board.md and HANDOFF:69; no H entry or doc bounds the certificate's domain.

**The one thing the author missed** (recorded in check2.md): "near-circular" overstates the safe domain — apsidal alignment is the load-bearing condition, which their own Δλ* trigger already absorbs. Raw-data nit: one "rebuild identical to the digit" exception (B_e08 max 244→245, miss rates identical).
