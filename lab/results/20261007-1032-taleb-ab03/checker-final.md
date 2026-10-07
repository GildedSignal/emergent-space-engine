Working...
Check complete: **Grade: silver** — `lab/results/20261007-1032-taleb-ab03/check.md` written; nothing else in the run folder touched, no git operations.

**What held under reproduction and attack:**
- `hlive_probe2.py` reproduced every row of `hlive2.json` bit-for-bit (22 s); dt-halving matches `dtcheck.txt` (median |ΔE| 4.325e-3 at both dt, hyper 94→104).
- Held-out seed 20261008: all headline figures generalize (109.1 vs 108.8 mean bits at 20 yr, p99/mean 1.13, hyper 2.1%, within-Hill 7.1%) — population properties, not seed artifacts.
- predictions.md (10:38) genuinely predates v1 (10:41) and v2 (10:44). Novelty confirmed: HANDOFF lists H_live as "not measured yet"; B18b's churn quote is verbatim from the frozen gate.

**Why not gold:**
- The dossier's "measured ≈ 0 bits at 1 play-hour" contradicts its own JSON (the 1-phr row measures 69.67 bits; it's void, not zero — the session-survival claim holds by construction of orbit-averaged kicks, not by measurement).
- My probe contradicts the stated absorption mechanism: (a, synodic-phase) bin medians absorb only 5.1% of dE variance (null 0.8%) — the drift is carried by per-body free eccentricity, not shared synodic state.
- `control_mu0_scarred: 0` is hardcoded in v2 (`if False else 0`), not measured; within-Hill's dt sensitivity (293→301) unreported.
- The deciding quantity — machinery vs irreducible bits — is open; the named gold experiment is the author's own secular-shadow twin, which my phase-locking result makes mandatory rather than optional.
