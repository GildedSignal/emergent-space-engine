Working...
Check complete. `check.md` written to `lab/results/20261007-1420-inversion-384f/` — **Grade: silver**.

**What I did and found:**

**Reproduction** (all five commands, clean tree; wall-times were the only free field):
- `s1`, `s2`, `s2scale` regenerate **bit-for-bit** on every counted field — the structural misses (cross recall 0.000) and the quadratic claim (candidates exactly C(N,2), ×4.01 per fleet doubling at fixed density) are solid.
- `s2fine` regenerates exactly — but contradicts the dossier's "1.000 fine-seeded" headline: the shipped code gives cross 0.8866 (k4) / 0.9667 (k8). The 1.000/6,391-checks figure came from a script version preserved nowhere (patch.diff empty).
- `s3`'s stored artifact is **empty** and the command takes **458 s**, not "~10 s" (862 locus clusters × per-body refinement — the author's own final rerun died the same way). Run to completion, it does regenerate the row, at k4 = 0.983 not 0.993.

**Truth validated:** my independent dense brute force returns the set-identical 413 on S3 (my first sweep claiming 986 was my own bug — zeroed-triangle self-pairs — caught and retracted after ultra-fine arbitration).

**My attacks:** (1) fresh S2 seeds: repair seed-robust at k8 (0.995–1.000) but k4 sits at 0.85–0.88; (2) congestion extreme on the funnel: the fixed-k repair **collapses** (k4 0.22, k8 0.40 under a jam) — k must scale with flux density; (3) forcing all funnel bodies into one group still leaves phase-rank ≤ 0.24 — the miss is not a tolerance artifact.

**Key adjudication:** the gold's own dossier (commit 8d339c5) scopes its train to the Binet-clump regime — under that switch S2/S3 route to the pairwise tier (quadratic, no silent drops), so the kill lands on the board's routing summary, which the author concedes in the lens section. Silver, not gold: one experiment short (the author's own named exact-intersection gate, regenerable ≤ 60 s, with k measured against congestion), plus the evidence defects above — all named in check.md.
