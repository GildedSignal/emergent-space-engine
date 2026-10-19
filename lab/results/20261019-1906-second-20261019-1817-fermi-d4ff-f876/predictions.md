# Predictions (pre-registered before the production run)

Question: d4ff's checker corrected the belt's conjunction law from the author's
84.09/root (theta-mixed annular dispersion) to an unmeasured instrument-reach
asymptote ~4.9/root (formula 2n<|dv|>_co-located), anchored by direct counts at
d = 1e5..2e6 root (27.75/40.3/48.8 per root). Nothing measures the reach that
the ledger actually prices (encounter 68 root, contact 0.0664 root). I built
two independent instruments on the shipped genesis (exact planar Kepler test
bodies, no mutual gravity — the shipped belt law):

- **MC**: steady-state pair-event rate = (|dn|/2pi) x P_theta(miss < d), miss =
  impact parameter of the local relative motion at the angular crossing;
- **brute**: exact Kepler propagation, per-pair debounced threshold crossings,
  sample-0 burn-in excluded.

Already seen (tuning, d >= 3e4 only): MC = brute at d = 1e5 (6.80 vs 6.19,
+10%) but MC runs 24% high at 3e4 (8.04 vs 6.09) — the slow tail
(|dv| <~ Omega|dr|, where the straight-line miss is wrong because the shear
carries the pair past before the radial offset closes) grows as d shrinks.

The held-out cases, written before the production MC and before brute at 1e4:

- **P1 (brute flatness, decisive for the reach law):** brute Gamma at d = 1e4
  (M = 1e5, T = 1e6 game-s) lands in **[4.5, 7.5] per root** — flat within
  +-25% of the 3e4/1e5 values (~6.1), i.e. the true reach law saturates at
  small d instead of rising like the uncorrected MC (8.9 at 1e4). If brute
  instead lands in [8, 11], the MC's small-d rise is real and P2 is wrong.
- **P2 (the instrument-reach constant):** the production MC, restricted to the
  shear-safe event set (|dv| > 10 Omega|dr|), gives Gamma(68 root) in
  **[3.5, 8]** per root per game-s, and the full MC (uncorrected) in [7, 13].
  The ledger number I will adopt is the shear-safe one, with the full MC as
  the upper bookend.
- **P3 (the author's error mechanism, reproduced):** the kinetic theorem fed
  the shell-annular dispersion (the author's construction) gives 70-95 per
  root (measured 83.3; their published 84.09) — i.e. their headline was an
  artifact of pairing bodies in the same 0.05-AU shell at random angles.
- **P4 (event speeds):** mean |dv| of counted events rises slightly as d
  shrinks (flux weighting): brute mean at 1e4 in [2.3, 3.5] km/s; MC event
  mean at 68 root in [2.3, 3.6] km/s. Both above the checker's 1.74 km/s
  co-located mean (unweighted) and below the author's 22.9.
- **P5 (downstream constants, the ledger sentence):** with the adopted
  Gamma(68): TP bar (encounter pair-events/game-s at 1e9) in **[2e2, 6e2]**;
  contacts at 1e9 in [0.2, 0.55]/game-s; stream row addition <= 0.006 cores
  at today's fired item cost (rtf 100); wake-up N (>= 1 contact/game-hour)
  in [1.3e7, 7e7]; C_contact in [2e4, 1e5]; belt-temperature C in [25, 90].
  All within ~1.5x of the checker's corrected constants — the closure
  sentence survives with the constant measured, not assumed.
- **P6 (the checker's table):** my instruments disagree with the checker's
  three-reach counts by a factor 4-8 at d = 1e5 (mine ~6.1-6.8 vs their
  27.75); I predict their counts included non-event presence contamination
  or missing burn-in exclusion, and that at least one of their numbers is
  not reproducible as a pair-event rate by exact propagation. (Falsified if
  a third independent counting method lands on 27.75 at d = 1e5.)

Kill criteria: if brute at 1e4 lands below 3 or above 12, or the production
MC's shear-safe Gamma(68) disagrees with the flat-brute extrapolation by more
than 2x, the instrument is not calibrated and the dossier reports a band, not
a constant.
