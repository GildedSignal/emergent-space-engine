# Predictions (written before the decisive runs, 2026-10-11)

Question: the shipped plane's frame-service capacity — at what members count M and time factor R
does the 60 Hz frame's contract break, and which stage's tail breaks it?

Basis for the guesses (measured just now, default 48 members, rtf 1, unpaced, 5 s):
frame p50 0.63 ms = engine 0.023 + gather 0.457 + json 0.102 + wire 0.044. The engine is 4% of
the frame; the unbudgeted readout (gather + JSON + wire) is 96%. Engine is budget-capped (5 ms,
overflow → rtf dip, never a hitch, by design). Gather reads every fleet member every frame (cheap
extrapolation); every handed-out member becomes a doll body read through a Newton light-cone
crossing (~6.7 µs, the readout lens's number).

The runs (each ≤ 60 s, ≤ 2 GB):
- A: members sweep at rtf 100, unpaced, 10 s: M ∈ {48, 500, 2k, 8k, 32k, 128k, 512k}.
- B: rtf sweep at M = 48 and M = 8k, unpaced, 5–10 s: R ∈ {100, 1e3, 1e4}.
- C: burst: M = 48 and 8k, rtf 100, paced, 20 s, --level 15 (11,561 g), per-frame CSV.
- D: controls: (i) digest invariance across engine budgets (0.5 vs 5 ms) and paced/unpaced at
  M = 48, rtf 100, 10 s; (ii) positive control: M = 512k must break visibly somewhere.

## P1 — members axis
Frame CPU p99 crosses 16.7 ms between M = 4×10³ and 3×10⁴. The breaking stages are the readout's
serialisation and gather (json + wire + view), NOT the engine: at every M the engine stage's max
stays near its 5 ms budget and hitch counts above 16.7 ms come from the readout stages. My point
guess for the crossing: M* ≈ 8×10³ (from 1.9 µs per seen emitter in json+wire, ~76 seen at 48
members).

## P2 — the handout leak (time axis)
At M = 8k, rtf 100, the frame cost grows over the run's game time: the battle's members that leave
the frame are handed out into the doll and each becomes a Newton-crossed body (~5–7 µs/frame each).
Prediction: frame p99 in the last quarter of the run > 2× the p50 of the first quarter, and
n_bodies at the end > n_bodies at the start. The tail's mechanism is the readout again, now
compounding with game time (a leak, not a burst).

## P3 — rtf axis
At M = 48 the frame never hitches up to R = 10⁴ (no frame above 16.7 ms); the failure mode is the
graceful dip: rtf lowest 1% falls below 0.9 somewhere between R = 10³ and 10⁴ (the engine budget
can no longer cover mandatory work per frame). At M = 8k the dip starts earlier (R ≈ 100–1000).

## P4 — the player's burst
At level 15 (11,561 g), paced, the burn frames cost ≤ 3× the coast frames and cause no hitch above
16.7 ms attributable to the burn (the player's wake is its own body's rebinds and reads). The
digest at the canonical cut is identical across engine budgets (0.5 vs 5 ms) and paced vs unpaced:
the budget moves work, never outcomes (the plane's own contract; verifying it is the allocator's
foundation).

## P5 — positive control (the instrument must be able to fail)
At M = 512k, rtf 100, the service level must break visibly: frame p99 CPU > 16.7 ms, or the rtf
lowest 1% < 0.5, or memory refusal. If nothing breaks anywhere in the whole matrix, the instrument
cannot fail and the run is VOID.

## Kill rule for the claim
If the frame holds p99 CPU < 16.7 ms at M = 10⁵, rtf 100 (nothing breaks inside the 2 GB budget),
the claim "the readout breaks first" is killed and the capacity is the measured number instead.
