# Predictions (written before the probe)

Probe: `skin_probe.py` — toy model of the encounter candidate skin tier. Bodies on a belt
(a-sorted), candidate window = 2(R+s) in a-space, conjunction re-evaluation deferred until a
body's accumulated drift (miss-distance units) since its last rebuild crosses the skin s.
Cost units: 1 pair-eval = 1, 1 stored-pair clock compare per orbit = 0.01, fire floor ignored.
Drift per body per orbit: lognormal, median d_med, p99/median = 10. Cases:
quiet (d_med = 0.02 R), kicked (0.1 R), formation (quiet + 5% of bodies at 100x d_med).
Configurations: global s swept over s/R in {0.25, 0.5, 1, 2, 4, 8, 16}; per-body skin
s_i = sqrt(R d_i / c_keep). 20 orbits, N = 20,000, seed fixed.

Cases I did NOT tune on: the formation case and the per-body-law comparison were chosen after
the analytic form but before any run.

1. Global s gives a U-shaped work curve; measured argmin s* matches sqrt(R d_eff / c_keep)
   within a factor 1.5 on the quiet and kicked cases.
2. Formation case: the best global s loses >= 1.5x total work and >= 3x p99 per-body work
   against the per-body law s_i = sqrt(R d_i / c_keep).
3. A global skin sized on the p99 drift (not median) is within ~1.3x of the per-body law on
   total work but still >= 2x worse on p99 per-body work.
4. Controls, both sides: at s = 0.25 R rebuild storms make eval work >= 4x the optimum; at
   s = 16 R the keep term makes total work >= 2x the optimum. If either side fails to show,
   the probe is VOID, not the law.
5. Because s* ~ sqrt(d), a 100x drift tail needs only a 10x skin: skins track
   sqrt(drift), not drift. (Consequence: per-body skins are cheap to size.)

If 2 or 3 fail (global skins match the per-body law), the lesson downgrades to "calibrate one
global skin on p99 drift" and the per-body machinery is deleted (via negativa applies to my
own proposal).
