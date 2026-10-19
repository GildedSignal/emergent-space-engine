# predictions — 20261018-2312-components-c2bd (the doll's time quantum)

Written after the instrument smoke-ran (k=7, extra=6, 0.2 orbits — cadence/EL plumbing only),
before any swept arm. The component: the shipped `Δs` law (ext.rs) gives every free body
`2^step_log2` kicks per period of its DOLL'S SHORTEST SECONDARY (the root doll: Cinder, 88 d),
whatever its own orbit; the fleet path (fleet.rs) instead sizes steps by the body's own tube
period. Scene: the plane (Cinder μ=2⁻²¹ at 0.39 AU, Home μ=2⁻¹⁸ at 1 AU, Giant μ=2⁻¹⁰ at
5.2 AU, Moon in Home's doll) + ladder belt at 2–3 AU. Floor: H0190's premise (32 kicks/orbit).

- **P1 (cadence, near-certain from the code):** the belt's steady kick interval is
  P_Cinder/2^k (0.69 d at k=7), kicks per own orbit 1,063 (2 AU) → 1,959 (3 AU), ~45× the
  32/orbit floor at k=7; the root doll's far bodies at 13–42 AU ride the same 0.69 d clock
  (8,000–34,000 kicks/orbit). Locals (Home's doll) ride P_moon/2^k.
- **P2 (the belt's behaviour, the held-out bet):** at k=4 (≈130–240 kicks/orbit) the belt's
  element drift vs the k=7 control stays bounded (|Δa|/a does not grow across checkpoints).
  At k=2 (≈66/orbit) I hold 50/50 that it stays bounded; at k=1 (≈33/orbit, H0190's floor) I
  predict a visible walk (|Δa|/a at the last checkpoint ≥ 3× its first-checkpoint value,
  monotone in checkpoint index) or refusals. **Kill criterion for the locality premise:** if
  the belt walks already at k=5 (≈260–490/orbit), the doll-global quantum is load-bearing at
  the belt and the coupling survives — the premise dies. **Kill criterion for the coarsening:**
  k=2 walking kills configurations k ≤ 2 at the belt, never the method (a local quantum sized
  by the dominant source may still hold between).
- **P3 (the near controls, both sides):** coarsening k coarsens every doll's far field at
  once; near-field refinement is Sundman's f′ (U_P + c), not k, so locals near Home are
  protected. The break candidates are the root doll's own far bodies: the 5.2 AU hauler class
  (Giant's tide, perihelion passages of e=0.05) — I predict it walks or refuses by k=3 while
  the belt still holds at k=2; if NOTHING breaks anywhere by k=1, the constant k=7 itself is
  over-paid doll-wide (a bigger kill, reported as such).
- **P4 (cost):** the universe's kick bill scales as 2^(7−k) (same bill per kick); the belt's
  share is its population share. The ladder's break #1 (10⁷ bodies ≈ 1.4 cores at k=7) then
  falls as 2^(7−k) for the belt's share.

Held-out axes I do NOT fly (domain): the player's thrust (C1's clock path), zoom/view,
encounters' hit exactness (law::hit reads the ramped state — coarser steps lengthen the ramp;
flagged as unmeasured), and seeds ≠ 1.
