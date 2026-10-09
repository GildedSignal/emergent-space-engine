# Predictions (written before the held-out runs)

Tuned on: seed 7, rtf ∈ {1, 100}, members ∈ {4, 48, 400}, seconds ∈ {12, 15}.
Instrumented binary; digests matched the uninstrumented main binary on every rerun.

Held-out cases (not tuned on):

1. **Seed 3, members 400, rtf 100, 12 s** — a different battle.
   - The gather's per-readout atom stays 9–13 µs (bodies_ns / readouts).
   - readouts ≈ 0.8–1.3 × live bodies; gather p50 ≈ readouts × atom, within ±50%.
   - The engine still overflows on ≥ 10% of frames (budget 5 ms), with no hitch above 16.7 ms.
2. **Seed 3, members 48, rtf 1** — the idle-observer regime, unseen seed.
   - Gather remains the largest single part of the frame (share > 50% of engine+gather+json+wire).
3. **Scaling extrapolation (not runnable within the 60 s limit, stated as a prediction):**
   at ~1,600 live visible bodies the gather alone reaches 16.7 ms (1,600 × 10.5 µs),
   the whole frame budget, with the engine still small; the plane's `--members` clamp (400)
   is what hides this today.

If (1) or (2) fails, the constraint claim is weaker than stated and the dossier says so.
