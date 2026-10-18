Working...
Check complete. `check.md` written: **Grade: gold**.

**What I did:**
- **Reproduction**: runner's regen (exit 0) verified line by line — every dossier number regenerates (footprints 10/148/149/477/479 MB, kicks 131,047 bit-identical across executions, catalogue flat, 0 frames over 12 ms). Applied `work/patch.diff` to a pristine tree myself; it is print-only. Timing maxima differ ≤0.4 ms from the dossier — box noise, disclosed.
- **Predictions**: `predictions.md` predates the flights; P2 (the decisive ±10% falsifier), P3, P4, P5 all held; P1 wrong in kind (27.5k wave is the step boundary, not kick₂) and honestly re-derived — verified against `fleet.rs:169` and `Universe::prune`/`key_prune` in code.
- **Three adversarial arms, all outside the author's grid** (`raw-checker/`): held-out N=10⁴ — flat 54–55 MB through kick₂; 10⁵ to 58,500 gs — the unflown third belt-wide wave (boundary₂, +~100k events) moves RSS 0 MB at 479, converting the author's inference into measurement across four waves; the named-unflown burn — per-body terms hold (bpb 1,410→1,477, cat constant, flat through kick₂) but resident memory grows 150→571 MB between waves: a real play-time ratchet in the mint channel (2403's), not the history terms.
- **Novelty**: ladder.txt and the 155-run nladder page have nothing past one step (longest prior flight: 25,899 gs, pre-boundary); the ~11× event-rate correction is new.
- **Page corrected in place**: "second kicks at 2×" (wrong — step ≈ 27.6k gs, kicks at 1×/3× the first items), "every prior wave flight" → "ladder-scale", plus the checker paragraph folding in the burn caveat and the two new wave measurements.

Gold because: reproduced, decisive pre-registered prediction held at every scale including my extensions, it retires the play-time failure mode on the board's top memory bottleneck and corrects a recorded input by 11×, at zero adoption cost. Tree restored to pristine.
