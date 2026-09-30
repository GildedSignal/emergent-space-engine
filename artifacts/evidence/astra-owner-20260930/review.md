# Owner review of 9b23fb1

Keep Darwin phase. Opus's recorded comparison of 6d64903 found 0.8% advance and
1.4e-3 period error at the old cell boundary; below p=7, 1–4%. His new-law sweeps
reported ~3e-6 advance and ~1e-6 period. The replacement removes the turning-point
slope discontinuity and makes repeated cycles a lookup, rather than a closure search.
No evidence supports reverting to the old map. Current verification is in these logs.

The baseline reproduces all three failures. At Q16 p=6.001007080078125, e=0,
flooring L independently leaves R_c=6,257,216 Q62 units above the stable minimum;
the barrier is only about 804,115 units. This is a quantization bug, not a negative-D
tolerance problem. Boundary conversion v2 floors L first, then E from that L's
potential at the requested periapsis (at the stable minimum for e=0).
Existing Key::new invariants retain their meaning. The whirl oracle now evaluates
Q16 p and Q30 e, which the constructor actually receives; its gates are unchanged.
The repeat test excludes the next cycle's endpoint. The smoothness test checks the
compiled turning-point interval exactly, with two Q62 rounding units.
GL8 nodes are computed once per oracle integral, retaining every integration panel.
The 5 integration tests fall from 20.99 s to 0.08 s; all 16 tests pass.

Baseline: 4,096 uncached compiles, median 18,583 ns, p99 45,292 ns.
Crossing reads: median 2,375 ns, p99 3,333 ns. Stage instrumentation attributes
79.1% to integration, 11.5% to cuts, 7.4% to roots, 2.0% to crossing conversion.
The instrumented run is not the latency result. OS sampling was denied.
Load 3.03/5.37/5.70, AC power, battery 100%; sysctl and thermal queries denied.

Remaining review findings to close in subsequent commits:
- The ellipse assertion uses the false inequality acosh(1+x) >= sqrt(2x).
- A one-unit bisection interval does not imply one-unit continuum root error:
  rounded polynomial residuals are amplified at double roots.
- The claimed universal 2^-30 rounding bound lacks conditioning factors.
- Tube is 32 bytes and lacks velocity; Tangent exposes secants, not certified kicks.
- Epoch and crossing reads reintegrate a panel, despite cached endpoints.
- docs/law.md is absent in this worktree; the integrator must reconcile its motion
  steps 2–3 with Darwin quadrature before merging. This work does not freeze a law.
