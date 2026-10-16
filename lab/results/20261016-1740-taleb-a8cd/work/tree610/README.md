# Emergent Space

A deterministic engine for a relativistic, emergent, faction-based 2D space game. It aims to run billions of ships, stars, planets and black holes, exactly and canonically, on one Apple M1. The goal is general relativity.

**What it computes.** It computes the universe's events: the points in spacetime where a prediction breaks, and what happens there.
- Everything between events is a formula with a certificate saying how long the formula stays exact.
- Compute follows surprise.
- The player is the only unpredictable input, and their influence travels at most at c.

**Where it stands.** The law is exact integer special relativity with contacts (`es-lattice-relativistic-v1`). Five execution modes give bit-identical results:
- the chronon reference;
- the event core;
- Metal GPU lockstep;
- the hybrid;
- regions under the least-slack allocator.

An independent GR oracle exists. Gravity is the next build. See [the handoff](docs/HANDOFF.md).

## Layout

- `crates/lattice`: the canonical law. Integer lattice, exact predicates, relativistic bounce, CPU chronon reference, digests.
- `crates/lattice-event`: the event core. Density-sized cells and a calendar.
- `crates/lattice-metal`: chronon mode on the Metal GPU.
- `crates/allocator`: regions, light-cone finality, least-slack scheduling, performance and efficiency cores.
- `xtask`: the scale ladder, the GR oracle, the independent references and the journal tools.
- `docs/`: the [handoff](docs/HANDOFF.md), the append-only [history](docs/HISTORY.md), design notes and the [original references](docs/reference/README.md).
- `artifacts/evidence/`: frozen evidence cited by the journal.

## Commands

```sh
cargo xtask history list            # the journal
cargo xtask history check
cargo run --release -p xtask -- test        # history check + all tests
cargo run --release -p xtask -- gr-oracle   # independent GR benchmark
cargo run --release -p xtask -- ladder7 artifacts/runs/ladder7 --modes=event,metal
```

Rust 1.90.0, two build jobs (M1, 8 GB). Tests and probes stay under one minute each.

The old engine line (inertial causal compiler, GEM-v0 gravity, native observatory) is archived outside the repo in `~/Research/emergent-space-archive`. Its history stays in git.
