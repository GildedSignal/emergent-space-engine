# Predictions (written before the flights)

Question: cf2a's encounters fleet row (4,510 cores at F = 10⁵ fleets, fleet share 99.77% of the
composed 10⁹ CPU ledger) prices contacts of formation members carried as compact belt bodies
through the pairwise candidate tier. The plane ships another route (`crates/universe/src/fleet.rs`):
a formation as ONE fleet entity — origin a tube like any body, members lattice bodies in a Fermi
frame, contacts one binned batch of the lattice law per epoch, advancement capped by light-delayed
deadlines. Its checker named this route "a shipped alternative route this run does not price at 10⁹".
This run prices it.

The flights (all shipped code + a members-clamp patch, `--bench --unpaced`, this shared Linux box):

- P1 (scaling, the kill test): the fleet class's wall cost is LINEAR in members over m = 48→3,072
  (fit exponent 0.8–1.2). The epoch contact batch is binned (lattice-metal: counting sort into
  spatial buckets, pairs tested only between adjacent cells), not a pairwise tier. KILL of this
  composition if the exponent reaches 1.5.
- P2 (the rate): per-member fleet cost at the Armada's low orbit (7,000 km, period ≈ 5,970 s,
  1,600–3,200 epochs/period ⇒ ≈ 0.27–0.54 member-events/game-s) is 0.1–10 µs per member per
  game-second on this box. If it exceeds 100 µs, the frame route cannot beat the quadratic tier
  even heliocentric, and the row stands.
- P3 (the composition): at heliocentric radius (period a year, same 1,600–3,200 epochs/period ⇒
  ≈ 7.6×10⁻⁵ member-events/game-s), F = 10⁵ fleets × 10⁴ members price at ≤ 10 cores against
  cf2a's 4,510 — the row falls by ≥ 450× and the "fleet-scale finder" requirement never exists.
- P4 (wiring debt, code-verified not flown): many fleets per universe need id ranges per fleet
  (`add_fleet` asserts one fleet), the player's loop must filter fleets by doll (universe.rs:733
  runs every fleet to the player's tick), and a heliocentric frame is doll 0 with the star's mass
  (validity: extent r_p/32 — a tight formation fits at 2 AU; clear of secondaries' shells).

Held-out cases (not tuned on): the second seed (7), and the m-scaling at 6,144 if the box allows.
