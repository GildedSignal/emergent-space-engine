# I0 selection — `codex/full-engine-integration`

Clean worktree: `/private/tmp/emergent-full-engine-integration`
Branch: `codex/full-engine-integration` from `254ba1f718771ec1d0a25bf59d0d555f7e57993e`.
Parent journal: `/private/tmp/emergent-g2-law`.
No whole-branch merge. Original packet worktrees were not deleted.
`production_law` stays null. Default `Engine::advance` stays `es-inertial-causal-v1`.

## Base

| Item | Value |
|---|---|
| Recoverable input | git object `254ba1f718771ec1d0a25bf59d0d555f7e57993e` |
| Inertial overlay | `/private/tmp/emergent-compiler-impl` (`codex/compiler-packets`) |
| Coupled compiler | `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response`) |
| Packet 6 reference | `/private/tmp/emergent-packet6-history` (types extracted; runtime not merged) |
| Packet 5 old-law | `/private/tmp/emergent-packet5-engine` reviewed, not merged |

## Selected

| Path | Overlay | Action | Why |
|---|---|---|---|
| Packet 0 inertial engine files | compiler-impl | copied | Exact geometry, WorkBudget runtime, families, causal tests |
| `crates/law-lab/src/coupled_*.rs` | coupled-response | copied then I0-fixed | Moving-source interval functions, repair, enclosure, compact sidecar |
| `crates/law-lab/src/lib.rs` | coupled-response | copied | Additive coupled modules; frozen G2 laboratory unchanged |
| Observatory gallery host | coupled-response | copied | `--no-default-features` H0124 library host |
| `crates/engine/src/policy.rs` | packet6, narrowed | created | Received-knowledge IR without Engine broadcast wiring |
| `crates/engine/src/archive.rs` | packet6, narrowed | created | Chunk/remainder schema **without** `truncated_admission` |

## Explicitly not selected

- Whole packet branches (`glm/packet*`, G2 compiled-spacetime under `crates/law-lab`).
- Packet 5 `truncated_gem.rs`, `TRUNCATED_COUPLED_LAW_ID` on `Engine::advance`, remainder `truncated_admission`.
- Packet 6 `runtime.rs` Broadcast delivery and `storage.rs` `Engine::seal_archive` (I1 connects these).
- Frozen `1dac658` evidence. Native wgpu path.

## Old-law fields reviewed (Packet 5→6)

Refused: `CanonicalState.truncated_admission`, `Engine.truncated`, envelope dual-law `TRUNCATED_COUPLED_LAW_ID`, `HistoryRemainder.truncated_admission`.
Kept as isolated types: `Broadcast`, `BroadcastReception`, `ReceivedKnowledge`, `PolicyProgram`, `ArchiveManifest`, `HistoryRemainder` (inertial law only).
