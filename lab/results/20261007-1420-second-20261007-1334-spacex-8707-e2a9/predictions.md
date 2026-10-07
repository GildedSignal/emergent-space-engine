# Predictions (written before the decisive runs)

Decisive runs: `hlive2.py --scene belt --sampler {b16,b17} --N 30000 --years 1000 --dt 0.1
--seed {7,8,9} --keep-sub 6000` (6 runs). Scene: the frozen B18b sampler (Darwin p uniform
over [2048, 2560), e Rayleigh σ=0.07 capped 0.6, angles uniform), placed at the two
power-of-two star-doll scales: b16 = [1.32516, 1.65644) AU (quiet), b17 = [2.65031, 3.31287)
AU (5:2/7:3/2:1 inside the band). Giant unchanged (m 1e-3, a 5.2, e 0.048). Smoke tuning was
N ≤ 6000, ≤ 200 yr only. The original scene's numbers (rate 1.0e-3/body/yr at q=1e-3, T*
5–7 yr) are the baseline; the checker's pure-2:1 case bounds a resonance-dominated scene at
5e-3/body/yr.

Held-out predictions:

1. **Null control on the B18b sampler** (m_p = 0, e up to 0.6, Kepler iters 7): max
   |Δa|/a ≤ 1e-11 and max |Δe| ≤ 1e-11 over 1000 yr. If larger, the e-tail breaks the
   generator and every other number is void.
2. **b16 (quiet) long-run rate** at q=1e-3: ≤ 2e-3/body/yr (at or below the original's
   1.0e-3 — a narrower band with no Jovian MMR inside it).
3. **b17 (loaded) long-run rate** at q=1e-3: in [1e-3, 5e-3]/body/yr — between the original
   scene and the checker's pure-2:1 bound. Above 5e-3 the claim's "4–5 orders of magnitude
   below memory pressure" needs restating.
4. **Refit cadence T\*** (first time the out-of-sample crossed fraction at q=1e-3 reaches
   25%, read off frac_crossed_vs_t): b16 in [5, 60] yr; b17 in [3, 40] yr. Both stay
   game-years (weeks of continuous play at rtf 100), which is what the claim needs.
5. **Growth exponent** of the reabsorbed e-residual (50→1000 yr): 0.4–0.8 at both
   placements (the band is 1.25 wide, less F(a) leverage than the original's 1.65).
6. **2:1 edge dominance in b17**: the dv profile's 3.25–3.30 bin ≥ 15× the band's quiet
   middle (2.70–2.75) in median |Δv| (the original scene's outer-edge multiple was 21–30×,
   but its belt had proportionally more non-resonant width to average against).
7. **Fit-noise control**: in-sample vs out-of-sample crossing rate at q=1e-3 within 30% at
   both placements. The degree-5 polyfit has less room on a 1.25-wide band; if this fails,
   the crossing rates are instrument, not physics.

What would kill the claim: (1) failing (void); (3) above 5e-3 **and** (4) below 0.5 yr —
scars arriving at session timescale would mean the resonance-loaded B18b belt CAN force
memory pressure at session scale, refuting the silver run's conclusion on the plane's own
sampler.
