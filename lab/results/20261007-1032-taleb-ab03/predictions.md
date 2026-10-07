# Predictions (written before the decisive run)

Probe: belt H_live rate under the plane's real dynamics (Giant μ=2⁻¹⁰ at 4.94 AU, e=0.05;
belt 2.0–3.5 AU, Rayleigh e σ=0.1, uniform angles; N=65,536 test particles + 4,096 Giant-crossers
at 5.5–6.5 AU). Wisdom–Holan drift-kick, heliocentric with the indirect term (law.md: "the origin's
fall"). Drift is exact per body; the "program" is the frozen birth state plus exact Kepler drift
(what shipmem's program covers for free). Scars = quantized column deltas vs the program, at the
tube's widths: E Q48 over the belt span, L Q32, ω and mean-phase u32 over 2π. Play-hour =
0.0114 game-yr at rtf 100 (1 AU orbit = 1 yr, solar-normalized).

1. **μ=0 control:** zero scarred bodies at every epoch (the harness measures dynamics, not numerics).
2. **Frozen-program scar at 1 play-hour:** mean 6–14 bits/body, ϖ-column dominated (secular
   precession: every body drifts; none is spared).
3. **Shape:** total bits grow ~ log t (precession-like), not linear; no saturation within 20 yr.
4. **Tail:** p99/mean ≥ 3 at every epoch; the top bodies sit within ~0.05 AU of a strong
   commensurability (3:1, 5:2, 2:1) or the belt edge.
5. **Smooth program control:** subtracting a smooth-in-a median drift curve (what a 2-parameter
   physical g(a) program absorbs) leaves mean ≤ 2 bits/body at 1 play-hour but p99 within 2× of
   the frozen-program p99 (the resonant tail is irreducible).
6. **Reabsorption:** the e-column reabsorbs (periodic forced oscillation crosses zero) but ϖ
   never does (monotone); net scar-set membership is monotone up to the e-column alone.
7. **Crossers:** Giant-crossing bodies (5.5–6.5 AU) gain no encounter scars within 20 yr
   (encounter rate ≪ secular rate at game timescales); if false, an encounter scar appears as a
   step in one body's bits.
8. **Extrapolation:** at 10⁹ belt bodies, the frozen program's lead over its birth cost
   (0.126 bits/body) is erased within the first play-hour; the smooth program's is not.

Kill criterion for the probe itself: if the μ=0 control scars any body, the harness is broken
(VOID). If the smooth-fit control absorbs the p99 as well as the mean (p99 residual < 2 bits),
then H_live at these horizons is program-absorbable and the 8 GB risk from belt H_live is
overstated — that falsifies my premise and I report it.
