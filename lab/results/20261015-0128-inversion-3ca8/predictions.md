# Predictions (written before the decisive run)

Question: does the shipped dense-order contact law (`es-lattice-relativistic-v1`, chronon
stepper, engine Q = 2²⁰) mint **false behaviour classes** in a many-body chaotic scene,
against a float twin of the same loop (same bins, same detection semantics, same id-order
sequential response, continuum SR impulses, no lattice rounding, no carries)? This ports
redteam-5cad's standard-map dwell result (chaos-shadowing page, open direction 1) onto the
shipped law's own machinery.

Scene: a 2D channel box, one heavy shuttler (mass 1000, β 0.6) + 64 light tracers (mass 1)
= the Fermi-pump regime the contact-carry runs measured two-body. Arms: `engine` (shipped
chronon, RelativisticV1), `float` (the twin), `coarse` (engine at Q = 2¹⁶), plus controls.

## Pre-registered expectations (not tuned on)

1. **Control-pos (equal masses, β 0.05): engine ≈ float.** Contact-carry measured equal-mass
   contacts exact to 1.4×10⁻⁶ per contact, so the per-body contact counts and the final-β
   distribution should agree closely (final-β quantiles within ~10%, contacts within ~5%).
   If they do not, my twin is the wrong instrument and the run reports that, not the law.
2. **Control-neg (one heavy + one light, 1000:1, β 0.6, the known-failing case): engine ≠
   float.** Contact-carry/33f1 measured γ pumping to 30–170 within ~15 contacts and |Σres|/KE
   median 7.4×10⁻³ at 2²⁰. I expect the engine arm's light body to end at a γ materially
   above the float twin's (ratio ≥ 2 in final β or in trapped dwell).
3. **Decisive arm (64 lights, 1000:1, β 0.6, engine Q): the tail diverges, the bulk holds.**
   Prediction: the light bodies' final-β **median** stays within 1.5× of the float twin
   (most lights are never pumped; most contacts are low-contrast-in-effect), but the
   **pumped tail** (p90/max final β, dwell above β 0.5, count of bodies still above 0.5 at
   the end = the "capture that never dissolves" class) exceeds the float twin by ≥ 2×.
4. **Coarse Q = 2¹⁶ exaggerates the distortion** (5cad found coarse Q crushes/inflates
   non-monotonically; contact-carry found per-contact error ~100× larger at 2¹⁶: 0.46 vs
   3.7×10⁻² of KE): I predict the tail distortion at 2¹⁶ is larger than at 2²⁰ (same sign),
   not smaller.
5. **The ledgers stay exact in every engine arm** (residual/carry bookkeeping never blows
   up) — the distortion, if present, is invisible to the law's own exactness certificates,
   which is the point: no gate, digest or ledger can see a false behaviour class.

Kill criterion for the premise "quantization mints false classes in the shipped dense
order": if in the decisive arm the engine and float tails agree within 1.5× on every tail
metric (p90 β, max β, trapped fraction, max dwell), the shadowing worry does **not**
transfer to the shipped dense order in this regime, and I report the clause as standing
there (domain-limited).
