# Coupled-compiler prompt completion evidence (2026-09-15, H0124)

Derived from `/private/tmp/emergent-g2-law/orchestration/prompts/continue-coupled-spacetime-compiler.md` in this turn, not from the H0122 markdown table. Inspected `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`, dirty overlay) and journal H0098–H0123. Marks: **proves** / **contradicts** / **incomplete** / **too weak** / **missing** / **prompt remainder** / **prompt skip**. A previous markdown audit is not this evidence.

**`in_scope_complete: yes`** for the prompt’s assigned laboratory exits. `production_law` is **null**. Default `Engine::advance` stays `es-inertial-causal-v1`. That null/inertial pair is success, not a hole.

Out of scope (not remaining in-scope failures): production gravity, Einstein two-body, galaxy, billion ships, manufactured 99.9% reuse (prompt: hypothesis, not a target to manufacture), native wgpu GUI (prompt: avoid wgpu until relevant; `--no-default-features --lib` host), architecture dumps, compact decode-only (H0106 sidecar remainder), pair-exterior new-entrant share (honest refuse at \(1.5193527764310737\)).

## Commands run this turn

Worktree `/private/tmp/emergent-coupled-response`. Disk ~18 GiB free; swap ~3.24 / 4.0 GiB used; RAM 8 GiB.

```
CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target
CARGO_BUILD_JOBS=1
CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never
cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1 --nocapture
# 47 passed; 0 failed; 8 filtered out
cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1 --nocapture
# 10 passed; wgpu not compiled
```

H0123 pins still hold on this HEAD (nocapture of `recoupled_three_body_reuses_and_repairs_certified_interval_functions`):

- encounter ratio `1.5193527764310737`
- leftover reuse/repair `0` at 16 / 128 / open-tail / lookback
- source ops `1188 vs 1675` and `1126 vs 1722`
- suffix `source_evolution` `11` / `24`
- copies `81` / `70`

Extra-ray-only fast-ships and cell-name-only three-bodies still fail: `overlay_api` / `required_query_consumers` / genesis ids `[0,1,99]` remain asserted.

## Sequence 1 — executable model and comparison contract

| Prompt requirement | What would prove it | Primary evidence this turn | Mark |
|---|---|---|---|
| Equations, units, order, IC/incoming/self, shared queries, finite semantics; explicit law version | Law file plus tests that refuse a different id | `docs/laws/linearized-retarded-gem-response-v0.md`; id `es-linearized-retarded-gem-response-v0`; `G=1`, `c=8`; `static_first_visibility_matches_derivation`; `truncated_gem_moving_eval_is_not_this_law` | **proves** |
| Ordinary evolving ICs; lattice must not make motion unsupported after first update | Moving-source `acceleration_at` returns a value | `truncated_gem_moving_eval_is_not_this_law`; `kick_changes_b_only_after_cone_then_feeds_back_to_a` | **proves** |
| Weak-field slice first; do not claim galaxies/compact objects solved | Unsupported cards + law “route not a claim” | gallery `solar_galaxy_black_hole_are_unsupported`; law §Supported regime | **proves** |
| Distinguish model / numerical / canonical error | Named bands vs leftover vs refuse | leftover-0 is this comparison (assert_eq 0, not 1e-7); gallery `BANDS_STATUS = "UNCONFIRMED"`; encounter refuse kept | **proves** as named |

## Sequence 2 — slow reference and compiled interval

| Prompt requirement | What would prove it | Primary evidence this turn | Mark |
|---|---|---|---|
| Both evolve all masses from same IC/interventions | Compile and `Reference::evolve_to` on the same genesis | `compile_is_not_evolve_then_copy` | **proves** |
| Reference never restarts from candidate state | Poison compiled worldtubes; genesis reference unchanged | `independent_reference_never_uses_candidate_state`; enclosure `independent_reference_is_from_genesis` | **proves** |
| Independent residual so shared mistakes cannot pass on parity alone | Checks that are not “compile equals itself” | `enclosure_ignores_candidate_residual`; `delayed_newton_is_not_gem`; `authored_worldtubes_fail_residual_certificate`; `successive_iterates_looking_similar_cannot_certify`; Euler/collocation split. Picard still calls shared `field_acceleration` (H0108); not a second GEM kernel | **proves**; **prompt remainder** Picard helper |
| Compile jointly with domain, incoming, error, outgoing history, repair | Stored fields + repair API | `SourceResponse.{domain,incoming,residual,interval_functions,worldtubes}`; `repair_recoupled_interval_functions` | **proves** |
| Not a renamed tick loop or trajectory table | Collocation ≠ Euler polyline | `compile_is_not_evolve_then_copy` | **proves** |

