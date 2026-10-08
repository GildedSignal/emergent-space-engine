Working...
Check complete. `check.md` written to the run folder; nothing else touched; no git operations.

**Grade: silver.**

**What held (gold-grade physics):**
- **6/6 reproduction targets bit-identical** from shipped code in a clean tree: controls, noether, `census base 8 plain`, `census two 8 plain`, `best base 8`, and the slowest cell `census flyby 6 plain 300` (3 min). p8.py verified byte-identical to the first run's commit. Every dossier table cell matches its stored record.
- **Predictions genuinely pre-registered** (15:35:57, before all decisive records); the two disclosed mid-run crashes match the runlog tracebacks.
- **Four adversarial attacks, all strengthening the kill:** k=4 → 0.35 and k=10 → 0.00 usable (kill holds over 64× ds range); a 24/octave fine grid finds zero missed or touching roots (the instrument is sound, two-planets 0/1600 is not a grid artifact); a co-rotating two-planet control (symmetry restored) is still 0/1600; a null-second-planet control reproduces the one-planet record exactly.

**Why not gold (the lab's own rule — a headline the log contradicts):**
1. "nan audit 0 everywhere" is false: flyby k6 has nan=164/165 of 2400 records (~6.8%, overflow at runaway α) — printed in the author's own runlog and reproduced bit-identically by me.
2. Prediction P8 ("nan fraction 0 everywhere") failed there but is reported as "P8 held: 0 nan".
3. Minor same-class slips: Z-collapse holds 7/9 not 8/9 (two k8 also inverts); the quoted 8.06e-12 appears in no shipped record (regenerable value: 7.6078e-12); the "no rotating symmetry" mechanism attribution is refuted by my co-rotation control even though the kill survives it.

**Gold step:** an erratum plus a 10-minute classification of the non-finite α-families (runaway-band vs in-band) — no new physics needed; the kill itself is fully verified.
