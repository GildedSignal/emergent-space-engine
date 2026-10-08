# Predictions — 20261008-2031-constraint-4b27 (written before the decisive run)

Baseline (already measured, this machine, warm/unpaced unless said):
- `xtask universe --bench` (paced, the player's loop): view_gather 73.7% of frame at rtf 1, 69.4% at rtf 100; engine 5.0%/17.7% (p99 at the 5 ms budget cap, 46/1800 overflow frames).
- Gather split: bodies loop 95% of gather; 62 readouts/frame at ~76 bodies; `state_rate` 11.3 µs each; its atoms: `cartesian` (orbit phase solve) 5.0 µs, `secondaries` 4.9 µs, `binding_at` 24 ns. Fleet loop 12 µs, player prologue 17 µs.

The change under test (event-gated readouts, `view.rs`): an emitter's crossing is re-solved exactly only when an event has been committed in its doll chain since its last exact solve, or the extrapolation span passes a curvature cap (relative error 2^-20); between those, the retarded state is extrapolated linearly from the last exact solve. Held-out cases — not tuned on:

1. **Readouts per frame at rtf 100** drop from 62 to ≤ 5 (median); warm gather p50 from ~690 µs to ≤ 150 µs (≥ 4×). Chain events land ≈ 1.5/frame in total (kicks+opens+boundaries = 2665 over 1800 frames), so the gate, not the cap, should bind.
2. **Readouts per frame at rtf 1** ≈ 0–1 (events per frame are 100× sparser); gather p50 ≤ 60 µs.
3. **Display error against the exact (cold) gather on the same state**, sampled every 100 frames: per-component |Δdirection| < 10⁻⁴; relative |Δlight_seconds| < 10⁻⁵; relative |Δshift| < 10⁻³. These follow from the 2^-20 relative curvature cap; anything larger means the extrapolation is wrong (e.g. I missed an event kind).
4. **Adversarial — a hot body:** a body whose chain is committed every frame (held burn, dense kicks) re-solves exactly every frame: no error growth, no saving for that body. The player itself is excluded from the loop either way.
5. **No outcome changes:** the universe digest at the cut is identical with and without the gate (the view is read-only); `cargo test -p emergent-universe` observation tests still pass.

Kill criterion: any sampled display error beyond the bounds in 3, or a readout drop < 10×, kills the mechanism as built (not the diagnosis).
