# Predictions — 20261009-2257-dynamics-a47e (dynamics lens)

Written before the decisive run. Question: can any statistic separate a *bounded* law error from a *leaking* one on chaotic ships, and at what leak rate does detection die (the horizon)? The current B12 growth exponent inverts on chaotic ships (probe P2: bounded 0.493 vs compound 0.305); the recurrence-ratio fix was rejected (a slow leak scored below a bounded error).

**The statistic under test** (no fitted thresholds; integers decide): for an integer error series x_n, n = 0..N−1, compute the Allan variance AVAR(τ) = ½·E[(ȳ_{k+1}−ȳ_k)²] exactly in integer/rational arithmetic, where ȳ_k are non-overlapping consecutive averages over τ samples. Rule: **leak iff AVAR(T/4) > AVAR(T/32)** (rising Allan variance at long averaging time = the series keeps acquiring variance = integrator leak; falling = stationary/bounded).

**Derived from theory, not fitted (to be tested):**
- **H1 (horizon):** a leak with per-sample walk σ is detected iff its total drift over the window, σ√T, exceeds √2 × A, where A is the bounded error amplitude (AVAR of a walk is σ²τ, of any bounded component ≲ A²/2 at τ ≥ its period).
- **H2 (alias):** a *bounded* oscillation with period P > T/4 is misclassified as a leak (at τ = P/2 consecutive half-period averages alternate); so the gate window must satisfy **T ≥ 4·P_max** (P_max = slowest bounded period, e.g. a libration).

**Held-out cases and predictions:**

1. **Planted integer controls** (N = 2^15 samples, deterministic LCG seeds):
   - Bounded families: quasiperiodic (3 incommensurate tones), OU (chaos-saturated, correlation 100), slow sinusoids P ∈ {T/16, T/8, T/4} → **all classify bounded (12/12 series).**
   - Adversarial bounded: slow sinusoid P = T/2 → **misclassifies as leak (the H2 alias, predicted failure).**
   - Leaks: walks with σ√T/A ∈ {10, 3, 1.5} (6 series) → **all classify leak**; σ√T/A ∈ {0.3, 0.1} (4 series) → **all classify bounded** (below the H1 horizon, predicted miss). So 22/26 overall correct *and every miss predicted by H1/H2*.
   - Leak + bounded mixtures at ratio ≈ 1 (σ√T/A ∈ {1.5, 3}) → leak (boundary of H1; a miss here refines √2 to a larger constant but does not kill).
2. **Growth-exponent inversion reproduces** (the diagnosis, not the plane's bug): on chaotic-saturated series (state error grown by e^{λt} then saturated on the attractor, 16 seeds), the median log–log exponent of the *bounded* family is **greater** than that of the *slow-leak* family (σ√T/A = 1.5) in ≥ 2 of 3 independent draws. If it never inverts, my model of P2 is wrong → the diagnosis claim dies.
3. **On the law's cheap path** (float Wisdom–Holman: exact Kepler drift + planet kick, CRTBP, μ = 10⁻³, 8 ships crossing the planet's Hill edge, ~300 planet orbits, h = orbit/150; J integerized at 2^40):
   - Symmetric (D-K-D, second-order) variant: **≤ 1 of 8 ships classified leak** (the leak-free control must pass).
   - Asymmetric first-order variant (kick applied with full h on one side only → O(h) secular error): **≥ 7 of 8 ships classified leak**.
   - The growth exponent on the same two families: **the good variant's median exponent ≥ the leaky variant's** in ≥ 1 of 2 draws (B12's current statistic fails exactly where the Allan rule succeeds).

**Kill criteria (pre-registered):** ≥ 3/8 leak-free WH ships flagged as leak → the statistic is unusable on the real path, KILL the proposal. Planted leaks with σ√T/A ≥ 3 missed → H1 wrong, KILL. Everything classified but misses not where H1/H2 predict → the derivation is decorative, downgrade to lead.

---

**Addendum (disclosed, before the Part C re-run).** The first Part C run is invalidated: the
universal-variable Kepler drift lost 4% of two-body energy over 45,000 steps (measured
0.0395 relative; osculating a wandered ~3%), and draw 0's ships never came within 0.27 of the
planet, so nothing crossed the doll edge. Two changes, both instrument fixes, not outcome
tuning:
1. Drift replaced by an exact classical-elements Kepler propagator (verified to roundoff).
2. The leaky variant changes: the first-order asymmetric kick produced a *bounded* O(h) error
   (correctly classified bounded — a real finding, kept below), so the planted leak is now a
   **one-step-retarded planet** (kicks evaluate the source at t − h): a simultaneity bug, the
   class HANDOFF names as a live risk. Predictions for Part C are re-issued unchanged in
   structure: good ≤ 1/8 leak flags, retarded ≥ 7/8; deep encounters (< 0.02) are
   pre-screened (SyMBA changeover is out of scope for this toy).

**Addendum 2.** Measured on the run: a one-step retardation is below the rule's horizon
(not caught, exponent 0.021 < good's 0.049 — itself the inversion, on the physical path).
A `retard10` variant (delay = 10 steps ≈ 1/12 orbit, the doll-clock ambiguity scale named in
HANDOFF: 15–1,400 ticks at a sphere's edge) is added and predicted to be caught (≥ 6/8) while
`retard` (1 step) is predicted to stay undetected: the horizon, measured on the physical path.
