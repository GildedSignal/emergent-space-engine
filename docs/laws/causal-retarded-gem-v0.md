# Tiny causal evolution law: retarded GEM patches

Law identifier: `es-causal-retarded-gem-v0`. Version 0. Isolated law-lab
specification. This is never `es-inertial-causal-v1`, never a production gravity
law, and must not be wired into the canonical engine. G2 stays FAIL.
`production_law` stays null.

This document is the executable-law contract for two or three moving sources.
Frozen falsifiers live in `scenarios/law-gates.json` under
`tiny_causal_law_research`. There is **no implemented map** in this revision:
fixtures are frozen before any new integrator. Combining the retarded monopole,
Euler coupling, absorbing capture, and Schwarzschild classifiers does not define
this law. This text is the spec patch of the [H0027](../HISTORY.md)
freeze after [H0029](../HISTORY.md) (journal as next ID after siblings, titled
below): (CONS)/(ABS) identity, capture history, (C-RET), pinned aberration event,
(EXT-EVOL), `short_binary_exchange` accounting, and uniform-segment (GEM-GRAD).
It is not a new law id and not a retune of `present_alignment_dot_min = 2047/2048`.

## Specification competition

Approved-plan G2 asks for a comparison of generator-friendly discrete variational
mechanics and piecewise-metric formulations. The 2026-09-12 review requires
actual equations or finite transition rules for moving sources, field/history,
initial/exterior data, characteristic cones, particle coupling, proper time, and
matter/field exchange. A formulation name is not a solution. Incomplete
specifications are rejected before code.

### Discrete-action candidate — rejected incomplete

Working title: `es-causal-fokker-avi-v0`.

Attempted content: a Fokker-type gravitational action on worldlines

`S_matter = -Σ_i μ_i c ∫ dτ_i`

`S_Fokker = (1/2) Σ_{i≠j} ∫∫ μ_i μ_j (u_i · u_j) δ((x_i-x_j)²) dτ_i dτ_j`

plus the hope that an asynchronous variational integrator (AVI) on those
worldline vertices would supply the update.

