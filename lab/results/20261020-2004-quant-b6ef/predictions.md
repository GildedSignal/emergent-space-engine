# Predictions (written before the decisive runs)

Instrument: `ES_SCAFFOLD_AUDIT` — print-only relaxed-atomic stage timers + counters (one settled
`LazyLock` load when off), buckets disjoint by construction (the coarser-word retry's inner stages
are suppressed while it runs). Scenes: the standing belt `nladder 30000 coast 60 1800` (7fd3's), a
N=10⁴ arm for N-flatness, and the plane cross-cell `xtask universe --kick-bench --seed 1 --rtf 100
--seconds 30`. This box's steal is bimodal (~±35%, 077c): walls are orders-of-magnitude evidence;
shares are the claim.

- **P1 (the τ-pair is the belt's biggest scaffolding term).** `orbit_state(t)` + `orbit_state(event_time)`
  together ≥ 5 µs/rebind and ≥ 35% of the rebind wall outside `from_state` on the belt.
  *Kill:* if the pair is < 35% of the outside-`from_state` bill, "the τ reads are the belt's next
  cut" is wrong and the bill names the real owner instead.
- **P2 (the event-time τ read is a pure recompute).** `orbit_state(old.event_time)` re-derives a
  value the old bind already computed and discarded (`Bound.orbit`): it costs ≥ 2 µs/call on the
  belt — deletable by caching one Scalar per Binding, no law change.
- **P3 (the retry is a plane term, not a belt term).** The coarser-word retry fires on < 5% of belt
  `bind_surface` calls and < 5% of its wall; on the kick-bench it fires on ≥ 20% of calls (7055's
  33% of hand-out compiles was a plane number).
- **P4 (the kick's readout and the τ read are the same decode).** `kick`'s `readout(t)` and the
  rebind's `orbit_state(t)` decode the same entry/tube/units at the same tick: per-call walls agree
  within 30%, and the pair is ~2 redundant decodes per kick that one fused decode (returning the
  state and the proper time) deletes.
- **P5 (plan_terminal is not hiding in the rebind on the belt).** TERM < 10% of the belt rebind
  wall. If TERM > 25%, 7fd3's "rebind" bucket was carrying crash-search work and the scaffolding
  story changes (I report it).
- **P6 (identity).** Audit on vs off: kick-bench `digest` and `replay_digest` identical; nladder's
  deterministic counters (kicks, events, refusals, dead) identical. Print-only beside the same
  paths — nothing the engine reads passes through the instrument.

What would make the run void: any digest or counter moving with the audit on (instrument not
print-only), or a load-hit belt wall (first-execution numbers kept but disclosed, min-of-two used
for the headline).
