# Predictions (written before the decisive run)

Question: is H_live — live distinguishing bits per game-second — bounded in steady play, and
does its per-body average stay under 64 bits (the 8 GB / 10⁹ line)?

## Fermi estimate first

Scene (the plane, seed 1, 48 fleet members): star + 4 planets + moon + player + fleet ≈ 60–150
live bodies. Belt bodies on compiled tubes carry 0 live bits (the generator re-derives them);
only kicked bodies carry a residual (4 × i128 in `Residual`, but in-use magnitude is what the
fit discarded: sub-quantum leftovers).

- bits(residual) ≈ 4 integers × (10–40 magnitude bits) ≈ 40–160 bits per kicked body.
- Rebinding reabsorbs: the plane recompiles an orbit on ~99% of kicks (taste log, 5 October),
  so a residual lives roughly one event. Steady-state live residual ≈ one event's worth per
  kicked body, not an accumulation.
- Kicks: 32/orbit/body unaveraged, 0.3/orbit averaged (H0190). Ship orbit ~10³–10⁴ game-seconds.
- Decisions: the script burns 4 game-seconds apart → 8 bits / 4 s ≈ 2 bits/game-second.

So predicted gross creation ≈ (kicks/s × 30–80 bits/kick) + 2; net H_live slope ≈ 0 after the
first orbit (creation ≈ reabsorption). Live bits per live body ≈ (kicked fraction) × ~100 bits
≪ 64 — the deciding average is the kicked *fraction*, not the count.

## Held-out predictions (not tuned on)

- **P1 (rtf invariance):** bits per *game-second* — gross created, reabsorbed, net slope, and
  live-bits-per-body — are functions of simulated time, not wall time. At rtf 1, 100, 1000
  (same seed, same canonical script) they agree within a factor of ~2 (finite windows: the runs
  cover different game-time spans, so the transient is weighted differently).
- **P2 (boundedness):** net live bits per game-second slope ≤ 10% of gross creation after the
  first ship orbit; live bits per body < 64 bits at every rtf tried.
- **P3 (per-kick bits):** mean bits created per kick lands in 20–200 bits.
- **P4 (digest):** the bench digest at seed 1, rtf 100, same seconds, is unchanged by the
  instrumentation (read-only counters).

## Kill criteria

- Live bits per body ≥ 64 → the 8 GB / 10⁹ premise is broken at the *scene* level already.
- Net slope > 0 persistently (linear growth over 10⁴ game-seconds) → H_live is not bounded in
  steady play and "one hour" cannot be promised without reabsorption work.
