Working...
Check complete: `lab/results/20260930-2250-redteam-03c8/check.md` written, nothing else touched in the run folder.

**Grade: silver.**

What I did and found:

**Reproduction** — both programs recompiled and rerun in a scratch tree: `run-out-v3.txt` and `isco-out.txt` match **bit-for-bit**. `patch.diff` is empty. Timestamps confirm `predictions.md` (22:55:41) precedes all outputs; the decisive v3 output follows the last source edit. The banded model implements r1's frozen rung literally (bands, u_k at geometric centre, continuity, light variant, sampler box, 1% gates) — no strawman.

**Adversarial checks** (beyond the required three):
- Independent elliptic-quadrature oracle (no ODE integration) confirms the run's exact values: timelike ≤1.2e−7, light ≤2.6e−5 relative.
- Step-halving *at the failing point* (author only did it elsewhere): the 6.7% ISCO error is identical from h=2e−4 down to 2.5e−5 — model error, not solver error. The headline stands.
- m-scan to 128: non-monotone quantization noise confirmed, but m=128 eventually passes — "raise m is not the fix" is true only as "not monotone or cheap".
- Fine light scan: the m16 >1% sliver ends at b≈5.209, not 5.22.
- I measured the fix the author only asserted: gradient-linked band width drops the plateau to ≤0.67% at 12–234 crossings/cycle (inside r1's ≤512 budget) and cures the separatrix sticking.
- Found ulp-sensitivity at the separatrix: a 1-ulp change in band centres flips the banded outcome while exact GR is robust — the strongest case for a dedicated negative control.

**Why not gold**: H0207 (same day, earlier) already recorded "near-circular precession 1–7% off" — uncited by the dossier; the phenomenon isn't new, only its attribution to r1's frozen configuration, the region map, the photon-ring sliver, and the r5/r6 gates-missing finding (verified: no r5/r6 in `lab/rungs/` despite §7). Also several number slips (13/26 is really 9/26; H0204 miscite; finding 7 has no reproducing script) — none load-bearing. The named gold experiment: freeze r1 v2 with the extended seed grid, a graded-band candidate, and a separatrix negative control; my probe already supplies the expected numbers.
