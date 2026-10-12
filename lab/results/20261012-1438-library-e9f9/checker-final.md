Working...
Check complete. `check.md` written: **Grade: silver.**

**What held up:**
- Reproduction bit-identical (`diff` clean, 86 s vs the author's 117 s on a shared machine); every dossier number verified against the regenerated output, including the calibration line and the competitors' positive-control failure (0/200 on the c=0.02 leak).
- Predictions discipline is real: re-issued before the decisive run, one honest miss, one disclosed instrument fix (h re-frozen on the t₃ family), controls pass both sides.
- All seven library quotes verbatim in the cached export; CUSUM absent from HISTORY — the gap (H0215 "B12 unusable until rebuilt", redteam-b12-stat's named hole) is live.
- My slow-walk extension (per-orbit steps at the noise floor, the regime probe 1 actually killed) catches 93–100% — stronger than what the author measured.

**What breaks it:**
- The headline "0% false alarms at 20× amplitude" is a construction artifact: with exactly P ticks per period, the bounded sinusoid's per-orbit mean is identically zero, so A=20 is the same test as A=1.
- Adversarial case: a bounded error detuned 0.1% (precession — the engine's core GR behaviour) at the author's own A=20 arm false-alarms **200/200** (median orbit 9) under the frozen (k,h); breaking condition ≈ A·ε ≳ k. Sign-alternating leaks also pass (author-disclosed, confirmed).
- Competitors were stand-ins, not the shipped statistics; "the doll knows its period" fails for the plane's integrated orbits.

**Path to gold (named in check.md):** rerun on the plane's actual Jacobi series with a negative family that includes detuned bounded error, plus the two stated requirements the freeze lacks — minimum leak c (sets k) and A·ε < k.
