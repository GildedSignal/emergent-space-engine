Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-0932-system-0d46/check.md`, with the author's `wiki/view.md` corrected in place (three overstatements) and the tree restored to the shipped base.

**What I did:**
- **Reproduced**: applied `work/patch.diff` myself; regen exit 0, digest bit-identical (`4fb49739…`). Timing numbers shift ~1.8× on the shared box (gather 2.94→5.26 ms p50, 6.9→12.3 µs/body — load 1.24–1.58 recorded in the logs); load-independent laws reproduce exactly (219 cands/capture = 51% of bodies; control 97 answers × 11 cands). Probe cross-validated against the bench's own `view_gather` stage timer (5.63 vs 5.26 ms, share 0.61).
- **Predictions**: mtimes confirm pre-registration; P1/P2 held, P3 half-held and honestly reported; kill criterion nowhere near.
- **Adversarial**: seed 7 (same laws); **outside the author's range** — the CLI clamp lifted exactly as the dossier names, crowd at ~2,330 bodies: 10.4–10.6 µs/body (linear law and the 10⁶ extrapolation stand), one capture = **98.5% of all bodies** (the "≈50%" is the 428-body ramp point of the 1.00·K law, not a constant), one settle-drained scan at 6.8 µs/cand — the answer law measured on the crowd itself for the first time.
- **Novelty**: no prior gather↔phase-word connection on the view page or in HISTORY; all citations (b77d-1fcf, efd4, 5f36, 224 B pin) verified against the wiki.

**Why silver, not gold**: the ≈300× deletion is projected, not built — the run's own caveats name the unmeasured crossing-vs-row decomposition. The one experiment: wire the phase-word tier into the emitter loop with 2df1's display-exactness audit. Not lead: everything reproduces, the domain extends, and the unification is a genuinely new direction on the board's #1 bottleneck.
