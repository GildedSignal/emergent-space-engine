# Predictions (written before the decisive run)

The experiment (the checker's named gold path): attribute the kick's whole-resolver time on the
plane's real path, then time the jet rebind (docs/law.md "strong-field reuse … re-anchored") on the
same replayed kicks. Baseline digests verified first: replay `0e02bf0f34481650…`, memo 1125/0.0%/51
keys, all bit-exact with run 20261011-2306-system-3367.

P1 (attribution, ships): the rebind component — `Rebinding::from_state` on the exact post-kick
state, i.e. fit + fresh cycle compile + readout + residual — is the majority of the whole
`step::process` sample: median ≥ 60% of 35 µs (made) and ≥ 60% of 93 µs (leavers). `Orbit::compile`
alone ≥ 40% of the whole. Falsified if the rebind is a minority: then the fictitious-clock part
(forces, ext, planning) dominates and the dossier's caveat wins.

P2 (jet time): the implied jet kick (whole − from_state + fold) drops ≥ 10× on the leaver
population (the checker's bar: from ~93 µs to ≤ ~9 µs) and ≥ 5× on made bodies. Anything less is
reported as the honest ceiling of the deletion.

P3 (anchor rate): at the red-team's threshold drift* = √(floor/C) = √(10⁻⁶/1.88) ≈ 7.3×10⁻⁴, with
drift accumulated per body as Σ|Δv|/|v| since the anchor, anchors per kick ≤ 0.05. I expect the
plane's tides to give per-kick |Δv|/|v| ≈ 10⁻⁶–10⁻⁵, so almost no anchors. At drift*/100 the
anchor count grows ~linearly (≤ 0.5 per kick) — the arithmetic check, not a law.

P4 (input equivalence): re-running `Rebinding::from_state` bench-side on the post-kick state
reproduces the resolver's own new-entry trajectory key for ≥ 95% of Cycle rebinds (it must be the
same deterministic function of the same state; edge/unit conversions are the only slack).

P5 (player): the player's ~0.5–1 ms per resolved item is ≥ 50% the same rebind path (compile
dominated), so the memo/jet deletion extends to it; if not, the i128/fictitious-clock part owns it
and the original dossier's "could not attribute" gap resolves the other way.

Each is decided on the same replay the record already regenerates; no new scene, no seed change.