## Sequence 3 — one complete physical loop

| Prompt requirement | What would prove it | Primary evidence this turn | Mark |
|---|---|---|---|
| Two moving sources alter one another; A→B only after cone; B then A | Pre/post cone GEM-a vs control | `kick_changes_b_only_after_cone_then_feeds_back_to_a` | **proves** |
| Held-out ships/rays/clocks/contact return values | `Ok` values, not `UnsupportedDomain` | `held_out_ship_ray_clock_contact_are_supported` (`tau>0`, `ray.t>1.1`, `0<clock≤1`, `cd>0`); recoupled compiled queries; `fast_ships_overlay_returns_compiled_ship_ray_clock` | **proves** |
| Ray after motion; source change in flight; direct vs subdivided | Same ray/source across splice | `ray_in_flight_direct_matches_subdivided` | **proves** |
| Authored futures cannot pass | Residual / enclosure reject | `authored_worldtubes_fail_residual_certificate`; `authored_worldtubes_reject_enclosure_not_the_true_solution` | **proves** |
| Compact family + extraction | Distinct masses change Φ | `family_extraction_changes_field` (`laboratory_family`) | **proves** |
| Quiet vs encounter that requires refinement | Encounter share refuses | `encounter_differs_from_quiet`; `compiled_pair_exterior_does_not_cover_massive_encounter`; share refuse pinned `1.5193527764310737` | **proves** |

## Sequence 4 — interval reuse and repair of equivalent completed histories

| Prompt requirement | What would prove it | Primary evidence this turn | Mark |
|---|---|---|---|
| Increase query count and quiet horizon independently | Two knobs, no hardcoded `f=1` | `query_count_and_horizon_are_independent_and_not_hardcoded_f` | **proves** |
| New entrants reuse source/transport work | Share of a compiled pair with a new mass, leftover vs independent | `compiled_pair_exterior_does_not_cover_massive_encounter`; recouple is recovery (`recouple_compiles_encounter_and_keeps_share_refuse`), not pair-exterior reuse. Prompt allows refuse; linearized GEM cannot certify that share at 1.519 | **prompt remainder** / honest refuse |
| Regular evolution does not replay every reference step | Prefix copy of certified interval functions vs independent kicked same-IC | `recoupled_three_body_reuses_and_repairs_certified_interval_functions`: copies 81, **1188 vs 1675** (\(\approx 0.291\)). Extra-ray tests fail if labelled equivalent completed source histories | **proves** as prefix copy; **prompt skip** 99.9% |
| Localized intervention vs full recompute | Repair leftover vs independent same-IC; suffix ops in the denominator | leftover **0**; **1126 vs 1722**; suffix `source_evolution` 24; `Charge.repair=1`; `Charge.total` > source ops; copies 70 ≠ denominator | **proves** |
| Persistent perturbation defeats overlong certificate | Repeated kicks refuse stale cert | `overlong_independence_certificate_is_defeated_by_repeated_kicks` | **proves** |
| Refinement settles; queries do not alter truth | Failed `q≥1` rejects certificate; observer charge does not mutate sources | `failed_contraction_does_not_silently_certify`; `refinement_overlay_records_independent_enclosure_not_ka`; `source_ops_unchanged` on extra-ray overlay | **proves** |
| Navigation reuses transport; fail closed outside domain | Nav tests | `navigation_reuses_transport_and_recovers_forward_v0`; `navigation_fails_closed_outside_explicit_domain` | **proves** |
| Define reuse-fraction denominator; equivalent completed histories through horizon including recovery | Named denom + compile-through-horizon ops | `source_ops = source_evolution + retarded_solves` of independent kicked compile; extra-ray `extra_ray_n_times_s_is_not_equivalent_completed_source_histories` and reuse-API sibling | **proves** as named |
| Compact as compile storage / decode-only | Decode reconstructs worldtubes from compact | `worldtubes_stay_named_remainder_not_decode_only`; H0106 sidecar. Do not polyline | **prompt remainder** |

## Sequence 5 — six-card visual instrument

