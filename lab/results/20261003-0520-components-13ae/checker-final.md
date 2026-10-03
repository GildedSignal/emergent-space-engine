Working...
Check complete. `lab/results/20261003-0520-components-13ae/check.md` written: **Grade: silver**, nothing else in the run folder touched (all scratch work in `/tmp/check13ae`).

**What I did (30-min budget):**

1. **Reproduction — exact.** `one.py 0.18 0.3 1` and `0.30 0.3 -1` return bit-identical numbers to grid.jsonl; `analyze.py` regenerates every dossier table from the stored grid; patch.diff is empty (work fully self-contained). Timestamps confirm predictions.md (05:31:39) preceded the decisive grid (05:32–05:43).
2. **Baseline de-strawmanned.** The 2Q closed form matches its numerical double average at machine precision (2.2×10⁻¹⁶) and I re-derived it independently from the Hamiltonian — the 14–127% error is genuine truncation.
3. **Six adversarial cases:** no compounding over 30→100 planet orbits (6.63→6.60%); e₀=0.45 grid gap interpolates smoothly (3.9–12.2%); 0.35 R_H boundary honest (23.5% vs 2Q's 64%); fresh RNG phases shift errors ≲1%; independent event recount confirms the floor (0.30–2.18 events/moon-orbit at rtol 10⁻¹⁰, 0.05–0.43 at behaviour tol, wdot shift ≤2.4×10⁻³); truth converged at 1.4×10⁻¹⁰.
4. **Novelty:** no prior evection/single-average entry through H0211; r9's KILL (τ₀ = 0.0036) is the antecedent — this run's premise correction (truncation boundary, not method boundary) is the new result.

**Why silver, not gold:** held-out prediction P2 overreached (claimed ≤3% through 0.30 R_H, measured 12.8–47% at 0.26–0.30), author-reported. One experiment away: the second-order Lie/Deprit average (or TRACE/JANUS changeover) extending the 10% gate past 0.30 R_H.

**Key author misses:** the 0.2–0.25 R_H envelope is prograde-leaning (retro low-e breaks the gate at 0.20); avg1Q loses badly to the design's own kick-N in the outer regime (0.6% vs 46.7% at 0.30 retro) so the unquoted kick/avg1Q crossover (~0.22–0.26) is the adoptable fact; the "0.2–1.2 events" range matches neither measured tolerance; event counts hardcoded; figure's N⁻² guide contradicts the measured N⁻¹.
