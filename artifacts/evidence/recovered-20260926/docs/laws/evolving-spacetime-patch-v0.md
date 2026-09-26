# Evolving spacetime patch v0

Law identifier: `es-evolving-spacetime-patch-v0`. Version 0. Isolated law-lab
specification. This is never `es-inertial-causal-v1`, never
`es-causal-retarded-gem-v0`, never a production gravity law, and must not be
wired into the canonical engine. G2 stays FAIL. `production_law` stays null.

This document freezes one small **evolving spacetime patch**: two massive
bodies, one test ship, one light ray, one clock. Gravity is encoded in the
**metric / geometry of the patch**. Sources compile that shared geometry;
worldlines traverse it; they backreact; the compiler reuses the patch while
certificates hold. Isolated per-ship forces, Minkowski signals bolted onto a
gravitational clock, and delayed Newton will not close the loop.

This text is the spec patch of the [H0033](../HISTORY.md) freeze after
[H0034](../HISTORY.md) independent review of CONSIS / GEO-N / CACHE:
(GEO-T)/(GEO-N)/(CLK-G) bind to **one object in `P`**, coordinate/affine
arrival is named **before** tick binning, and a certificate is source digest
+ remainder + **future cone of the change** (per-event). It is not a new
law id, not a retune, and not a Shapiro-magnitude freeze. A law-lab
`advance_patch` now exists against these frozen fixtures. GEM (MAP) is not
this object.

Frozen falsifiers live in `scenarios/law-gates.json` under
`evolving_spacetime_patch_research`. Combining the retarded monopole, Euler
coupling, absorbing capture, Schwarzschild classifiers, and the GEM spec
does not define this patch. GEM (MAP) is **not** this object. The laboratory
map fills `g` from GEM (METRIC)/(GEM-a)/(CLK) and implements metric nulls;
it does not implement GEM `advance_map`.

## Governing loop

A controlled source change must change **motion, light arrival, and elapsed
proper time consistently** from that same compiled geometry. Then **direct
versus subdivided evaluation** and **cache reuse** must match. A candidate
that updates only one observable, or that evaluates ship / ray / clock from
three unrelated formulas, fails `CONSIS` even if each formula looks locally
sensible.

Planar laboratory geometry is the trace of a **3D-derived** kernel (`1/r`,
never `log r`). Delayed-Newton-as-G2 is a named negative control. G2 stays
FAIL.

## Domain, units, identities

- Spatial geometry: laboratory plane `z = 0`. Green functions and falloff are
  the planar restriction of a 3D kernel.
- `c = 64`, `G = 1`. Tick `Δt = 1/c`. Position projection quantum
  `q_x = 2^-20` (same dyadic as the coupled research stepper; **not** the
  frozen orbit ladder).
- Cast (exact): two massive sources `N_mass = 2`, one test body `μ = 0`, one
  null geodesic, one clock along a named worldline. A third massive source is
  `UnsupportedPredicate` and fails closed. `N_mass = 1` is refused for this
  law id (that is the Schwarzschild equatorial patch, a different contract).
- Subluminal massive and test worldtubes: `|v|² < c²`. Superluminal tubes
  refuse.
- Weak-field exterior of the compiled patch, except on the compact branch,
  which uses H0021 absorbing capture rather than a geodesic integrator.
- Distinct from: `es-inertial-causal-v1`, `es-causal-retarded-monopole-v0`,
  `es-causal-retarded-coupled-v0`, `es-schwarzschild-equatorial-v0`,
  `es-causal-retarded-gem-v0`, `stationary-verlet-q-v1`,
  `stationary-shell-lapse-q-v1`.

## GEM as a candidate metric, not the patch

`es-causal-retarded-gem-v0` may **fill** the patch metric. It is not this
law.

