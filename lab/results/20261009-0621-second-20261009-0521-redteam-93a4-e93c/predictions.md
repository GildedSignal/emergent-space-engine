# Predictions — second author on redteam-93a4 (frozen before the decisive runs)

Task: the checker's gold path. (1) Make the isolation control (candidate's
sources slaved to truth; only the reader's tube READ differs) the decisive
metric. (2) Add an encounter clause to the kill domain: a body pair whose
truth separation ever drops below 2·√3 ≈ 3.464 mutual Hill radii
(Gladman's Hill-stability boundary, the same style of oracle-domain exclusion
B12/B13 use) is in the encounter regime and is excluded; the harness
(`news2.c`) prints the running minima `hillT0 hillT1 hillSS hillmin`.
(3) Freeze the two-sided rung draft.

Already run as setup verification (reproduces the checker, not held out):
iso μ=1e-3 R=5 flat 3.32e-07/30 P_T, iso naive 3.33e-02/30 P_T, free-fall
floor ≤ 3e-10 at 3 P_T, no-iso news2 ≡ news bit for bit.

Scene D throughout (M=1 fixed, S and J of mass μ kicked by each other, reader
T massless on a circular orbit; truth = instantaneous Newtonian; laws in
lockstep, dt = P_S/2500; G=c=1). "Read error" = max|ΔE_T|/|E₀| under iso.

## Held-out predictions

1. **μ-sweep under iso (κ=0.3, R=5, 30 P_T):** the pure read error is second
   order in μ: maxdE ≈ 3.3e-7 / 3.3e-9 / 3.3e-11 at μ = 1e-3/1e-4/1e-5, i.e.
   per-decade ratio ≈ 100 (log-log slope 2.0 ± 0.15). This turns the
   original's *inferred* μ² (free-run, fixed time) into a direct measurement.
2. **Boundedness under iso, long run (μ=1e-3, R=5, 100 P_T):** maxdE ≤ 1e-6
   (i.e. the 30 P_T value is not the start of a monotone walk; the reader's
   own orbit drift dT/rT may grow but the energy error stays ~3e-7).
   Confidence 70%.
3. **Letter-trip case rescued by measurement (μ=1e-2, R=5, iso, 30 and
   100 P_T):** hillmin ≈ 5.3 > 3.464 (in-domain even at this μ), and the pure
   read error is bounded ≤ 1e-4 (checker saw 2.17e-5 → 5.11e-5 by 30 P_T;
   I predict ≤ 2e-4 at 100 P_T, decade ratio ≤ 3). The free-run's 2.3e-2 was
   inter-law source divergence (dS/rS ≈ 2), not the read.
4. **Geometry sweep, in-domain (μ=1e-3, R ∈ {3, 5, 8, 10}, iso, 30 P_T):**
   hillmin > 3.464 for all four; read error ≤ 3e-6 each, growing weakly with
   R (light time ∝ R): roughly flat-to-4× from R=3 to R=10. No secular case.
5. **Crossing reader R=2 (μ=1e-3, iso):** hillmin ≈ 0.26 ≪ 3.464 — excluded
   by the clause; the read error nevertheless grows ≥ 1e-2 by 30 P_T even
   under iso (deep conjunctions inside J's Hill sphere; law.md's changeover/
   pair-event regime). The clause is *necessary*, not cosmetic.
   R=2.5: hillmin ≈ 2 (still excluded), read error ≥ 1e-4 by 30 P_T.
6. **Close sources rJ = 1.2 rS (μ=1e-3, R=5):** free run: hillSS ≈ 2 < 3.464
   (excluded) and dS/rS explodes (checker: → 4960). Under iso the reader's
   read error is still corrupted through the light time (J–S kicks 6× closer,
   ~40× stronger inside τ): I predict ≥ 3e-6 at 30 P_T, i.e. ≥ 10× the
   baseline, growing across decades. The clause cuts exactly here too.
7. **Carlip variant under iso (law=2, μ=1e-3, R=5):** no amplitude gain over
   the plain tube (checker's free-run showed 4e-5 vs 3e-7); under iso I
   predict the acceleration term still does not reduce the read error below
   the plain tube's (it adds curvature the drift already carries).
8. **Domain audit:** every case the original letter admits (dominant mass,
   μ ≤ 1e-2, κ ≤ 0.3, R ≤ 10) fails the *original* kill criterion only
   through the encounter regime or inter-law source divergence; with the
   isolation metric + encounter clause the candidate passes everywhere
   in-domain. This is the claim upgraded from inferred to measured.

## Kill criterion (this run)

The premise (tube read needs no acceleration term) is broken if any
in-domain case (hillmin ≥ 3.464 throughout, μ ≤ 1e-2, κ ≤ 0.3, R ≤ 10)
shows, under iso, a monotone read error reaching ≥ 1e-3 within 100 P_T, or
a μ-slope measurably below 1.7 (first-order leak: kicks enter at O(μ), i.e.
the light-time extrapolation misses them at leading order).
