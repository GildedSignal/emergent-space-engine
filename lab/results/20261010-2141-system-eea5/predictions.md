# Run 20261010-2141-system-eea5 — predictions (written before the decisive experiment)

## Question

The plane's kick path is `kick -> rebind -> bind -> Rebinding::from_state` (a full
trajectory compile) at **every** kick (crates/universe/src/step.rs:28,381;
bind.rs:226). If so, one number — the rebind-per-kick — is simultaneously:
(i) the engine's dominant compute cost (board focus #1: kicks),
(ii) the destroyer of all sharing (a fresh exact cycle key per kick: the memo
    hits 0% on distinct kicks, lab 5 Oct), so the population-scar layer (B18,
    H_live) grows at one fresh trajectory per kick,
(iii) the encounters re-pay trigger (a rebind is an element change: candidate
    pairs re-set; lab gold components-4643: 92% of per-kick evals are window
    setup).

## Held-out predictions (not tuned on; the code path suggests the structure, the magnitudes are my own Fermi guesses)

- P1 (structure): on the plane's own scene, compiles-per-distinct-kick = 1.0
  (every kick pays a fresh `Rebinding::from_state`); distinct exact ShapeKeys
  ≈ distinct kicks (cross-body sharing ~0).
- P2 (the decisive number): the compile is the majority of the kick resolver's
  time: median compile share ≥ 50% of the per-kick sample (my guess 60–90%).
  The rest (readout, forces, sigma-delta, remainder) is minor.
- P3 (throughput): ship-class items dominate the resolved items (≥ 80%), and
  the fleet's handed-out members are most of the kicks; kicks per game-second
  is set by cadence, so the compile share scales straight into engine cost.
- P4 (memory side): live memory stays bounded during the run (catalogue free
  list + prune): the compile churn is CPU, not RAM. The cost of zero sharing
  is not bytes-growth per body but the loss of the compression ceiling: with a
  fresh key per kick, no two bodies ever share a cycle, so a population's scar
  layer must carry a full per-body trajectory reference (no program reuse).

## What would make the claim wrong

- If compiles-per-kick < 1 on most kicks (some reuse path exists), or the
  compile share is < 30%, the jet's ceiling is small and the kick cost lives
  elsewhere (readout or forces) — the unification still holds structurally but
  the lever ranking changes.
- If P4 fails (memory grows during the run), the story changes from "sharing
  ceiling lost" to "unbounded history": a different, worse bug.

## Experiment

`universe --kick-bench --seconds 10` (pure resolver, per-kick µs, memo shapes)
with one added measurement: a compile-time accumulator around
`Rebinding::from_state`, reported as compile share per kick and
compiles-per-kick. Plus `universe --bench --seconds 10 --unpaced` for the
throughput/memory side (items, µs per item, bytes_per_body, catalogue_live).
Both under 60 s, machine state recorded by the tool.
