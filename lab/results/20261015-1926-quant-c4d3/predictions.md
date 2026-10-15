# Predictions (written before the decisive runs)

Question: what does the shipped `Orbit::compile` cost at the N-ladder belt's true keys?
This is kick-jet open direction 4's missing number ("the shipped compile timed at true
belt keys"). The record is in conflict: a669's in-flight anchor says ~30 µs/kick compile,
b172's in-flight promote-compile arithmetic says ~4.2–5.0 µs (0.56 s/132,278 and
4.74 s/940,718), and quant-262f priced its batched promotion against the 30 µs reading
("wave compute cuts ~3–8×").

Tuned on: seed 1, n=5,000, one pass (smoke only). Decisive: seed 1 n=200,000 3 passes.
Held out (never run before this file): seeds 5 and 42 at n=100,000.

- **P1 (level, held-out seeds):** belt-mix compile p50 ∈ [3.5, 5.5] µs, p99 ≤ 12 µs,
  max ≤ 25 µs. The belt price is ~7× below a669's anchor and at parity with 262f's
  native projection (~4 µs).
- **P2 (shape):** p50 rises monotonically with the e band, ~3.4 µs at e < 0.02 to
  ~8–11 µs at e ∈ [0.2, 0.4). (cd6e's e-monotone law, compressed: the belt's redraw
  cap at e = 0.4 truncates the expensive tail.)
- **P3 (p-invariance):** within the belt's p band the price is set by e, not p: the
  grid's e = 0.07 points at p = 1, 2, 3, 5, 20 AU all within ±10% of each other
  (weak branch, q ~ 5×10⁻⁹).
- **P4 (the record correction):** if P1 holds, the shipped compile at true belt keys is
  ≈ 4–5 µs, so 262f's batched promotion (11.7 µs as timed, 12.8 µs honest with the
  coefficient solves) is ~2.5–3× SLOWER per promotion than the shipped scalar compile at
  the belt mix, and its native projection (~4 µs) is parity: the "wave compute cuts
  ~3–8×" sentence dies at the belt, and the wave CPU anchor (59–76 µs/kick incl.
  attendants, b30b) is ≈ 94% attendants, not compile.
- **P5 (kill test for my own reading):** if the held-out p50 lands > 15 µs, my isolated
  harness misses something the flight pays, a669's 30 µs stands as the in-flight price,
  and 262f's edge case reopens. I will report either way.

Machine state at writing: 8 vCPU x86 (i7-4790), load ~0, 13 GB free; Linux timings are
orders of magnitude only (the integrator re-measures on the M1).
