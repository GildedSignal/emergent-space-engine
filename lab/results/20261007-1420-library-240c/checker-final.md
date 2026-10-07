Working...
Check complete. `check.md` written to the run folder; nothing else there touched (`work/patch.diff` is empty — probe-only run; my adversarial scripts stayed in /tmp).

**Grade: silver.**

What I verified, in order:

1. **Reproduction — bit-identical.** `python3 probe_b12_stat.py | diff - probe-out.txt` → empty. Every dossier number (96/96 at threshold 0.10, bounded max −0.066 vs leak min +0.193, fleet-16 median-passes/worst-seed-flags 0.496, variogram kill at 0.847) matches the stored output. Prediction timing honest (predictions 14:27:54 < run 14:30:20; P1/P3 failed and are reported as findings, not buried).
2. **Context claims check out.** B12's current rule in law.md line 71 is exactly "growth exponent ≤ 0.2 on the median seed"; `q-b12-design` is first in `lab/queue.txt`; HANDOFF line 71 names the inability. No prior Allan/variogram work in docs — it replaces redteam-b12-stat's failed recurrence ratio.
3. **Adversarials.** Fresh seeds: 0/96 miscalls (threshold not overfit). The decisive attack — the gate's real series length, which the probe never varies (law.md: ≥20 crossings; probe uses 2048): with leak at 10× floor, **0 false leaks at every N from 20 to 2048**, but 2–3/16 per-seed misses below N=256, clean at N≥256. Bounded oscillation slower than ~3 periods per scene false-leaks 16/16 (the author's stated risk, unmeasured by them); marginal leaks (1–2× floor) sit in a transition zone the dossier presents as a fixed dead band; AR(1) ρ≥0.99 reads as leak.

Why silver, not gold: validated where the probe lives, unvalidated where the gate lives — the author's own P3 admits no real plane Jacobi series was tested, and adoption requires freezing (N, horizon-to-period ratio, threshold) together in B12 v2, not "one slope fit per seed". The named gold experiment: the classification matrix at gate-real N on the plane's real Jacobi population with planted controls both sides plus the slow-oscillation and AR(1) cases.
