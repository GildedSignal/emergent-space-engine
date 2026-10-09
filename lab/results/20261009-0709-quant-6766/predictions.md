# Predictions (written before the decisive runs)

Tuned on: n = 1 000 and 2 000 only (smoke). Those gave ≈ 21 µs per event (kicks and boundaries
mixed ≈ 1 : 1), ≈ 230 ns per entity for an empty frame, 1 039 bytes per body. Held out: every
n ≥ 10⁴, the perf counters, and the profile split.

The machine here is a Haswell i7-4790 (4C/8T, 32 KB L1d, 256 KB L2, 8 MB LLC, 64 B lines),
shared, 8 vCPU visible. Orders of magnitude only; the integrator re-measures on the M1.

- **P1 — the event path's memory wall.** At 1 KB/body the working set crosses the 8 MB LLC near
  n ≈ 8 000, so even 2 000 was partly streaming. I predict ns/event grows monotonically with n and
  at n = 10⁶ is between 1.5× and 3× the n = 2 000 value (≥ 30 µs/event). LLC misses per event rise
  from < 1 (n ≤ 10⁴) to several (n = 10⁶).
  *Killed if* ns/event at 10⁶ is within 1.2× of n = 2 000, or misses/event do not grow with n.
- **P2 — the frame's fixed cost.** `advance` recomputes every entity's deadline (rekey) and drains
  the calendar's remaining heap every frame, resolved events or not. I predict the empty frame
  stays linear at 200–300 ns per entity: ≈ 2.5 ms at 10⁴, ≈ 25 ms at 10⁵, ≈ 250 ms at 10⁶ — the
  16.7 ms frame budget of a 60 Hz presentation breaks near n ≈ 7×10⁴ on this class of core,
  whatever the events cost.
  *Killed if* the per-entity empty-frame cost at 10⁶ falls below 50 ns (sublinear or amortizable
  as built).
- **P3 — bytes per body.** `bytes_per_body` ≈ 1 039 on the live store (tubes + histories +
  catalogue). I predict HWM grows at ≈ 1–1.5 KB per body, so 10⁹ bodies need ≈ 1–1.5 TB against
  the 8 GB target: the gap is ~100×, and `shipmem`'s population programs are not optional at any
  cadence.
  *Killed if* the marginal bytes per body measured from HWM(n) is below 400 B.
- **P4 — where the nanosecond goes.** I predict the profile at n = 10⁵ is dominated by the event
  arithmetic itself (kick integration, tube apply, Scalar i128 maths): top functions ≥ 60% of
  cycles, the calendar (queue sift) < 10%. The lever named by the board (fewer kicks per orbit)
  is then the right one, and the queue is sound as built.
  *Killed if* the calendar or the rekey path takes > 30% of cycles in the eventful run.

Controls on both sides: the empty frame is the negative control (0 events, measures only the fixed
cost); the eventful rounds are the positive (events dominate the round at 20 000 events). perf
runs subtract a rounds = 0 run (construction only) from a rounds = 8 run to attribute counters to
the event path.
