# Predictions — eclipse parity at game velocities (run 20261018-0035-redteam-22d1)

Written BEFORE the decisive experiment. Target: representation.md §2 L59's cure for the
missing opacity ("static occlusion is one interval test per row", the page's direction 5),
at occluder and observer velocities the game actually flies (ladder scenes carry a 0.9c
stream; r6's standard scene is β 0.5–0.9999).

Instrument: exact 2-D flat-geometry float64 (c = 1), three candidate wirings of the
occluder test against the correct law (W3, exact segment-vs-worldtube):

- W1 snapshot — occluder at the frame time t_O (the "static" test as literally written);
- W2 retarded — occluder at one retarded time (t_O − d/c, its sprite's position);
- W2′ per-ray — occluder at each row's own retarded grazing time (t_O − d·cosψ/c).

Held-out cases (not tuned on): the oblique-velocity arm (45°), the observer-velocity arm
(β_O = 0.5, cross-checked against check2's aberration numbers), the exact rim-onset form
for W2, Arm B's sprite-consistent differential Shapiro delay, and the price.

- **P1.** W1's eclipse onset/egress error is exactly the light time d/c from occluder to
  observer, at every β (independent of speed — the error is a retardation, not a speed
  effect). At fleet distances (d = 100 ls) eclipses are mis-timed by ~100 s.
- **P2.** W2 is exact on-axis; its rim onset error is d·(1 − cos θ_half) where θ_half is
  the arc's half-width — 0.13·d on the every-planet-approach arm (d = 2R, θ = 30°),
  0.005·d at 10R. So even the render-consistent wiring misses ~13% of a light time on the
  wide-arc arm.
- **P3.** W2′ ≡ W3 to machine precision at constant velocity (any direction, including the
  oblique arm): per-ray retarded-time evaluation IS the worldtube test for a straight
  worldline. The next term is the occluder's acceleration, size ~a·(d/c)²/2.
- **P4.** Mid-transit misclassification (W1 vs W3, fraction of the 10⁴ sky rows): Jaccard
  falls below 0.2 once β·d/R ≳ 2 (nearly disjoint arcs — the blackout sits in the wrong
  sky patch); above 0.999 at planet-realistic β·d/R ≲ 0.1.
- **P5 (observer arm).** My independent instrument reproduces check2's aberrated half-arcs
  for a 30° static arc at β_O = 0.5 (17.6° approaching, 49.8° receding) within 0.5°, and
  judging parity on coordinate arcs at β_O = 0.5 misclassifies ≥ 10% of rows on that arm.
- **P6 (Arm B, strong field).** The sprite-consistent differential Shapiro delay across a
  transit at r_o = 20M, b ≈ 10M, R_p = 1M is O(M·R_p/b) ≈ 0.1–0.5 s — below W1's d/c ≈ 2 s
  but a ≥ 5% distortion of a β = 0.5 transit's duration (4 s), and invisible at planet β.
  The naive (no sprite cancellation) delay 2M·ln(4r_E r_O/b²) is ~an order larger and is
  NOT the observable.
- **P7 (price).** The exact W3 test costs < 0.5 µs/row vectorised on this box (order of
  magnitude only, shared x86): the occlusion test is not the bill at 10³–10⁵ rows/frame;
  the wiring decision is.

Controls: positive — the static arcs reproduce e59e's published counts (1667/10⁴ at d = 2R,
319/10⁴ at 10R); negative — W1 at β 0.9, d = 100R must disagree with W3 (else the
instrument is broken).
