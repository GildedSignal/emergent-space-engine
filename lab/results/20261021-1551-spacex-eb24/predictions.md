# Predictions (written before the decisive arms; smoke arm 3000 coast 4 s already flown to prove the instrument, not tuned on)

Arms: A = 3000 coast 20 s rtf 100 (the fallback arm); B = 30000 coast 20 s rtf 100 (the fence arm);
C = 100000 burn 20 s rtf 100 (the memo arm); D = 100000 burn 20 s rtf 2000 (the wall arm).
Each arm flown with the pre-check off and on (`ES_SCAN_PRECHECK=1`), attribution on (`ES_SCAN_SPLIT=1`).

1. **Digest identity:** on every arm the settled digest is the same string off and on (the pre-check
   returns the memo's own `Arc`; construction, plus the smoke arm already agrees).
2. **The global epoch is dead on a busy plane:** pre hits < 5% of captures on A, B, C — while the
   memo (the same domain decided after the walk) hits on a large fraction of same-tick captures on C
   (9b03 measured 47%). Mechanism: between two captures at the same tick the belt kicks (rebinds),
   which bump the global epoch but preserve every binding AT the past tick `t` through history —
   exactly the rebinds the memo tolerates and my certificate does not. The pre-check as wired (one
   global counter) cannot capture od 3's promised 47–50% deletion on this plane; the exact cheap
   form needs per-body epochs checked over the last scan's near list (still ~|near| loads, ~50×
   under the walk).
3. **Attribution (the news-fed ceiling):** the walk is loop-dominated on every arm: radial ≤ 15%,
   the loop ≥ 80%. Inside the loop, after subtracting the clock-read bias (~2 reads ≈ 40–60 ns a
   candidate on this i7-4790), the build half (checks + `Scalar::add` + the 224-B tuple push) is
   35–65% of the loop — i.e. a news-fed window that only skips the build for unchanged candidates
   caps at ~half the walk; the lookups must go too (the tuple IS the lookup's clone).
4. **The overpayment is time-measurable:** `memo walk_ns` (walk time on captures the memo then
   hits) ≥ 20% of total walk time on C — the pre-walk certificate's deletion ceiling in time, not
   just count.
5. **Wall arm:** on D the per-capture costs match C (same candidates/capture; captures arrive more
   often), and the walk stays the scan's dominant term ahead of the answer half.

Kill criterion for od 3 as wired: if pre hits ≈ 0 everywhere AND the per-body variant is not flown
clean, the dossier reports the deletion as unearned, not as adopted.
