Working...
`check.md` written — **Grade: silver**.

**What the check established:**

1. **Reproduction, bit-for-bit.** Both scripts (`check_oracle.py` ~2 s, `shapiro_gather.py` ~10 s) reproduce every number in `evidence.txt` exactly in a clean directory. `work/patch.diff` is empty; `git status` shows the tree untouched. Timestamps prove `predictions.md` (23:21:56) preceded the decisive scripts (23:31/23:32) and frozen evidence (23:35) — pre-registration was genuine.

2. **Independent oracle confirms the physics.** I built an r(φ) RK4 from the conserved (E, L) with explicit periapsis root-finding — a different variable, integrator, and turning-point treatment than the author's u-space Simpson quadrature. After fixing two bugs in *my own* integrator (bad periapsis bracket; v≤0 start killing the outbound leg), agreement is Δφ ≤ 1.5×10⁻⁴ and T ≤ 3×10⁻⁵ on all six rows including the deep conjunction rays. End-to-end from my T: conjunction 85.7° (author 86.0°), quadrature 64.4°, near-side 41.9°.

3. **The attack is not a strawman.** representation.md §2 names only "Newton's method finds the crossing" + "memoized deflection(b)"; law.md §Observation is identical minus timing; §6's view row has no delay term; no operational definition of the cone's timing exists anywhere. r6 is absent from `lab/rungs/` and representation.md §7 speccs it cost-only; B0–B19 judge angles and rates, never retarded emission events. The fix claim checks out: law.md §Motion 4/6 already integrates dt/dψ for light parameterized by b, so T(b) is one memo column.

4. **Novelty and the secondary attacks verified.** HISTORY's Shapiro hits are the pre-pivot evolving-patch law's GEO-N residual, not the view; B16 was deflection angle. The doc-integrity attack's three claims all match law.md, and the cited run `20261006-0346-redteam-df81` exists on its published branch.

5. **Adversarial additions.** The near side is stronger than the dossier stresses: the climb-out floor 2M·ln((r_o−2M)/(r_e−2M)) ≈ 11 M keeps every r_e=6 emitter ≥42° out of phase at *all* orbital phases — the flat gather is never right.

**Why silver, not gold:** the finding is gold-quality (reproduced, independently confirmed, novel, one-step adoptable), but the rubric's letter — "held-out predictions held" — fails on two pre-registered quantitative predictions (the 1e-6 δt=Δt_Shapiro identity; the magnitude bands), both disclosed, both failing in the direction that strengthens the attack. The named gold experiment: implement the T(b) crossing fix on this harness with fresh held-out predictions (r_e = 12, 30, a β≈0.9 stream) showing sub-pixel residual while the flat control fails — that run ships the r6 criterion with a verified mechanism.
