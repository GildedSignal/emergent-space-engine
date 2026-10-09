Working...
Check complete. `check.md` written: **Grade: gold.**

**Reproduction** — clean tree, empty patch; `kick_absorb.c` byte-identical to the first author's; the decisive 452-line ladder regenerates **bit-for-bit** (sorted diff empty, identical analyze md5); every extras claim (systematic death hz=8/33 with Hmax/Hbase 9.3×/115×, ε-scaling, h-convergence, curvature probes) matches the logs. Predictions were frozen before the ladder and honestly scored, misses reported as misses.

**My attacks** (seeds 3/4, e=0.7, e=0.99, margins 16/0.5/0.25, fd 1e-4/3e-3, 1000-orbit cold):
- Kill at s ≤ 0.05 is seed-robust and e-robust; e=0.7 even thickens it (s=0.1 fails nav there).
- The two horns pinch: margin=16 still fails nav (1.75e-3) at 5.2× cost; margin=0.25 passes cost but fails nav 59×.
- One corner pass found — margin=0.5, fd=1e-4, seed 1 at s=0.05 (602 ev/4.4e-4; seed 2 fails cost) — so "any margin" is over-absolute; the honest reading is a knife-edge band 0.05–0.1. Recorded as a refinement, not a refutation (outside the frozen config set, one seed, inside the disclosed FD slack).
- fd=3e-3 cannot compile at s=0.05 — a warning for the integer law's curvature estimator near the skin.
- Cold N=1000: 2.32e-4 monotone — the dossier's extrapolation caveat verified quantitatively.

**Why gold**: the first checker's named experiment, executed on the design's own mechanism with both controls holding; it corrects law.md:35's premise (0.05 compiles/kick inverts to 1.0/kick in the skin, 2.6–6.6× the whole fixed-step budget, or navigation lost 2–57×); adoptable in one step (routing on (p−6−2e)/p to the dense order + seed-swept gate). The one named residual risk: the dense order's own cost near the separatrix is unmeasured — that is the next run before the routing threshold freezes.
