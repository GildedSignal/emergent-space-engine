# Predictions (written before the decisive runs)

Tuned on: seed 1, m1500, rtf 1, 8 game-s (probe off: 232 hand-outs, 120 retries = 52%, digest
c56cbde4f1d0824c…; probe on: same digest, 0 retries, hand-out bind 487→232 µs). Everything
below is on cases I have not run.

The probe (`ES_WORD_FIRST=1`): `bind_surface` derives the unit word from the state's own key
(the same key the compile reads) and binds once at that word, instead of compiling, finding the
word too small, and compiling again. The pre-shifted call is bit for bit the shipped retry's
second bind; any error falls back to the shipped path.

| # | Held-out case | Prediction |
|---|---|---|
| P1 | Digests, seeds 3, 5, 7 at m1500 rtf 1; seed 3 at m4000 and m8000 rtf 1 | bit-identical off/on at every scene |
| P2 | Retries (FIT2) with probe on, all scenes | 0 calls — the key-derived word never undershoots what `word_for` reads off the finished entry (Cycle: apoapsis from the key; Passage: the compiled-out edge, the very argument passed to `Passage::compile`) |
| P3 | Retry rate with probe off, all scenes | 50–65% of hand-outs (the fermi run's 52–63% band) |
| P4 | Hand-out cost per item (H_BIND / calls), probe on vs off | drops 40–55% everywhere hand-outs occur (one compile instead of ~1.5) |
| P5 | `lost_bodies`, `bodies`, `bytes_per_body`, overflow counts | unchanged at every scene (the only divergence hole — a compile that errors at the state's own word but succeeds at the coarser one — must not fire; a changed `lost` list falsifies the probe) |
| P6 | Flying pace, m400 rtf 100, 8 game-s | no hand-outs at all (the quant run's finding), so FIT2 = 0 both ways and the digest pair still matches |
| P7 | A no-`prof` build (the exact shipped feature set), seed 3 m1500 rtf 1 | digests identical off/on, and equal to the prof-on digest of the same scene (timers must not reach outcomes) |

What would make it wrong: P2 failing (a FIT2 > 0 with the probe on) names a key whose compiled
trajectory needs a different word than the key implies — the prediction's premise dies and the
retry stays necessary. P1/P5 failing (a digest or a lost-body change) names the error-path hole
above; the probe is then unsound as shipped and only a two-phase bind (key, then word, then
compile) inside `from_state` can be adopted.
