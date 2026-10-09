Working...
Check complete. `lab/results/20261009-1210-inversion-c529/check.md` written: **Grade: silver**.

**What I did:**
- **Reproduced** from `work/patch.diff` in a clean tree: build 6 s, `control`/`heldout`/`audit` — every physics number bit-identical to the author's files (only wall-clock `secs` differs). `audit_check.py`'s independent Kepler solver confirms the E1 audited pair (d_min 1.836e-4 vs 1.779e-4, dump truncation; frozen order, 1.24 % of horizon sub-ρ).
- **Predictions verified**: `predictions.md` predates all result files; every pre-registered range held; the two soft misses are disclosed in the dossier.
- **Attacked** (own `attack.rs`, removed after; method embedded in check.md): I pulled the gold's dossier from `8d339c5` — its certificate specifies "**rebuild on overtakes**", which the author never tested. Since mean-longitude order is piecewise-constant between overtakes, rank at encounter time equals that watch: **H1 drops from 50.3 % missed to 0.0000 at k=4** — the horizon headline ("needs rank 42") binds only a t0-anchored watch. **E1 survives perfect refresh** (50 % of events, rank*=10; seed variant 43 %, rank*=12) — the frozen-order kill is robust. **M1** seed-robust (97.4 % cross misses at t0; cone 542/542 and 6000/6000 stand).
- **Novelty**: the gold's dossier flagged e-spread as an untested risk; no H entry measures it; the frozen gate ("gold run's scenes and a dense ring") would not catch E1/M1.

**Verdict**: two of three legs (frozen-order e-spread, traffic/trigger-blindness) are measured, reproduced, seed-robust, independently audited, and adoptable as gate scenes + bounds + per-pair ΔU classification. The horizon leg is overturned by the gold's own specified design. Silver; the one experiment to gold is rerunning the horizon leg against rebuild-on-overtakes and re-issuing the claim on the corrected legs. Tree restored to HEAD; nothing else in the run folder touched; no git operations.
