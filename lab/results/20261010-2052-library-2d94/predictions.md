# Predictions — held out before the decisive probe

Probe (see `work/band_vs_fixed.py`): one body, a=1, e=0.6, μ=1, under a real third-body
tide (m_p = 3e-3 on a circular orbit a_p = 2.2, same plane), integrated by RK4 at
T/16384. The "generator" is exact Kepler from the last kick. Policies:
- **fixed**: re-anchor every Δt = T/j (the current law: kicks at a fixed step in phase).
- **band**: re-anchor the first check step at which |r_true − r_gen| > w (checks at dt_c).
Metrics: kicks per orbit, max deviation (the certificate error), kick phase vs conjunction.

Cases below were NOT tuned on (I chose e=0.6, m_p, a_p before any run; the first run
will be e=0.6 only; e=0.9 and the controls come after).

1. **Band beats fixed at matched error (e=0.6):** at equal max deviation, the band
   policy fires ≥ 2× fewer kicks per orbit than the best fixed cadence.
   Kill for this lesson if < 1.5× on both e=0.6 and e=0.9.
2. **Kicks track conjunctions:** ≥ 60% of band kicks fire while the angular separation
   from the perturber is < 45°; fixed kicks are uniform by construction.
3. **A mean-sized check rate bursts:** with check interval dt_c sized from the *mean*
   tide strength, max deviation exceeds w by ≥ 2×; sized from the *peak* tide, overshoot
   stays ≤ 1.3× w. (The certificate's margin must be bought at the tail.)
4. **Controls, both sides:**
   - m_p = 0: band fires **0** kicks over 10 orbits (no surprise, no work); fixed fires
     its full cadence regardless (work for no reason). This is the instrument's zero.
   - fixed with j = 512: max deviation ~ tiny; fixed with j = 4: error explodes — the
     instrument detects failure on both ends, so it is not a control that cannot fail.
5. **e=0.9 (held out):** the band/fixed kick ratio at matched error is *better* than at
   e=0.6 (error growth is more concentrated in phase), ≥ 3×.

If 1 and 5 both fail while 2 and 4 pass, the honest reading is: for smooth periodic
tides a phase-locked fixed cadence is already near-optimal, and the deviation band only
pays when surprises are intermittent in time — then the lesson narrows to "the band is
the sleep primitive" (prediction 4), not a cadence win.
