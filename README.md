# Emergent Space

A native astronomical observatory over a deterministic, generator-native causal laboratory.

The repository implements exact rational worldlines, swept contact certificates, finite-speed messages, simultaneous impulse batches, indexed ship families, sparse interventions, causal observations, bounded response caches, and atomic replayable checkpoints. The native Rust observatory uses **wgpu / Metal**, with pale-blue charts, ivory panels, fine ink geometry and quiet astronomical notation.

**This is not a qualified full gravity engine.** The physical-law laboratory evaluates two executable candidates and retains their failed gates. The billion-population / ten-billion-year tests measure the inertial compression mechanism. They do not establish integrated gravitational scale.

## Continue development

Start with [the agent handoff](docs/HANDOFF.md). [The development history](docs/HISTORY.md) records what changed and why, and [the update procedure](docs/history-workflow.md) keeps it current. The original approved plan, conversation, research and aesthetic references are preserved in [the reference index](docs/reference/README.md).

```sh
cargo xtask history list
cargo xtask history search "compression"
cargo xtask history check
```

## Run

The checked-in toolchain is Rust 1.90.0. Build concurrency is limited to two jobs for the M1/8 GB target.

```sh
cargo observatory
```

Drag to pan, scroll to zoom, click a symbol to inspect, and press Space to play/pause. Switch between the scientific diagnostic chart and the delayed sensor chart. Use **Set course** to apply a controlled heading, send signals to selected identities, or save/restore through Archive. Enter a ship identity from `10000` through `1000009999` to decode a member of the billion-ship transit population. Initial local objects have identities `1`–`5`.

The observatory displays the laboratory law and actual committed time. Long work runs on a separate worker and reports progress. Chart symbols and radii are schematic. The initial finite-radius celestial symbol is an occluder, not a secretly enabled gravitational body.

To create a local macOS application bundle, run `./scripts/package-macos.sh`. The result is `artifacts/Emergent Space.app`. This is a local development build.

## Verify and measure

```sh
cargo xtask test
cargo xtask reference
cargo run --release -p xtask -- qualify
cargo xtask verify artifacts/runs/latest/billion-ships.checkpoint
```

`qualify` writes provenance, test output, event evidence, benchmarks, Fermi worksheets and law results under `artifacts/runs/latest`. It intentionally exits **2** when the physical-law gate fails. Exit 2 must not be interpreted as a successful full-engine release. `bench`, `law-lab`, and `fermi` can also run separately.

```sh
cargo run --release -p emergent-observatory -- --screenshot artifacts/screenshots/observatory.png --frames 120
```

## Structure

| Component | Responsibility |
|---|---|
| `crates/engine` | Exact laboratory law, events, indexed populations, responses, persistence |
| `crates/law-lab` | Independent, versioned stationary gravity/metric experiments and frozen rejection gates |
| `crates/observatory` | Native presentation with a worker-owned engine and snapshot/command bridge |
| `xtask` | Reproducible tests, mechanism benchmarks, provenance and gate reports |
| `scenarios` | Frozen numerical/workload definitions |
| `orchestration/tasks.json` | Dependency graph, module ownership and acceptance packets |

Read `docs/architecture.md`, `docs/fermi.md`, `docs/laws/inertial-causal-v1.md`, and `docs/law-lab.md` for contracts and current limitations. The reference artwork informs materials, color, typography and spatial composition; its panel layout, factions and missions are not requirements.