| Prompt requirement | What would prove it | Primary evidence this turn | Mark |
|---|---|---|---|
| Six cards, look-for, charged overlays, unsupported marked | Host actually calls this slice per card | `frozen_catalog_has_six_cards_and_no_seventh_physics`; `gem_cards_show_look_for_and_are_not_inertial_relabelled`; solar/galaxy/BH `Unsupported`; fast-ships `overlay_api=complete_required_queries_compiled` + `required_query_consumers>0`; three-bodies `overlay_api=recouple_compiled_pair` + genesis `[0,1,99]`; fleet A→B→A `compile_source_response`; `unsupported_cards_refuse_inertial_paint_as_this_law` | **proves** |
| Native GUI | Clicked wgpu window | Prompt: avoid wgpu until relevant; `native_gui_compiled: false`; `--no-default-features --lib` | **prompt skip** |
| Do not equate inertial overlay with this law | Default engine law inertial; GEM host id | `run_record_keeps_production_law_null_and_engine_inertial`; `charged_reuse_overlay_does_not_re_evolve_sources` | **proves** |

## Acceptance

| Prompt requirement | What would prove it | Primary evidence this turn | Mark |
|---|---|---|---|
| Workload declared before results | Dated declaration, not post-hoc `f=1` | `docs/laws/recoupled-reuse-workload-declaration-20260914.md` on the worktree; test cites it | **proves** |
| Unconfirmed bands stay unconfirmed | Gallery does not invent a band after seeing leftover-0 | `BANDS_STATUS = "UNCONFIRMED"` in `run_record_keeps_production_law_null_and_engine_inertial` | **proves** |
| Required queries returning unsupported fail the capability | Laboratory unwraps values | `held_out_ship_ray_clock_contact_are_supported`; compact four-kick decode refuse is the sidecar remainder, not a missing GEM query | **proves** |
| Charge buckets used through horizon | init, source_evolution, retarded_solves, field, coefficient, factorization, validation, consumers, repair, fallback, history, reconstruction, verification | `Charge` in `coupled_source_response.rs`; suffix 11/24 pinned; `total > source_ops` | **proves** |
| Op counts, wall time, cold/warm, memory, hashes, workload | Recorded Charge + wall_ns + hashes | `ChargedReport.wall_ns_*` and `independent_compile_wall_ns` (N=3); `worktree_head` is baseline `254ba1f…`; no RSS sample | **proves** ops/wall/workload; **prompt remainder** bookkeeping RSS / dirty-overlay hash |
| Measured break-even / 99.9% | Hypothesis, not a manufactured target | Prefix-copy \(1-1188/1675\approx 0.291\); cheaper than one independent kicked compile on this fixture. 99.9% not a gate | **prompt skip** as manufactured target; measured fraction reported |
| M1/8GB; do not weaken after seeing results | JOBS=1; 1.519 kept; leftover gates not loosened | This turn: JOBS=1, CACHE=never, `--offline --locked`, `--test-threads=1`; pin `1.5193527764310737`; leftover `assert_eq!(…, 0.0)` | **proves** |
| Keep production selection separate; do not replace `Engine::advance` | `production_law` null; `LAW_ID = es-inertial-causal-v1` | `run_record_keeps_production_law_null_and_engine_inertial`; engine `crates/engine/src/lib.rs` `LAW_ID` | **proves** (success, not a hole) |

## H0098 carry-forward

| Prompt requirement | Primary evidence this turn | Mark |
|---|---|---|
| Reproduce discriminating relational failures, then fix only what this experiment needs | `h0098_zero_force_does_not_move`; `truncated_gem_moving_eval_is_not_this_law` | **proves** |
| Do not extend truncated-GEM genesis specials | same tests; this law id is distinct | **proves** |

## Assigned exits vs game destination

Prompt assigned exits for a **bounded weak-field laboratory slice** (model, independent Euler reference, A→B→A loop, held-out queries, prefix reuse/repair of equivalent completed histories, six-card library host with unsupported marked, Charge through-horizon, 1.519 refuse kept) **prove** on current HEAD.

Prompt-allowed remainders/skips named above: compact sidecar / decode-only; pair-exterior new-entrant share refused at 1.519; Picard shares `field_acceleration`; 99.9% not manufactured; native GUI skipped; RSS / dirty-overlay hash bookkeeping.

99.9% reuse, production gravity, and wgpu are **not** remaining in-scope failures. `production_law` staying null is **success**.
