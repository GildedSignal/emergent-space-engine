# Predictions (written before the decisive flights)

Instrument: `crates/universe/examples/zonecad.rs` — cbe6's `beltcad` verbatim (same scene:
star + Jupiter 2⁻¹⁰ at sep 527e6, same sampler, same scaled-Jacobi metric), with the belt drawn
from the shipped birth law (`ladder_ship`'s belt arm) and kept by ddeb's census class. Control
verified first, before these predictions were acted on: `beltc` (cbe6's circles) reproduces cbe6's
step-4 belt numbers to the digit (worst J 9.4e-6–1.2e-5), and the printed per-ship kick step H
confirms step_log2 = 4 ↔ 16 kicks/planet-period. Bar: B12's frozen 1e-4 on the worst scaled
Jacobi, zero deaths/refusals. Horizon 100 planet periods (cbe6's), walk check at 400.

Fermi estimates (the honest brackets; the experiment exists because I cannot separate them):

1. **Zone 3:1 floor (q = 2, the census's dominant fine zone, 9.4% of the belt).** The zone sits
   6.8–7.1 Hill out — the clean belt's own conjunction geometry (cbe6's certified draws 6.3–8.8) —
   so per-conjunction force error is the same scale; the resonance adds *coherent* phase error
   across conjunctions (libration). Point prediction: **step 5 (32/Giant-period) PASS** (worst J
   2–6e-5), **step 4 (16/GP) FAIL** (1–3e-4): the floor is 32/GP ≈ 10.7 per own orbit at the 3:1,
   24× below the census's borrowed 256/own-orbit. Confidence 0.4 — the bracket I cannot close by
   argument: (a) step 4 passes → zone floor = cbe6's belt floor, headroom jumps toward the board's
   ~10³ (ddeb's premise correction retracts); (b) no step ≤ 8 passes → the census's 256 was
   optimistic; (c) error walks with horizon / never falls with cadence → q = 2 exits the cadence
   scheme like first order (67be), and the desync cannot fly 17.8% of the belt at any cadence.
2. **Bridge floor (gap 5–6.3 Hill, interior; the census's B64 class, 41% of the belt).** The gap
   shrinks ≤ 25% below cbe6's certified edge (6.3 Hill); tides grow ~1.7×; the n⁻² ladder puts
   step 4 at ~2e-5. Prediction: **step 4 (16/GP) PASS** (worst J 1–4e-5), step 3 (8/GP) FAIL
   (> 1e-4). Confidence 0.7. Then the census's "optimistic" bridge line (16) becomes the measured
   one and the composed rate drops accordingly.
3. **Clean eccentric control (gap ≥ 6.3 Hill, outside every q ≥ 2 zone, e ≤ 0.23).** Step 4 PASS
   (worst J 1–3e-5): cbe6's circles passed at ~1e-5, e adds apoapsis excursion, cbe6-checker2's
   hauler e-draw (e to 0.23) passed at 3.2e-5. Confidence 0.9. This also closes cbe6's own named
   gap (circular starts) with the plane's actual e-draw.
4. **No deaths, no read refusals, no doll captures** in zone/bridge/clean at any step ≥ 4: the
   strong-class cliff (1.5–3 Hill, deaths at step 4) is a different geometry; 5–9 Hill conjunctions
   never approach the surface (49,000 root units).
5. **Δe (the resonant pump).** Clean belt over 100 P: 9e-4–7.8e-3 (cbe6). Zone: 0.005–0.05 (the
   resonant pump is stronger), step-independent per ship at passing steps (cbe6's built-in
   control); corrupted only where the Jacobi bar is already broken.
6. **Composed headroom (the census re-priced with the measured floors).** With zone 32/GP and
   bridge 16/GP: composed rate ~30–50 events/body/belt-orbit → **headroom 180–320×** (point 240×):
   ddeb's correction stands (an order below ~10³), now pinned by a measured floor, not a borrowed
   one. If the zone floor is 4: headroom 280–700× ≈ the board's sentence (correction retracts). If
   the zone is uncertifiable: 17.8% of the belt exits the grid at any cadence — stronger than 78×,
   a different claim (the desync alone cannot fly the plane's belt).
7. **Draw stability**: seeds 1/2 agree within ×3 on worst J per class (6–16 ships of a 10⁶
   population; the worst-of-N statistic is draw-noisy), and the floor's octave does not move.

Kill criteria for the instrument itself: the beltc control failing to reproduce cbe6, any
zone/bridge death at step ≥ 4, or the kick-rate print disagreeing with the step dial — each VOIDs
the arm until explained.
