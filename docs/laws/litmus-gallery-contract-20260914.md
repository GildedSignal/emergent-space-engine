# Litmus gallery contract (2026-09-14)

Packet 1 freeze of the six visual cards, seed/comparison rules, coupled
transition, and root interfaces. Machine-readable companion:
[litmus-gallery-contract-20260914.json](litmus-gallery-contract-20260914.json).

**Not** a gravity law, GLM shortcut, gallery UI, or `Engine::advance`
wiring. Canonical engine law remains `es-inertial-causal-v1`. Observatory
is a host: reuse existing `ViewMode`, `inspect` / `observe_with_budget`,
and `history_digest` names. Numeric magnitude bands are **UNCONFIRMED**;
Julien has not chosen them.

Governing sources: heading-check card; draft 0.3 behavior instrument and
seed tables in [compiler-engine-plan-20260913.md](../compiler-engine-plan-20260913.md);
H0075 visual families; H0070 light-bend as must-feel.

## How to judge (quick, seed-aware)

Each run names an `intended_outcome_class`. Judge that class, not a
poster animation.

1. **Glance** the card's look-for for this class (~5 s).
2. **Fast-fail** if any looks-wrong cue is present.
3. Open physical/correctness checks only when the glance is ambiguous.

A second seed may yield a different allowed class. That is expected. It
cannot erase the first result. Do not search seeds until the law appears
to work. Passing the gallery increases confidence over the tested domain;
it does not prove all future emergent behavior. A newly found interaction
failure is a retained counterexample on the relevant card, not a new
scene-specific physics rule.

## Shared overlay and display rules

All six cards share one optional **work overlay**: `reuse`,
`newly_compiled`, `refinement`, `repaired_prediction`. Sampling it is a
`WorkBudget`-charged request and **must not change the world**
(`history_digest` at a declared committed cut stays put). Cached playback
is labeled with its actual `law_id` and source revision; it is never a
fresh validation run. Display magnification of a tiny effect must be
labeled; changing a physical parameter must update all consequences
together. Historical reconstruction, cache eviction and subdivision
checks run across cards rather than becoming more scenes.

## Six frozen cards

### 1. Fast ships, light and twins

- **id:** `fast-ships-light-twins`
- **Glance:** Light always leaves at `c`; clocks and sky fit the motion.
- **Look for:** Pulses reach moving receivers in an order that matches
  emission events and finite `c`. A boosted observer sees direction and
  arrival times change while the same physical events stay put.
  Accumulated proper time fits the worldline (twins after reunion, or a
  one-way traveling clock versus a stay-at-home clock).
- **Looks wrong:** Emitter speed is added to light; rotating or boosting
  the camera changes *when* pulses meet; reunion aging is equal after a
  high-speed trip; already-received pulses reorder after a frame change.
- **Do not force:** Not every seed is a closed twin circuit or a textbook
  Doppler poster. A one-way pulse to a receding ship is enough if
  arrivals and clocks fit the motion. Some seeds may omit reunion.
- **Allowed classes:** `one_way_pulse`, `moving_receiver`, `twin_reunion`,
  `aberration_only`.
- **Checks underneath:** local light speed; aberration; admitted Doppler
  ratios; accumulated proper time from the same geometry as the pulses.

### 2. Solar system and hierarchy

- **id:** `solar-system-hierarchy`
- **Glance:** A supported hierarchy stays organized; a kick breathes, it
  does not snap to a circle.
- **Look for:** Bound configurations initialized in a supported stable
  regime remain organized over the declared duration. Perturbations and
  precession appear smoothly. Inner and outer motions keep distinct
  timescales.
- **Looks wrong:** Every seed spirals in or out numerically; every orbit
  is forced perfect despite perturbations; a small kick instantly
  circularizes *or* unbinds the whole hierarchy; inner and outer periods
  look the same.
