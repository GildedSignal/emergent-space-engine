# Predictions — 20261007-0621-components-8306 (the kick's rebind, the jet on the integer law)

Written after the cost calibration only (compile ≈ 4.9 µs fresh key, 0.49 µs memo hit;
weak-field p-only kicks already hit the memo). The scan (C measurement) and all stream
runs below are decided before running them. Held-out cases are the ones I did not tune on.

- **P1 (scan, C).** Jet error against an exact recompile scales as C·drift² (drift =
  max |ln p|, |ln e| since anchor) with C = O(1) for the advance and the period
  (df81's float C ≈ 1.9–2.0 for Δφ; I expect the same order on the integer compiler).
- **P2 (scan, jump floor).** The integer compiler's increments as a function of the key
  are piecewise-smooth (panel layout, cuts, separatrix conditioning change discretely).
  I predict a visible jump floor in the error at small drift, from re-paneling:
  error(δ→0) plateaus at 1e-9…1e-7 rather than 0. If the plateau exceeds ~3e-8 the jet's
  achievable accuracy is set by the compiler's discreteness, not the Taylor remainder.
- **P3 (stream, belt row).** Correlated kicks ε = 1e-6 on e, weak field (p = 5.27e8,
  e = 0.1), n = 10 000, floor 1e-6: the drift rule (δ* = √(floor/2) ≈ 7.1e-4) re-anchors
  about every n* = δ*/ε ≈ 700 kicks, compiles/kick ≈ 5/700 ≈ 0.007 (5 compiles per
  anchor: 1 exact + 4 central-difference derivatives), and max error stays ≤ floor.
- **P4 (stream, big kicks).** ε = 1e-4 correlated: n* ≈ 7, compiles/kick ≈ 0.7 — no win
  over always-compile (1.0/kick). Confirms df81's catastrophic row on the integer law.
- **P5 (stream, Peters row).** Strong field (p = 50, e = 0.5), p-kicks ε = 1.1e-3 growing
  (df81's a = 20–50M numbers): re-anchor nearly every kick; the jet is useless there
  (the law already adopts Peters' a(t) as the generator — this confirms why).
- **P6 (negative control).** Frozen anchor increments (no derivatives), same belt stream:
  error grows linearly in drift and exceeds the 1e-6 floor within ~10 kicks at ε = 1e-6
  (the harness detects drift; the jet's derivative term is what buys the two extra orders).
- **P7 (held-out, high e).** e = 0.9 (near-separatrix): C for the period grows ≥ 10× vs
  e = 0.5 (the clock is singular at e = 1), n* shrinks ~3×, but the rule still holds
  (max error ≤ floor).
- **P8 (held-out, strong field both axes).** p = 50, e = 0.5, ε = 1e-6 on both axes
  coherently: no weak-field collapse, both partials live; same law as P3.

Kill criterion for the jet configuration: if P3's max error exceeds the floor with the
rule active (the re-anchor rule does not bound the error on the integer compiler), or if
the jump floor of P2 exceeds 1e-6 at any (p, e) in the scan, the jet is killed as a
per-kick mechanism on this law and the compile stays.
