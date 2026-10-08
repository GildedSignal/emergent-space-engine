# Predictions (written before the decisive experiment)

The decisive experiment is the checker's named one: wire the re-anchored jet into `Work::kick`'s
rebind path behind a flag (`ESE_JET`), run `behave --law plane` B12/B13/B17 and the universe
suite, and re-measure the realized saving on the plane at rtf 100, including the increment's
actual cost against the one-readout proxy.

The jet as wired: a rebinding kick keeps the compiled entry (the cycle and its tables), re-places
the tube on the exact state through the cycle's own radius cut (`at_radius`), carries the exact
remainder in the turn+residual (the readout at the event is exact, bit for bit), and re-anchors
(recompiles exactly, as before) when the accumulated offset — the velocity residual the placement
now carries — crosses 2⁻¹¹ of the word (the law's rule: error C·offset² under the 10⁻⁶ floor,
√(floor/C) ≈ 7×10⁻⁴ ≈ 2⁻¹¹). Passages, word refits, handoffs and placement failures fall back to
the full compile.

Cases I have not tuned on, and what I expect there:

1. **Gates.** `behave --law plane` B12 (Jacobi exponent), B13 and B17 (resonance) stay green with
   the jet on. If any fails, the jet as wired is a law change at the plane's cadence and the
   claim's "wiring buys it" is refuted, whatever the speed.
2. **Realized saving at rtf 100.** The plane's kick median with the jet on falls by at least
   1.7× against the same machine's jet-off median (the probe's ceiling at rtf 100 was ~2.5×, and
   the increment costs more than the one-readout proxy). Below 1.5× the claim's magnitude does
   not survive wiring.
3. **The increment's true price.** The jet increment (radius cut + angle + decode + turn +
   residual, no fit, no compile) costs more than one readout (3.3 µs) — I expect 5–15 µs — but
   well under half a compile (≥ compile/2 kills the lever per the dossier).
4. **Compiles per kick.** With the re-anchor rule at 2⁻¹¹ of the word, the fraction of rebinds
   that still compile is 5–30% (the probe's mean cell residence was 8.7–22 kicks; the offset rule
   re-anchors more eagerly than a memo cell exit).
5. **Determinism.** Two jet-on runs at the same seed give identical replay digests (the jet is
   deterministic integer code); the digest differs from jet-off, as the tube placement differs.
6. **Universe suite.** `cargo test --release -p emergent-universe` is green with the jet compiled
   in (flag off = the shipped path untouched).

Cloud/x86: orders of magnitude only.