- **Do not force:** Not every seed is a miniature Solar System. A binary
  plus distant companion, a compact pair, or a mildly eccentric hierarchy
  all count. An unbound flyby belongs to three-body / encounter classes,
  not as an automatic solar-system fail.
- **Allowed classes:** `supported_hierarchy`, `binary_plus_companion`,
  `perturbed_precessing`, `compact_pair`.
- **Checks underneath:** timescales, source recoil, drift, magnitude
  relations. Formation from arbitrary matter is a separate claim.

### 3. Three bodies

- **id:** `three-bodies`
- **Glance:** Nested seeds can stay bound; encounter seeds can swap,
  eject, or go messy.
- **Look for:** At least one hierarchical diagnostic seed can remain
  bound over the declared window. Encounter seeds can exchange partners,
  eject a body, or become chaotic. Trajectories stay continuous through
  close passes.
- **Looks wrong:** Every seed must remain stable to pass; bodies jump
  through encounters; the “chaotic” seed is a looped identical animation;
  a different late trajectory is treated as a compiler regression.
- **Do not force:** Do not require the same late identity. Stability is
  one class, not a universal pass. Report the mix of bound / exchange /
  ejection / chaotic outcomes.
- **Allowed classes:** `hierarchical_bound`, `partner_exchange`,
  `ejection`, `chaotic_close_pass`.
- **Checks underneath:** conserved/accounted quantities; short-time
  reference behavior; ensemble outcomes. Chaos does not excuse a
  compiler changing the selected law.

### 4. Galaxy-like self-gravitating population

- **id:** `galaxy-like-population`
- **Glance:** The crowd shears together; mass, not sprites, moves it.
- **Look for:** Coherent collective motion and shear. An introduced
  perturber dents the flow. Member masses affect the common field.
- **Looks wrong:** Decorative test particles; every seed is forced into
  a spiral; already-seen motion changes when more members are `decode`d;
  a reduced scene is sold as cosmological formation.
- **Do not force:** Not every seed is a grand-design spiral. A clumpy
  disk, a triaxial blob, or a sheared stream can pass if collective and
  mass-responsive.
- **Allowed classes:** `sheared_disk`, `clumpy_collection`,
  `triaxial_blob`, `perturber_response`.
- **Checks underneath:** mass accounting; density/velocity profiles;
  perturbation response over declared dynamical times.

### 5. Black hole, near-mass rays and clocks

- **id:** `black-hole-near-mass`
- **Glance:** Closer pass: more bend, more delay; too close, no return;
  clocks agree with that story.
- **Look for:** A connected family from weak flyby through strong
  bending/delay into absorbing capture. Near-mass clocks run slow in a
  way compatible with the same geometry.
- **Looks wrong:** Rays pass through an absorbing region; extra delay
  vanishes after a cache or partition change; bend, delay and clocks
  disagree (one effect faked, the others left Minkowski); interiors are
  required to tell the capture story.
- **Do not force:** Not every seed is a photon-sphere postcard. A
  weak-field graze plus one capture seed is a valid family. How *much*
  bend remains band-UNCONFIRMED; whether light bends and takes extra
  time is must-feel (H0070).
- **Allowed classes:** `weak_flyby`, `strong_bending_delay`,
  `absorbing_capture`, `near_mass_clock`.
- **Checks underneath:** supported compact trajectories, reception,
  committed history. Absorbing capture (H0021) is enough; Kerr interiors
  are out. Extra delay is not a Shapiro-as-product catalog number.

### 6. Fleet, asteroid and causal intervention

- **id:** `fleet-asteroid-causal`
- **Glance:** Many specks matter together; news arrives at different
  times; later motion feels the change.
- **Look for:** Many small masses jointly affect a larger body. Weak
  influence accumulates. A source or course change reaches different
  observers at different times and produces later feedback.
- **Looks wrong:** Remote bodies react before possible influence; old
  gravity disappears at capture; small-body effect is dropped; overlay
  sampling moves the asteroid.
