# Predictions (written before the decisive experiment)

Run: 20260929-1835-redteam-2ef5. Decisive experiment E1: mean-motion resonance vs the kick layer.

Setup I have NOT tuned on: two planets (m = 3e-3 M each) at period ratio 2.0 and at a
non-commensurate control ratio 2.30, e0 = 0.05, star mass 1, Newtonian 2D, over ~2000 inner
orbits. Truth = velocity-Verlet N-body. Design models: (B) per-conjunction kicks computed
along undisturbed Kepler cycles (the "certificate" kick, phase kept); (A) the same kicks
replaced by their average over conjunction longitude (the doc's "tidal kicks, with averaging",
costed in representation.md §6 from H0190's 114x).

## Predictions, cases I have not tuned on

1. At exact 2:1, truth's resonant angle phi = 2*lam2 - lam1 - varpi1 will librate
   (bounded oscillation) with libration period of order 50-300 inner orbits, and e1 will
   be pumped by an amount >= 0.02 (i.e., e roughly doubles or more at some phase).
2. Model A (averaged kicks) will show phi circulating monotonically at the secular
   precession rate and e1 staying within 1e-3 of its initial value — the resonant island
   is entirely absent. Prediction: max|e1_A - e1_truth| / e1_truth >= 1 (order-of-magnitude
   miss), while model B tracks truth's e1 envelope within ~30% and reproduces libration
   (same sign of dphi/dt reversals, libration center within ~0.5 rad).
3. Control at ratio 2.30 (no commensurability): models A and B both match truth's varpi
   drift within a few percent and e stays flat — averaging is fine off resonance
   (consistent with H0190; no strawman).
4. Secondary predictions (E3, checked after): the exact Schwarzschild test-body precession
   exceeds the 1PN value 6*pi/p by ~2-8% relative at p = 20 (r3's seed floor), which
   contaminates r3's `prec` gate (which has no truncation exclusion, unlike `period`).
5. Minsky rotation bias (E4): the forward-Euler mutual-update rotation has a systematic
   prograde frequency bias of ~eps^2/24 relative per step; holding 1% precession accuracy
   at r = 1000 M needs eps <= ~1e-2 (~10^3 steps/cycle) and at r = 10^6 M needs
   eps <= ~3e-4 (~10^5 steps/cycle) — as costly as the stepping path the doc claims to
   beat, unless cycles are computed by exact per-band rotations and memoized.

If (2) fails — i.e. the averaged model does capture the libration — my top attack dies and
I report the premise as surviving.
