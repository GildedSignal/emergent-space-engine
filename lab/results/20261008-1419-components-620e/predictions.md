# Predictions (written before the decisive run of kickfloor)

Held-out cases: the 64 belt positions are a deterministic xorshift sweep the evaluator was not
tuned on (I never looked at individual positions); the exactness check compares the integer path
against the `Scalar` path over all of them.

1. **Exactness.** The integer path agrees with the `Scalar` path to **< 0.1 quanta of a 2^-30
   velocity word** (the deviation is driven by rounding the inputs at 2^-30, ≈ 3e-9 relative, not
   by the Newton iteration, which saturates u64 precision in 5 steps). If the deviation reaches
   1 quantum, my exponent bookkeeping has a bug — the run must then be treated as VOID on
   exactness and only the timing parts used.
2. **Force evaluation.** The integer-native acceleration runs **10–40× faster** than the `Scalar`
   one (each `Scalar` op carries `Result` plumbing and a full renormalization; a pull + weight is
   ~40 such ops).
3. **The rebind dominates a fired kick.** `bind` costs **more than the force evaluation and the
   secondaries readout together** (a Kepler fit plus tube construction versus ~40 soft ops).
4. **The secondaries' readout** (4 planets: tube `cartesian` ×4 plus a Vec) costs **1–3 µs**,
   comparable to or more than the `Scalar` force evaluation.
5. **Summary.** A fired level-0 kick today lands in the **3–10 µs** range; the floor version
   (integer force + the jet's 0.05 compiles/kick + secondaries shared per epoch) in
   **100–400 ns**; idiot index **20–60×**.

What would make the run uninteresting: if `bind` were already cheap (< the force eval), the
rebind/jet story would be dead weight and the bottleneck would be the soft arithmetic alone.
