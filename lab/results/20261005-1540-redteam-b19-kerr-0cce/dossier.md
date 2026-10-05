# Dossier: red-team of gate B19 (rotating holes) — the negative-energy dispute settled

## Claim

The builder's verdict is right and criterion (4) is right, but for a wrong-stated reason: **future-directed
negative-energy timelike and null geodesics do exist inside the ergosphere (counter-rotating, L < 0, all
plunge; confirmed by raw Christoffel RK4 integration), but no bound one exists** — every fully-future scan
of the two-turning-point pockets comes back empty — so "every negative-energy solution is past-directed"
is true only of the *bound* solutions, and the judge's `future()` test (P ≥ 0) is exactly equivalent to the
true test (u^t > 0) on allowed states, though its doc-line justification ("dt/dτ has the sign of P") is
false in general.

## Bottleneck

Not a board bottleneck: this is the pre-freeze red-team of B19 (Julien, 5 October: "yeah i like both
especially rotating black holes"). What it deletes is doubt: the gate's most exotic criterion (Penrose)
can freeze as written, with a one-line doc fix in `kerr.rs`/`rotating.rs`; no logic change anywhere.

## Evidence (all in this folder; `python3 oracle.py`, 6 s, exit 0; full log `findings.txt`)

Oracle built from the metric only (equatorial Boyer–Lindquist, M = 1): constants by lowering, u^t three
independent ways (2×2 Cramer solve; A(E−ωL)/(r²Δ); ε/α from the ZAMO split), future = u^t > 0 = E−ωL > 0,
plus a raw RK4 integration of the Christoffel equations (no first integrals inside the integrator).

- **Anchors** (P1): ISCO and photon orbits of both senses at χ ∈ {0.5, 0.9, 0.998} match BPT's closed
  forms to ≤ 4×10⁻⁸ (bisection on a 40-digit finite difference); det = Δ, α² = −g_tt + g_φφω², and the
  radial polynomials (timelike and null) reproduce r⁴ṙ² from the metric to 1.4×10⁻³⁹.
- **Existence, timelike** (P2): at r = (r₊+2)/2, ZAMO-frame v_φ = −0.9995: E = −2.61 / −6.95 / −11.37,
  L < 0, u^t = 187.71 / 120.24 / 129.10 > 0 — identical from all three computations to 30 digits — P > 0,
  R ≥ 0 down to r₊ with **no root of R between r and r₊**: the arc reaches the horizon.
- **Existence, null / Penrose** (P3): the split of a v_φ = 0.6 parent: backward photon E_back =
  −0.0206 / −0.0550 / −0.0900 < 0, ε = 0.25 > 0 (future), u^t > 0, L_back < 0, E_fwd > E₀ (gain 5.2%,
  8.0%, 11.8%), E and L conserved exactly (≤ 1.7×10⁻⁴¹); the same split at r = 3 gains nothing (E_back > 0).
- **Integration** (the falsifier, float64): all three bodies and all three backward photons plunge
  (r → r₊) with u^t > 0 throughout; E drifts ≤ 2.1×10⁻⁴ (bodies) and ≤ 2.5×10⁻¹³ (photons); control
  (retrograde circular, χ = 0.9, r = 12) stays at r = 12.0000 with dE/E = 0.
- **No bound negative-energy orbit** (P4): exhaustive cubic-root scan, χ ∈ {0.01 … 0.9999}, |E| ∈
  [10⁻⁴, 1), |L| ∈ [10⁻³, 10³] timelike (pockets found: 9 → 2087 as χ grows, matching the builder's
  "such solutions exist"), E = −1 null with L ∈ [−10⁴, −10⁻²]: **zero pockets fully future** by the
  builder's P test *and* by the true u^t test (which agree on every pocket).
- **The P test is sound where used** (P5): u^t = A(E−ωL)/(r²Δ), so future ⟺ positive ZAMO energy; on
  611,608 sampled allowed states (R ≥ 0, r > r₊): sign(u^t) = sign(P) = sign(E−ωL) with **zero**
  mismatches; zero future E < 0 allowed states at r ≥ 2 — criterion 4(b)'s "nowhere else" holds (the
  forged (E, L) at r′ ∈ (2.2, 30) are each refused for a true reason: R < 0 or u^t < 0).
