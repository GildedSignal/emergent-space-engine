Working...
Check complete. `check.md` written to `lab/results/20261007-1843-dynamics-1b1f/`; nothing else in the folder touched, no commits, scratch removed.

**Grade: silver.**

What I did and found:

- **Reproduction (bit-exact).** Reran g3, k17, g7 from the shipped `stir.py` in a clean copy: identical encounter counts, kick counts, and full rate series (8973/715786; 9606/630957; 5295). Every dossier table number and both scaling laws recompute from the stored artifacts (frozen 2.00/1.95, N 0.89; kicked 2.85/2.29). Two trivial deltas: k16 de/dt 1.5e-5 vs quoted 1.1e-5, and the quoted frozen-control Fano band omits c9 = 2.08.
- **Predictions held-out for real.** `predictions.md` (18:53:06) precedes `grid.sh` (18:53:11) and all results; the author's 5/8 missed bands argue against post-hoc fitting.
- **Attack 1 (decisive):** the T=800 cold extension the dossier itself prescribed — rate 0.105→0.247 from orbit 400→800, still accelerating, e_mean 0.04→0.10, Fano 0.01 (arrivals regularize). The "load attractor ≈ 0.1" is a horizon value, not a fixed point; "near-Poisson" is horizon-limited too.
- **Attack 2:** fresh seed 4 — late 0.094, Fano 1.37; seed-robust within 400 orbits.
- **Attack 3:** m=1e-5 at R_cap=1e-2 — belt destroyed (a_std→0.17) yet load still rising (0.70): "ruin is self-limiting" is radius-dependent, not a law; kicked R_cap exponent 2.11 there.
- **What survives, strengthened:** the engineering conclusion — encounter budgets must be drifting means (static wrong by ×2.5+ per session), scars accumulate superlinearly, cost ∝ R_cap^2+ → thinnest skin.
- **Gold path named:** add the missing sink (fragmentation/escape), 3 cold seeds to ~1600 orbits — find the equilibrium load or prove its absence.
