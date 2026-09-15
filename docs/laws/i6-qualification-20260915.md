# I6 same-model qualification matrix — 15 September 2026

Plan I6 exit is **this matrix existing and run**, not a green promotion.
`production_law` remains **null**. `CANONICAL_GRAVITY_ACCEPTANCE` remains
`diagnostic-only`. Full-engine remains **incomplete**. Frozen `1dac658`,
H0052/H0054, and H0124 counts are unchanged. FAIL rows are not deleted.

Machine-readable companion:
[i6-qualification-matrix-20260915.json](i6-qualification-matrix-20260915.json).

## One identified model

| Field | Value |
|---|---|
| Canonical law | `es-inertial-causal-v1` |
| Diagnostic response | `es-linearized-retarded-gem-response-v0` |
| Near-mass keep | `es-schwarzschild-1pn-gem-v0` (v0 Newton interface FAIL row kept) |
| Implementation | `emergent-full-engine-integration` |
| Workload | connected family + hierarchy + in-flight ray + observer/policy + archive |
| Promotion | **false** |
| Full engine | **false** |

## Observatory

Native `EngineBridge` hosts `emergent_engine::Engine`. `--world connected` is
the I6 scene. GEM gallery is not the qualification world.

## Gates (re-run after 1PN + domain-local field authority)

| id | status |
|---|---|
| observatory-same-engine | PASS |
| compiler-inertial-facts | PASS |
| persist-replay | PASS |
| cold-history-query | PASS |
| galaxy-quadrupole-skip | **FAIL** 0.478 vs 0.05; direct sums admitted |
| moving-multi-mass-compact | **UNSUPPORTED** (1PN + stationary Sch still cannot) |
| sch-gem-accel-continuity-v0 | **FAIL** Newton GEM 0.10 (row kept) |
| sch-gem-accel-continuity | **PASS** 1PN GEM vs Sch Γ^r_tt ≤ 0.05 |
| engine-canonical-gravity | **PASS** admitted-interior `authorizes_gem_events`; global diagnostic-only |
| family-moment-as-galaxy-skip | **FAIL** N=4 KEEP is not an all-galaxy skip |
| production-promotion | **FAIL** |
| envelope-pressure / frozen-target | UNSUPPORTED |

## Six cards

| id | status |
|---|---|
| fast-ships-light-twins | PASS |
| solar-system-hierarchy | PASS |
| three-bodies | PASS |
| galaxy-like-population | PASS via direct sums; quadrupole FAIL visible |
| black-hole-near-mass | **UNSUPPORTED** (moving multi-mass) |
| fleet-asteroid-causal | PASS (N=4 family-moment only) |
| crossing | **FAIL** (required gravitational crossing still unsupported) |

Envelope targets remain targets. Behavior gates use remainder bands / independent
oracles. This matrix does not pin leftover==0.0, 1188/1675, or 1.519….