- **Do not force:** Not every seed needs a visible asteroid shove in one
  short loop. Cumulative effect may be tiny — if magnified, label it. A
  too-sparse fleet is a reported outcome, not a cue to hunt a prettier
  seed.
- **Allowed classes:** `collective_nudge`, `slow_backreaction`,
  `staggered_arrival`, `capture_keeps_history`.
- **Checks underneath:** materialized small-world comparison;
  direction/magnitude of moving-source response; source/field exchange;
  A→B→A feedback.

## Coupled transition (not a seventh physics)

**id:** `coupled-fleet-hierarchy-inflight-ray-observer-boost`

A fleet perturbs a hierarchical system while a ray is in flight and the
observer changes speed. The crossing is required gallery exercise, not a
new law. It reuses cards 2, 1/5 and 6: hierarchy organization, in-flight
light, observer boost, and delayed many-body feedback. Look-for is the
conjunction of those glances. Looks-wrong if any participating card's
fast-fail fires, or if the ray's committed history changes because the
observer boosted.

## Seed and comparison rules

A seed is random input to a particular generator and RNG version. It is
not the identity of a universe across all code changes. Randomness stays
tied to semantic identities and purposes (`semantic_random(seed, entity,
event, purpose, lane)` / `emergent-space-random-v1`), never task order
or family partitioning.

| Change class | What stays fixed | What must agree |
|---|---|---|
| `compiler_only` | Law, resolved initial state, interventions; same committed cuts | Canonical outcomes **exactly**, including chaotic worlds. Chaos does not excuse a compiler changing the selected law. |
| `physical_law` | Literal shared initial states where both laws admit them; new `law_id` retained | Short-time physical relationships, regime-dependent magnitude anchors, ensemble structure. Long chaotic trajectories need not coincide. |
| `law_aware_init` | Declared common distribution of physical regimes; both generator versions and both resulting states recorded | Behavior across that distribution. Recomputing equilibrium ICs for a new law is a **separate** experiment, not a matched-state comparison. |
| `generator_only` | Physical law and a declared target distribution | Generated-state properties and outcome distributions. The same numeric seed may now produce a different world. |

**Banks.** Use a small **diagnostic** set for daily feedback plus a
**predeclared held-out** bank. Report unstable, rejected and failed
cases as well as successful ones. If initialization rejects an
inadmissible state, declare that rule independently of the future
outcome and retain the rejection rate.

**Forbidden.** Searching seeds until a law looks good. Handpicked-seed
rescue. Treating a second pretty seed as erasure of a first failure.

Numeric seed integers and generator versions for a future gravity law
are **UNCONFIRMED**. This freeze locks roles and comparison semantics,
not lucky numbers. When a generator exists, record `law_id`,
`rng_version`, `seed`, normalized parameters, resolved initial state,
interventions, observing frame and queried cuts on every run.

## Dimensionless controls

These are scenario controls and diagnostics, not object-class switches
in the law:

| Control | Symbol | Role |
|---|---|---|
| Speed over light | `v_over_c` | kinematic / twin / boost regime |
| Compactness | `compactness_gm_over_r_c2` = `GM/(r c²)` | weak vs strong field |
| Mass ratio | `mass_ratio` | hierarchy / three-body / fleet |
| Closest-approach ratio | `closest_approach_ratio` | flyby vs capture vs encounter |
| Perturbation duration | `perturbation_duration_orbits` | backreaction window |

Exact values are rational strings (engine style). Display floats are
presentation only.

## Regimes and numeric bands (UNCONFIRMED)

Julien has not chosen bands. Placeholders below are **not gates**. Do
not invent a universal percentage. Do not reward exaggerating one effect
while leaving others unchanged. Exact algebraic inertial limits may keep
strict tests; approximate gravitational models need explicit
accuracy-and-duration bands once chosen.

