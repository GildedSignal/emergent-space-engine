# Predictions (written before the decisive run)

Probe: `work/b12_cusum.py` — can any statistic separate a **bounded** energy error
from a **compounding** one? Three regimes, as the engine knows them:
(i) bounded symplectic oscillation + i.i.d. noise (fixed-step control: flat),
(ii) energy error that *walks* (random walk; the failure that killed per-body steps, probe 1),
(iii) systematic leak (drift per event).

Observable under test (v2): the **per-orbit mean** of the energy error — sampled at the
orbit's own period, not per tick (the doll knows its period; one integer adder per kick).
Statistic: two-sided CUSUM with allowance k and threshold h, both frozen from the
calibration arms only (c0 bounded A=1, c1 leak 0.02/orbit). Competitors on identical
streams: log-log exponent of max|e| (B12-current style) and window RMS ratio
(redteam-b12-stat's recurrence ratio).

## v1 result (kept as a record)
v1 differenced the raw stream and my "bounded" arms contained `cumsum(noise)` —
regime (ii) mislabeled as (i). CUSUM flagged them (P3/P4 "false alarms" were true
positives on a walking error). Streams rebuilt; predictions below re-issued (v2)
before the v2 run. Amplitudes are matched so amplitude alone carries no signal.

| id | case | expectation (v2) |
|----|------|-------------|
| P1 | bounded at A = 1, 2, 5, 20 (20× calibration amplitude) | CUSUM alarms 0% of seeds at every A (amplitude-invariant); exponent flags ≥ 50% of seeds at A = 20 (misrank, H0215 probe-P2 mode) |
| P2 | leak halved and quartered (c/2, c/4) | CUSUM still alarms on 100%; delay ≈ linear in 1/c; window-ratio falls toward its control threshold |
| P3 | diffusive walk σ = 0.005/orbit (regime ii) | CUSUM alarms (compounding must be caught) with delay ∝ h²/σ²; exponent and ratio are blind (slope ≈ 0.5 absorbs it / ratio ≈ 1) |
| P4 | bounded with heavy-tailed (t₃) i.i.d. noise, and pure periodic echo, zero noise | CUSUM false-alarm < 5% of seeds |

Controls: c1 (leak 0.02) must alarm 100% for every statistic; c0 (bounded A=1) must
alarm 0%. If either fails, VOID (instrument broken, not the method).
