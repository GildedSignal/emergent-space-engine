# Dossier — library lens: what Julien's practitioners say about kick cadence, with a measured probe

**Claim.** For the tide-kick layer, the cadence trigger must fire on an
**impulse quantum** (accumulated ∫g dt, the delta a hedger rebalances on), not
on a force-change quantum (∫|dg|, the gamma): the force-change trigger earns
nothing at matched work, while the impulse quantum matches the clock's error
with 3–5× fewer kicks (13× at relaxed error) at the same tide-evaluation
count — a strict win wherever a kick costs more than its quadrature (the plane
recompiles on ~99% of kicks), and it cannot resonate with the synodic
frequency the way a clock cadence provably does.

**Bottleneck.** Board's live question #1: "fewer kicks per orbit at the same
behaviour: kicks dominate the engine's cost"; taste log 6 Oct: "the lever is
cadence (q-cadence queued)". Expected gain: 3–5× fewer kicks per orbit at
unchanged behaviour; what it deletes: the clock cadence's per-body kick rate
and its aliasing failure mode.

**Evidence** (all numbers from `probe2.py`/`probe2dv.py`, reproducible with
`python3 probe2.py A|B|C` then `python3 probe2dv.py A|B|C`, each ≈ 25–75 s,
one core, < 300 MB; machine state in `machine.txt`):

Toy: 48-particle belt (a∈{0.8..2.0}, e∈{0.05..0.6}) under a circular
perturber, T=100; truth DOP853 rtol 1e-12 vs 1e-13 control max|Δe| = 1.2e-10;
positive control: clock K=1536 reaches p95 1.1e-5. Both laws share one
machine: Kepler drift + GL8 tide quadrature per window; kicks are held
impulses applied at interval close. Work = g-evaluations.

- Clock (U) config A: p95|Δe| 1.06e-3 → 8.4e-5 for K=12→192 (evals 5.2k → 83k).
- Force-change trigger (T, ‖Δg‖ ≥ c·μ_p/R³): config A at 27.6k evals best
  p95 3.17e-4 vs clock 2.62e-4 at 20.7k evals — **equal error at 1.33× MORE
  evals: no gain**; same on held-out B (1.76e-4 vs 1.74e-4). **KILL (P5).**
- Impulse-quantum trigger (D, Σ_window‖∫g dt‖ ≥ c₂·(μ_p/R³)·(2π/n_p)):
  config A, nW=64, c₂=0.05: p95 2.82e-4 at 24.6k evals with **2219 kicks**
  (clock at that error: ~2400 kicks); c₂=0.45: p95 4.28e-4 with **472 kicks
  vs clock's ~1584 at the same error (3.4× fewer)**; c₂=4: 750 kicks→8×.
  Error is flatter across eccentricity (e≥0.4 p95 3.4e-4 vs clock 4.8e-4).
  Held-out B (inclined 30°), same c-list, no retuning: 3.8e-4 at **73 kicks**
  (clock: 2304 kicks for 1.7e-4) — the kick saving transfers, at ~2× error.
- Config C (μ_p=3e-3, R=3, strong tide): both held-impulse triggers fail
  (p95 ~2e-2, e-subgroup ~1e-1) — outside the kick layer's regime, exactly
  where the design already routes deep flybys to the one-exact-pair-event law
  (regime number U/√(μ_p/b), m-meso-motion).
- Aliasing, measured: clock U in config C is non-monotone in K (U48 1.6e-2,
  U96 5.8e-2 — worse at finer cadence): a clock can resonate with the
  synodic frequency. A quantum trigger has no frequency to resonate.

**Predictions** (`predictions.md`, written before the decisive run): P1 (≥2×
eval gain for the force-change trigger) **failed — that is the result**: the
variable the trigger watched (force change) is not the variable the error
grows in (impulse applied late on a diverging path). P2 held only through the
impulse form (flatter error across e; the near-circular subgroup gains
nothing, as predicted). P3 held-out transfer held for the kick ratio, not for
evals. P4 held (Δϖ orders like Δe). P5 kill criterion fired for the
force-change law and is reported as a kill. P6 (T-walk check) not run — time;
the rung must carry it. The impulse-quantum run was designed **after**
diagnosing the force-change kill (H0183: a failed expectation is not a failed
method): it is exploratory on A, held-out on B/C.

