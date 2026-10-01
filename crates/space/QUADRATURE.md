# Darwin quadrature: bound and arithmetic scope

This proves the **quadrature truncation bound**, for the real integrands of the
compiled shape. It does not turn the rounded integer law into exact continuum GR.
The key, roots, panel cuts, node rounding and final output rounding are separate.
The v1 ellipse assertion is withdrawn: acosh(1+x) < sqrt(2x) for x>0, and a uniform
ellipse radius and integrand maximum were never established.

## A real-interval bound (no guessed ellipse)

On a panel [a,b] contained in [0,π], put h=b−a (the **full** width),
U=c+A cos ψ, D=2(m₃−A cos ψ), H=1−2U. Their strictly positive minima are
U₀=c+A cos b, D₀=2(m₃−A cos a), H₀=1−2(c+A cos a).
For scatter only D is used, so U=0 at infinity is harmless.

Let S=max_[a,b]|sin ψ| and C=max_[a,b]|cos ψ|. For j=1,…,8 put
v_j=A*(S if j odd else C)/j!. Then |U⁽ʲ⁾|/j!≤v_j and both
|D⁽ʲ⁾|/j!, |H⁽ʲ⁾|/j!≤2v_j.

For any positive V and exponent α>0, given V≥V₀>0 and
|V⁽ʲ⁾|/j!≤v_j, define

    F₀ = V₀^(−α)
    F_n = Σ[j=1..n] (n+(α−1)j) v_j F_(n−j) / (n V₀).

**Proof.** The normalized Taylor coefficients f_n of f=V^(−α) at any
point obey V f′+α V′f=0. Equating the coefficient of degree n−1 gives
n V f_n = −Σ (n+(α−1)j) V_j f_(n−j). Every multiplier is positive
for 1≤j≤n and α>0. Taking absolute values, the stated lower/upper bounds
and induction proves |f⁽ⁿ⁾|/n!≤F_n uniformly on the panel.

Use (V₀,v,α)=(D₀,2v,1/2), (U₀,v,2), (H₀,2v,1), obtaining G,Q,J.
Convolution bounds products by Leibniz's rule. Thus the three B₈ are

    φ: G₈
    τ: (G*Q)₈ / L
    t: E (G*Q*J)₈ / L.

