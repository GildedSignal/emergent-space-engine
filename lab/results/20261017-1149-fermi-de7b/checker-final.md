Working...
Check complete. **Grade: gold** — written to `lab/results/20261017-1149-fermi-de7b/check.md`.

**What I did:**
- **Reproduced** from a clean tree at base e8490901, applying `work/patch.diff` myself: arms 6/7/8 and `ledger.py` byte-identical (h p50 28,141/14,071/7,035; pairs 9,700/9,621+79/9,700; 2/4/8 events per body; dead 0). Ledger arithmetic recomputed by hand — all cores regenerate.
- **Verified the mechanism in shipped source** at the exact cited lines: one `full` (step.rs:705) → Boundary at `t+full/2` (:717), Kick at `t+full` (:718); `boundary_clock` plans nothing; `ds`'s only cadence input is `cfg.step_log2` (default 7). Also checked the non-clock path (:587-588) — it derives both items from one `step_for` too; no independent boundary scheduler exists anywhere.
- **Adversarial, outside the author's domain:** levers 5 and 9 (two octaves beyond each side — welding exact, five octaves total), N=3×10⁴ (29,700 belt bodies, 100% pairs), rtf=600. The 79/87 kick-only plans are scan-point artifacts, confirmed by rescans.
- **Novelty:** decides kick-cadence's named open direction 1 (8ffc); no prior run measured the boundary's lever response.
- **Page:** faithful fold; corrected one overstatement in place ("100% of 9,700 belt bodies" → exact pair counts, arm 8 = 9,621/9,700 at its scan point). Topic stays open (split legality at S≈20 is 7f97/1db4's question).

Predictions were pre-registered; substance held, with the disclosed sign/label error on which arm is coarse. Tree restored clean.
