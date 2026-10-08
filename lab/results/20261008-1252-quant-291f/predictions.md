# Predictions — the player's decision as a market order (written before any run)

Question: when the player issues one decision (hold a level-15 burn, release it 10 s later),
what is the compute wake — its size, its owners, its spread over frames — against a coasting
twin, at rtf 100 with the plane's 5 ms wall engine budget per frame?

Frozen protocol: `wake.rs` (crates/universe/examples/wake.rs), panel seeds 1, 2, 3, 30 s
(1800 frames) per arm, burn from frame 600, release at frame 1200. ABBA repeat on seed 2.
Negative control: a word-0 (keys 0, level 0) decision at frame 600. Positive control: the
burn twin's player digest must differ from the coast twin's, with zero refusals, else VOID.

Frozen kill rule (the claim under test is plane.md §7: "Nothing takes an unbounded
synchronous claim on the frame"):
- KILL the bounded-wake claim if in ANY panel seed a frame inside the wake window
  (600..1800) has engine wall time > 10x the coast twin's p99.9 engine time for that seed.
- HOLD if the wake's worst frame stays <= 3x the coast p99.9. Between 3x and 10x: silver,
  the slack skin must own the wake explicitly.

Predictions on held-out cases (no tuning before the panel):

- P1 (size). The wake is O(1) bodies: total extra events resolved in the burn arm minus the
  coast arm over the whole run stays under 5,000 (the player's own recompiles, its handoff
  chain, and neighbourhood/encounter checks; nothing cascades into other bodies, because an
  event writes only its own body). If the wake exceeds ~50,000 events, the wildcard is not
  O(1) and P5 of PRINCIPLES is wrong as implemented.
- P2 (tail). The burn arm's p99.9 frame engine time is within 3x of the coast arm's on every
  panel seed (the flush happens at the player's own kicks inside the wall budget; the
  horizon, not the frame, absorbs the burst). No KILL expected; the interesting number is
  the worst single frame and what owned it.
- P3 (owners). The wake's cost is owned by the player's tube recompiles and any doll
  handoff (opens/handoffs/boundaries stats), not by kicks of other bodies and not by the
  fleet (encounters stay ~0: the burn is along the orbit, away from the fleet's Fermi
  frame; the player starts 20 km ahead of it and leaves).
- P4 (spread). After the release at frame 1200 the per-frame event delta returns to ~0
  within 60 frames (the wake is bounded in time, not a new steady-state cost).
- P5 (budget). Overflow frames (mandatory work not fitting the 5 ms budget) are 0 in both
  arms on all seeds at rtf 100 (the plane's own claim: 100x with no hitch in CPU time). If
  the coast arm already overflows, the instrument's budget is mis-sized for this box and the
  run is VOID for P2/P5, not a physics result.
- P6 (negative control). The word-0 decision's wake is exactly 1 event (the decision
  itself) and ~0 extra engine time. If it wakes anything more, the instrument measures
  bookkeeping, and the whole run is VOID.

Machine-state note: shared 8-vCPU x86, loadavg recorded per run; orders of magnitude only,
per the lab rules. The M1 numbers are the integrator's to take.
