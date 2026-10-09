# Predictions (written before the decisive run)

Run: 20261009-2120-redteam-ace6. Oracle: Schwarzschild null geodesics in the equatorial
plane (M = 1), RK4 on u'' + u = 3u^2 with dt/dphi and Euclidean arc length ds/dphi carried
along; emitter on an exact circular geodesic (Omega = r^{-3/2}), static observer. The
design's gather (representation.md §2, law.md "Observation") selects the emission event by
a Newton solve on the cone; its implicit time law is the original conversation's
"retarded observation time t - d/c". Cases below were NOT tuned on.

Notation: "flat" gather = t - d/c with Euclidean d. "Bent" (steelman) gather = light path
bent by the doll's deflection (exact geodesic shape) but timed at flat speed along the arc.
"Exact" = geodesic time transfer. Phase error = Omega * (t_emission_gather - t_emission_exact),
the wrong orbital phase the player is shown.

| # | Held-out case | Prediction |
|---|---|---|
| P1 | r_e = 8M, r_o = 500M, primary image, any alignment | flat phase error 25-60 deg |
| P2 | Same scene, bent (steelman) vs flat | bent >= 90% of flat error (the log-term coordinate delay dominates; arc excess is O(theta^2 b) ~ 0.3M) |
| P3 | Scaling in r_e at r_o = 500M (primary): r_e = 20M | 5-14 deg; r_e = 50M: 1-4 deg |
| P4 | Control, far from the hole: r_e = 400M, r_o = 5000M | < 0.5 deg (the premise survives there) |
| P5 | Ring-lattice time resolution at the observer (cell = r*ln2/16 in time) vs the 1-deg phase resolution needed (0.0175/Omega) at r_e = 8M, r_o = 500M | lattice quantum 30-70x coarser than the effect it must resolve |
| P6 | Winding images (path wraps the hole once) at r_e <= 10M | their extra delay is order one orbit period or more, so their phase error exceeds 90 deg; the deflection(b) memo alone cannot order them |
| P7 | Integrator control: halving dphi changes reported phase errors by < 0.5 deg; deflection of a b = 20M ray matches 4/b + 15pi/4b^2 within 2e-3 rad | must hold, else the run is void |

What would make the attack fail: if P1 and P3 come out <= 2 deg everywhere, the gather's
flat time law is player-fine inside 7-50M and the premise stands (then only P6/P5 could
still bite, and I would report the premise as surviving).
