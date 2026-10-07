# Predictions (written before the decisive run, H=24000)

Run: `python3 exp.py 24000` in this folder. Scene and laws as in exp.py's
docstring. These are the cases I have NOT tuned on (all tuning/debugging ran at
H<=400, where nothing resonant has time to develop and the memo is cold).

1. **Cadence.** B's kick events per particle-orbit land at 0.55-0.75 (the
   synodic rate 1-(a/a_J)^1.5 for a in [2.6,3.3]); the law's current
   orbit-averaged tide cadence is ~0.3/orbit, so the unified event is cadence-
   parity with the design's cheapest layer, not a cadence loss.
2. **Memo.** With the phase rotation's period <= 64 conjunctions and ~500
   events per particle, the shared synodic-impulse memo hits >= 0.8 of
   conjunctions after warm-up (vs 3.3% at H=400). This is the contrast with
   the dead (E,L) cycle memo (0% on distinct kicks): the impulse key is the
   pair's quasi-static geometry, not the victim's ever-changing invariants.
3. **Away from resonance (q_return < 0.8):** median relative error of the
   apsidal precession rate <= 0.15 for B; >= 0.2 for A (the analytic
   quadrupole alone at alpha = a/a_J ~ 0.55 misses higher orders). Final-e
   error <= 0.005 absolute; e-envelope ratio B/REF in [0.9, 1.1].
4. **Near the 2:1 (detune +-0.5%..3%):** REF pumps e (pump_ref > 1.2 at the
   centre); B pumps too, over-pumping by 1.3-3x (r4 v2's first-order-in-mu
   legacy: the per-conjunction impulse lacks phase feedback); A pumps nothing
   (pump_A = 1.0 by construction) and misprecesses. The conjunction-longitude
   cluster statistic q_return separates the band (> 0.9 at +-0.5%, falling to
   < 0.8 by +-3%) with no extra machinery.
5. **Kill criteria for the configuration** (not the method): away-set
   precession-rate error > 0.5 median, or events/orbit > 2, or memo hit rate
   < 0.3 at H=24000. Any of these kills "one conjunction event carries the
   kick" as the layer design and hands it back to the cadence queue.

What this replica cannot decide: integer exactness, the Diophantine timing
cost at scale, multi-planet keys, and the parent tide (not a pair event; it
keeps quantum accumulation). Stated in the dossier.
