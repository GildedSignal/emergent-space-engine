# Predictions (written before the policy comparison runs)

Tuned-on case (already measured, not evidence): members 600, rtf 4, seed 1, fixed 5 ms budget:
36/600 overflow frames, rtf lowest-1% = 0.0, worst hitch 13.1 ms, 0 hitches > 16.7 ms.

Policies under test (session-layer only, engine untouched):
- P1 adaptive: AIMD cap in [1, 13] ms — ×1.5 on overflow, ×0.9 after 8 clean frames, ×0.7 if the frame's wall time exceeds 15.5 ms.
- P2 work-ahead: idle frames advance the target beyond the wall clock (credit = unspent budget ms, capped at 50 ms wall of lead; drained on overflow).

Held-out expectations, to be judged on cases not tuned on (seed 7; members 200):

1. Digest control: every policy at the same seed/cut/log gives the same digest as P0
   (the design claims schedule-independence; if this fails, that is the finding).
2. P2 at binding bursts: overflow frames fall at least 3×; rtf lowest-1% rises from
   ~0 to at least a third of the median; hitch counts above 16.7 ms stay 0.
3. P1: rtf lowest-1% at least 2× P0's; worst hitch stays under 16 ms (the cap trades
   frame time for throughput, not for missed deadlines).
4. P1+P2 combined is no worse than either alone on lowest-1% RTF.
5. On the untuned seed, the direction of every effect is the same (sign robustness).
6. At rtf 1 (unbinding), every policy behaves within noise of P0 (no regression when
   the budget never binds).
