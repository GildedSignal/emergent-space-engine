# Predictions (written before the decisive flights)

Scene: shipped `nladder`, N = 10⁵ (100,028 bodies), seed 1, burn (L8 held from frame 60),
rtf 100, 12 ms budget, Linux /proc probe (`LADDER_PROBE_GS=1000`), RSS guard 1,600 MB,
wall cap 420 s. Arms: A shipped (`ES_SCAN_TTL_S` unset), B `ES_SCAN_TTL_S=16`,
C `ES_SCAN_TTL_S=8` (shorter cap). These cases are outside my grid: I have flown only the
N=0 coast smoke and the N=10⁴ coast control (b_per_body 2,463, catalogue 10,076 — the
record's digits).

- **P1 (the ratchet reproduces on arm A):** resident hits the 1,600 MB guard between
  25k and 50k game-s (4447's second checker: 37,123 gs at this exact rung), held rising
  through the flight, `held_end ≈ mints − answers` to within the drain's take.
  Kill: if A ends flat under 900 MB, my build is not the record's arm.
- **P2 (the fence deletes the ratchet on arm B):** resident stays under 900 MB through
  the same horizon, no guard hit, RSS flat in the last 40% of the flight (slope < 1 MB/1k gs).
  Kill: if B also staircases to the guard, the retention is not the scan queue's, and
  4447's mechanism attribution is wrong.
- **P3 (the bound is the fence, not the drain):** held_max ≈ TTL·λ_entries ≈ 26 ± 12 on B
  (λ_burn ≈ 0.835 distinct/game-s, ~1.95 entries/mint), `expired ≈ mints − answers`.
- **P4 (the deletion price — Musk's add-back bar):** the encounters the TTL arm fails to
  log are < 10% of arm A's logged encounters (the player is interstellar; most expired
  scans answer empty). If ≥ 10%, expiry-without-answer is not shippable as-is: the fence
  must answer before it expires (the allocator's job, not the queue's).
- **P5 (frames unharmed):** B's p99 ≤ 15 ms and over-budget frames within A's class
  (both arms tolerate the shared box's load; timing is not the instrument here).

Honesty notes: held counts and RSS are load-elastic on this shared box (4447's own
caveat); the invariant content is the counter identity (mints = answers + expired + held)
and the ledger counts. The TTL arm is a law change (expired scans' encounters never log):
digests differ from A by construction, and P4 prices exactly that difference.
