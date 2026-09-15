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
| Moving compact | `es-moving-schwarzschild-1pn-v0` laboratory **PASS**; hosted on connected Engine; GEM-to-horizon wrappers stopped |
| Implementation | `emergent-full-engine-integration` |
| Workload | connected family + hierarchy + in-flight ray + observer/policy + archive |
| Promotion | **false** |
| Full engine | **false** |

## Observatory

Native `EngineBridge` hosts `emergent_engine::Engine`. `--world connected` is
the I6 scene. GEM gallery is not the qualification world.

## Gates (re-run after Engine-hosted moving compact)

| id | status |
|---|---|
| observatory-same-engine | PASS |
| compiler-inertial-facts | PASS |
| persist-replay | PASS |
| cold-history-query | PASS |
| galaxy-quadrupole-skip | **FAIL** 0.478 vs 0.05; direct sums admitted |
| moving-multi-mass-compact | **PASS** `es-moving-schwarzschild-1pn-v0`; compactness 0.5 admitted |
| sch-gem-accel-continuity-v0 | **FAIL** Newton GEM 0.10 (row kept) |
| sch-gem-accel-continuity | **PASS** 1PN GEM vs Sch Γ^r_tt ≤ 0.05 |
| engine-canonical-gravity | **PASS** admitted-interior `authorizes_gem_events`; global diagnostic-only |
| family-moment-as-galaxy-skip | **FAIL** N=4 KEEP is not an all-galaxy skip |
| production-promotion | **FAIL** |
| envelope-pressure / frozen-target | UNSUPPORTED |

## Envelope rungs (measured; not the target)

Freeze of independent activity / queries / reconstruction was declared before Instant/RSS/digest. Fixed ICs are many-seed capable, not the universe. Process RSS is `ps` of the test process, not an isolated heap. Nested Charge is GEM `ledger_total` (children included). Behavior is reception+replay / persist+in-flight / independent oracle, not leftover==0 or frozen op counts.

| id | status | rss_kb | wall | digest prefix | ledger_total | owned_bytes |
|---|---|---|---|---|---|---|
| tiny-complete-loop | **PASS** | 4656 | 10.5 ms | `b101a4a7a1486402` | 0 (inertial) | 4766 |
| connected-family-hierarchy | **PASS** | 7808 | 36.9 ms | `65b7b76ab4a2346b` | 1052 | 5130 |
| pressure-sweeps | **FAIL** | 5920 | 13.8 s | `951cc96ad9f4ae86` | 928 | 157961 |
| frozen-integrated-target | **UNSUPPORTED** | — | — | — | — | — |

Pressure freeze: packed quiet/hot (64 bodies, 10 families / 48 members, horizon 80). Limiter **sequential-query**: independent inertial oracle 12.1 s and disagreed (`oracle=false`); replay and far-family decode held. Cooperative yield paused 217 times (advance 842 ms). Collocation 21.6 ms. Reconstruction 833 ms. Residual CanonicalState 158 KB. Not a ≤4 GiB / 30 FPS / billion-identity claim. Envelope-pressure **gate** stays UNSUPPORTED.

## Held-out comparison bank

Re-seeding cannot erase galaxy quadrupole FAIL 0.478.

| comparison | seed | status |
|---|---|---|
| compiler_exact | `0x16B0_1D03` | PASS replay+oracle |
| numerical_refinement | `0x16B0_1D04` | PASS RK2 vs RK4 remainder 1.35e-2 ≤ 0.05 |
| physical_law | `0x16B0_1D05` bank id | PASS family-moment remainder band on N=4 rest fixture; not an all-galaxy skip |

These rungs do **not** promote envelope-pressure or ≤4 GiB / 30 FPS / billion-identity hour.

## Six cards

| id | status |
|---|---|
| fast-ships-light-twins | PASS |
| solar-system-hierarchy | PASS |
| three-bodies | PASS |
| galaxy-like-population | PASS via direct sums; quadrupole FAIL visible |
| black-hole-near-mass | **PASS** moving 1PN until r_if, Sch geodesic, capture 0.5→8.5 |
| fleet-asteroid-causal | PASS (N=4 family-moment only) |
| crossing | **PASS** same Engine hosts capture + ships/policy/archive; remainder 1.35e-2 vs 0.05 |

Exact remaining gap: comparable-mass strong-field NR (mass ratio > 0.1 inside
`r_if`); crossing is Engine-hosted diagnostic compact, not canonical gravity.
Linearized GEM wrappers remain stopped (H0144). Galaxy quadrupole skip 0.478
and family-as-galaxy-skip FAIL rows kept. Envelope-pressure and frozen-target
stay **UNSUPPORTED**; tiny/connected rungs PASS; pressure-sweeps rung **FAIL**
(sequential-query limiter, oracle mismatch) and does not promote those gates.

Envelope targets remain targets. Behavior gates use remainder bands / independent
oracles. This matrix does not pin leftover==0.0, 1188/1675, or 1.519….