| Required item | Named? | Hole |
|---|---|---|
| 2–3 moving sources | Partial | Delay EL equations exist in the continuum Fokker analog, not as a finite laboratory map with a mesh, quantum, and simultaneous-commit rule. |
| Independent field/history | No | Direct interaction eliminates the field. There is no remainder state to evolve. |
| Initial/exterior data | No | Incoming/omitted mass has nowhere to live except as extra worldlines, which the tiny-N domain then has to list. |
| Characteristic cones | Partial | The δ((x-x')²) support is the Minkowski cone, but AVI local timesteps are defined for nearest-neighbor mechanical meshes, not this retarded coupling. |
| Particle coupling | Partial | Variation of `S_Fokker` is a coupling, but it is not the GEM force law that cancels gravitational aberration. |
| Proper time | Partial | `dτ` is in the action; the inertial-v1 `2^-32` floor and compact fail-closed rule are not. |
| Matter/field exchange | No | No field four-momentum. Inelastic capture is not a stationary point of this elastic action. |
| Signals | No | Photons are not worldlines in the attempted action. |
| Interventions | No | External Δp is not a variational vertex with a flux ledger. |
| Absorption | No | Merger would be bolted on, which is how the current coupled capture zeros momentum without transfer. |

Lew et al. on AVIs concern specified mechanical systems with a local discrete
Lagrangian. That literature does not certify this gravitational construction.
A 2D spacetime-mesh action is also rejected: planar ships still require a
3D-derived kernel, not logarithmic 2D gravity. A 3D lattice Einstein-Hilbert
action could in principle carry independent field degrees of freedom, but it is
not a tiny 2–3 source laboratory law (mesh, discrete d’Alembertian, boundary
remainder, and inelastic vertex are all unnamed). Therefore the discrete-action
direction is **rejected at specification**.

### Piecewise-metric candidate — accepted on the tiny domain

Working title, now the law id: `es-causal-retarded-gem-v0`.

Each committed piecewise-inertial source segment carries a constant-velocity
linearized metric patch (gravitoelectromagnetic / retarded Liénard-Wiechert
potentials of 3D linearized gravity, restricted to the laboratory plane). The
metric at an event is Minkowski plus the retarded sum of those patches, plus a
certified omitted-tail remainder that is part of the state. Particles follow
the GEM geodesic force of the excluded-self field. Compact membership reuses
`r_s = 2μ/c²`. Capture is absorbing **with** transfer of laboratory coordinate
momentum `p := μ v` into the survivor; the exchange ledger is audit-only.
Clocks, Minkowski signals, and accounted interventions are named transition
rules of the same state.

This is the piecewise-metric direction in the linearized moving-source regime,
not another stationary Schwarzschild/Kerr classifier, not delayed Newton, and
not 2D log gravity. Linearized superposition is the named two-source rule;
there is no exact interacting GR 2-body metric, and this spec does not pretend
to supply one.

## Domain, units, identities

- Spatial geometry: the laboratory plane `z = 0`. Every Green function and
  falloff is the planar trace of a **3D** kernel (`1/r`, never `log r`).
- `c = 64`, `G = 1`. Gravitational parameter `μ` is the source strength
  (`GM` in these units). Tick `Δt = 1/c`. Position projection quantum
  `q_x = 2^-20` (same dyadic as the coupled research stepper; **not** the
  frozen orbit ladder `2^-22..2^-24`).
- Bodies `N ∈ {1,2,3}`. `N = 1` is admitted only for static-kernel and
  inertial-clock controls. Dynamical claims require `N ∈ {2,3}`. `N ≥ 4`
  is `UnsupportedPredicate` and fails closed.
- Subluminal: `|v|² < c²`. Superluminal worldtubes are rejected.
- Weak-field exterior: `|Φ|/c²` bounded away from `1/2` except on the compact
  branch, which uses absorption rather than a geodesic integrator.
- Distinct from: `es-inertial-causal-v1`, `es-causal-retarded-monopole-v0`,
  `es-causal-retarded-coupled-v0`, `es-schwarzschild-equatorial-v0`,
  `stationary-verlet-q-v1`, `stationary-shell-lapse-q-v1`.

## Complete state `S`

`S` at an admitted cut (integer tick) is:

1. **Matter.** For each body `i`: identity, piecewise-inertial worldtube
   (committed segments `(t0, t1, x, v, p, μ)`), capture flag, proper time
   `τ_i`. Laboratory coordinate momentum is `p := μ v` (not Minkowski
   four-momentum). Segment `μ > 0` sources; there is no `is_planet` flag.
   Captured bodies stay listed: future segments are halted with `μ = 0` and
   `p = 0`. Committed **past** segments keep their sourcing `μ` (only future
   sourcing dies).
2. **Field/history.** The committed worldtubes are the retarded source
   history. The metric at an event is defined by (METRIC) from that history.
   Same-tick updates are invisible (excluded-self; simultaneous commit).
3. **Exterior remainder.** `OmittedTail { R, μ_bound, enclosure, P_remainder }`
   is part of `S`, not a query-only annotation. `P_remainder` is a coordinate-
   momentum interval. Incomplete omit without a remainder fails closed.
4. **Exchange ledger.** Compact remnants `(Δμ, Δp, survivor, tick)` are
   **audit-only**. Accounted intervention flux `(tick, identity, Δp)` is the
   only ledger charge in (CONS).
5. **Clocks.** `τ_i` as accumulated by (CLK).
6. **Signals.** In-flight and received addressed messages with emission events
   `(t_e, x_e)` and inertial-v1 Minkowski reception.
7. **Interventions.** Scheduled external burns, applied on pre-batch state at
   their tick.

Authored future worldtubes are not state. Observation is not state mutation.

## Named equations and transition rules

### Cones and retarded events

**(C-CONE)** Event `e = (t, x)` lies in the closed past cone of source event
`s = (t_s, x_s)` iff `t ≥ t_s` and `c²(t - t_s)² ≥ |x - x_s|²`. On-cone
equality is visible. A query in a source’s future refuses.

**(C-RET)** The retarded event of source `i` at query `e = (t, x)` is the
intersection of the past light cone of `e` with the inertial worldline of the
latest committed segment of `i` that meets that closed cone.

- Solve `c²(t - t_ret)² = |x - x_seg(t_ret)|²` with `t_ret ∈ [t0, t1]` and
  `t_ret ≤ t` on that segment. On a subluminal inertial piece the intersection
  is unique when it exists.
- It is **not** the latest worldtube vertex (kink) that still lies in the
  causal past. A hopping-endpoint rule is not this law. A kink is the retarded
  event only when it *is* the cone∩worldline point.
- If no segment meets the cone, that source does not source `e`.
- (C-CONE) is one rational comparison. Ambiguous `f64` escalates to an exact
  dyadic or fails closed. An iteration cap is `BranchBudgetExhausted`, not a
  guessed retarded time.

**(C-SEG)** A velocity kink is a segment boundary. The latest visible segment
is the one (C-RET) selects. Same-tick bodies cannot see each other’s newly
committed segment. Radiative `1/r` impulses on a kink’s future cone are
**omitted** (see GEM-GRAD): the field of a segment is its uniform-velocity
near field only.

### Linearized metric patches (3D-derived GEM)

Let `r_ret = |x - x_ret|`, `n̂ = (x - x_ret)/r_ret`, `β = v_ret / c`, and
`γ = 1 / sqrt(1 - β·β)`, all at the retarded event of source `i`.

**(GEM-Φ)** / machine id `GEM-PHI`: `Φ_i(e) = -μ_i / [r_ret (1 - n̂ · β)]`.

**(GEM-ξ)** / machine id `GEM-XI`: `ξ_i(e) = Φ_i(e) β`  (equivalently `-μ_i β / [r_ret (1 - n̂ · β)]`).

**(METRIC)** `g(e) = η + Σ_{i visible} h^{(i)}(e) + h_remainder(e)`, where
`h_00 = -2 Φ / 1` in units that reproduce `g_00 = -c²(1 + 2Φ/c²)`,
`g_0k = -4 ξ_k / c`, `g_{jk} = (1 - 2Φ/c²) δ_{jk}`, and `Φ = Σ_i Φ_i`,
`ξ = Σ_i ξ_i`. The remainder contribution is an enclosure, not a silent zero.

**(GEM-E)** `E = -∇Φ - (4/c) ∂ξ/∂t`.

**(GEM-B)** `B = (4/c) ∇ × ξ`.

**(GEM-GRAD)** On a uniform (constant-`β`) segment, with retarded quantities
`r = r_ret`, `κ = 1 - n̂ · β`, `D = r κ`, and `Φ = -μ / D`, the laboratory
derivatives are

`∇Φ = (μ / D²) [ -β + n̂ (1 - β²) / κ ]`

`∂Φ/∂t = (μ c / (D² κ)) (β² - n̂ · β)`

`∂ξ/∂t = β ∂Φ/∂t`

`∇ × ξ = (μ / D²) ((1 - β²) / κ) (n̂ × β)`

because `ξ = Φ β` and `β` is constant on the open set whose (C-RET) event
lies on this segment. (GEM-E) and (GEM-B) then give `E` and `B`. Static
`β = 0` recovers `∇Φ = μ n̂ / r²` and `ξ = 0`. Acceleration-dependent
Liénard–Wiechert `1/r` radiation is identically zero on a uniform segment.
**Radiation at kinks is omitted:** a velocity discontinuity does not inject
a named impulse into `E` or `B`. When (C-RET) switches segment, the field
jumps from one uniform-segment near field to the next; that jump is admitted
and is not a radiative sheet. Coincidence `r = 0` remains `Singular`.

**(GEM-a)** For body `i`, `a_i = E_{≠i} + v_i × B_{≠i}`, using the excluded-self
field of committed history. This is the linearized geodesic force. Instantaneous
equal-and-opposite particle forces are **not** a rule of this law.

**(GEM-STATIC)** If every visible source has `β = 0`, then `ξ = 0` and
`a = -∇Φ` with `Φ = -Σ μ / r`, the existing 3D-planar monopole. A candidate
that disagrees on the frozen rest fixture has the wrong static kernel.

**(GEM-ABERR)** Retarding a Newtonian source position and evaluating
`a = -μ n̂_ret / r_ret²` without (GEM-ξ), (GEM-E), (GEM-B), and (GEM-GRAD) is
**not** this law. Those velocity-dependent terms cancel leading gravitational
aberration (Carlip, gr-qc/9909087). Delayed Newton is a named negative
control. The frozen cosine is scored at the post-cone event
`(t, x) = (1/8, (0, 4))` against **present coasting Newton** (the Newtonian
acceleration using the source’s present position at that same `t`, not a
retarded Newtonian position). The monopole negative control uses **that
same event**. `present_alignment_dot_min = 2047/2048` on `β = 1/16` is
frozen and is not retuned.

### Clocks

**(CLK)** On a committed inertial segment, the canonical rate is

`rate = floor(2^32 * sqrt(max(0, 1 + 2Φ/c² - |v|²/c²))) / 2^32`

with `Φ` the excluded-self potential at the segment’s starting event.
Elapsed proper time on the segment is exactly `(t1 - t0) * rate`. Subdivision
does not insert another rounding. If `1 + 2Φ/c² - |v|²/c² < 0`, the clock
fails closed (compact/spacelike), it does not floor to zero as a gravity
result. When `Φ = 0`, (CLK) is identical to inertial-v1. Preserve
inertial-v1 as the `Φ = 0` control; this law does not change that quantum.

### Signals

**(SIG)** Addressed signals propagate on Minkowski cones with the inertial-v1
reception predicate `|Δx|² ≤ c² Δt²`, `Δt ≥ 0`. Reception is certified per
receiver; a broadcast is not simultaneous receipt. Shapiro delay and metric
null geodesics are out of domain (`UnsupportedPredicate`). A received payload
that is a burn becomes an intervention at the **next** tick (no zero-time
signal cascade). Reception does not source gravity.

### Interventions

**(INT)** An external burn at tick `k` adds `Δp` to the target’s pre-batch
coordinate momentum `p := μ v` and appends `(k, id, Δp)` to the intervention
ledger (the CONS charge). The body’s μ is unchanged unless the command says
otherwise. The gravitational field of the new momentum is the field of the
new committed segment: invisible inside the burn’s future cone, visible on
and after it. Unaccounted burns fail the exchange falsifier.

### Absorption and exchange

**(ABS-CLASS)** Compact radius `r_s = 2μ/c²`. Membership compares `r² c⁴`
with `4μ²`: Interior / OnHorizon / Exterior. Tie: OnHorizon. Coincidence
`r = 0` is `Singular` (refuse, never NaN).

**(ABS)** If body `i` is OnHorizon or Interior of a retarded-visible source
`j` with present (post-capture-cut) `μ_j > 0`, capture is a finite transition
at that tick. Coordinate momentum `p := μ v` is transferred, then the captured
body is zeroed in the listed sum:

- `μ_j ← μ_j + μ_i` on **future** segments of the survivor
- `p_j ← p_j + p_i`
- `p_i ← 0` on the captured body (it stays in `Σ_i` with this zero)
- future segments of `i`: `μ ← 0`, worldtube halted, `τ_i` frozen
- committed **past** segments of `i` **keep** their sourcing `μ`; only
  future sourcing dies
- ledger `+= (tick, captured=i, survivor=j, Δμ=μ_i, Δp=p_i)` as an
  **audit** record, not a second charge in (CONS)

Mutual interior or mutual OnHorizon: the survivor is the earlier body in
`S`’s matter/worldtube order; the other is captured. If `i` is interior to
several sources, capture into the earliest such source in that order.
Pre-batch `p` is used. Do not apply `p_i ← 0`, exclusion from `Σ_i`, and a
ledger charge together.

This is **not** Schwarzschild merger and **not** the H0019 halt that zeros
`p_i` without transfer. Newton `1/r²` is not evaluated on or inside `r_s`.

**(CONS)** One conserved accounting sum on listed coordinate momenta
`p := μ v`:

`Q = Σ_i p_i − Σ_ledger Δp_intervention`

The sum runs over every listed body, including captured bodies after
`p_i ← 0`. The compact ledger is audit-only and **does not** appear in `Q`.
Isolated capture leaves `Q` unchanged: transfer into the survivor cancels
zeroing of the captured `p`. Isolated accounted burns leave `Q` unchanged:
`Δp` is added to both the body and the intervention ledger.

`P_remainder` is a coordinate-momentum **interval** for omitted mass.
CONS is interval **membership**, not equality of endpoints and not a
requirement that the interval be a singleton:

`Π ∈ Q + P_remainder`

with `Π` the conserved total implied by genesis plus accounted flux. If
nothing is omitted, `P_remainder = {0}` and CONS is exact equality on `Q`.
A linearized-GEM field Poynting/stress remainder is **omitted** from `Q`
(named: this is a tiny-N particle-plus-exterior-enclosure identity, not
Einstein-equation conservation). Unexplained loss fails the exchange
falsifier. Instantaneous Newtonian third-law `Σp` balance is **not** this
identity; `short_binary_exchange` is pre-cone zero / post-cone nonzero plus
this accounting, not a 3rd-law test.

### Exterior through evolution

**(EXT-INIT)** A finite authoritative root is well-posed only when completeness
is declared and unlisted mass is listed, enclosed, or refused. The frozen unit
source at `r = 16` cannot be a silent zero at `r = 1`.

**(EXT-EVOL)** The remainder is part of `S`. After any positive-duration
advance, exactly one of:

1. **Keep enclosure.** Update `OmittedTail { R, μ_bound, P_remainder }` so
   the new interval still contains the omitted mass’s possible contribution
   at the new cut (sound enclosure; it may grow). CONS is rechecked as
   membership in this updated interval.
2. **Promote.** Copy omitted mass into listed worldtubes and set
   `P_remainder = {0}` **before** the omitted cone can affect (GEM-a),
   (ABS), (CLK), or any other canonical decision.

A query-time enclosure that vanishes from future `S` without promotion
fails. Promoting after that cone has already been used in a decision fails.
A small listed coherent perturbation that will matter after its cone must
remain in `S` until then.

**(EXT-OBS)** `inspect` / `position` / sensor queries do not mutate `S` or the
history digest. Observation does not create gravity.

### Finite map

**(MAP)** Admitted cuts are integer ticks. One tick:

1. Apply (INT) burns scheduled at `k` on immutable pre-batch `S`.
2. Deliver (SIG) receptions whose reception tick is `k`; burns in payloads
   become interventions at `k+1`.
3. Classify each body by (ABS-CLASS) against retarded-visible sources.
   Mutual interior uses worldtube order (ABS). Captured bodies follow (ABS)
   (`p_i ← 0`; past `μ` kept). Others evaluate (GEM-a) on committed history,
   then symplectic-Euler on coordinate `p := μ v`: `p ← p + μ a Δt`,
   `v = p/μ` for present `μ > 0`, `x ← x + v Δt`, project `x` onto
   `q_x = 2^-20`. Halted captured bodies do not Euler.
4. Accumulate (CLK).
5. Commit every next segment simultaneously (C-SEG). Past captured segments
   remain in history with their original `μ`.
6. Update the remainder by (EXT-EVOL): keep enclosure or promote before the
   omitted cone can affect a decision.
7. Return the full post-state and the earliest pending event in the remaining
   horizon (contact, capture, signal, remainder-influence, intervention).

**(PROP)** `Φ(t_out, t_in, S)` returns position, momentum, phase (segment
parameter), proper time, interval enclosure, exchange ledger, remainder, and
earliest event. Fate-only classifiers are not this map. Unsupported domains
and exhausted budgets are distinct from admitted answers.

**(COMPOSE)** At admitted cuts,
`Φ(t2, t0, S) = Φ(t2, t1, Φ(t1, t0, S))`.
Computational splitting must not insert another rounding or change the
physical mesh. Direct versus subdivided evaluation is a frozen falsifier.

## What existing kernels are, relative to this law

| Kernel | Relation |
|---|---|
| Retarded monopole v0 | Static-kernel and cone control. Authored worldtubes. No (GEM-ξ), no clocks, no exchange. Negative control for (GEM-ABERR). |
| Coupled Euler v0 | Same-tick excluded-self and two-way retarded **trajectory** shape. Delayed Newton, not GEM. Capture zeros momentum: negative control for (ABS). Does not integrate the remainder. |
| Compact / exact-branch | (ABS-CLASS), (C-CONE), fail-closed budgets reused. Production `terminating_exact_branches` still fails because GEM field *values* remain `f64` until enclosed. |
| Schwarzschild equatorial v0 | Stationary one-source **classifier**. No time propagation of `(x, p, τ)`. Negative control for (PROP). Moving/two-source queries already fail closed there; this law is the moving-source contract those classifiers refused. |

## Frozen falsifiers

Fixtures are in `tiny_causal_law_research` and were written **before** a GEM
map. Do not retune numeric bounds after seeing a candidate. Do not implement
authored futures to pass `three_source_admitted_ivp`.

| Probe (review) | Frozen fixture ids | Reject or stop if |
|---|---|---|
| Complete dynamic transition | `three_source_admitted_ivp` | Futures are authored, source equations missing, or clocks/absorption use unrelated rules. |
| Causal moving-source exchange | `translating_source_aberration`, `short_binary_exchange`, `accounted_burn_precone`, `capture_transfers_momentum` | Pre-cone response, unexplained exchange loss, wrong static kernel, excessive aberration (delayed Newton), or treating `short_binary_exchange` as Newtonian 3rd-law `Σp`. |
| Exterior through evolution | `exterior_remainder_survives_step`, `coherent_perturbation_eventually_matters` | Remainder disappears after a step without promotion, promotion after the omitted cone affected a decision, or observation sources gravity. |
| Useful finite branches | `grazing_cone_tie_visible`, `unsupported_four_source_refuses`, `budget_exhausted_not_a_sign` | Iteration caps choose a sign, or refusal covers advertised support. |
| Actual propagation and reuse | `propagation_returns_state`, `composition_direct_vs_subdivided` | Only fate is returned, or subdivision changes canonical `S`. |
| Clocks / signals / observation | `clock_inertial_limit`, `signal_on_minkowski_cone`, `observation_does_not_source` | Gravitational clocks silently replace inertial-v1 at `Φ=0`; metric-null signals are guessed; queries mutate `S`. |
| Named negative controls | `retarded_newton_fails_aberration`, `coupled_euler_zeros_capture_momentum`, `schwarzschild_classifier_not_propagation`, `static_kernel_matches_monopole` | A “pass” obtained by relabeling H0011/H0019/H0024. |

Aberration bound, frozen as a cosine of acceleration directions against
**present coasting Newton** at the post-cone event `(t, x) = (1/8, (0, 4))`
on the translating fixture (`β = 1/16`):
`present_alignment_dot_min = 2047/2048`. The monopole negative control
`retarded_newton_fails_aberration` uses **that same event**. Delayed Newton
is expected to fail that bound; GEM is expected to pass it. Do not retune
the cosine. `static_kernel_relative_error_max` matches the existing
backreaction relative scale `1e-12` and is not an orbit threshold.

`short_binary_exchange` is a two-sided causal probe plus (CONS) membership
after an accounted velocity-exchange rearrangement: pre-cone influence is
zero, post-cone influence is strictly nonzero. It is **not** a simultaneous
`Σp` third-law test.

## Arithmetic

Law-lab rationals are `Ratio<i128>`. Every supported predicate must bound
every intermediate or fail closed (`ExactConversionOverflow`). Exact rational
cone/compact identities on tiny fixtures do not prove an unrestricted
arithmetic domain. GEM field *values* in this laboratory may be `f64`; that
keeps the production `terminating_exact_branches` gate failed until those
values have enclosures.

## What must exist before any new map code

1. This specification, with the named equations above (done).
2. Frozen falsifiers in `scenarios/law-gates.json` without edits to old
   numeric thresholds (done).
3. A spec-module check that those fixture identities cannot be renamed,
   dropped, or reordered silently (done).
4. Independent review of (CONS) and the aberration cosine bound ([H0029](../HISTORY.md)).
   A floating candidate is never sufficient evidence of a canonical branch.
5. Spec patch of the holes that review named (this document). Keep
   `present_alignment_dot_min = 2047/2048`. Do not implement (MAP) in the
   same change as the patch.
6. Then, and only then, a law-lab implementation of (MAP) that is scored
   against the frozen fixtures without retuning. No engine wiring. No G2
   promotion path that is delayed-Newton. No 2D log kernel.

Until (MAP) exists, every dynamical fixture is an expected FAIL with reason
`map not implemented; fixtures frozen`. That failure is the freeze, not a
license to stub authored trajectories.

## Non-claims

Not G2. Not production. Not Kerr. Not interacting Einstein gravity. Not FMM.
Not delayed-Newton-as-G2. Not an orbit-tuned Kepler map. Not a replacement
for inertial-v1. Field values remain `f64`. Compact certification stays
failed (absorption is not Schwarzschild). `terminating_exact_branches` stays
failed. Billion-ship / ten-billion-year gravitational qualification remains
unqualified.
