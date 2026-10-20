# Predictions — 20261020-1326-second-20261020-1210-taleb-9ed1-94e2

Written 13:58, before every decisive flight (T1–T3, C1, C3 below). Disclosed pre-work:
the 5e4/30 s smoke flight (calibration only: the instrument prints, envs off = shipped
bits, no freeze at 5e4 — max answer 0.86 ms over cand=194, near=203, no filter bail)
and the X1 no-trace baseline draw at 1e5, flown before T1 to bound the trace's overhead.

The checker's named gold experiment: instrument the held-scan answer path (candidate
count, doll population, per-candidate price) across 1e5–3e5, then price the two built
fixes. Gold lands when a fix holds the answer under the 12 ms budget at 3e5 without
losing the en=178 encounters.

Arms (all: burn scene, rtf 400, budget 12 ms, seed 1, fence ES_SCAN_TTL_S=16,
stagger ES_STAGGER_GS=14000 — 9ed1's decisive config; ES_ANS_TRACE / ES_ANS_CHUNK as
noted):

| id | N | sec | trace | chunk | question |
|---|---|---|---|---|---|
| X1 | 1e5 | 130 | off | off | no-trace baseline (probe overhead, fresh draw) |
| T1 | 1e5 | 130 | on | off | the answer path at the birth rung |
| T2 | 2e5 | 130 | on | off | ditto at 2e5 |
| T3 | 3e5 | 120 | on | off | the freeze object, instrumented |
| C3 | 3e5 | 120 | on | on | the fix: incremental answering at the frame budget |
| C1 | 1e5 | 130 | on | on | the fix at the birth rung (cheap-answer inertness) |

## P1 — the freeze's anatomy (the instrument's reading)

At 3e5's freeze frame, the answered scan carries cand ≥ 0.3×doll (≥ 9e4) at
2–8 µs per candidate; normal answers at the same rung carry cand ≤ 2e3. **Kill bar:**
the freeze scan's cand < 3e4 — then the walk is not candidate-set-driven and the O(N)
story dies.

## P2 — why the filter passes everyone

The freeze scan's mint saw the radial filter bail (`near=-`) or pass ≥ 9e4, and the
scan's interval is the player's long step: h_gs ≥ 1e4 (the ~27.9k gs clock), making the
radius window `(v + speed_cap)·h` wide enough to cover a quarter of the doll's
registered radial ranges (the `bodies/4` bail in radial.rs). **Kill bar:** h_gs ≤ 1e3
at the freeze — then the interval story dies and the bail must have another cause.

## P3 — the exact linear bound (fix B priced on the walked set)

On the freeze scan, the exact bound `|d| − |w| > near` skips ≥ 50% of the walked
candidates (the shipped comment's own band is 70–86%; the 5e4 smoke reads 97% on
normal scans). **Kill bar:** skip fraction < 30% at the freeze — then the bound buys
little exactly where the walk hurts.

## P4 — fix A holds the budget without losing the encounters

With ES_ANS_CHUNK=1 at 3e5: max_ms ≤ 40 ms (prediction; the budget's own latch should
keep it ≈ 12–25 ms), era-1 max ≤ 13 ms, and the en≈178 object IS logged (a completed
answer batch of en ≥ 100 encounters), with the flight's total encounters ≥ the
non-chunked arm's total at the same rung. **Kill bars:** max_ms > 120 ms, or the
en ≥ 100 batch missing, or total en < the non-chunked arm's.

## P5 — fix A's price (no kill bar; a price, not a pass)

The freeze answer completes within ≤ 300 frames of its mint (its ~1.2 s of walk paid
out of the frames' budget slack, ~4–10 ms a frame); held_max stays ≤ 350 (the fence
bounds the pile behind the in-progress front scan); peak RSS within A6's 1,515 MB
± 15%.

## P6 — the per-body constant (the checker's law re-read by the instrument)

Freeze-answer ms / doll_n ∈ [3, 6] µs at every rung 1e5–3e5 (the checker's 4.2–4.4
µs/body from frame walls; the instrument reads it per answer, per candidate).
