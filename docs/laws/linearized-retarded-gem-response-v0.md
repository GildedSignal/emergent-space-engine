# Linearized retarded GEM source response (v0)

Law identifier: `es-linearized-retarded-gem-response-v0`. Version 0.
Isolated law-lab experiment. **Not** `production_law`. **Not** `Engine::advance`.
Default engine law remains `es-inertial-causal-v1`.

This is a coherent weak-field slice of the named GEM-v0 formulas
(`docs/laws/causal-retarded-gem-v0.md`) with **executable moving-source
arithmetic**. Finite semantics are f64 with declared bands. That is a new
law version: cache, partition, and refinement must not change physical
outcomes inside those bands.

H0097: a missing terminating jet in `Ratio<i128>` is not a proof that
moving-source formulas cannot exist. This slice does not extend truncated-GEM
genesis specials.

## Supported regime

| Quantity | Admitted | Outside → `UnsupportedDomain` |
|---|---|---|
| Field strength | `max ‖Φ‖ / c² < 0.05` | compact / strong-field cards |
| Speed | `max ‖β‖ < 0.25` | relativistic compact remnants |
| Geometry | planar motion, 3D-derived `1/r` kernel | 2D log gravity |
| Sources | N = 2…8 massive participants plus test ships/rays/clocks | galaxies as solved dynamics |
| Incoming field | Minkowski, `h_free = 0` | cosmological / GW backgrounds |
| Radiation at kinks | omitted (GEM-GRAD) | GR quadrupole radiation |
| Exterior remainder | laboratory lists every mass; remainder = 0 | certified omitted tails |

Route, not a claim of solution: the same retarded GEM kernel is the weak-field
limit of a later compact-object match (Schwarzschild static anchors already
exist as a separate kernel) and of a later collective multipole/family residual
(relational summaries preserved as aggregation, not as a second force law).
Those domains stay **unsupported** on this id.

## Units, order, balance

- `G = 1`, laboratory `c = 8`. Masses `μ` are gravitational parameters `GM`.
- Approximation: linearized gravity `O(G¹, β¹)` on piecewise-inertial worldtubes.
  Acceleration-dependent Liénard–Wiechert `1/r` radiation is identically zero
  on a uniform segment and is **omitted at kinks**.
- Source/field balance: committed worldtubes source `Φ, ξ`; excluded-self
  `E, B` accelerate those worldtubes `(GEM-a)`. No instantaneous 3rd-law
  particle forces.
- Self-influence: omitted (`≠ i`). Coincidence `r = 0` is `Singular`.
- Initial/incoming: each body has a genesis inertial segment starting at
  `t = 0`. Queries before a source exists receive no contribution from it.
  No stuffed rest field at spacelike genesis (unlike truncated-GEM compile).

## Named equations (executable)

**(C-CONE)** `t ≥ t_s` and `c²(t − t_s)² ≥ |x − x_s|²`. On-cone is visible.

**(C-RET)** Past-cone ∩ inertial segment. Quadratic lookback `u = t − t_ret`:

`( |v|² − c² ) u² + 2 (R · v) u + |R|² = 0`,
`R = x_query − (x0 + v (t − t0))`.

Retarded root `u ≥ 0` with `t_ret` in the segment. Same-tick newly committed
segments are invisible. Hopping the latest kink is **not** this law.

**(GEM-Φ)** `Φ_i = −μ_i / [r (1 − n̂ · β)]`.
**(GEM-ξ)** `ξ_i = Φ_i β`.
**(METRIC)** `g_00 = −c²(1 + 2Φ/c²)`, `g_0k = −4 ξ_k / c`, `g_jk = (1 − 2Φ/c²) δ_jk`.
**(GEM-GRAD)** on a uniform segment, spec derivatives; static `β = 0` recovers `∇Φ = μ n̂ / r²`.
**(GEM-E)** `E = −∇Φ − (4/c) ∂ξ/∂t`.
**(GEM-B)** `B = (4/c) ∇ × ξ` (planar `z` component).
**(GEM-a)** `a_i = E_{≠i} + v_i × B_{≠i}`.
**(CLK)** `dτ/dt = sqrt(max(0, 1 + 2Φ/c² − |v|²/c²))` from the same `Φ`.
**(NULL)** Euclidean-path first-order: `dt = (1 − 2Φ/c²) dl / c`,
`dn̂/dl = (4/c²) E_⊥` (Einstein factor from `g_00` and `g_ij`).

Delayed Newton `a = −μ n̂_ret / r_ret²` is a **named negative**, not this law.

## Finite branch / tie semantics

| Situation | Decision |
|---|---|
| On-cone equality | visible (closed cone) |
| Ambiguous retarded root | take the minus-branch quadratic root; refuse if `u < 0` or off-segment |
| `1 + 2Φ/c² − v²/c² < 0` | clock fails closed (compact/spacelike), not a gravity answer of 0 |
| Superluminal `‖v‖ ≥ c` | refuse worldtube |
| Required moving-source / ray / clock / contact in the admitted laboratory | must return a value; `UnsupportedPredicate` is a **capability fail** |
| Outside admitted regime | `UnsupportedDomain`, not a silent empty sky |

Compiler splits, caches, and certificates are not allowed to change committed
events inside the numerical band below. A new finite rule is a new law id.

