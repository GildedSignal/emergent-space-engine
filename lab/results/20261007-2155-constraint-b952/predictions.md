# Predictions (written before the decisive run)

Held-out cases (not tuned on; the scaling runs above were the tuning):

1. **Ramp share of the readout.** `state_rate` (with ramp) on the plane's heliocentric ships costs ~18 µs; `root_state_raw` (tube + chain, no ramp) will cost < 3 µs. Prediction: the ramp/`partial` field evaluation is > 70% of the view's readout unit cost on kicked bodies.
2. **Surprise fraction per frame at rtf 100.** With a one-instrument-quantum gate (direction change > 10⁻³ rad ≈ one pixel at 60° FOV on 1080p, or |Δshift| > 0.01), fewer than 30% of the plane scene's emitters change per 60 Hz frame at rtf 100; the median emitter's direction moves < 10⁻⁴ rad/frame. So a surprise-gated view cuts readouts ≥ 3× on this scene, and ≫ 10× for the far sky (distances ≥ 10⁷ ticks).
3. **0.9c toward stream at 1e6 ticks does NOT amortize** (bearing rate β·dt/dist ~ 0.3 rad/frame): the gate's saving there is < 2×. The amortization follows distance and speed, not body count — the far sky is where the 10⁶-emitter galaxy lives.

If 2 fails (most emitters move a pixel per frame), the constraint moves from "readout per emitter" to "readout unit cost itself" (the 18 µs), and the dossier says so.
