# Predictions (written before the decisive experiment; no bench run has been made yet)

Instrument: `./target/release/xtask universe --bench --seed S --seconds T --unpaced --threads K [--members N]`
on this Linux box (8 vCPU, shared). Digest at the canonical cut, `/usr/bin/time -v` peak RSS, the report's
`frame_cpu_ms` and `engine_cost_by_kind`. Orders of magnitude only (cloud timings are Linux/x86).

## P-A — process-restart determinism (the ruin state "silent nondeterminism")
The in-repo tests all run inside one process; the bench binary is the only cross-process path.
- Predict: two separate processes, same seed/config, give the **same** `digest` and `cut_tick`; ditto `--threads 4` vs `--threads 1`.
- Control: seed 4 vs seed 3 must differ (the tests say the digest is sensitive; if it does not differ the instrument is broken).
- Why I expect pass: no `HashMap`/`HashSet`/`RandomState` in `crates/universe` or `crates/engine` (audited by grep);
  `resolve_wave` applies updates in key order. Risk I have not excluded: anything seeded from the OS or wall clock in the
  bench session (`session.rs`) leaking into canonical state.
- If it fails: reachable ruin state, the premise "independent of ... schedule and hardware" is wrong today.

## P-B — convexity in fleet size at the scene's own scaling (constant density)
`scenes::battle` spaces bodies on a grid of side ~sqrt(n)*5q, so doubling members doubles the *volume*, not the density.
- P-B1 (cost): frame CPU grows with exponent **1.0 +/- 0.3** in members (48 -> 1536). Per-body neighbours constant
  means contacts per body constant. Held-out risk: the event core's velocity classes or queue grow superlinearly.
- P-B2 (memory): peak RSS per member flat within ~3x across the same range; reported `bytes_per_body` roughly constant
  (a Vec-doubling transient is allowed). Held-out risk: the hand-out materialises all members at once at dissolution.
- P-B3 (seed spread, fat tails from configuration alone): at members = 384, total fleet cost across 3 seeds varies by
  **< 2x**. If > 3x, the allocator must be sized for the worst seed, not the mean.

## P-C — fixed-volume density growth (the black-swan cell; only if time permits)
A custom world at the extent of members = 48 while n grows (density proportional to n): the one-10^6-ship-fleet-in-one-cell case.
- Predict: per-frame cost exponent in n **>= 1.8** (SAP-style candidate pairs ~ n^2 at fixed volume), i.e. the shipped
  battle core is convex in density even though it is linear at its own scaling. This quantifies what the allocator and
  the doll's slicing must absorb, and is the in-engine twin of the board's `q-candidate-degree` question (which answered
  the fixed-density case).

## Kill criteria
- P-A differing digests across processes with one seed/config = the run's headline (ruin found).
- P-B1 exponent > 1.4 at constant density kills "constant density is cheap in the shipped core".
- P-B2 RSS/body growing > 3x kills "memory is flat in members".
- A run that cannot finish in 60 s or approaches 1.5 GB RSS is stopped, not extended.
