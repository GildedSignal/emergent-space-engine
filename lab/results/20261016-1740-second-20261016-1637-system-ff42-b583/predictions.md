# Predictions (written before the decisive experiments)

Question (the checker's named gold experiment): does the verified-guess wiring, cured —
mirrored around the **unrounded** periapsis epoch and verified over a **±k window** with
`k = ceil(‖residual offset‖ + 8 quanta) / |dr/dt per tick|` (both closed-form from the
binding) — drive the crash search's fallback to ~0, on the author's grid, on held-out
adversarial cases, and on the plane's own flights, with tick identity everywhere?

What has already been run (the tuning set): `diag2` on the author's 36-case grid — with the
unrounded epoch the miss `a − g` is 0 on all 24 answered bound cycles and ≤ 1 tick on the
flybys, and `‖offset‖·quantum / |dr/dt|` predicts the miss (0.98 → 1, 1.59 → 1). The window
size law is measured, not assumed.

Held out (not run at prediction time): random `after` phases (mid-fall, pre-crossing,
next-cycle, +3 periods, already-inside), e 0.1–0.97 sweeps, non-unity dolls (μ = 3/2),
grazing periapsis within 10⁻³ of the surface, and the plane's own flights
(`frame_digest`, kick-bench s3 flying and battle).

Predictions:

1. **Tick-exact everywhere**: the cured guess equals the shipped bisection's answer on
   ≥ 99.9% of held-out cases (fallback is the safety net; equality is by construction —
   the risk is a units bug in `to_doll`/`to_tube`, none found in diag).
2. **Fallback → ~0**: window-verified ≥ 95% of answered cases across all held-out regimes
   including flights (k from the bound covers the residual by construction; the cap k ≤ 8
   only bites where Δr/|dr/dt| > 8 ticks — grazing falls, absent from these scenes).
3. **Window cost**: mean readouts per search ≤ 4 (two verifications where g hits; the
   ±k walk adds ≤ 2 per miss step), against the reference's ~11 (grid) / ~29 (flying).
4. **Flight identity**: `frame_digest` digests and kick-bench replay digests bit-identical
   patched vs pristine; leaver kick µs falls toward the bind-only floor (the search term
   collapses; the flying leaver median should drop well under the shipped 199 µs line,
   order-of-magnitude Linux box).
5. **Composition**: if flight fallbacks = 0, the warm start + AB-IQI stack (2ae0, not on
   main) has no work left on these scenes — the structural guess subsumes its domain and
   the stack becomes fallback insurance only. Kill for the claim: any tick mismatch, any
   digest change, or fallback > 5% on mid-fraction held-out cases (the offset would then
   be law, not noise — ff42's kill criterion, unchanged).
