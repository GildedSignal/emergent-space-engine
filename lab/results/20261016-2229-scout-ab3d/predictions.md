# Predictions (written before the decisive run)

Question: can a sound, cheap angular certificate replace the player's in-belt O(N) scan walk
(scan-queue: S = (N−314)×4.2 µs, 340× over the S < b/2 ≈ 6 ms bar at 10⁵, unmeasured beyond)?

The falsifier: a float replica of the shipped belt (`scenario.rs::ladder_ship`: a ∈ [2,3) AU,
e Rayleigh σ=0.07 redrawn above 0.4, uniform ω and phase; ship radius 34·2⁸ root units ≈ 12.9 km;
`near` = 2¹⁰·(r_a+r_b); h = the belt interval 28,141.5 s and 1,000 s), truth = the float twin of
the shipped predicate (linear relative motion over [t, t+h] within `near`, positions/velocities
from Kepler). The certificate: stage 1 = mean-longitude window widened by each body's exact
max|ν−M| (the checker2-corrected sound form of 3999's price), stage 2 = anomaly-resolved true
longitude (Newton or a 4-term equation-of-center series widened by a tabulated tail ×1.5), then
the exact readout on survivors.

Numbers I expect, derived by arithmetic before running (held-out cases marked †):

1. Stage-1 keep fraction (σ_e 0.07, h = 28,141.5 s): 4–12% of N. This is the replica control:
   it must land in 3999's sound-price band (4.5–9% at their margin; mine is per-body exact).
2. Stage-2 keep fraction: 0.08–0.3% of N (arithmetic: ε_θ = (near+|w|)/r ≈ 3–8×10⁻³ rad,
   shear over h ≈ 0.3–0.6×10⁻³ rad, uniform phases → (2ε_θ+2·shear)/2π ≈ 1.2×10⁻³).
3. Survivors to the exact readout ≈ stage-2 count; at N = 10⁵ that is ≤ 0.5 ms of readouts
   (≤ 120 × 4.2 µs), and the answer S(10⁵) lands at 0.6–1.5 ms total → under the 6 ms bar.
4. † At N = 10⁶ the composition with the shipped 4.2 µs readout lands at 4–9 ms (marginal:
   the readout bill ~1,200 × 4.2 µs ≈ 5 ms alone); with a 0.5 µs closed-form readout it is
   under 3 ms. I predict the bar is met at 10⁵ and marginal at 10⁶ on the shipped readout.
5. † Stage-2 cost: 15–60 ns/candidate for the series form, 40–120 ns for Newton (x86, orders
   of magnitude). If > 200 ns, the price claim dies (kill criterion K3).
6. † Soundness: zero missed true hits on every default scene and every seed, including the
   positive control — a formation cluster of 500 bodies placed at the querent's own phase
   (truth non-empty; correlated phases are where a too-tight cut must fail; any miss = K1).
7. † Negative control (cost, not soundness): an all-e=0.4 belt — stage-1 keeps 25–50%, the
   composed S blows the bar; the tail regime is the certificate's failure domain and belongs
   to the phase-neighbour rank (taleb-09b5) or the population answer.
8. † Halving h to 1,000 s: keep fractions fall ~proportionally to ε_θ (the |w| term shrinks);
   S falls with them.
9. † Fresh seeds (2, 3): all fractions within ±30% of seed 1's.

Kill criteria, pre-registered: K1 any true hit rejected (the configuration is unsound as built);
K2 composed S(10⁵) > 6 ms; K3 stage-2 cost > 200 ns/candidate. A KILL kills this configuration,
never the method (PRINCIPLES 9).

Free parameters and how they are fixed before looking at miss counts: the series tail margin is
tabulated on a dense (e, M) grid against exact Newton and widened ×1.5; ε_θ is widened by 10⁻⁶ rad
(float hygiene); nothing else is tuned.