| Regime id | Typical controls | Example observables | Band |
|---|---|---|---|
| `kinematic` | `v_over_c` | pulse order, aberration, twin aging | UNCONFIRMED |
| `weak_field` | small `GM/(r c²)` | graze bend, extra delay, clock rate | UNCONFIRMED |
| `close_encounter` | `closest_approach_ratio`, mass ratio | partner exchange vs jump | UNCONFIRMED |
| `strong_field_compact` | compactness near capture | connected flyby → capture | UNCONFIRMED |
| `collective` | population, mass accounting | shear, perturber dent | UNCONFIRMED |
| `slow_backreaction` | `perturbation_duration_orbits` | fleet-on-asteroid, A→B→A | UNCONFIRMED |

Schwarzschild clocks, trajectories and weak-field bending remain
*validation references* for static spherical domains, not proof that a
dynamic multi-source compiler exists.

## Root interface freeze

Every gallery run or playback record carries the fields below. The JSON
Schema for a run record is the `interface_schema` object in the companion
file; `$ref`s resolve relative to that object.

- `card_id`, optional `coupled_transition_id`
- `law_id` (engine default `es-inertial-causal-v1`; gallery gravity law
  UNCONFIRMED)
- `rng_version` (inertial hasher prefix `emergent-space-random-v1`)
- `seed` (`u64`)
- `intended_outcome_class` and reported `observed_outcome_class`
- `seed_bank`: `diagnostic` or `held_out`
- `comparison_class` from the table above
- `normalized_parameters` (five controls; unused may be JSON `null`)
- `resolved_initial_state` (committed genesis: bodies/families/digest)
- `interventions` (engine `RecordedIntervention`: tick, observer,
  command, event_id)
- `observing_frame` (observer id, velocity as `v_over_c`, knowledge
  channel)
- `queried_cuts` (committed ticks; each cut may carry `history_digest`)

### True-state versus observer knowledge

Channels **must** be distinguishable. Names match the host:

| Channel | Engine / observatory name | May reveal | Must not |
|---|---|---|---|
| `diagnostic` | `ViewMode::Diagnostic`; `inspect` / `position` at committed `t` | coordinate-time state, true present positions | mutate canonical history |
| `historical_sensor` | `ViewMode::HistoricalSensor`; `observe` / `observe_with_budget` | emission coordinates that have reached the observer | silently substitute inferred present positions; empty sky on incomplete query |
| `decode_only` | `decode` | generator parameters | certify a future |
| `work_overlay_sample` | charged `WorkBudget` overlay request | reuse / compile / refine / repair visualization | change the world or `history_digest` |

Incomplete sensor queries are pending/warning (`ObserveResult.complete
= false`), never a silent empty sky, and do not mutate `history_digest`.
In-world planners use `historical_sensor` only. Omniscient diagnostics
stay explicitly separate. `canonical_hash` on a snapshot is
`history_digest(through)` at a declared completed cut.

### Work-overlay sample request

```
kind: reuse | newly_compiled | refinement | repaired_prediction
charged: true
budget: { operations, max_events }   // WorkBudget
mutates_world: false
```

### Cached playback

Must label actual `law_id` and source revision. Never presented as a
fresh validation run.

### Magnification

If display scale of a physical effect ≠ 1, a visible label is required.
Chart camera zoom of the whole scene is ordinary presentation; scaling
one consequence (delay, clock lag, fleet nudge) independently is
magnification.

## Observatory host (types only)

Reuse, do not rewrite: `ObservatoryWorld`, `ViewMode`, `UiSnapshot`
(`canonical_hash`, `law_name`, `warning`, `progress_label`),
`UiCommand`. Gallery cards are future consumers of these types plus the
JSON run record. This packet does not add a gallery UI.

## Refuse

- Wiring laboratory gravity through `Engine::advance`
- Implementing a new physical law or the GLM shortcut
- Full observatory gallery implementation as this packet
- Searching seeds to make a law look good
- Claiming numeric bands are approved
- Treating `decode` coverage as a world change
- Treating overlay sampling or query order as license to change
  `history_digest`
- A seventh physics for the coupled transition