The n-point Gauss–Legendre remainder on an interval of full width h is
h^(2n+1) (n!)^4 f^(2n)(ξ)/((2n+1)((2n)!)^3). This follows by integrating
the degree-2n Hermite interpolation remainder at the Gauss nodes; the squared
monic Legendre polynomial has integral (n!)^4/((2n+1)((2n)!)^2) on [0,1].
See [NIST DLMF §3.5(v)](https://dlmf.nist.gov/3.5#v).
For n=4 and |f⁽⁸⁾|≤8! B₈ this becomes

    |I_panel − GL4_panel| ≤ h^9 B₈ / 44100.

Sum the nonnegative bounds over panels and double for a full bound cycle.
No cancellation is assumed. It holds at A=0 (then B₈=0) and arbitrarily
near the admitted separatrix; the bound can grow as the denominators shrink.
It applies equally to partial panels in the readout solver. If any minimum
is nonpositive there is no bound from this formula; it must not return zero.

## Fixed-shape node and sum rounding

The following adds a conditional arithmetic bound to the real quadrature bound.
It holds before `convert`, for the normalized clock integrands g(ua/U)² and
g(ua/U)²/H. Write q=2^-62 and ε=(64A+1)q. Nodes deviate from the exact GL4
nodes by <2^-60 radians and each weight by <2·2^-61. The cosine polynomial's
error is <32q: its sine tail after degree 27 is <q/100; each nested rounding
adds <3q, propagated with factor ≤(π/2)²/6<0.412, and the final product and
rounded π add <3q. These bounds give |U_hat−U|≤ε and |D_hat−D|≤2ε.

Suppose D₀>2ε, U₀>ε, H₀>2ε. Put

    gmax = D₀^(-1/2)
    eg = ε/(D₀−2ε)^(3/2) + 2^-41
    qmax = ua/U₀
    eq = ua ε/(U₀(U₀−ε)) + q
    rτ = qmax²;  eτ = 2 qmax eq + eq² + q
    rt = rτ/H₀;  et = eτ/(H₀−2ε) + 2ε rτ/(H₀(H₀−2ε)) + q.

The mean-value theorem gives the first errors. `isqrt` and the preceding
reciprocal floor together add <2^-41 to g for these bound/scatter panels
(D≤1). Each fixed-point division or Q62 product adds <q at its output.
With h=b−a and werr=8·2^-61 the panel's absolute arithmetic errors are bounded by

    φ: h eg + werr (gmax+eg)
    clock: h(eg r + (gmax+eg) er) + werr(gmax+eg)(r+er) + 4·2^(s−103)(r+er).

Use (r,er)=(rτ,eτ) or (rt,et). The final term is essential: each of the four
clock nodes floors its weighted g to Q(103−s) **before** multiplying by the clock
ratio. It is an absolute error, not an error proportional to panel width.
The first test attempt omitted this term and failed; the diagnostic log is retained.
Final conversion, key quantization and rounded-root sensitivity remain separate.
Version 2 uses s=max(55,1+bit_length(g_max)), normally Q48, instead of v1's Q40.
This preserves weak clock responses without overflowing strongly conditioned sums.

`src/quadrature_tests.rs` evaluates this recurrence diagnostically in f64 on
the actual panels, checks GL4 against independently generated/refined GL8,
and checks integer quadrature separately against the conditional arithmetic bound.
It includes the behave sampler, circular, high-e, near-separatrix and scattering
panels, and a degree-eight witness that rejects an underestimated coefficient.
These numerical checks support the proof; their f64 evaluator is **not** an
outward-rounded runtime certificate and must never authorize a branch or kick.

## Why there are wider values

Tube is four u32 words, 16 bytes; velocity components are i32 Q30. Keys and
increments use pairs of u32. Epoch/phase arithmetic uses checked u64 addition;
cycle repetition uses checked u64 products. The cycle is shared, not per body.

The retained wider exceptions have explicit reasons:

The node kernel exposes proven u64/i64 operand ranges to the compiler: cosine's
Horner temporaries are <2.5·2^62, g and both clock ratios fit u64, and shifting
the weighted g by s leaves <2^62. Thus its products use 64-bit operands with
128-bit results. The optimized and original arithmetic produce identical full
Cycle records on the 256 behave keys (SHA-256 recorded with the benchmark).

- u is Q62 while the admitted separatrix gap is only 2^-42. Q30 would round
  that gap to zero. Squaring a Q62 root coordinate needs up to 124 product bits;
  the same precision is retained for trigonometry to avoid magnifying node errors.
- E is Q48 (E² Q96) because circular-orbit radial excess can be below 2^-40.
  L is Q32 with allowed value ≤4096: L² needs up to 89 bits. L·u needs up to
  107 bits on the general input envelope. Widening is local to the compiler.
- With D≥2^-42, g≤2^21; Q42 g therefore needs 64 unsigned bits. A weight in
  Q61 times g is up to 125 bits. Bound g_max with D_min minus 64 Q62 units
  (the cosine error cannot lower D by that much). Each clock ratio is <2^64,
  Σ weights <2^63, and s>bit_length(g_max), so clock half-sums are <2^126.
  The angle half-sum is <π·2^124. All fit signed i128.
- P's reciprocal mantissa may use 65 bits; output conversion multiplies it by
  clock sums. `mul_shr` constructs a 256-bit product from four 64×64 products
  and refuses an out-of-range result. This avoids overflowing an intermediate.
- A signed 64-bit secant times a signed 64-bit kick may need 126 bits; prediction
  widens that multiply, then checks the sum and output range.

These widths do not certify a universal continuum error. In particular, a
rounded residual is divided by |R′| near a simple root and has square-root
sensitivity near a double root. There is no valid uniform one-Q62-unit root
error or 2^-30 relative clock-error claim. The admitted output range also
requires each full-cycle increment to fit u64; otherwise compilation returns Range.

The API's central derivatives are finite differences in encoded E/L units.
Their steps, signs, component order, 16 guard bits and unit conversions are public.
Small probes amplify rounded-root noise: the retained p=1000 test showed ~2% error
in a small clock derivative with Q40 sums at ΔL=2^-10. The oracle test uses ΔE=2^-23 and ΔL=L/2048;
these are tested operating points, not universally certified probe sizes. A kick is
a multiply-add **prediction**; recompilation remains authoritative. Topology
changes, unbound probes and overflow return errors. A Hessian/remainder bound
for authoritative kick reuse is future work for the response compiler.
