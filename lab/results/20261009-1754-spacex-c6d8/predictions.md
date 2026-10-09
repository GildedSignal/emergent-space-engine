# Predictions (written before the decisive run)

Question: how many bits of live distinguishing information (H_live) does the plane's universe
actually create per ship per game-second, and does law.md's "+62 bits per kick, −60 per
reabsorption" match the measured journal?

Tuned on: nothing yet (the instrument is written before any run; the numbers below are Fermi
estimates from the law's constants, not fits).

## Held-out cases and expectations

1. **P(dv = 0 quanta) per kick binding, per component > 0.8** (sigma-delta carries sub-quantum
   parts; whole quanta should be rare on the plane's tides). If most kicks apply whole quanta,
   the quantization is coarser than I believe and the +62 bits/kick is realistic as a live rate.
2. **Bits per binding (residual deltas + carry + key deltas, empirical magnitude-class entropy)
   between 15 and 90**, point estimate ~45: the residual refit dominates, dv contributes almost
   nothing. This brackets law.md's +62; if the measured value is < 6 bits the +62 line is wrong
   by 10× and the memory budget is much looser than the spec assumes.
3. **Cadence**: bindings per ship per game-second between 0.01 and 5 at rtf 100 (fleet members
   kicked far more often than made bodies; the split will show it).
4. **Saturation**: at the measured rate, 64 bits/ship (8 GB / 10⁹) is consumed in 10¹–10⁵
   game-seconds with no reabsorption. If it is < 10² game-seconds, the scar layer as specified
   (+62/−60) cannot hold a session and reabsorption must be refit-per-kick — a law change.
5. **Robustness (not tuned on)**: seed 2, members 400, rtf 20 give bits per binding within ×2
   of the seed-1 run and P(dv=0) still > 0.8. A swing beyond ×2 says the tuned scene is not
   representative and the number is scene-bound, not law-bound.
6. `bytes_per_body` today (plain tubes) is 60–300 bytes: ≥ 8× over the 8 bytes/ship budget
   before any distinction is stored (the idiot index on storage).
