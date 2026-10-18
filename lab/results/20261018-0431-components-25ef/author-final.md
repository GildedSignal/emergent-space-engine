Working...
Run complete. Deliverables in `lab/results/20261018-0431-components-25ef/`: `dossier.md`, `predictions.md` (written before the run), `regen.sh`, `work/patch.diff` (+52/−12 on `bind.rs`/`step.rs`/`observe.rs`, flag-gated), `wiki/a-word.md`.

**Claim:** the (a, ȧ) two-word acceleration store passes every frozen readout gate — worst readout/map ratio 1.11× against the 3× bar where the one-word read 356×, the no-jump gate the one-word failed at 3.85–5.07e-2, step-squared fall 15.9–18.3× — and its write costs zero extra source evaluations (the kick's own field evaluation is the word, the previous kick's word is the derivative's other point), so `observe::partial`'s per-read field evaluation is deletable and the measured 1.45× gather deletion (549f/f2b7) is collectible.
