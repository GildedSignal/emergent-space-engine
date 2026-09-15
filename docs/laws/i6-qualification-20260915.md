# I6 same-model qualification matrix — 15 September 2026

Plan I6 exit is **this matrix existing and run**, not a green promotion.
`production_law` remains **null**. `CANONICAL_GRAVITY_ACCEPTANCE` remains
`diagnostic-only`. Full-engine remains **incomplete**. Frozen `1dac658`,
H0052/H0054, and H0124 counts are unchanged.

Machine-readable companion:
[i6-qualification-matrix-20260915.json](i6-qualification-matrix-20260915.json).

## One identified model

| Field | Value |
|---|---|
| Canonical law | `es-inertial-causal-v1` |
| Diagnostic response | `es-linearized-retarded-gem-response-v0` |
| Implementation | `emergent-full-engine-integration` |
| Workload | connected family + hierarchy + in-flight ray + observer/policy + archive |
| Promotion | **false** |
| Full engine | **false** |

A candidate with mixed PASS and FAIL/UNSUPPORTED required cards cannot select
`production_law`. This run is that candidate.

## Observatory

Native `EngineBridge` hosts `emergent_engine::Engine` (`scenario::observatory`
by default; `--world connected` loads the I6 scene). Same crate and law as
I1–I5. The GEM-response gallery in `observatory/src/gallery.rs` is **not**
the qualification world.

## Gates

| id | status |
|---|---|
| observatory-same-engine | PASS |
| compiler-inertial-facts | PASS |
| persist-replay | PASS |
| cold-history-query | PASS |
| galaxy-quadrupole-skip | **FAIL** remainder 0.478 vs band 0.05; admitted direct sums |
| moving-multi-mass-compact | **UNSUPPORTED** |
| sch-gem-accel-continuity | **FAIL** accel remainder 0.10 vs 0.05 |
| engine-canonical-gravity | **FAIL** diagnostic-only |
| family-moment-as-galaxy-skip | **FAIL** N=4 rest KEEP is not an all-galaxy skip |
| production-promotion | **FAIL** |
| envelope-pressure | UNSUPPORTED |
| envelope-frozen-target | UNSUPPORTED |

## Six cards

Each card names look-for, allowed outcome class, model/regime, and comparison
type. Failing inputs and unconfirmed magnitudes stay visible.

| id | status | class | comparison |
|---|---|---|---|
| fast-ships-light-twins | PASS | `one_way_pulse` | compiler_only oracle |
| solar-system-hierarchy | PASS | `supported_hierarchy` | physical_law band 0.05 |
| three-bodies | PASS | `hierarchical_bound` | physical_law |
| galaxy-like-population | PASS via **direct sums** | `clumpy_collection` | quadrupole skip FAIL remains visible |
| black-hole-near-mass | **UNSUPPORTED** | `near_mass_clock` | stationary only |
| fleet-asteroid-causal | PASS | `staggered_arrival` | family KEEP on N=4 fixture only |
| coupled-…-boost (crossing) | **FAIL** | `crossing` | gravity not canonical |

Daily gallery seed `0x14C0_55ED`. Held-out seeds `0x16B0_1D01` /
`0x16B0_1D02` are predeclared; they do not erase FAIL cards.

Envelope: tiny PASS; connected PASS; pressure UNSUPPORTED; frozen target
UNSUPPORTED. ≤4 GiB / 30 FPS / billion-identity hour remain **targets**.

## Behavior, not leftover pins

Compiler-only gates compare independent inertial contact/arrival oracles to
engine ticks/subjects/digest. Physical-law gates use the 0.05 remainder band.
This matrix does not `assert_eq` leftover==0.0, freeze 1188/1675 ops, or pin
`1.5193527764310737`.
