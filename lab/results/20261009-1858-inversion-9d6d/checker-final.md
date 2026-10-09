Working...
Check complete. `lab/results/20261009-1858-inversion-9d6d/check.md` written; nothing else in the run folder touched.

**Grade: gold.**

What I did:
- **Reproduced all six scenes exactly** from `work/patch.diff` in a clean tree — every statistic (p50/p99 rank, miss(k), encounter counts) identical to `evidence.jsonl`, including the two load-bearing ones: miss(k=4) = 50.8% at m=1200 and 80.4% for the bunched fleet.
- **Predictions verified pre-registered**: `predictions.md` (19:11:34) precedes `evidence.jsonl` (19:13:25); kill criterion stated and not triggered; P9's two sub-misses disclosed.
- **Four adversarial cases**: (1) collapse confirmed on a new axis (κ=3 as m1200·1e-4 matches m300·4e-4); (2) **gap found** — e-spread ≫ band inflates rank well past κ (mean 3.87→11.70 at σ_e 3e-2), the sizing law has no e-term; (3) **static/dynamic corrected** — I built a probe measuring rank *at encounter time*: p99 ≤ 4 in every scene including the bunched killer, so the gold's rebuild-on-overtakes design misses ~0; its true hidden defect is the rebuild volume m·κ/2, making the gold's 10⁶-store arithmetic off by ~600× — the κ law covers both forms; (4) arithmetic audited (E|Δn| = 0.5·band, encounters ×14.2, p99/κ linear).
- **Novelty**: no prior sizing work exists — the follow-up `b-coorbital-cert` run was VOID, HANDOFF restates the gold unsized.

Gold stands because the killed premise (constant k, O(n·k) cost) is demonstrated exactly and adoption is one step; the two defects (miss-attribution to the static variant only; the unmeasured e-term) are named in the check for the integrator, with the hardening experiment specified. Machine: load 1.4–2.4 of 8, every process < 100 MB.
