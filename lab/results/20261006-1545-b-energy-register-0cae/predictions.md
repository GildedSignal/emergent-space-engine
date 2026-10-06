# Predictions (written before the decisive run)

The change: the register holds the geodesic's own energy (`E−1` from the tube's key, `ext::tube_invariants`),
the drift's `y = H_D + p_t + c` reads the same constant, and the kick acts on the **canonical** momentum
(`force::canonical_kick`) so that `ΔL_GR = x×Δp` exactly pairs with `Δp_t = w·∂_tU_P`. The register's word
renormalises instead of refusing (thrust toward c). Held-out cases (not tuned on):

1. **P3' per kick:** `|ΔJ| ≤ 2` quanta of `2^pt_exp` for every kick of 12 ships over 20 planet periods
   (1.5–3.5 Hill radii, the B12 scene's distribution). Expected max ~1 quantum (sigma-delta rounding and the
   velocity-word quantisation, `Ω·x×ε_v` at ~1/64 of a quantum).
2. **P3' along a drift:** `|J(t) − J(t_kick)| ≤ 1` quantum sampled mid-step on the binding's own readout.
   Expected ≤ 0.05 (second order in the rebinding remainder).
3. **P3' trend:** `|J_last − J_first| ≤ 8` quanta per ship. Expected ~1 (a bounded carry random walk).
4. **Control (can fail):** the same kick applied to the coordinate velocity — the law as it was — moves J by
   `≥ 10³` quanta at the strongest kick. Expected 10⁴–10⁵ (the tide kick per kick is ~10⁻⁹ of velocity;
   `ΔJ ≈ (E/lapse − 1)·Ω·(x×Δv) + Ω·L·Δ(E/lapse)` scales with it).
5. **The invariants' self-check:** `tube_invariants(key)` equals the geodesic invariants of the tube's own
   decoded state (`force::geodesic_of`) to better than the key's quantisation: `|(E−1)_key − (E−1)_state| ≤ 10⁻¹³`
   and `|L_key − L_state|/L ≤ 10⁻¹⁰` over the bindings the run visits. (The circular control `L² = r²/(r−3)`,
   `E = (r−2)/√(r(r−3))` is verified symbolically in the doc comment; this is the numeric one.)
6. **Gates after:** B13 stays 60/64 with marginal failures of the same class (the register does not change the
   flyby mechanics; the canonical kick's `Δv` differs from the old one by `O(v²·Δv) ≈ 10⁻¹²`); B17 at
   `--plane-step 6` unchanged; G1–G6 unchanged (no kicks on the single-mass core); the universe suite green
   (the two known-ignored tests stay ignored, not run).
7. **The thrust regression (6 October, β ≈ 0.05 / 0.125):** `a_lost_ship_says_why_and_keeps_its_readings`
   passes again — the ship is lost only past γ ≈ 2000 with a `Range` fault from the orbit compile, its
   readings frozen (the pre-v2 behaviour), and no refusal before β 0.999.

If (1) fails at 10–100 quanta on strong kicks, the canonical map's arithmetic (not the law) is the suspect:
the Scalar round-trip `v→p→v′` rounds at the velocity word's own quantum. If it fails at 10³+, the kick is
not Noether-paired and the representation is wrong.
