Working...
Check complete. `check.md` written; nothing else in the run folder touched; the working tree is back to pristine (only untracked `lab/results/`); no commits or pushes.

**Grade: gold** — as a refutation, matching the taste log's precedent for premise-killing golds (`components-4643`, `components-98bc`'s adjudications).

**What I reproduced from my own runs** (patch applied by me in a reverted clean tree, every number regenerated, not read):
- **Speed, real**: rtf 100 off 76.1 → on 27.3 µs (**2.79×**, stored digests `eccc7f5a…`/`639804a5…` byte-identical, deterministic across repeats, 119/2486 = 4.8% compiles); rtf 30 3.23×; members-200 2.57×; seeds 2/3 ≈1.9×; increment 8.57 µs; flag-off digests identical to the **pre-patch shipped tree** (verified by reverting and rebuilding).
- **Refutation, real**: jet-on B13 **41/64, worst ΔE ∞** (off control: 60/64, worst 2.12e-2 = the recorded shipped state; B12 miscalibrated and B17 timeout properly non-adjudicating); lifecycle invariant **12× off, cos −0.074**, exact to the author's digits.
- **Predictions audit**: `predictions.md` (18:04:54) precedes all decisive jet-on runs; the only earlier artefact is a jet-**off** regeneration carrying no jet fields. Prediction 1 failed exactly as its own text pre-registered ("if any fails… refuted, whatever the speed") — a kill criterion written before the run.

**My adversarial additions**: tightened the anchor to `1<<40` myself → 60/64, worst 7.99e-2, renewals 376 (the author's tightened result exactly — no rescue, and the speed dies with it); closed the author's leg-selection door three ways (half-interval error 10⁻⁸, monotone anchor response, the lifecycle test *is* the ¾-orbit differential); measured the missed fast-forward fade (**2.51× at rtf 200, 1.43× at 300**), which bounds the prize even if the derivative half is built.

**Nits found** (immaterial, in check.md): "55/55" is 54; "43×" anchor is actually 256×. The load-bearing correction stands: the Entry carries phase tables, no (E,L) sensitivities — the silver's "one flag away" and its checker's "already carries the derivatives" are both wrong, and the jet stays unwired until the key-tracking half exists.
