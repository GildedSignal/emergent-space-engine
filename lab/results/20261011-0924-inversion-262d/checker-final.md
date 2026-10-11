Working...
Check complete. `lab/results/20261011-0924-inversion-262d/check.md` written — **Grade: silver**.

**What I did:**

1. **Reproduced** all four dossier commands from a clean copy (empty `patch.diff`, no repo edits): every JSON regenerates **bit-identically** (C2 11 s, C1 20 s, A 34 s, B 82 s; peak 1.48 GB). File mtimes confirm `predictions.md` (09:46:50) predates every output, and the last `probe.py` edit predates all decisive runs.

2. **Three adversarial cases of my own:**
   - **Near-twin truth attack** (σ_a/a=10⁻⁵, e₀=0.15 — the least-covered regime): event finder vs 65,536-sample brute force — zero disagreement on every encounter at both thresholds. Found one 15.6% refinement deviation vs the claimed 1.5% (no classification flip).
   - **Ξ-scaling fresh point** (A at T=32, never run by the author): catch 11.5% at Ξ=42 vs ~14% predicted — the 1/Ξ law holds.
   - **At-encounter rank in true longitude** (B, 18,680 encounters): catch 99.99%, median rank 0 — the dossier's "surprise" (40% at-encounter catch "also fails") is a **mean-anomaly artifact**; along the orbit in longitude the gold's literal claim is true everywhere. Secondary claim overturned.

3. **Novelty:** the core kill is **not new** — `taleb-3ebf`/`b04d` (gold, ~3 h earlier this morning) already measured that period spread breaks the static phase sort (≈47 orbits at 10⁻⁴ a-spread), and the built tier (`adce00d6`) is not a static rank-4 list but horizon-bounded sorting with swept-spread disarm and slack. What survives as new and adoptable: the catch-collapse numbers, per-orbit re-sorting shown insufficient (kills the timer escape), and the real open question — what event maintains any horizon-bounded tier in the quiet steady state that law.md's "no work per orbit" sentence defines. The kinetic λ-sort fix is argued, not measured, with a dip-class exactness gap.

Silver, not gold: reproduced and real, but the headline duplicates this morning's gold, one secondary claim is wrong, and the fix is unmeasured — the named gold experiment is to build the kinetic sort and run the quiet-horizon case through the built tier and b04d's merge-join.
