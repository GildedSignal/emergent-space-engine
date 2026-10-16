# Predictions — 20261016-1120-scout-79ed (binet-cells, the per-band u_k refit)

Written before the decisive run, from analysis only (fe85's record, the frozen r1 rung, the
ported oracles). Arms: FROZEN (u_k = band geometric centre, the r1 letter), CONT (frozen,
except an orbit contained in one band uses u_k = sqrt(u_peri·u_apo) of its own turnings),
GEO (one law for every band: u_k = sqrt of the geometric mean of the u-extremes the orbit
attains inside that band — identical to FROZEN for purely crossing bands).

P1 (fe85's family reproduces): FROZEN m=16 deterministic e=0 circles placed at the worst
band offset fail the 0.1% period bar at p below ~60; m=32 below ~35. Advance error there is
first order (ratio ~ band offset), halving per m-doubling.

P2 (the refit deletes the family): CONT and GEO put the same circles at the float floor
(< 1e-10 relative) at every p in [8, 1000], both placements (edge and centre), every m —
because with u_k = u_c the band ODE's circular solution coincides with the exact GR circle
(1/L^2 = u(1-3u) makes u_p = u_c, A = B = 0).

P3 (sampler, m=16): FROZEN reproduces fe85 (period 255/256, precession 255/256; the miss
is the near-circular seed ~p=13.6, e~0.002). CONT and GEO: 256/256 on both. m=32 stays
256/256 everywhere. Crossings median unchanged (57 ± 3 at m=16).

P4 (held-out strong field, no regression): at (p=8.5, e=0.9) FROZEN advance error ~1e-3
(fe85); GEO shifts it by less than 2x in either direction (the periapsis turning band's
constant moves toward the visited range — direction not predicted); CONT is bit-identical
to FROZEN there (not contained). Separatrix-margin rows (p-(6+2e)=0.3) stay under 5e-3.

P5 (plunge branch unchanged): ISCO both rows correct and capture misclassified = 0 in all
three arms at m=16 (the refit only moves constants toward visited ranges; r=5.5-band
constants stay above 1/6).

P6 (the law property, the honest cost): GEO changes u_k in the two turning bands of every
bound orbit (periapsis and apoapsis bands always contain a turning), so it changes the
advance of nearly every seed at second order — no digest compatibility anywhere; CONT is
bit-identical for every multi-band orbit and changes only the contained family. Predicted
fraction of sampler seeds whose m=16 advance moves > 1e-6 relative under GEO: 90-100%;
under CONT: 0-15% (only near-circular straddling/contained seeds).

P7 (m=8, exploratory, may fail): fe85's m=8 failures (precession 252/256, period 245/256)
are dominated by the near-circular family, so CONT/GEO lift m=8 precession to >= 0.99; the
period may still sit below 0.99 (second-order eccentric tail at the 8.7% band width). No
confidence: this is the run's one genuinely uncertain call.

Kill bar for the candidate (stated before the run): if CONT or GEO leaves any deterministic
worst-offset circle above 1e-6 relative period error, or drops the m=16 sampler below
FROZEN's pass counts, or misclassifies any capture/ISCO row, the refit is dead as stated.
