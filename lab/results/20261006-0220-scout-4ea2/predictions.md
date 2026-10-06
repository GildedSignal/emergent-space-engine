# predictions.md — 20261006-0220-scout-4ea2 (written before the decisive float run)

Scene: B13's (xtask/src/behave/restricted.rs): μ = 1e-3, sep = 5.27e8, R_p = 4.84e4,
SOI = sep·μ^0.4 ≈ 3.33e7, planet period P = 2π·sep^1.5. Ships per assist.rs: q ∈ [1.2,50] R_p
log-uniform, v∞ ∈ [1.67e-5, 6.7e-5], ψ uniform, start at 1.5·SOI on the incoming hyperbola.
My own RNG, not the gate's stream. Truth: DOP853 rtol 1e-12, checked against 1e-13 (the gate's
own convergence rule, 1e-4). Nothing is tuned; the patch radius is swept, not fitted.

Already observed (reproduction, not a prediction): the plane fails B13 60/64 with worst
ΔE 1.26; PLANE_TRACE shows two failing-class ships with handoffs=0 (kicks=2 and kicks=113 over
the whole window) — the entry into the planet's doll is never seen.

Laws compared, all asked for the state at the truth's t_exit (the gate's protocol):
- L1 starved cadence (negative): heliocentric drift-kick, H = 2^round(log2(T_pass/64)),
  T_pass = the heliocentric conic's passage duration (2× periapsis-to-start leg); the kick is
  the planet's direct pull at the interval midpoint. This is the plane's star-doll rule.
- L2 one event (patched conics, Öpik/Valsecchi): heliocentric Kepler outside a patch sphere of
  radius R_pch, one exact planetocentric hyperbola inside; entry/exit found by root-finding on
  the two conics (analytic detection, zero stepping). R_pch ∈ {0.5, 1.0}·SOI.
- L3 event + resolved interior: same analytic entry; inside the patch, drift-kick with drift =
  planetocentric Kepler and kick = the star's tide, H_in = 2^floor(log2(T_enc/64)), T_enc = the
  passage duration inside the patch (the plane's own in-doll rule); exit at the outward patch
  crossing; heliocentric Kepler after.

Seed sets: A matched (48 from B13's distribution), B near-parabolic corner (16 smallest
e_h − 1 from a wide ψ scan, v∞ near the top of its range), C fast (8, v∞ = 6.7e-5, q ≤ 5 R_p).

## Predictions

1. **L1 starves where e_h → 1.** It fails ≥ 8 of set B's 16 (rel err > 1% in ΔE or ΔL), and its
   failures correlate with ≤ 4 kick boundaries landing inside the encounter window. The ratio
   T_pass/T_enc (what a pure-cadence fix would have to pay) grows ≥ 50× over the set as
   e_h − 1 falls below ~0.3; the event laws pay nothing there (events independent of e_h).
2. **L2 (one event) fails slow encounters.** On seeds with planetocentric v∞ ≲ 3e-5 the star's
   tide during the encounter and the planet's pull outside the patch cost > 1% of ΔE (I expect
   median errors of a few % there); on set C (fast) it passes ≥ 7/8 within 1% at exactly 1 event.
3. **L3 passes at constant events.** ≥ 90% of judged seeds across all sets within 1% in both
   ΔE and ΔL, at ≤ ~70 events per encounter (1 detection + ≤64 in-doll kicks + 1 exit + 1
   rebinding), independent of e_h — including the corner where L1 fails and the plane's own
   B13 fails today.
4. **Patch radius:** moving R_pch from SOI to 0.5·SOI improves L2's slow-end error but L3 is
   insensitive to it (the interior resolves the tide), so the choice is not load-bearing for L3.
5. **Truth quality:** ≤ 10% of seeds excluded by convergence (1e-12 vs 1e-13) or by the
   reference passing inside the planet; exclusions reported.

What would falsify the adoption claim (L3 as the near-parabolic channel): if L3 needs
significantly more than ~64 in-doll steps to hold 1% (i.e. the interior itself is the cost, not
the entry), or if its error on set B exceeds ~3% (the doll's interior approximation is then not
the plane's real failure mode, and the entry-detection story is wrong or incomplete).
