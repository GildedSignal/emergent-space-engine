Working...
Check complete. `check.md` written: **Grade: lead**.

**Verdict summary**

- **Reproduction: pass.** Clean tree at base f8056f86, patch applied, `regen.sh` rerun (~2.5 min): deterministic digits identical (game_s, kicks to the last digit at N≤4×10³, readout counts), timings within load noise (µs/body 13.4→23.4 vs author's 12.8→23.3). Instrument verified faithful to `nladder.rs`'s coast flight; the blind-certificate premise confirmed in source (`flight_sweep.rs:120` gathers every frame; `nladder.rs` only post-flight; `view.rs` walks every body, no cull).
- **Adversarial extensions (3 outside the author's grid):** N=16×10³ → 24.1 µs/body, linear; blind N=1000 → p99 6.0 ms, 0 over (the break rung's own control); rtf 1 → readouts/seen **1.81 vs 1.80 at rtf 100** — the "engine's advancing state keeps the memo half-cold" mechanism is wrong (the re-bracket is cadence-invariant; TICK_SECONDS = 4.9 µs means a fresh integer root every frame at any rtf), though the measured law itself strengthens.
- **Why lead, not gold/silver:** the headline is already the wiki's held result — flyable-frame **4875** (same day, silver): view-owned flyable frame from ≈8×10², 19–23 µs/body warm, with **4143** having wired the row-set cure (220×); view **649c** (15 Oct): in-band 19–22 µs/body, ≥97% of frame, readouts/emitter 1.96–2.00. Neither dossier nor the proposed page cites them. Held-out predictions P1/P2 also missed (honestly disclosed).
- **Page corrected in place:** the conflict resolution had silently dropped the `[Second checker 99da … Gold.]` paragraph and 2403's heading while claiming "resolved additively" — both restored, and a `[Checker 25f7]` bracket appended with the reproduction, extensions, mechanism correction, novelty citations, and the N=500 crossing correction (p99 is already 14 ms at 500).

Tree outside the run folder restored to pristine.
