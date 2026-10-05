Working...
Check complete. `lab/results/20261005-2129-m-spacetime-498b/check.md` written — **Grade: silver** — nothing else in the run folder touched, no git operations, all work in `/tmp/check-498b`.

**What I did:**

- **Reproduction (bit-exact).** `work/patch.diff` is empty, so clean-tree runs of `probe_mks.py`, `probe_farey.py`, `arbiter_christoffel.py` regenerate every number identically (both metrics JSONs `diff`-empty; arbiter prints +0.48% = the quoted "+0.5%"). Runtime 2m19s, matching the ≤135 s claim.
- **Attack (4 rounds, ~15 s compute each).** Symmetric p/d=20 boundary reads 0.49% (between the author's 0.14% and 3.1% — boundary interpolates); opposite-side light at b=400M reads 0.82% MKS-vs-oracle; an independent Binet quadrature gives 0.2361360, confirming the dossier's unshipped "0.23614" oracle; mixed-sign decelerating boosts stay exactly closed across v=0; 5-digit Farey composition exact.
- **Sharpest adversarial finding:** the harness's perihelion observable measures radii about the *origin*, so off-axis mass layouts corrupt it — my control (one off-axis mass, where MKS is exact by construction) reads a fake 76% error. Therefore the dossier's "cells aggregating distant sources are inside the valid domain" is unmeasured by this instrument, not validated — and my 3/5-source numbers are instrument noise, which I report as such rather than as a kill.
- **Audit.** gravity-law.md:41 carries the verbatim open question; no Kerr–Schild/rank-1 prior art anywhere in docs/HISTORY; law.md:41 + representation.md:50 already decided rapidity-linear thrust, so the Farey arm's real addition is the quantization/carry study. Pre-registration timing is consistent (21:38 → 22:03) but `run.log` is empty.

**Why silver, not gold:** predictions 1–2 failed as registered (3.1% vs "2%"; +58% vs "0.1%") and were disclosed — the same bar that held the 1 October red-team at silver — and nothing ran in the integer/rung path; the dossier itself concedes a rung is the honest next evidence. Named gold experiment: wire MKS rank-1 integer deposits as gravity-law rung 2's β-rule, with a centre-of-mass-based observable, including one ≥3-source case.
