Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did:**

1. **Reproduced.** The runner's `regen.sh` regenerates every arm within ~1% of the dossier (311.7 ms/6,393 ev at 10⁵; 1,204.1/24,535 and 1,219.4/24,819 at 2×10⁵ seeds 1/2; coast 11.98 ms, 0 over; exponent 1.95 vs 1.94). I rebuilt from the applied patch myself and verified the code claims by reading `universe.rs` (`pull_ships(key, !in_root)` at :769 with the engine's own "burst … outside the budget" comment; hold-the-scan at :1164). Patch is instrument-only, digest-neutral defaults.

2. **Attacked outside the author's range:**
   - **5×10⁴ burn** — no wave monsters at all; only the unnamed second seam fails (9 frames, 1 event, 17–19 ms). Cliff onset sits between 5×10⁴ and 10⁵; onset is drain-rate (machine) conditional.
   - **rtf 200 at 2×10⁵ burn** — monsters grow to 30,301 events (vs 24,535), spaced 25 frames = 83 game-s (item cadence is game-time). The +5.8k events ≈ the halved drain's removed capacity: **batch = wave demand − what the budget-cut drain removed** — the unbudgeted-pull mechanism confirmed quantitatively, and the author's "linear in N" model corrected.
   - **belt_first 10⁵** — wave window N-independent, density ∝ N.

3. **Novelty (why silver, not gold).** The committed M1 record `artifacts/runs/nladder/ladder.txt` ("AFTER 32e9e986", "BEYOND THE GATE") already measured this break at 3×10⁵ (1,280 ms, 37,938 events), named the pull seam, ran passing coast controls, and made the 20 s-window critique. This run is a careful lab-side confirmation/interpolation (new N, seeds, spacing, recovery, second seam) — real and verified, but not a 10× move or deletion. The one experiment to gold is the run's own named fix: hold the scan past the wave with `frame_digest` unchanged.

4. **Page corrected** where it overstated ("linear in N" missing the drain term; "schedule-conditional, the phenomenon is not" ignoring the machine-conditional onset) — author text preserved, checker brackets added. Also flagged in check.md: P6's "never lags > 0.1 s" clause failed literally (1.448 s during the wave) yet was reported as held.

Tree restored clean; nothing committed or pushed.
