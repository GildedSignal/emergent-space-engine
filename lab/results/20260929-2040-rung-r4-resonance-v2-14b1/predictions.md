# Predictions (written before any law run)

Calibrated only on the truth (cases 0–4, dense RK4). The law configurations have not been run at the time of writing.

## Setup reconstruction (the red-team's `e1_resonance.py` is not in this container)

Frozen: restricted 3-body, coplanar, G=1; primary M=1; inner test particle m1=0, a1=1, e1(0)=0.01, varpi1(0)=0, M1(0)=0; perturber m2=3e-3, circular, varpi2=0, w2 = lambda2(0) = 0 (base) or 4.0 (shifted); period ratio 2:1 exact (n2 = n1/2, a2 = ((1+m2)/n2^2)^(1/3)); 200 synodic periods; sample cadence 25/inner orbit. Truth-2400 (converged max_e to ~1e-6 vs 600/1200) is the reference.

## Truth anchors achieved

- res-2to1: max e1 = 0.1417 (14x the initial e); conc = 0.34-0.53 depending on resolution.
- res-2to1-shift: max e1 = 0.1713 (close to the rung's 0.175 anchor); conc = 0.22-0.30.
- Known weakness: the concentration of the truth is not resolution-converged (chaotic resonant angle): base 0.53@1200 vs 0.34@2400, shift 0.29 vs 0.22. max_e is converged to 3e-6. I report this and judge against truth-2400 as frozen.

## Predictions

- truth-1200 (positive, judged vs truth-2400): e_pump ratios 1.0000; lib ratio >= 1.3 (conc@1200 > conc@2400 in both resonant cases); controls pass; dense_steps 0; kicks 0. It passes every criterion.
- arc-g8 / arc-g16: pump ratios in [0.8, 1.25] (first-order Gauss-Picard captures the pumping rate; the libration feedback keeps phase errors from compounding monotonically). g16 ~= g8 (the integrand along 1.5-orbit windows is smooth; quadrature error is not the bottleneck). lib ratio: expected in [0.7, 1.6]; the risk is that the law's angle decorrelates from the truth's chaotic realization and the concentration ratio lands below 0.8 even though the law librates. Controls pass. kicks_per_orbit: median over the five cases = 0.683 (conjunction rate 1 - n2/n1 per inner orbit).
- arc-g8-half: same behaviour, slightly better phase tracking; kicks median 1.37.
- averaged (negative): the orbit-averaged kick erases the conjunction phase; e1 stays within secular wiggle of 0.01 -> pump ratio ~0.06-0.25 (FAIL pump), conc ~ 0 -> lib ratio << 0.8 (FAIL lib). The 2.15 control also fails for it (truth envelope 0.0403 vs ~0.010).
- none (negative): pump ratio ~0.07 / 0.06 (FAIL), conc -> circulation (FAIL lib), controls: r5.00 and r2.55 pass (truth envelopes ~0.0103/0.0100, none 0.0100 -> within 20%), r2.15 fails (0.0100 vs 0.0403).

## What would falsify the arc design here

If arc-g8's pump ratio lands outside [0.8, 1.25] with g16 agreeing, the first-order windowed map itself misprices the resonant pump (v1's over-pumping would then be about the map, not the instantaneous-kick approximation). If g8 != g16, quadrature resolution is the bottleneck and the window needs finer nodes. If lib ratio fails while the angle visibly librates in the series, the criterion is measuring chaotic decorrelation, not the law.
