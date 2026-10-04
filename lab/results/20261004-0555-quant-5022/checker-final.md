Working...
Check complete. `check.md` written; nothing else in the run folder touched; no git commands run.

**Grade: silver.**

**What held under reproduction and attack:**
- **Bit-for-bit reproduction** of tuning.sh, decisive.sh, verdict.py, and rk4 in a scratch copy — every JSON row, the same two tuning crashes, H4's reference ejection at the same position. Timing order verified from mtimes: tuning 06:09:26 → predictions 06:10:35 → decisive 06:11:07, held-out seeds absent from tuning.
- **The invariant J\*** (with the μ(r·r_p) term) I verified both symbolically (dJ\*/dt ≡ 0 for the coded flow) and by rk4 (1.9e-13 over 200 orbits) — the layer's J drift is purely integrator.
- **The load-bearing negatives survived all five attacks:** 1024-references converged to ≤0.3% (so the 10% gate is meaningful); y4 dominated at every budget ≤64 events (fails H2's apsis +14% at 48 events, J error ~20× kdk at equal events even at 96); uniform cliff 64 with gain 1×; α≈1 J-walk reproduced at 4096/orbit.

**Why not gold:** the queue item is `q-correctors` and the board lists "correctors" first — meaning a WHFast-style symplectic corrector/modified kick, which the run never tested (only coarsening and Yoshida-4). The premise's named half is one experiment short of dead. Plus wording dents: "regardless of cadence" is wrong in size (walk ∝1/cadence: 3.1e-4@64 → 4.8e-6@4096), y4's "wrecked" apsis actually decays with cadence, and the cliff=64 is knife-edge across the near-2:1 band (3/5 nearby seeds pass at 32).

**Biggest miss found:** the quiet floor — at μ=1e-5, **2 events/orbit** passes (+0.09% apsis). Per-body headroom is ≥32×, not the conceded 4×; the author's proposed selector follow-up is undersold by their own frozen μ≥3e-4 scope.
