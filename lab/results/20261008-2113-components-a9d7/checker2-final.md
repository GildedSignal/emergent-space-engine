Working...
Check complete. `check2.md` written; worktree restored (0 modifications outside `lab/results/`).

**Verdict: gold.**

What I did:
- **Reproduced bit-exactly**: applied `work/patch.diff`, rebuilt, reran all four cases — digests identical to the author's summaries; the author's own `shrink.py`+`analyze.py` on my clean rerun returns every dossier cell (85.91 bits/kick, 103.74 net bits, +2.035/doubling, 34.18 carry bits, 1,497.5 B/body).
- **Verified the instrument's premises in engine source**: sub-quantum kicks genuinely fire nothing (`step.rs:374`); zero dv=(0,0) rows in the data; merged double-fires preserve the net deviation exactly.
- **Four attacks, none broke it**: eccentric belt e≤0.9 (rate 3.6e-5, 87.1 bits — holds), N=2048 (3.6e-5, 87.4 — extrapolation to 10⁹ stands), lattice requantization control (86 → 17.9 bits at σ/100 — the causal mechanism confirmed on the author's own data), full growth-curve refit (concave, monotone, +2.0/doubling fair).
- **Novelty**: HANDOFF listed H_live "not measured yet"; the inversion (rate affordable, lattice fatal) is new.
- **Predictions**: pre-dated the runs (timestamps); 4 of 8 missed, all disclosed — and the misses are the finding.

Recorded misses: the lens brief's `xtask --bench`/dashboard integration was not built and the deviation not stated; the documented reproduce chain breaks at `shrink.py` (undocumented xz step); pre-registered n differed from what ran; position/timing scars unmeasured (conservative direction).
