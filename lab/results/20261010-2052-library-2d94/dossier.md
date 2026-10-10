# Dossier — 20261010-2052-library-2d94 (Julien's library lens)

**Claim.** Practitioners who paid real money for cadence — option desks with zone hedging
(Whalley–Wilmott), not clock schedules — replace the engine's fixed-phase kicks with a
per-body deviation band; measured on a float toy, that trigger needs 2.8–6.7× fewer kicks at
equal worst error (8–20× at loose tolerances, floor-limited by my coarsest fixed j=4), fires
**zero** kicks when nothing perturbs the body, and the band *is* the error certificate
(worst error = w by construction), so gates judge a bound instead of re-measuring an
emergent error. Full lessons with verbatim quotes: [lessons.md](lessons.md).

**Bottleneck.** Board focus #1: "fewer kicks per orbit at the same behaviour — kicks dominate
the engine's cost"; the taste log names cadence as the lever (q-cadence queued). Gain: about
half an order in kicks/orbit at fixed behaviour on smooth-tide orbits, plus the sleep term
(quiet bodies pay nothing, where today every body pays its cadence). Floats explore; only
integers would decide a canonical outcome — this run informs the design, it is not a gate.

**Evidence** (commands, each < 60 s, Linux x86 shared, orders of magnitude only):
```
cd lab/results/20261010-2052-library-2d94/work && python3 band_vs_fixed.py   # 5.4 s
```
One body (μ=1, a=1) under a real third-body tide (m_p=3e-3 at a_p=2.2), truth RK4 T/8192,
generator = exact Kepler from the last kick (`work/band_vs_fixed.py`; numbers in
`work/metrics.json`, `work/run.out`):
- Band `w` vs best fixed cadence at equal-or-better worst error: e=0.6: 2.8× (w=3e-4),
  5.2× (w=1e-3), 4.2× (w=3e-3), 4.0× (w=1e-2); e=0.9: 4.0–6.7× (4.4× at w=3e-4). Fixed j=4…512.
- Certificate property: band max deviation = w within 1.00–1.05×; fixed error is emergent,
  ∝Δt² (5.3e-3 → 3.6e-7 from j=4 → 512, e=0.6) and unknown until measured against a tide.
- Controls both sides: m_p=0 → band 0 kicks in 10 orbits, fixed j=64 fires 639 (work for no
  reason, principle 14); fixed j=4 error explodes (5.3e-3), j=512 → 3.6e-7. Kepler-only
  energy drift 6e-13 (the 4e-3 drift with the tide is physical tide work, not integrator error).

**Predictions** ([predictions.md](predictions.md), written before the run): P1 held
(2.8–5.2× at e=0.6 vs predicted ≥2×, kill line 1.5×); P5 held (e=0.9 better, 4.0–6.7×); P4 held (both controls).
**P2 failed**: kicks near conjunction were 26–53%, not ≥60% — at a smooth always-on tide the
win is *not* intermittency but refusing to kick while accumulated error is still below the
band. **P3 not exercised**: coarse checks burst ≤1.05×, so tail-sizing could not be shown;
it plausibly bites only at steep conjunctions, which the law already routes to exact pair
events (m-meso-motion). Both failures narrow the claim; they are reported, not absorbed.

**What would make it wrong.** The toy has one smooth tide and an exact Kepler drift. If real
kick windows are dominated by resonance phasing (kicks must fire at locked phases regardless
of deviation), the band degenerates to a phase clock and only the sleep term survives.
Adoption cost: a cheap deviation estimator per body between kicks (the law already
interpolates states between step boundaries, law.md §"a body's state between kicks"); the
check must cost less than the kick it saves — plausible since it is reads, not recompiles.
Fit with PRINCIPLES: #3 "Compute only surprises" (0 kicks at 0 tide); #14 "no work for no
reason"; #22 "the simulation tells us what's next not us" — the deviation state schedules
the kick, not the frame; #21 rough first, the band is the budget stated up front.

**The lens.** What this lens may have missed: the library holds no collision-detection or
EDA practitioners, so lesson 4's mechanism (sweep-and-prune, KDS) is practitioner knowledge
outside Julien's highlights, anchored only by Munger's inversion and his own O(N²) note; the
Taleb-heavy library biases me toward band/tail framings where a phase-locked cadence may be
provably optimal for the resonant case; the probe is float, single body, Linux cloud —
orders of magnitude, re-measured on the M1 before any adoption.
