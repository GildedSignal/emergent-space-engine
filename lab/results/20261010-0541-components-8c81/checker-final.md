Working...
Check written: `Grade: silver`.

**Verification performed** (clean tree, `git apply work/patch.diff`, tree restored after):

- **Reproduced all dossier numbers**: 34.3–34.6 µs pure kick resolve with 3000/3000 rebinds; 51.9 µs/item over the *identical* 49,619 items; readout/secondaries/tide ≈ 3.4 µs each; signed 2.97 vs crossing 0.383 µs (8×); knots 6/16/42/86; Entry 176/Segment 184 B. One divergence: e=0.95 compile 63.5 µs vs the dossier's 128 µs (order preserved).
- **Code confirms the mechanism**: `kick` fires `dvq != [0,0]` against the velocity word, then `rebind` always retires a Segment and emits a new Entry; `apply` pays a `root_state_raw` after every event (measured 6.96 µs — same as the ramped 6.87 the dossier cites, so that attribution holds).
- **Adversarial cases**: all 23 ships rebind 400/400 (100% universal, 30–44 µs/kick); the first kick fires ~7×10⁹ velocity quanta (the claimed 10-order quantum gap, measured); `root_state_raw` vs `root_state` — no material difference.
- **Prediction timing holds** (predictions.md 05:50:36 < probes 05:54:04 < dossier 05:54:42), though P2/P5 were postdictions from already-measured numbers and P1's answer was on the public board.

**Why silver**: the decomposition reproduces and generalizes, but the two headline facts were known (H0210 "kicks cost 29 µs"; taste log "~99% recompile, Sonnet wires it"), the run wires nothing, and the 34× index rests on the floor's only unmeasured number — the asserted 0.1 µs force evaluation, when `secondaries`/`tide` are themselves readouts costing 6.8 µs measured. The named fixes deliver ~2.7×, not 34×. The gold experiment: extend phase-carry to the secondaries/tide reads and measure per-item against 50.4 µs.
