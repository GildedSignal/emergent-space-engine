# Predictions — second author on 20261012-0753-quant-dafc

The checker's named gold experiment: bisect the canonical-digest flip (`6ce6…` ↔
`56f4…` at one command, one seed, one cut, `threads=1`), then re-derive the
frontier on ≥ 3 seeds with the machine state pinned. This file is written before
any run of mine (the shipped binary is built; no bench cell has run yet).

## The competing hypotheses for the flip

The digest (universe.rs `digest()`) hashes, per body: physics (doll, event_time,
tube, trajectory key, turn, residual, carry, units, proper, the ext register),
bookkeeping (`step`, `interval`, `anchor`, the `plan` list, `thrust.since`,
`events`, `refusals`, `fault`), plus dolls, fleets, inputs, handouts and
`enc_digest`. The wall enters only through `frame_to`'s `want` (per-frame tick
target from wall `dt`) and `Budget::wall`'s `Instant` deadline.

- **H-bookkeeping (my prior: 0.65).** The canonical *state* is
  schedule-independent, but the digest mixes in schedule-dependent fields —
  most likely the per-body `events`/`refusals` counters (items resolved *during
  frames* vs during the final `settle` differ with pacing jitter), or
  `prune()`-induced faults (prune runs every 64 *frames* at a `now`-dependent
  depth, so pacing jitter changes what history is forgotten when; a needed read
  then refuses or recomputes). Predicts: physics field-group hashes identical
  across attractors, bookkeeping group differs.
- **H-physics (my prior: 0.30).** The schedule leaks into canonical state (a
  plan item's tick, an ext-register flush, or an encounter hash computed on a
  different window). Predicts: physics fields differ at the cut; the engine's
  own contract ("delays work and never moves a decision") is broken — a bigger
  finding than the prior run's whole frontier.
- **H-cut (my prior: 0.05).** The two attractors are different cuts or input
  logs (the checker says both were `406050894` with identical inputs; I will
  verify, not assume).

## Predictions (all falsifiable before I look at any field-level data)

- **P1.** Unpaced runs (`--unpaced`, `wall_dt` fixed at 1/60 → deterministic
  `want` sequence) all give one digest, across ≥ 4 repeats.
- **P2.** Paced runs at `--rtf 100 --seconds 20` (the checker's cell) give ≥ 2
  distinct digests within ≤ 6 repeats on this box, whatever its load.
- **P3.** Field-group hashes at the cut (physics vs bookkeeping vs enc/fleet)
  will localise the flip to one group; I predict the bookkeeping group (H-bookkeeping).
- **P4.** If P3 lands on bookkeeping: excluding the offending field(s) from the
  digest (a probe patch, disclosed, never shipped) collapses the attractors to
  one digest — i.e. the *engine* is schedule-independent and the *digest
  definition* was the bug (one-line fix: hash canonical state only).
- **P5.** If P3 lands on physics: the differing field will be in one body class
  first (ships on the root doll with the ext register, or the player), and the
  first divergent item tick will sit inside a frame whose target straddled a
  decision tick — the wall-derived target moving a canonical decision's
  *effect*, not its tick.
- **P6.** Seeds 2 and 3 at the checker's cell (paced) also flip or hold as a
  function of pacing jitter, not of seed: seed changes the digest value, not
  the instability (the instability is a property of the wall→target path, not
  of the scene).

## What would make each hypothesis wrong

- H-bookkeeping dies if the physics group differs at the cut in any pair of
  attractor runs. H-physics dies if physics groups match in every pair. H-cut
  dies if cuts/inputs/logs are byte-identical (they print in every report).

## Kill criterion for the run

If P1 fails (unpaced also flips), the wall is not the only leak and the bisect
must widen (threads, HashMap iteration order, address-dependent seeding) —
report which, with evidence, even if the 90 minutes end mid-bisect.
