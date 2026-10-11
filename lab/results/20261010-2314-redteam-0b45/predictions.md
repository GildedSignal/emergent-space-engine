# Predictions (written before the decisive experiment)

Attack: the view's gather (representation.md §2 "Light is gathered at the observer";
law.md "Positions are gathered at the observer's past light cone. Lensing takes
deflection(b) from the doll's memo"). The specced mechanism — one Newton solve of
the emission time from the tube, plus a deflection(b) memo for the arrival
direction — contains no term for the curved optical travel time (Shapiro delay).
The retarded emission event is then solved with a straight-line light time.

Setup: Schwarzschild, G = c = M = 1, equatorial 2D (the game's plane). Static
observer at r_o = 1000, emitter on a circular orbit (exact: dφ/dt = r^(-3/2)) at
r_e ∈ {6, 8, 10, 20, 50}, local orbital β = √(1/(r_e−2)) ∈ {0.5, 0.41, 0.35,
0.24, 0.15}. Oracle: null geodesics by exact first integrals (u″ path equation,
dt/dφ = 1/(b·u²·(1−2u))), integrated by composite Simpson with a turning-point
substitution. Attacked gather: bisection/Newton on t_obs − t_e = Euclidean
distance (identical tube, identical Newton — only the light-time model differs).
Primary image; orbital phase swept over 60 points, occultation-capped.

Cases I have NOT tuned on (held out): the exact per-radius numbers below come
only from the Fermi estimate Δt ≈ 2M·ln(4·r_e·r_o/b²); nothing has been run.

1. Flat control (integrator machinery, 2u³ and (1−2u) terms removed): the
   u-space integrals must reproduce Euclidean Δφ and travel time to < 1e-6
   relative, and the gather's emission-time error δt must be < 1e-6 M.

2. Oracle against textbook GR (independent check): the curved-minus-flat travel
   time agrees with 2M·ln(4·r_e·r_o/b²) within 5% for b ≥ 15.

3. The gather's emission-time error equals the Shapiro delay of the same path
   (two independent computations of the failure): |δt − Δt_Shapiro| < 1e-6 M.

4. Held-out magnitudes (Fermi only): at r_e = 8, r_o = 1000, the emission-time
   error reaches 5–15 M at conjunction and has median 2–6 M over the orbit; the
   apparent displacement of the sprite along its motion is r_e·Ω·|δt| ≈ 1–4 M
   (3–25% of the orbit radius), i.e. 1–4 px at 1080p framing the whole system
   (frame ≈ 2000 M) and 50–200 px when zoomed to frame the orbit (frame ≈ 2.2·r_e).

5. Scaling with β (held out): the displacement scales ~linearly with β
   (r_e = 6 vs 50 differ by ~3× in β; the delay also grows as b shrinks near
   conjunction, so I expect the max to grow slightly faster than linearly).

6. A premise that should survive: the cost table's "≈ 0 for undisturbed bodies"
   (§6) survives a Fermi check — 10⁹ bodies × 0.3 kicks/orbit ÷ 10⁴ s ≈ 3×10⁴
   kicks/game-second, consistent with the table's 6×10⁴ at 50 ns each; the
   resonance-adjacent fraction of a belt (~10% within W = 2.5·μ^(2/3) of the
   strong low-order resonances at μ ~ 10⁻³) triples their kick rate and stays
   far below a core. No measurement needed beyond arithmetic.
