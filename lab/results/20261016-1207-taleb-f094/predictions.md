# Predictions (written before the scaling runs)

Exploratory (already run, N=0, 48 members, seed 1, rtf 100, 12 ms): the worst frame of the
opening (f62, 11.86 ms, lag 1.448 game-s) is 26 `opens` + 26 `leavers`, all cost in the fleet
class (11.7 ms); teeth f9-f11 (2+7 leavers), tail f63 (5). Each hand-out = `resolve_handout`
(bind_surface + insert + replan ≈ 450 µs) — b29a's sticky promotion, paid en masse.

Held-out cases (not tuned on):

1. **Members scaling (the player's own fleet, served page cap 400):** the leaver count and
   total opening hand-out work scale ∝ members. At 200 members ≈ 2× the 48-member leaver
   count (~70), at 400 ≈ 4× (~140); the frame stays budget-capped (≤ 12 ms + one item), the
   presented lag grows roughly ∝ members (≥ 5 game-s at 400). Unbudgeted (Budget::events
   max), the single exodus frame at 400 members lands 60-150 ms; at 1,600 members 0.4-1.5 s
   (3cfc's class).
2. **Belt N-flatness:** at belt N ∈ {10⁴, 10⁵} (same 48-member fleet), frames 0-90 show the
   same leaver counts (±2, a different RNG stream is not used — identical, since the fleet is
   independent of `extra`), the same f62-class worst frame (ms within noise of the shared
   box), and the exodus remains the worst frame of 0-90 at both N. The belt's first-kick wave
   (~750 game-s) is outside the 90-frame window (150 game-s) at rtf 100.
3. **Mechanism:** at the worst frame, opens = leavers exactly, and the per-leaver cost
   (fleet-class µs ÷ leavers) is 300-600 µs at every members and N. If the worst frame at any
   N is *not* the hand-out wave (opens ≠ leavers, or leavers grow with belt N), the mechanism
   claim is wrong.
4. **Boundedness:** leavers stop after the opening (0 in frames 100-400 at 48 members); no
   second exodus at the same scale. If a later equal-size wave exists, "one-time opening" is
   wrong and the term is periodic.