| Patch obligation | GEM v0 | Still missing for this loop |
|---|---|---|
| Shared compiled geometry | (METRIC) names `g(e) = η + Σ h^{(i)} + h_remainder` as a query field | No patch object, causal domain, certificate, or reuse rule |
| Test-body geodesic | (GEM-a) is the linearized geodesic force of excluded-self `E,B` | Euler on a per-body force is not traversal of a compiled slab |
| Clock | (CLK) uses `1 + 2Φ/c² − \|v\|²/c²` from that `g_00` | Admitted as the laboratory quantum **if** `g` is GEM; not a separate gravity clock |
| Null geodesic / light arrival | **Out of domain:** (SIG) is Minkowski; Shapiro and metric nulls refuse | The hole that keeps GEM from closing this loop |
| Source-change invalidation | Cone rules exist as field visibility | No compiled-patch certificate that must die when a cone enters the domain |
| Cache / composition | (COMPOSE) is specified for GEM (MAP). GEM (MAP) is **not** this object | Must hold on the **patch** state, including ray and clock |
| Backreaction | Excluded-self coupling is named; (CONS) is under independent patch | This law requires sources to recompile `g`; it does not implement GEM (CONS) |
| Compact / branches | (ABS-CLASS) reused | Capture-with-transfer is not Schwarzschild; GEM field values remain `f64` |

Do not retune GEM's frozen cosine `2047/2048`. Do not implement GEM
`advance_map` from this document. GEM (MAP) is **not** this patch's (MAP).
GEM (METRIC), (GEM-a), and (CLK) may **fill** `g` / `(Φ, ξ)` in `P`. A
sibling owns the H0029 CONS / capture-history / C-RET / aberration-event /
EXT-EVOL spec patch on the GEM file. This patch spec does not edit that
file.

If GEM (METRIC) is the admitted fill, then (GEO-T) / (CLK-G) / (GEO-N) must
all read **that same** `g` in `P`. GEM (SIG) is then a named **negative**
control for (GEO-N), not an implementation shortcut.

## Named objects

### (PATCH-S) State of the patch

At an admitted cut (integer tick), the patch state `P` is:

1. **Sources.** Two massive piecewise-inertial worldtubes
   `(id, t0, t1, x, v, p, μ)` with `μ > 0` on sourcing segments. Committed
   **past** segments keep their sourcing `μ`. Authored future tubes are not
   state.
2. **Compiled geometry.** One object in `P`: a metric field `g` on the
   causal domain, or its admitted fill `(Φ, ξ)` that determines that `g`
   (GEM (METRIC) is the candidate) from committed history plus remainder.
   (GEO-T), (GEO-N), and (CLK-G) all read **this** object. It is not a
   per-ship force cache, and not a private trio of Φ-responsive formulas
   that happen to co-move.
3. **Test body.** Identity, worldtube with `μ = 0` (does not source),
   laboratory `p`, proper time `τ_T`.
4. **Null ray.** In-flight or received: emission event `(t_e, x_e)`, spatial
   path support, affine/coordinate parameter, reception event or pending.
   The ray does not source.
5. **Clock.** Named worldline (the test body, unless a fixture names a rest
   clock) and accumulated `τ`.
6. **Remainder.** `OmittedTail { R, μ_bound, enclosure }` is part of `P`.
   Incomplete omit without a remainder fails closed.
7. **Certificates.** A live certificate is the triple
   `(source-history digest, remainder, future cone of the change)` plus the
   propagator identity. Validity is **per-event**: event `e` may use cached
   `g` iff the digest matches committed sources, the remainder is the same
   object, and `e` is strictly before every committed source-change's closed
   future cone. There is no global TTL. The frozen ship time `t = 1/16` is
   when **that ship** at `(4, 0)` must not see old `g`; it is not domain-wide
   expiry.
8. **Ledger.** Accounted interventions only. Observation is not state.

Inspect / position / sensor queries do not mutate `P` or any history digest.

### (PATCH-DOM) Causal domain

The compiled `g` is authoritative only on a closed spacetime region `D`
whose every event's causal past, relative to the two sources, is covered by
committed history plus the remainder enclosure.

- Event `e ∈ D` may be evaluated by the reusable propagator.
- An event outside `D` is `UnsupportedPredicate` or requires a different
  compiled patch; it is not silently evaluated from a neighbor's `g`.
- On-cone source visibility follows the existing closed-cone rule:
  `t ≥ t_s` and `c²(t − t_s)² ≥ |x − x_s|²`. Equality is visible.
  (C-CONE) is one rational comparison. Ambiguous `f64` escalates or fails
  closed. An iteration cap is `BranchBudgetExhausted`, not a guessed
  membership.

