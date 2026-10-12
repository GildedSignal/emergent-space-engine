Working...
The run is complete and reproducible (regenerated bit-consistent numbers on a second execution).

**Claim:** The rebind after a kick — the engine's dominant event at 24–27 µs — sits ~270× above its two-integer floor because every kick refits and recompiles the orbit (0% memo hits, 2000/2000 distinct shapes measured on `crates/space` itself), and the adopted jet closes this to within ~10× of the floor at a re-anchor interval measured here at 38 kicks (correlated δv/v = 10⁻⁶, 10⁻⁶ floor; 510 for a walk; error ∝ D² with C ≈ 0.8 across kick sizes, directions and fields) — provided the memo's period derivatives ∂Δt/∂E, ∂Δt/∂L are carried, which is load-bearing, not optional: without them the jet's error crosses the floor by kick 2.
