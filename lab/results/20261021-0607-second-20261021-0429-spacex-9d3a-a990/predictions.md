# Predictions — 20261021-0607 (second author on 20261021-0429-spacex-9d3a)

Written after one N=1000/6 s `rows` smoke only (and the flyable-frame page's public numbers);
before every arm at 1e5/3e5. The experiment is the checker's named one: the census flown under the
adopted row-set gather (`rows`: fill once, then `gather_half` every frame, the flyable frame's own
loop), against the oracle gather (`sparse`) and no view (`none`).

What the smoke showed (N=1000, 6 s): readouts/frame 118, live@300f = 1.00, rebuilds at slack ≥ 300
= 0 — at small N the whole belt is on canvas at the fitted zoom and the row-set reads it densely.
The row-set's per-body read law is the wheel: `q = min(4·interval, drift bound)` per read, capped at
DUE_CAP = 16384 frames. So for the off-canvas majority the reads come as a ramp — dues ≈ 4, 16, 64,
256, 1024, 4096, then the cap — and for the on-canvas set at the drift bound (half a pixel ×4 slack).

- **P1 (the wheel reads everyone early, so "zero-post-birth" stays low):** at 1e5 over 20 s,
  zero_post_build ≤ 2% (the ramp's first dues are ≤ 350 frames, inside any 20-s flight). The premise
  kill is NOT "nobody reads the belt" — it is the gap law.
- **P2 (the live set at the policy's own slacks):** at 1e5/20 s under `rows`: live@1 frame ≤ 5%,
  live@1 s ≤ 15%, live@5 s ≤ 35%, live@20 s (slack 1200) ≤ 60%; and live@16384 (the wheel's cap)
  ≤ 5% — the wheel's own quantum already defines the live set.
- **P3 (the demotion return bill, the gold number):** at 1e5 over 20 s under `rows`, rebuilds per
  build-born gen at slack 300 ≤ 0.01 (no gap > 300 within 1200 frames); over the 300-s arm
  (18,000 frames) the steady law appears: ≈ 1 return/gen at slack 1200 (the 4096-frame gap) →
  ~0.003 returns/body/wall-s ≈ ≤ 20 cores at 1e9 (4.4 µs a compile) against the oracle gather's
  ~440 — and **0 view-driven returns at slack = the wheel cap (16384)**: gaps never exceed the cap.
- **P4 (flat in K):** steady view readouts/frame under `rows` at 1e5 and 3e5 within 2× of each other
  (bounded on-canvas set), against the oracle's 8.7·N per gather.
- **P5 (controls, must reproduce):** `none` at 1e5: ≥ 99.7% zero_post_build; `sparse` at 1e5:
  4/100,032 zero-post-birth, live 10/20/60% at 1 f/1 s/5 s; engine-side read counts identical
  across `none`/`sparse`/`rows` at 1e5 (the engine is deterministic and view-independent).
- **P6 (the ramp is the 20-s read law):** median post-birth reads per build-born gen at 1e5/20 s
  under `rows` lands in 3–6 (the ramp: dues ~4, 16, 64, 256, 1024).

If P3 holds, the memory row's closure is: "demote at the view's own quantum (the wheel's cap); the
return bill is then zero from the view side and the live set is the event set plus the bounded
on-canvas rows" — the premise restored with a number, adoptable in one step.