The frozen laboratory domain is the slab of events that can affect the test
ship, ray, and clock out to horizon `t = 1/8` on the frozen positions below.

### (PATCH-INV) Source-change invalidation

A source rearrangement (μ change, accounted burn, capture, or newly
committed segment) at event `s` **invalidates** compiled `g` at every event
`e` with `e` on or after the closed future cone of `s`. Invalidation is
**per-event**, not a domain-wide expiry.

The frozen ship event `(1/16, (4, 0))` is when **that ship** must not see
old `g`. It is not a global TTL of the certificate. Events still strictly
inside the complement of the cone (for example a far remainder query, or
the pre-change ray's reception) may keep the old `g` until their own cone
membership flips.

- Inside that cone (strictly before the change is visible **at `e`**):
  cached `g` and the three observables at `e` must match the pre-change
  patch.
- On and after the cone **at `e`**: continuing to serve the old certificate
  at `e` is a failed invalidation, even if a later recompute would have been
  cheap. A cache hit after this rule fails (CACHE).
- Same-tick updates are invisible to simultaneous peers (excluded-self;
  simultaneous commit).
- Invalidation does not require waiting for a query. The per-event future
  cone of each committed change is part of `P`.

### (PATCH-PROP) Reusable propagator

`U(t_out, t_in, P)` advances the patch on admitted cuts and returns the full
post-state: source tubes, compiled `g` (or a live certificate pointing at
it), test-body `(x, p, τ)`, ray reception or remaining parameter, clock `τ`,
remainder, earliest pending event (capture, reception, remainder-influence,
invalidation, intervention).

Fate-only classifiers are not this propagator. Schwarzschild circular-radius
identity is not this propagator.

Reuse is allowed only while the per-event certificate holds. Reuse after
(PATCH-INV) is a failed cache, not an optimization. Direct versus
subdivided evaluation still matches (COMPOSE).

### (GEO-T) Test-body geodesic

The test ship follows a **timelike geodesic of the compiled `g`**,
excluded-self (it does not source; it does not feel itself).

The geodesic equation on `D` is

`d²x^μ / dλ² + Γ^μ_{αβ}[g] (dx^α/dλ)(dx^β/dλ) = 0`

with `Γ` from the same `g` that the ray and clock use.

If the admitted fill is GEM, the slow-motion laboratory reduction is GEM
(GEM-a): `a = E_{sources} + v × B_{sources}` with `E,B` from the same
`Φ, ξ`. That reduction is still **geometry**: it is not a Newtonian force
that can be swapped independently of (GEO-N) and (CLK-G).

Instantaneous equal-and-opposite particle forces are not a rule. Delayed
Newton `a = −μ n̂_ret / r_ret²` without the metric is a named negative
control.

On or inside `r_s = 2μ/c²` of a retarded-visible massive source, H0021
absorbing capture is the fallback. Coincidence `r = 0` is `Singular`.

### (GEO-N) Null geodesic

The light ray is a **null geodesic of the same `g`**:

`g_{μν} dx^μ dx^ν = 0`

**(Discriminator.)** Arrival is the **coordinate/affine** reception event of
that geodesic: the parameter `λ_*` and coordinate time `t(λ_*)` at which
the ray meets the named rest receiver on the spatial path. The falsifier
compares those coordinate/affine arrivals. It does **not** discriminate by
tick bin.

**(Commit.)** Tick delivery is how reception is committed into `P`: the first
admitted tick `k` whose bin `(k−1, k]` contains `t(λ_*)`. That binning is
the same contact-tick contract as inertial-v1. A candidate that matches
ticks while the coordinate/affine `Δt` still equals Minkowski or the
pre-change patch fails (GEO-N).

Minkowski reception `|Δx|² ≤ c² Δt²` is the **Φ = 0, ξ = 0 control**, not
the gravitational ray.

When every visible source has `β = 0` (frozen rest fixtures), the linearized
one-way **coordinate** travel time along the Euclidean spatial path `γ` of
length `L` is

`Δt = (1/c) ∫_γ (1 − 2Φ/c²) dl`

with **the same** `Φ` that enters `g_00 = −c²(1 + 2Φ/c²)` and
`g_{jk} = (1 − 2Φ/c²) δ_{jk}`. Because `Φ < 0` for positive `μ`, this is a
delay relative to Minkowski (Shapiro), not an advance.

Required inequalities, **no magnitude bound**:

- `Δt_{P_Δ} > L/c` (strict delay versus Minkowski on the same path)
- `Δt_{P_Δ} ≠ Δt_{P_0}` (post-cone arrival differs from the pre-change patch)

Pre-cone arrival must **match** the pre-change patch. Do not freeze a
Shapiro number. Do not retune a delay after seeing a candidate.

When a visible source has `β ≠ 0`, `g_{0k} = −4 ξ_k / c` from the same `ξ`
as the test-body law participates in the null condition. A light law that
drops `ξ` while (GEO-T) keeps it fails (CONSIS). Acceleration-dependent
radiation at velocity kinks is omitted unless the admitted metric fill names
it; GEM uniform-segment near field is the candidate fill.

Shapiro delay guessed from a catalog, Schwarzschild `4μ/(c²b)` deflection
without time of flight, and inertial-v1 Minkowski signals are not (GEO-N).

### (CLK-G) Clock from the same metric

Elapsed proper time along the named worldline `x^μ(λ)` is

`c² dτ² = −g_{μν} dx^μ dx^ν`

On a committed inertial segment the laboratory quantum is

`rate = floor(2^32 * sqrt(max(0, 1 + 2Φ/c² − |v|²/c²))) / 2^32`

with `Φ` the excluded-self potential of the **same** `g` at the segment's
starting event. Elapsed proper time on the segment is exactly
`(t1 − t0) * rate`. Subdivision does not insert another rounding. If
`1 + 2Φ/c² − |v|²/c² < 0`, the clock fails closed (compact/spacelike).

When `Φ = 0` and `ξ = 0`, (CLK-G) is identical to inertial-v1. This law
does not change that quantum. A gravitational clock that silently replaces
inertial-v1 at vacuum is a failed control. A metric clock that uses a
different `Φ` than (GEO-T) and (GEO-N) fails (CONSIS).

### (EXT-P) Remainder / exterior

The omitted tail is part of `P`. After any positive-duration advance, either
the omitted mass is still enclosed by the updated remainder, or it has been
promoted to listed history **before** its cone can affect a canonical
decision of the ship, ray, or clock. A query-time enclosure that vanishes
from future `P` fails. Observation does not create geometry.

The frozen unit source at `r = 16` cannot be a silent zero at the ship
`r = 4`.

### (BR-P) Terminating branch

Supported predicates terminate in one rational comparison or fail closed:

- Cone membership of a source change relative to ship / emission / reception
  events (Before / On / After). Tie: On (visible).
- Compact class `r² c⁴ ≶ 4μ²`. Tie: OnHorizon (capture fallback).
- Cast membership: not two massive sources, or extra massive sources, refuse.
- Remainder completeness: incomplete omit refuses.
- Exhausted comparison budget: `BranchBudgetExhausted`, never a guessed
  geodesic sign, Shapiro sign, or clock sign.

Unsupported: Kerr, interacting exact 2-body GR, exact elliptic Shapiro
catalog, generic scatter turning roots, `N_mass ≥ 3`. Field *values* of `g`
may be `f64` in this laboratory; that keeps production
`terminating_exact_branches` failed until those values have enclosures.

## Named transition rules

### (CONSIS) Same-metric consistency

(GEO-T), (GEO-N), and (CLK-G) are not three independent probes. They are
three readings of **one object in `P`**: the compiled metric `g`, or its
admitted fill `(Φ, ξ)` that determines that `g`. The object is patch state,
not a private cache per observable.

Let `P_0` be the baseline patch (no source change) and `P_Δ` the patch after
the frozen source change at `t = 0`. At a pre-cone event of that change,
ship position, **coordinate/affine** null arrival, and elapsed `τ` from
`P_Δ` must equal those from `P_0`. At a post-cone event, **all three** must
differ from `P_0`. That co-movement after the μ change is **necessary, not
sufficient**.

Sufficiency: the three post-cone values must be the (GEO-T), (GEO-N), and
(CLK-G) evaluations of **that same object in `P_Δ`**. A private trio of
Φ-responsive formulas — three local expressions that each move after μ
changes but do not share the compiled `g` / `(Φ, ξ)` in `P` — **fails**
(CONSIS), even if each formula is causal and each observable co-moves.

Reject if:

- only the ship moves, while light stays Minkowski and `τ` stays inertial;
- only the clock redshifts, while the ship stays inertial and light stays
  Minkowski;
- only a Shapiro-like delay is applied to light, while the ship uses delayed
  Newton and the clock uses a different potential;
- GEM (GEM-a) is applied to the ship while GEM (SIG) receives the ray;
- a private trio of Φ-responsive formulas co-moves without sharing `g` /
  `(Φ, ξ)` in `P`.

### (BACKREACT) Sources recompile geometry

The two massive bodies are not test particles. Each next massive segment is
the excluded-self response to the compiled `g` of committed history (or an
accounted intervention). After those segments commit, `g` is recompiled.
Authored future worldtubes fail `two_source_one_ship_one_ray_one_clock`
(`authored_futures: false` in the harness JSON). The test ship and ray do
not source. Instantaneous present-state two-body Newton is a negative
control.

This rule names the loop; it does not implement GEM (CONS) and does not
claim Einstein-equation conservation.

### (COMPOSE) Direct versus subdivided

At admitted cuts,

`U(t2, t0, P) = U(t2, t1, U(t1, t0, P))`

on the full patch state, including `g` or its live certificate, remainder,
ship, ray, and clock. Computational splitting must not insert another
rounding or change the physical mesh.

### (CACHE) Cache reuse matches

Let `C` be a compiled propagator for domain `D` with a live certificate.
The cache **key** includes the source-history digest (and the remainder).
Evaluating `U` from `C` must match evaluating `U` from source history on
`D`. Evict `C`, recompile from the same `P`, and compare full canonical
state. A cache hit after (PATCH-INV) **fails**. Alternative refinement
order and pause/resume must not change canonical `P`. Direct versus
subdivided evaluation still matches (COMPOSE).

## Frozen laboratory cast

Rationals below are exact. `c = 64`. Genesis time `−65536`.

| Role | Position | Velocity | μ |
|---|---|---|---|
| Massive A | `(0, 0)` | `0` | `1`, then `2` at `t = 0` |
| Massive B | `(8, 0)` | `0` | `1` (unchanged) |
| Test ship + clock | `(4, 0)` | `0` | `0` (does not source) |
| Rest receiver | `(4, 4)` | `0` | `0` |

Light rays (same spatial path, two emission times):

- Pre-change ray: emit `(t, x) = (−1, (4, 0))` toward `(4, 4)`. Minkowski
  flight `Δt = 4/c = 1/16`. This ray's reception is a pre-change control.
- Post-change ray: emit `(1/8, (4, 0))` toward `(4, 4)` after the ship
  event `(1/16, (4, 0))` has seen A's change. Reception must differ from
  Minkowski and from the same path through `P_0`.

Two-sided times at the ship relative to A's change at the origin:

- Pre-cone: `t = 1/64` (before `4/c = 1/16`)
- On-cone: `t = 1/16`
- Post-cone: `t = 1/8`

Horizon for composition/cache: `t0 = 0`, `t1 = 1/64`, `t2 = 1/8`.

Remainder control (additive to the cast, not a third dynamical source in
the admitted IVP): omitted unit mass at `(16, 0)` with enclosure `R = 16`,
`μ_bound = 1`, or fail closed.

## Frozen falsifiers

Fixtures are in `evolving_spacetime_patch_research` and were written
**before** a patch map. Do not retune numeric bounds after seeing a
candidate. Do not implement authored futures to pass the admitted IVP.
Do not edit old production-gate thresholds or GEM's `2047/2048`.

| Probe | Frozen fixture ids | Reject or stop if |
|---|---|---|
| Complete patch cast | `two_source_one_ship_one_ray_one_clock` | `authored_futures` not `false`, missing `g`, or clocks/rays use unrelated rules |
| Motion from geometry | `source_change_moves_ship` | Pre-cone ship motion, or post-cone inertial |
| Light from geometry | `source_change_delays_light` | Pre-cone arrival change; post-cone `Δt ≤ L/c` or `Δt = Δt_{P_0}`; tick-only match while coordinate/affine arrival is Minkowski or baseline; any frozen Shapiro magnitude |
| Clock from geometry | `source_change_shifts_clock` | Pre-cone `τ` change, or post-cone inertial `τ` at `Φ ≠ 0` |
| Same metric | `same_metric_consistency` | Any one of motion/light/`τ` updates without the others from the same object in `P`; or a private Φ-trio co-moves |
| Direct vs subdivided | `direct_vs_subdivided_patch` | Subdivision changes canonical `P` |
| Cache reuse | `cache_reuse_matches`, `source_change_invalidates_certificate` | Cache ≠ recompute; cache hit after (PATCH-INV); cache key omits source-history digest; treating ship `1/16` as a global TTL |
| Exterior | `remainder_in_patch_state` | Remainder disappears after a step, or observation recompiles `g` |
| Finite branches | `unsupported_third_massive_refuses`, `budget_exhausted_not_a_geodesic` | Iteration caps choose a geodesic/Shapiro/clock sign |
| Φ = 0 clock | `inertial_clock_when_phi_zero` | Gravitational clock replaces inertial-v1 in vacuum |
| Observation | `observation_does_not_recompile` | Queries mutate `P` |
| Named negative controls | `minkowski_signal_not_metric_null`, `delayed_newton_not_the_patch`, `schwarzschild_classifier_not_evolving_patch`, `gem_force_without_null_geodesic_fails_consistency` | A “pass” by relabeling H0011 / H0019 / H0024 / GEM (SIG) |

`pre_lightcone_response_max = 0`. Post-cone influence is strict for all
three observables. No Shapiro magnitude, no orbit period, and no aberration
cosine is frozen here. GEM's translating-source cosine stays on the GEM
key. The harness JSON records `authored_futures: false` on
`two_source_one_ship_one_ray_one_clock` because this table claims it.

## Finite map

**(MAP)** Admitted cuts are integer ticks. One tick:

1. Apply accounted interventions on immutable pre-batch `P`.
2. Advance in-flight (GEO-N) on the coordinate/affine parameter; deliver
   receptions on the tick that contains `t(λ_*)`. A received burn becomes
   an intervention at the **next** tick. Tick delivery is commit, not the
   (GEO-N) discriminator.
3. Classify compact membership of the test body against retarded-visible
   sources; capture uses H0021 fallback. Otherwise (GEO-T).
4. Accumulate (CLK-G).
5. Advance massive sources by (BACKREACT) on committed history.
6. Commit every next massive segment simultaneously.
7. Recompile `g` on `D`, or keep it at event `e` iff (PATCH-INV) says the
   per-event certificate still holds at `e`.
8. Update the remainder by (EXT-P).
9. Return full `P` and the earliest pending event.

(MAP) is the laboratory `advance_patch`. Score it against the frozen
fixtures without retuning. Authored trajectories and Minkowski rays remain
invalid substitutes. Compact certification and terminating exact branches
stay failed because field values of `g` remain `f64`.

## What must exist before any new map code

1. This specification, including the CONSIS / GEO-N / CACHE identities
   (done).
2. Frozen falsifiers under `evolving_spacetime_patch_research` without
   edits to old numeric thresholds (done). `authored_futures: false` is in
   the harness JSON (done).
3. A spec-module check that those fixture identities cannot be renamed,
   dropped, or reordered silently, and that the spec-patch pins cannot
   drift (done).
4. H0029 CONS holes patched **in-tree** on the GEM spec and `tiny_causal`
   identities (sibling; not this change). A floating candidate is never
   sufficient evidence of a canonical branch.
5. Then a law-lab implementation of this (MAP) scored against **these**
   frozen fixtures without retuning. No engine wiring. No G2 promotion.
   No 2D log kernel. No delayed-Newton-as-G2. Do not implement GEM
   `advance_map` from this patch. GEM (MAP) is not this object.

## Non-claims

Not G2. Not production. Not Kerr. Not interacting Einstein gravity. Not
FMM. Not delayed-Newton-as-G2. Not 2D log gravity. Not GEM (MAP). GEM
(METRIC)/(GEM-a)/(CLK) may fill `g`. Not a replacement for inertial-v1.
Not engine wiring. Field values of `g` remain `f64`. Compact certification
stays failed. `terminating_exact_branches` stays failed. Billion-ship /
ten-billion-year gravitational qualification remains unqualified. No
Shapiro magnitude is frozen.