- **Planted laws** (P6): (a) ω := 0 answers E = +7.75 (never negative) and dφ/dt = −0.1136 < 0 inside
  the ergosphere → fails 4(a) and 3; (b) Schwarzschild fudged to the ISCO keeps b_c = 3√3 = 5.196 in
  both senses against Kerr's b± = +4.10/−6.14 (χ = 0.5) … +2.11/−7.00 (χ = 0.998) → misclassifies
  retrograde capture at e.g. b = −6.10 → fails 2(d)/5; (c) a split returning |E_back| breaks the
  conservation sum by 5.3×10¹³× the 8-ulp bound and E_back < 0 → fails 4(c).

## Predictions

Written before the run (`predictions.md`, P1–P7). **All held**: anchors < 10⁻¹² predicted, measured
≤ 4×10⁻⁸ (my bisection tolerance, still 4 orders under every threshold); existence at all χ held with
the exact states exhibiting it; "no bound fully-future orbit, timelike or null" held; the P/u^t
equivalence held with zero exceptions; all three planted laws fail the intended criteria. The one
prediction I got wrong in the reading of the builder: I expected to find states where P and u^t disagree
*on allowed states* — they exist only in the forbidden region (the band (ℓ_P, ℓ_fut) between the turning
points is exactly where R < 0), which is why their scan's verdicts are all correct.

## What would make it wrong

My scan could miss a thin fully-future pocket between grid points: refuted three ways — the P and u^t
tests agree pocket-by-pocket, the equivalence has a closed-form proof (u^t = A(E−ωL)/(r²Δ), A, Δ > 0
outside the horizon; and allowed ∧ future ⟹ P > 0 since future needs λ/e > A/(2ar) while P < 0 needs
λ/e < (r²+a²)/a < A/(2ar)), and the integration shows the actual states doing what the scan says.
The integration is float64 with fixed steps (drift ≤ 2×10⁻⁴ worst case, at χ = 0.998 where the horizon
is 0.47 M from the start); the mpmath exhibits carry the precision argument.

## Cost of adoption, and fit with PRINCIPLES

Adoption cost: **one doc-line each** in `kerr.rs` (`forward()`: "future-directed iff P ≥ 0" → "iff
E−ωL ≥ 0; on allowed states this equals P ≥ 0, since u^t = A(E−ωL)/(r²Δ)") and in `rotating.rs`'s module
docs ("the solutions with E < 0 are all time-reversed" → "all *bound* E < 0 solutions are past-directed;
the tubes are future-directed and plunge"). No criterion, threshold, seed or planted law needs to change.
Fit: "Measure before claiming" and "a failed expectation is not automatically a failed method" — the
builder's expectation survived an adversarial oracle; "oracles are guards, not shepherds" — the row's
wording ("none is bound: they plunge") is exactly what the physics says, so the guard was already right.

## The lens (what red-team eyes may have missed)

I attacked the sign convention first and hardest (it is where the builder's phrasing is genuinely wrong);
the row's other five criteria I judged only through passability-in-principle and planted-law coverage,
not by running the judge's Rust code end to end — a checker with a Rust toolchain should still run
`cargo test -p xtask behave::kerr` on `wt/b19-kerr` and confirm `agreement()` prints ≤ 10⁻¹¹. The
"lopsided shadow" as a *view* effect and off-plane Lense–Thirring precession remain outside a 2D
equatorial law by construction (the plane is an invariant submanifold); I flag, but did not gate, that
criterion 5's deflection window (|b| from 1.05·|b_c| to 300) never probes the prograde–retrograde
asymmetry *between* the two critical parameters (b ∈ (b₊, |b₋|) = e.g. (2.11, 7.00) at χ = 0.998, where
every photon of either sense scatters but with sense-dependent deflection) — one extra seed family there
would close it.