## Error budgets (declared before candidates)

Distinguish three residuals:

1. **Model error** vs GR: unconfirmed. Do not score this slice as Einstein two-body.
2. **Numerical error** vs a slower same-law reference: source position at the
   laboratory horizon `H = 6` must stay within `0.05 D` when `dt_ref = dt/4`.
3. **Canonical / compiler**: identical IC + interventions + `dt`, direct vs
   subdivided at an interior event, observables within `1e-8` relative or
   `1e-10` absolute, whichever is larger.

Causal bands (laboratory fixture below):

- Pre-cone: `|a_B(kick) − a_B(control)| / a_scale < 1e-8` for all samples
  with `t < t_kick + |x_B − x_A_kick|/c − dt`.
- Post-cone: the same ratio exceeds `1e-3` by `t_kick + |Δx|/c + 2 dt`.
- A→B→A: after a further light-crossing, `|a_A(kick) − a_A(control)|`
  excluding A's own impulsive `Δv` exceeds `1e-3 a_scale`.

Independent (not parity) checks: finite-difference `∇Φ` vs GEM-GRAD; static
kernel; delayed-Newton post-cone event disagrees with GEM; authored worldtubes
fail the GEM-a residual certificate.

## Comparison contract

| Change | Must agree |
|---|---|
| Compiler / cache / split / query count only | Canonical observables of this law |
| `dt` refinement | Numerical band (2) |
| Different law id | Short-time causal structure and magnitude anchors only |

The slow reference is constructed only from genesis + the intervention list.
It never starts from a compiled candidate state.

## Concrete moving-source example (complete loop)

Two equal masses, laboratory `c = 8`, `G = 1`, `μ_A = μ_B = 1`.

Genesis `t = 0`: A at `(−4, 0)`, B at `(4, 0)`, both at rest. Separation
`D = 8`. They are spacelike: `c² Δt² = 0 < D²`, so **neither sources the
other** at genesis. This is required, not a bug. Truncated-GEM stuffed a rest
`Φ` here; this law does not.

Light-crossing `τ = D/c = 1`. At `t = 1` the genesis events lie on each
other's cones:

- Query at A: `(t, x) = (1, (−4, 0))`. B's genesis `(0, (4, 0))` satisfies
  `c² Δt² = 64 = |Δx|²` (On).
- `β_B = 0`, `r = 8`, `n̂ = (−1, 0)` from B to A.
- `∇Φ = μ n̂ / r² = (−1/64, 0)`, `E = −∇Φ = (1/64, 0)`.
- `a_A = (1/64, 0)` toward B. By symmetry `a_B = (−1/64, 0)`.

Control: no intervention. Both fall inward after `t = 1`.

Kick: accounted `Δv_A = (0, 1/8)` at `t_kick = 1.25` (after motion has
begun). The kick event is a new inertial segment. B remains on A's
pre-kick segment until the cone of the kick arrives:

`t_see_B ≥ 1.25 + |x_B(t_ret) − x_A_kick| / c ≈ 2.25`.

Until then `a_B(kick) = a_B(control)` at the causal band. After that, B's
GEM-E uses A's moving post-kick `β` and displaced retarded position, so
`a_B` changes. B's subsequent worldtube therefore differs. That difference
reaches A after a further crossing `t_see_A ≳ 3.25`, changing `a_A` beyond
A's own impulse. That is physical A→B→A, not a visibility flag.

Held-out consumers, from the **same** evolved sources:

- Ship emitted at `t = 1.1` from `(0, 3)` with velocity `(1/8, 0)`.
- Ray emitted at `t = 1.1` from `(0, 3)` toward `+x` (after source motion
  began). Kick at `1.25` occurs **while the ray is in flight** (`L/c ≈ 1`).
- Clock rides the ship; `Φ` is excluded-self at the ship's events.

Direct vs subdivided: split source compilation at `t = 1.25`; ray arrival
and ship state must match the unsplitted run.

Compact family: four additional masses `μ = 1/8` near `(0, −3)` evolved as
full participants. A far query must change when one member is extracted.
Quiet: the two-body laboratory with no third body. Encounter: a mass `μ = 2`
on a flyby through the mid-plane.

Linear interval closure (H0098 operators, specialized to this example):

After the kick, treat deviations from the control worldtubes as delayed
gains. For lookback `τ ≈ 1` and nearly-constant slow-motion coupling
`r = αβ` of the pair,

`δx_A(t) = u H(t − t_kick) + α δx_B(t − τ)`,
`δx_B(t) = β δx_A(t − τ)`,

which sums to the geometric series `u (1 − r^{n+1}) / (1 − r)` with
`n = floor((t − t_kick) / (2τ))`. That **shortcut** is a certificate
candidate over a quiet interval. It is rejected when a persistent
perturbation or encounter makes the residual of `X = Φ(X)` miss the
contraction band; then the interval is refined (paid recompute). It is
not a hardcoded `f`.

## What this does not do

- Select `production_law` or replace inertial `Engine::advance`.
- Solve galaxies, black-hole interiors, or Einstein two-body radiation reaction.
- Treat H0079/H0090 constructed `f = 1` as validated savings.
- Call later-tick GEM formulas impossible because `Ratio<i128>` could not
  represent them.
