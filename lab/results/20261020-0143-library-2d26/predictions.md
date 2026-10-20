# Predictions (written before any flight; the arms are the shipped `nladder` burn scene, seed 1, rtf 2000, 12 ms, plus one coast control)

Protocol: `ES_FRAME_TRACE` (print-only patch, off = shipped bits untouched) dumps per-frame (frame, engine ms, events, lag s). Onset = first frame with ms > 3× budget. Slack(i) = Σ max(0, budget − ms) over frames before onset; Excess = Σ max(0, ms − budget) over frames from onset to the end of the flight (the wave's undelivered work, 1d47's amortization term). Coverage = Slack/Excess.

- **P1 (compute-ahead cannot prepay the wave):** coverage < 1 at BOTH burn rungs (10⁵, 2×10⁵). Band: 0.05–0.6. Mechanism if it holds: the wave's excess grows ~K-proportional (0c0f's max ratio 1.88 between rungs) while pre-onset slack grows only with frames-before-onset.
- **P2 (the flight's whole-flight slack DOES cover the wave — amortization is sound, prepayment is not):** Excess / Total-flight-slack ∈ [0.2, 3] at both rungs. This is the decision split: schedule (drain at budget, ee4d/1d47) vs prepay (compute-ahead, 0c0f's open direction 3).
- **P3 (the lag is the wave's excess priced at the budget, and it is asymmetric):** worst lag (s) ≈ (Excess/12 ms)/60 × rtf-adjusted scale — register the weaker form: lag(2×10⁵) > lag(10⁵), and the lag's recovery slope after the wave is shallower than its onset slope (drain at budget, not burst).
- **P4 (the ebb is real at play-relevant cadence):** p50/budget ∈ [0.30, 0.65] at both burn rungs (0c0f read 0.46–0.51 at rtf 2000; their ≤0.25 letter failed).
- **P5 (negative control):** the coast arm at 10⁵ has NO wave: max < 3× budget, over ≤ 5 frames, excess ≤ 1/10 the burn arm's (the burn gate, 0c0f's checker (c)).
- **P6 (held-out quote property):** all 5 lesson quotes byte-identical against a fresh Readwise export, verified by script against highlight ids.

Adversarial half (checker's to extend): rtf elasticity is disclosed — at rtf 400/100 the over-count and p99 move (0c0f's checker (a)); my coverage/lag numbers are rtf-2000 arms and the coverage ratio is cadence-robust only if pre-onset gs and onset gs are cadence-locked (onset is a game-time event, gs ≈ 14.7–15.4k; frames-before-onset scales with rtf, so coverage DROPS at play cadence — registered: coverage(rtf 100) < coverage(rtf 2000), the prepay route is weaker where the player actually is).
