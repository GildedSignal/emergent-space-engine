# predictions.md -- run 20261006-0220-q-fermi2-tide-v2-26a7

Written BEFORE the decisive `python3 verify.py` (v2) run. v2 = shipped verify.py
with the 0dee checker's named fixes: relative rdot^2 guards, mpmath msqrt clamp,
circ-6.02 added, Richardson omega, B.frame added, B.coord gated at a measured
floor with an in-run refinement probe. Pilots already run (not tuned on the
decisive families' outcomes): errA flat in nsteps at <= 3e-14 on whirl/ecc/circ
families; errW flat in nsteps (h-limited); crosscheck_redteam.py done.

1. **Every family passes the gated checks** (A C^P <= 1e-8, A omega <= 1e-9,
   B.frame <= 1e-9, B.coord <= 2e-2, D <= 1e-12, X.redteam <= 1e-12), including
   the re-admitted circ-6.01 and the new circ-6.02. Expected worst A C^P
   ~ 2-5e-9 on parabolic/far and unbound/post-min (long windows; the shipped
   instrument floor, not a formula error); expected worst B.frame ~ 1e-12;
   expected worst B.coord ~ 1e-3..1e-2 with refinement ratio >= 0.5 (flat =
   round-off floor). If B.coord's ratio < 0.5 the floor story is wrong and the
   run must be read as a failure of that gate, not bent.
2. **Richardson omega**: worst A omega drops from the shipped 4.6e-7 to
   <= 1e-10 (h^4 extrapolation of an h-limited second difference).
3. **circ-6.01 / 6.02 behave as exactly circular**: their windows are the full
   1/8 dynamical time (no collapse to ~0 from spurious turning detection), and
   their A/B/D errors sit at the same floor as circ-1000, not at the whirl
   level.
4. **Held-out (not tuned on)**: the radial families (L=0) keep omega = 0 to
   1e-15 and C diag(m, m, -2m); the parabolic dPhi/dphi = -1/2 exact anchor
   stays <= 1e-15 at r = 5..500; eigenvalues stay E-independent to 1e-14.
5. **Cross-check (already run, stands independently of verify.py)**: the
   red-team's corrected kernel -w(3 gamma^2 - 1), +w agrees with
   tide_boosted's C22/C33 to ~1e-15 at ten radii; their geodesic-pair
   measurement converges to my closed form as (hspan, eps) -> 0 at r = 6
   (radfac 1.5579 -> 1.4984 vs 1.5000) and r = 3.1 (18.52 -> 16.008 vs
   16.0000). No v2 change should disturb this (black box: schwarztide.py
   untouched).
6. **What would falsify the reference**: an A C^P or B.frame error that scales
   with window length on a family where the pilots ran flat (would mean a real
   formula defect appearing only on long arcs); circ-6.0x failing any gate the
   other circulars pass (would mean the near-ISCO admission is premature, not
   just a guard fix).