**What would make it wrong.** The probe's kick is free beyond its quadrature;
in the plane, a kick triggers a recompile and re-anchor, so the true saving is
the kick ratio times the per-kick side-cost — if the Sonnet memo wiring makes
kicks cheap (no recompile), the impulse quantum buys little and cadence stays
a clock. The sensor (tide window setup) is NOT reduced by any trigger: the
92%-window-setup floor stands, and only averaging (H0190: 114×) attacks it.
The toy is 2-source, planar births, float; C shows the domain edge. Cost of
adopting: one integer comparator on an accumulator the carry machinery
already keeps; deletes the per-body cadence constant. PRINCIPLES fit:
"Nothing is evolved that can be derived" (3) and "no ticks … we only care
about changes" (14) — but with the measured temper: event-triggering does not
 repeal the quadrature floor; principle 26's "steal from practitioners with
 skin in the game" is what fixed the variable (delta, not gamma).

**The lens (5 lessons, quotes verbatim from the Readwise export cached in
this folder; each kept only because it changes a decision in q-cadence):**

1. *"When retrieval practice is spaced, allowing some forgetting to occur
   between tests, it leads to stronger long-term retention than when it is
   massed."* — Peter C. Brown, Make It Stick. Mechanism: the review fires at
   the edge of accumulated drift, so work follows decay, not the clock. But
   the drift of an orbit is the impulse already delivered, not the force's
   change — the probe killed the gamma form and passed the delta form.
   Change: q-cadence's trigger is an impulse quantum (integer carry
   comparator). Test: the rung above.
2. *"Humans tend to do better with acute than with chronic stressors,
   particularly when the former are followed by ample time for recovery."* —
   Nassim Taleb, Antifragile. Mechanism: concentrated corrections + long
   clean drifts beat evenly spread small ones; a max-interval safety cap
   would rebuild the chronic clock. Change: no interval cap in q-cadence; the
   strong-tide regime is excluded by the dimensionless number instead (config
   C is the measured reason). Test: C-like seeds gated by U/√(μ_p/b).
3. *"These traders lose money frequently, but in small amounts, and make
   money rarely, but in large amounts."* — Nassim Taleb, Fooled by
   Randomness. Mechanism: judge and size on tails: the clock's error is
   non-monotone in its own cadence (aliasing, measured in C), so any
   single-cadence judgement is a coin flip; the p95 over seeds at swept
   cadence is the only honest gate. Change: q-cadence's criteria sweep the
   cadence ratio on the negative control. Test: plant a resonant cadence and
   require the gate to fail it.
4. *"look for single decisions that remove hundreds or thousands of other
   decisions"* — Tim Ferriss. Mechanism: one dimensionless quantum per regime
   replaces per-body scheduling state (and transferred unretuned to B and C).
   Change: q-cadence carries no per-body cadence bookkeeping. Test: two
   belts, one c₂.
5. *"simply by establishing a high filter, then picking opportunities that
   pass such threshold"* — Nassim Taleb, The Logic of Risk Taking (on
   Buffett). Mechanism: an unambiguous integer crossing; no soft
   near-threshold work, no dithering where chaos and waste concentrate.
   Change: the trigger reuses the sigma-delta carry comparator the law
   already has (representation.md: Inose–Yasuda 1962) — q-cadence adds a
   rule, not a part (principle 17's best part is no part). Test: none beyond
   the rung; it is a deletion.

**Lens blind spot.** A library of wisdom books quotes philosophy, not
mechanism: every mechanism above is mine, anchored to his quotes — the
checker should attack the mechanism, not the quotation. Analogies that
changed no decision (crisis-hunter position sizing, Chouinard's simplicity,
Munger's inversion) were cut.
