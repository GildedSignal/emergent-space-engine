# Predictions — run 20261006-0737-q-secular-v2-5f69 (second author on q-secular)

Written BEFORE the decisive belt runs, per the lab README. This run re-does
20261005-2231-q-secular-008e with the checker's required fixes; the scene, laws,
selector, estimators and kill arithmetic are the first author's, unchanged except
for the three fixes below, all made before any belt run and disclosed here.

## Fixes made before the decisive runs (and when they were justified)

1. **`accel()` accumulation** (the checker's finding): pass j now contributes to
   every row except row j itself; run 008e's `out[j] = 0.0` wiped row j's previous
   pass (Saturn never kicked).
2. **Planet LL matrix α-power**: the outer planet's row now carries single α
   (against b_{3/2}), the inner row keeps α². Justified BEFORE any exact run by the
   quadrupole limit of the doubly-averaged l=2 disturbing term with the Lagrange
   equations' 1/(n_i a_i²) prefactor: inner body ϖ̇ ∝ (m_k/M) n_i α³ = (n_i/4) μ α²·3α,
   outer body ϖ̇ ∝ (m_i/M) n_k α² = (n_k/4) μ α·3α. Run 008e used α² in both rows.
   Test-particle (belt) rows are α² under either convention and are unchanged.
3. **mu-consistent initial velocities** (checker's minor note): n = sqrt(mu/a³)
   with mu = 1+m, so the initial state is exactly the intended osculating
   (a, e, ϖ, M) of each body's own drift problem.

Instrument runs made before this file (planets only, no belt): the tolerance
ladder and the LL-driver comparison [C]. Their planet-level numbers (exact |z_S|
dips to ~0.004 at t ≈ 84 kyr, ends ~0.046; |z_J| rises to ~0.060) are therefore
NOT held-out predictions; everything about the belt below is.

## Frozen scene (as the first author specified, with fixes 1–3)

Sun (GM = 1) + Jupiter (a = 5.2026, e = 0.0484, μ = 9.54e-4, ϖ = 0.8) + Saturn
(a = 9.537, e = 0.0539, μ = 2.858e-4, ϖ = 2.1), mutually interacting, heliocentric
WH (per-body Kepler drift, midpoint kick, direct + indirect terms). 1,024 belt test
bodies: a ~ U[2.0, 3.3], e_free ~ U[0.02, 0.23], β ~ U, M0 ~ U, z(0) = z_forced(a)
+ e_free e^{iβ} with z_forced from the corrected matrix; β redrawn while |z(0)| >
0.25 (so e ≤ 0.25 as specified). T = 149,022.4 = 2,000 Jupiter orbits. Seed 20261005.

## Frozen laws

1. **LL**: first-order Laplace–Lagrange, exact Laplace coefficients, planets on
   their mutual modes from the corrected 2×2 matrix. (Run 008e's α² matrix variant
   is reported as a driver diagnostic, not as the law.)
2. **Rings**: exact double averaging (Gauss rings), 24×16 midpoint quadrature,
   RK4 at dt = T/384, planets on their LL-mode ellipses (driver = corrected LL).
3. **Kick (the plane's)**: same WH as truth at h = P(2 AU)/64 = 0.2776.
   Truth h = 0.125 (1,192,179 steps); convergence partner h = 0.1875.

## Frozen estimators and kill arithmetic (unchanged from 008e)

amp = e_free; ĝ = linear fit of unwrapped arg(z − zf_LL(t)) over samples with
|z − zf| > amp/3; rate_err = |ĝ_law − ĝ_truth|/ĝ_truth; evec_err =
max_t |z̄_truth − z_law|/amp; PASS = rate_err ≤ 0.05 AND evec_err ≤ 0.10;
Fraction(L) = |admitted AND PASS|/1024. KILL R2 if Fraction(rings) < 0.50 or if
any admitted body was inside a resonance's width measured from run-averaged ⟨a⟩.

## Frozen truth-verification protocol (new this run, stated before the truth runs)

The planets-only ladder decides between unconverged numerics and chaos. Bars:
- drift self-test vs DOP853: < 1e-13 (measured 1.8e-15 ✓).
- exact heliocentric vs exact barycentric: pairwise ladder gaps must either stay
  < 1e-6 over the whole run, or define a divergence onset t_div; if the ladder
  runs disagree with each other at fixed tolerance (non-monotonic in rtol), the
  instrument is broken and the run stops.
- WH(h = 0.125) vs exact: max|Δz_S| < 5e-3 (10% of Saturn's e scale) up to t_div;
  beyond t_div the comparison is envelope-only (min |z_S|, dip time, |z_S|(T)
  within ~15%), because no float integration of a chaotic trajectory can do better
  and PRINCIPLES #2 makes behaviours, not trajectory identity, the standard.

## Predictions (belt = held-out; nothing belt-level has run)

1. Admission fraction 0.77–0.84 (selector frozen; zf shifts slightly with the
   corrected matrix, mostly through the e_eff and linearity guards).
2. Convergence (h = 0.1875 vs 0.125 on z̄): median |Δz̄| ∈ [2e-5, 5e-4], p90 < 2e-3.
3. **LL**: Fraction(LL) ∈ [0.00, 0.15]. Even with the corrected driver, first-order
   LL cannot follow the belt's nonlinear amplitude response to 10% of amp.
4. **Rings**: Fraction(rings) ∈ [0.40, 0.75] — the honest coin-flip zone. It passes
   the inner belt strongly (a < 2.5 AU, where 008e's rings already tracked the
   swing with a wrong driver) and degrades outward (α_S up to 0.35, α_J to 0.63,
   second-order-in-μ secular coupling). My lean: just below the bar.
5. **Leak clause**: 5–40 admitted bodies end inside an MMR width from ⟨a⟩
   (chaotic a-diffusion at resonance edges is real physics the κ = 2 width model
   does not fully contain, and the corrected driver does not remove it).
   → Predicted verdict: **KILL** (~75% via leak clause, remainder via fraction),
   now against a truth whose Saturn actually exchanges secular amplitude.
6. Kick law: 3:1 and 5:2 depletion signature reproduced (pumped fractions within
   20% of truth's in both zones); median evec_err(kick) on admitted bodies ∈
   [3e-4, 3e-3]. Same-integrator caveat as 008e applies.
7. If Fraction(rings) ≥ 0.5 AND zero leaks (the surprise): R2 survives at belt
   scale with a corrected driver, and 008e's kill was the bug, not the physics.

## What would make this run wrong

- The ladder showing the exacts disagree non-monotonically with tolerance
  (instrument, not physics).
- WH-vs-exact exceeding 5e-3 before any divergence onset (another code bug).
- Estimator sensitivity to zf_LL(t) from the corrected matrix corrupting ĝ the
  same way for all laws (it cancels in law-vs-truth differences; if it does not,
  the rate estimator is the suspect, not the laws).
