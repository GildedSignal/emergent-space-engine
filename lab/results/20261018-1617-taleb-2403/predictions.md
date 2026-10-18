# Predictions (written before the decisive runs)

Question: is the held-scan mint rate λ (arrivals per game-second) a law constant (the record's
0.0526 coast number, K-flat) or the player's pacing (the wildcard)? Every λ in the record was
measured on a coasting player; the census (acf2) names the trigger as the player's own event
clock t (521/573) — which a burn densifies (the memo finding: during burns the player re-times
a pending kick essentially every frame).

Arms: `xtask universe --bench` at levels 0/8/12, seed 1 + held-out seed 2, members 48 and 400
(30 s wall, rtf 100 → 3,000 game-s); `nladder 10000 coast|burn` (20 s wall) for scale.
Instrument: ES_MINT print-only probe (digest-identical on/off, checked on the 5 s smoke arm).

- P1 (control): outside burn windows, λ ≈ 0.05–0.15 /game-s in every arm (the record's law).
- P2: inside burn windows at L8, λ ≥ 3× the same flight's coast-phase λ.
- P3: λ_burn rises with throttle level (L12 > L8 > L0).
- P4: seed 2 within ~30% of seed 1 at L8 (game-lawful arrivals, b8e2's seed-independence
  transfers to the burn phase).
- P5: members 400 opens the head-count channel (cls_len > 0 once deaths start) but λ stays
  player-paced (within ~50% of the 48-member arm).
- P6: at ladder scale (nladder 10⁴) the burn arm's held max exceeds 20 where coast's is ~0–3,
  and its peak footprint grows ≥ 100 MB over coast in 20 s of wall.

Kill criterion for the claim ("λ is the player's pacing"): if λ_burn/λ_coast < 2 in every arm,
the arrival rate is burn-invariant and the coast number stands as the fence-sizing rate — also a
result (the fence is safe as sized).
