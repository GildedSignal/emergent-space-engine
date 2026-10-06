# Held-out predictions — run 20261006-1249-library-8f99

Written before the probe `slack_probe.py` is run. Float toy, structure only (rates vs slack width), orders of magnitude only.

Setup: a massless body on a near-circular orbit (e0 = 0.05) around a primary (M = 1), perturbed by a companion (μ = 0.03) at a2 = 5, e2 = 0. Truth: DOP853 full three-body, rtol 1e-12. Cheap model: the plane's — osculating Kepler around the primary, refit at each "setup"; prediction error e(t) = |x_pred − x_true|, relative to the primary (a pair window's frame). Slack width w: re-setup when e crosses w upward. r(w) = setups per inner orbit.

Cases (chosen before running): `nr` a = 1.0 (synodic ratio 11.18, non-resonant), `det` a = 2.65 (near, off resonance), `res` a = 2.714 (interior 5:2).

1. **nr (the bounded majority):** e(t) is quasi-periodic and bounded by an amplitude A_nr; r(w) falls roughly as a power law w^(−α), α ∈ [0.3, 1], below A_nr, and reaches **zero** (no setups at all) for w ≥ A_nr within 60 orbits.
2. **res (the unusual that happens usually):** resonant pumping makes e(t) grow secularly; at widths up to 100 × A_nr, r(w) is still non-zero (no floor), with a steeper slope than nr's.
3. **Sizing consequence (the decision):** the smallest global width that keeps the resonant pair's setup rate at or below the nr pair's floor-crossing rate is ≥ 10× A_nr, so a global slack width spends ≥ 10× more slack than the bounded majority needs. Slack must be per-pair, re-estimated from each pair's measured drift rate (the simulation decides), with resonant pairs escalated out of the skin tier.

If (1) fails — nr also drifts secularly — the conclusion strengthens (every pair needs adaptive slack). If (2) fails — res stays bounded like nr — then a single global width near the common amplitude suffices and adaptivity buys nothing; that would kill the lesson's change.
