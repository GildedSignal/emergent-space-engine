Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did**

- **Reproduced**: applied `work/patch.diff` at base `8d9e7f88`, rebuilt, and reran three arms — `lad_n400_s1`, `lad_n1600_s1`, `lad_n6400_s2` are byte-identical to the regen data. The `worlds::gas` mirror is faithful to the shipped source (same RNG seeding and call order). Identity, block decay, T ∝ side, spectra, band correlations: all regenerate.
- **Held-out**: P0/P2/P3-acoustic/P4 held; P1 and P5-mass were refuted (honestly reported — P5-mass reproduces on the author's leftover seed-2 arm). One failed held-out caps gold per the 1-October precedent.
- **Adversarial (outside the author's domain)**: higher β *tightens* the bound (m 1.59% at vmax 2¹⁷, 0.47% at 2¹⁸ — no mode at all); the gapped lattice (fill 0.3) shows no ringdown. But **n = 12800 breaks the letter**: whole-run m = 3.43% vs the claimed ≤ 2.4% (trend 1.4→2.4→3.4%), F1 = 3.33, and a burn-4096 probe shows the ringdown still decaying but not extinct at t = 12288 — the fixed-horizon m-instrument conflates the longer-lived transient with the steady state; ratio tails stay flat there, so the allocator deletion itself is safe where flown.
- **Record defects found**: the dossier's 6400 row and poly_r values are stale 2-seed/partial-file numbers (3-seed regen: 38.18-43.77, m ≤ 2.52%; poly_r F64 17.26, m 2.26%), and "regen.sh includes [the 12800 octave]" is false — regen.sh has no 12800 arm.
- **Page**: corrected `wiki/chaos-shadowing.md` in place (stale numbers, the self-contradictory "≤1.08 everywhere … 1.115", T range 4.8-7.9 not 5.7-9, definitional caveat on the identity, a checker bracket with my probes, and a fly-at-horizon-∝-side clause in direction 3).
- Tree restored to base; evidence in `data/chk/`; no git commands run.

**Gold path**: fly 12800 at horizon ∝ side to extinction with late-window m — my burn-4096 probe (blocks 88.6→12.0, still falling) predicts it confirms the ringdown law.
