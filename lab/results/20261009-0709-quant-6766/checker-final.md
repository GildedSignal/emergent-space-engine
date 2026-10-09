Working...
Check written to `lab/results/20261009-0709-quant-6766/check.md`. **Grade: silver.**

**Reproduced** (clean tree + patch): empty frame at 10⁵ = 77.9 ms drain → 13.5 ms break (5.8×, author 5.4×); per-event flat ≈21 µs; `bytes_per_body` 1039; plane tests 6/6 pass under the patch. Predictions discipline genuine (file order verified; P1 honestly killed, P2 confirmed stronger). Novelty: first measurement of the universe crate's per-frame fixed cost vs N — board item 4.

**Why not gold — the one-line break changes canonical outcomes.** Deadline order ≠ tick order, so the first too-late heap head can hide items whose tick is inside the frame; the drain resolves them (idle-time work), the break skips them, and `settle` exits on `events == 0` at that head. Measured with a 40-line digest-race harness (author's scenario, same seed):

| variant | digest at cut | unresolved t ≤ limit after settle |
|---|---|---|
| drain | `09f67947…` | 0 |
| break | `79d01861…` | 14 (earliest 2.6×10⁸ ticks below cut) |

Same `now`, same limit, different digest — against `universe.rs`'s own "the queue's own order … is only a schedule: nothing it breaks a tie by reaches an outcome". The guards pass only because they compare the break against itself; the author's own data held the signal (runi vs break event streams diverge every round) and the dossier argued the risk away instead of measuring it. A law change disguised as a schedule change (cf. taste log, 5 Oct).

**To gold:** a tick-ordered second index so `advance` breaks only when no due item remains behind the head, gated on digest equality + lag 0 against the drain at several cuts/histories.

Tree restored clean; nothing else in the run folder touched.
