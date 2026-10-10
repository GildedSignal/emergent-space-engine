# Co-orbital certificate proposal

Uncommitted on `wt/cx-b-coorbital-cert`; base `a838a284a27a6813434362cc2adfde946d2085db`. Nothing merged.

**Scoped PASS:** 21 crate tests. The independent r8 v3 oracle core is copied verbatim; full all-pairs truth runs on the eight gold scenes, the checker jam and a dense eccentric ring. Initial/final overlaps are separate from interior local minima. Two zero-contact gold scenes are negative controls.

| Scene | Truth | Misses before -> after | Setups before -> after | Checks before -> after |
|---|---:|---:|---:|---:|
| checker-jam | 484 | 43 -> 0 | 19900 -> 18335 | 1979 -> 1979 |
| dense-ring | 768 | 512 -> 0 | 32640 -> 256 | 1024 -> 1024 |
| gold-800 | 11 | 2 -> 0 | 319600 -> 1866 | 60 -> 60 |
| gold-adj | 253 | 20 -> 0 | 19900 -> 12000 | 1060 -> 1060 |
| gold-bunch24 | 49 | 1 -> 0 | 19900 -> 2653 | 226 -> 226 |
| gold-bunch25 | 30 | 3 -> 0 | 19900 -> 4729 | 118 -> 117 |
| gold-bunch26 | 117 | 19 -> 0 | 19900 -> 7115 | 451 -> 451 |
| gold-bunch28 | 65 | 5 -> 0 | 19900 -> 11959 | 289 -> 287 |
| gold-uniform | 0 | 0 -> 0 | 19900 -> 136 | 1 -> 1 |
| gold-wide | 0 | 0 -> 0 | 19900 -> 243 | 2 -> 2 |

False reports: 0 before and after on every scene. Before: 3/3 original unit tests pass; after: 10 unit + 11 independent-truth/cost tests pass. Full release command: 15.4 s, peak RSS 110,084,096 bytes. Every measured test is under 60 s and every measured process under 2 GB. Power, load, swap and available thermal status are in the raw logs; early sandbox-denied readings are retained.

Ring cost gate (visits + setups + proposed passage checks + boundary checks; inner state evaluations excluded): before FAIL at N=32, truth=32, work=752 > bound=512; after PASS at N=32/64/128, truth=N, work=8*N <= 16*N. The before total in summary.json is corrected by corrections.json; the original raw log is authoritative.

Scale gate: before phase certificate UNBUILT; after N=10^3/10^4/10^5/10^6 eccentric-ring bodies, neighbours=N, max_k=1. The high-e Wide arming test keeps the passage-overlap cap. Tree tests cover scrambled IDs and unequal child radii. The first new Wide fixture was Full-only and failed its non-vacuity assertion; its failure is retained in after/crate-first-probe.log. A tangent high-e fixture exercises Wide and passes, with the same assertion.

Mechanism: midpoint mean-longitude sorting; contact angle + bounded equation of centre + frequency drift over the full horizon bounds every possible partner. Shared shapes cancel the common equation of centre. The dimensionless swept phase spread/circumference selects the phase representation below a semicircle; otherwise the envelope/arming tiers apply. No fixed rank-four truncation, no quadratic stored pair list. The imported lab tree also needs canonical ID ordering at same-leaf pairs and enclosing unequal child disks; both fixes are covered.

**Limits:** sorting is O(N log N), then streaming traversal O(N*k), with O(N) storage. k is window occupancy, measured up to 162 in the jam; it can grow with N in mixed/crowded shapes. Phase kicks rebuild the group, rather than maintaining kinetic order. These are float research APIs, with no universe wiring or integer-law qualification. The full frozen r8 v4 rung (dip quantum, twenty 100-orbit belts, steady/scaling/kicks) was NOT RUN; this is its independent truth-construction component, not integrated qualification. Frozen criteria/evidence and the original crate method/truth/pairs code are unchanged.

Reproduce: `cargo test --release -p emergent-encounters -- --nocapture`. For before contact/cost measurements: `ENCOUNTER_BASELINE=1 cargo test --release -p emergent-encounters --test phase_truth -- --nocapture` (expected failures). References, source hashes and all scene counters: summary.json plus corrections.json. Raw logs retain failed controls and environmental readings.
