The silver'Done. The checker's four named defects are each closed on a record that regenerates from one command (`python3 probe.py`, 15 s, 618 MB, rerun byte-identical):

1. **Cold at belt density** (the decisive experiment): 40.29 bits raw / 41.74 corrected → **5.22 GB at 2 dof, 7.83 GB at 3 dof — does not break 8 GB**; the 47.9-bit figure is now correctly attributed to `cold_dense_x2500` (both parameters in the scene name). Cold Σ-linearity exactly 1.0000, β = −0.9939 over five decades.
2. **Estimator bias** measured, not just flagged: +1.453 ± 0.015 bits, constant across three decades of σ; all absolute H corrected.
3. **Time conversion fixed**: 16 384 orbits = 53 454 game-years = 534.5 real years of play at 100× (original said "8.5 years"); one honest year of play stores 26.7 bits → 3.3/5.0 GB.
4. **Digits regenerate**: churn 375.36/orbit = 6 076 events per 60 fps frame at 10⁹ bodies (the original's "per game-second" rate was per real-second at warp, mislabeled); live growth 8.676×10⁻⁴ bits/orbit vs creation 3 367.9 → 99.99997 % reabsorbed; floor-invariance triple recorded (±1 % MC spread).

All six pre-registered predictions held (cold-belt 38–42 bits measured 40.29; bias 1.2–2.0 measured 1.453; floor invariance ±4 % measured ±1.1 %). The kernel controls still pass and the impulse-only negative control still fails by 14.6×. The one gap neither run closed: the resonance/Lyapunov channel remains argued, not bounded (B18b).

**Claim:** the silver's claim now holds on a regenerating record — a 10⁹-body belt's live store is log-bounded (21.5 bits after one orbit, 35.7 after 16 384 orbits = 534 years of play at 100×, bias-corrected), a cold belt at belt density stores 41.7 bits (5.2/7.8 GB) and breaks nothing, only dense ×2500 regions break 8 GB at 3 dof, and churn (375.4 mutations/orbit/body ≈ 6 076 events per 60 fps frame), not memory, binds.
