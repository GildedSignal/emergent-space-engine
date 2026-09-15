# I3 keep/reject evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
Not I3 exit. Not I4–I6. Nested Charge `ledger_total` is the denominator. Source-only ratios are not total savings.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, base `254ba1f`, parent `e319bc9`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-engine --lib -- --test-threads=1` | PASS (31) |
| `cargo test -p emergent-engine --test causal_contract -- --test-threads=1` | PASS (18) |
| `cargo test -p emergent-engine --test i1_connected_scene -- --test-threads=1` | PASS (2) |
| `cargo test -p emergent-engine --test i1_increment2_authority -- --test-threads=1` | PASS (6) |
| `cargo test -p emergent-engine --test i2_composed_scene -- --test-threads=1` | PASS (1) — now via `advance_region` |
| `cargo test -p emergent-engine --test i3_representation -- --test-threads=1` | PASS (4) |
| `cargo test -p emergent-law-lab --lib i3_ -- --test-threads=1` | PASS (4) |
| `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` | PASS (54) |

## Two-region scheduler

`Engine::advance_region` rewinds the physics clock to that region's `certified_through`, scans only identities in the region range, and raises that region's cut. A lagging overlapping AABB (expanded by radius) refuses independent advance and requires `advance_joint`. Lost lookahead still refuses when an incoming emission is ahead of the source cut. I2 composed-scene cuts now use this path: hierarchy certified through 8 while family remains 0, then each region advances to 40 and reconcile yields a global cut.

This closes the H0130 leftover that certified cuts only overlaid one clock. It does not mint GEM events and does not solve broadcast indexing.

## Keep versus reject (nested ledger)

| Hypothesis | Domain | Total-cost | Decision |
|---|---|---|---|
| Interval collocation vs Euler `Reference::evolve_to` | Quiet two-body, H=1 ledger 578; H=3 ledger **1250** vs Euler **5602**; bytes 4229; coeff 222; cert 3; recon 12; factorization 18; random-time eval 1583 ns | Compile ledger grows with H and still includes construction/certificate/reconstruction | **KEEP** as cheaper than Euler in this quiet H≤3 pair domain. Failure: not a skip of evolution; collocation remains sequential. |
| Compact / phase+residual after worldtubes exist | Same quiet compiles; coefficient_construction > 0 | Fitted after collocation | **REJECT** as skipped evolution. Packet 3 PERIOD is algebraic control, not this GEM orbit. |
| Phase/secular skip of long quiet time / resonance | No admitted GEM resonance fixture | — | **REJECT** this slice. |
| Eccentricity / weak persistent forcing | H=2 eccentric ledger 944 / bytes 1749; filtered four-kick ledger 954 / bytes 666 | Still sequential collocation | No competing skip; numbers only. |
| Prefix repair vs recouple | Quiet pair + `laboratory_kick`, H=3. Repair ledger **923** vs recouple **1212**; runtime 923 vs 1212; reconstruction 19 vs 15; certificate 2 vs 2; bytes 1446=1446. `reuse_certified_interval_functions` ok. | Reconstruction and certificate charged | **KEEP** in quiet-kick H=3. Failure: not a general skip; close-entrant does not share this domain. |
| Local pair-inverse / Schur tide vs recouple | Quiet H=3 pair + `laboratory_distant_tide` | Schur: `Schur correction did not update pair interval functions`. Fallback triple recouple ledger **2514** | **REJECT** local sensitivity in this H=3 domain. Recouple remains the admitted solve. |
| Close-entrant share | `laboratory_encounter` on a compiled pair | Local refuse; recouple three-body ledger **2024** | Negative case kept. Recover through recouple. |
| Affine family bytes per logical identity | 8 members 300 B (37.5 B/id) vs 64 members 301 B (4.70 B/id); fragment/re-merge 864667 ns, logical 17 | Generator bytes, not query/extraction of every identity | **REJECT** “population solved”. Broadcast still walks a materialized range. A `war` name does not change mass, count, stride or radius. |
| Selective cold observe vs full restore | Seal/evict: resident 662 B → 2 B, evicted 2 events; seal 36.8 ms; cold observe 1.4 ms / 1 hit; restore 0.83 ms | Reconstruction is the restore/cold path, not a source-only saving | **KEEP** selective cold observe when the query is admitted. Full restore remains the fallback ledger. |

## I3 exit

Not proven. Kept methods have published domains and failure cases, but none removes enough sequential collocation to scale the same loop to long dynamical durations. Do not launch I4–I6 theater on this evidence.

## Honest leftovers (still binding)

- Broadcast indexing still walks a small materialized range.
- Family does not gravitationally perturb GEM (I4).
- Interval-wide GEM authority is still missing. Do not mint canonical gravity.
- Dense pair-inverse setup still grows with horizon.
