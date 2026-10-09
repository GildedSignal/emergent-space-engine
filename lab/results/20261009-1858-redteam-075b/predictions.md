# Predictions (written before the decisive run)

Attack: premise 3 + 6 of the lens list — representation.md §3: *"Perturbations are kicks on E and L. A cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add"* and §6's cost row *"Undisturbed orbits … ≈ 0"* / *"A cycle's first computation: new invariants only"*. The memo-hit measurement (5 Oct: 0% on distinct kicks) already forces every kick onto the derivative path or a recompile; the accuracy of that path has never been measured.

Falsifier (float64, C, ≤ 60 s): 1PN Binet orbit u″ + u = C + 3u² (M = c = 1) around one mass. Truth = RK4 (h = 1e-3, convergence-checked) with kicks applied at periapsis as instantaneous element changes with (u, u′) continuous: δC (an L-kick) and/or δu′ (an impulse). The design path carries the cycle map F(C, K) (apsidal advance per cycle) and u_p(C, K) only:
- **stale**: one compilation at (C₀, K₀), exact first derivatives, then multiply-add forever;
- **bucketed**: the live mechanism — memo keyed by quantized (C, K), fresh exact cycle + derivatives per bucket, derivative correction inside the bucket;
- **recompile** (positive control: must match truth), **ignore** (negative control: must fail).

Cases I did NOT tune on (held out until after the sweep): systematic-sign kicks at ε = 1e-5 (between my sweep points), and the near-separatrix orbit (e = 0.8, p = 8.0).

1. **Controls.** Recompile-each-kick tracks truth to < 1e-6 rad over 2000 cycles at every e. Ignore-kicks drifts > 1e-3 rad within 200 cycles at ε = 1e-4.
2. **Curvature is the driver.** The second derivative ∂²F/∂C² (exact, by finite differences on exact compilations) grows by ≥ 30× from e = 0.3 to e = 0.95 at p = 20, and by ≥ 10× more within 1 of the separatrix p = 6 + 2e.
3. **Stale absorption** (random-sign kicks, ε = 1e-6 relative per kick, 2000 kicks): accumulated phase error < 1e-4 rad at e ≤ 0.7; > 1e-3 rad at e = 0.95 or near the separatrix.
4. **Stale absorption under systematic drift** (ε = 1e-4 same sign): error grows quadratically in cumulative drift; crosses 1% of F before 500 cycles at e = 0.7.
5. **Bucketed absorption** (the live mechanism): to hold ≤ 1e-4 rad at e = 0.9 over 2000 kicks needs relative bucket q ≲ 3e-3. At kick size ε, a new bucket (recompile, ≈ 38 crossings by the r1 anchor) comes every ≈ q/ε kicks. At ε = 1e-3, q = 3e-3 that is a recompile every ~3 kicks → ≈ 12–13 recompiles/orbit at 32 kicks/orbit ≈ 500 crossing-evals/orbit: parity with the fixed-step control (350–700 steps/orbit, probe 2). At ε ≤ 1e-4 the compiled path keeps a ≥ 5× win.
6. **Held-out:** systematic ε = 1e-5 sits on the quadratic scaling between 1e-6 and 1e-4 rows (error ≈ 100× the ε = 1e-6 row); near-separatrix e = 0.8, p = 8.0 behaves like the e = 0.95, p = 20 row or worse.

Kill criterion for the attack: bucketed absorption cannot hold ≤ 1e-4 rad over 2000 kicks at any bucket that avoids a recompile per ≳ 10 kicks, for e ≥ 0.85 — i.e. hot orbits pay the kick rate in recompiles and the "≈ 0 / new invariants only" cost premise fails exactly where slingshots live. If it holds everywhere with sparse recompiles, the premise survives and the envelope is the result.
