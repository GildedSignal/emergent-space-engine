Working...
Check complete. `check.md` written to the run folder; nothing else touched (no `target/`, all author files at original mtimes, scratch variants in `/tmp/adv` only).

**Grade: silver.**

What I did and found:

- **Reproduction** — `cargo run --release` (18.8 s) regenerates every data line of `run.csv` bit-for-bit; `cargo test` passes; `patch.diff` is empty and the instrument verifiably drives the *shipped* `crates/shipmem` (`Program::seal_from`, `Enc::new(true)`, Elias–Fano) via a path dependency. Dossier numbers (slopes 2.81/3.06/5.08 bits/doubling, per-column bytes, G1 control flat, N-independence, P1≡P0) all re-derive from the CSV. Predictions were pre-registered (08:25) before the decisive run (08:45), and held except the phase-saturation half of prediction 4, honestly disclosed.
- **Adversarial** — (1) fresh seed: identical slopes; (2) systematic common-mode drift (12σ by k=4096): absorbed natively at 0.655 B/body, so the "no re-anchoring machinery" claim survives its strongest form; (3) the wrapped-phase "representation trap" **does not reproduce**: in the actual 4-column seal wrapping is free (9.72 vs 9.93 B/body at k=1), single-column it costs +0.75 B, and no construction yields the dossier's +1.6 B — the number is not regenerable from shipped code; (4) the "+2.05 bits/column within ~1 bit" calibration is ~3.9 bits/column at k=4096 (analyze.py's own docstring admits 1–2), a ≲1 B/body systematic that doesn't change the conclusion.
- **Novelty/fit** — answers the HANDOFF risk line ("H_live … not measured yet") with no prior measurement in HISTORY; deletes candidate re-anchor/repack machinery.

Silver rather than gold solely on the record, per the lab's own standard: one Evidence-section number (the trap) that shipped code cannot regenerate — the exact failure mode the taste log flags. The named gold-making experiment is a two-line wrapped-variant probe plus calibration fix, ~10 minutes.
