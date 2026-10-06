Working...
Check complete. `check2.md` written; tree restored to HEAD (only `lab/results/` remains, untouched otherwise).

**Grade: silver.**

**Reproduction** (clean tree `f639094`; note this box forces `CARGO_TARGET_DIR=/home/glmlab/lab-target-3`, so the dossier's `./target/release/xtask` path needs adjusting):
- Baseline seed 1: digests `2fd6e1ce…`/`c5d2cd0c…`, samples 23/9/32, memo 26 rebinds 0.0/0.0 — all match; medians drift on the shared box (55.9 vs 43.4 µs).
- Patched build: seed 1 and seed 7 digests match the author's staged JSONs exactly; every stage share within noise (made compile 12.9% vs 12.9%, fit 10.7% vs 11.1%, forces/readout 23.9%/8.9% identical); tallies exact (knots 7.6/18.2, tail 2.2/27).
- Digest invariance proven by my own baseline-vs-staged runs.

**Adversarial:** seed 3 (fit+compile 25%, readout family 61%, ratio 2.47×) and 55 s (23%/60%/2.59×, stage sum closes within 5%) both hold the structure. `step.rs:304` confirms the double `orbit_state` proper-time readout the subtraction attributes. Two misses found: the leaver compile share dilutes to 50% at 55 s (mix-dependent), and the quantized memo starts hitting at 16% there — "memo 0%" is 20 s-window-specific, exact stays 0.0.

**Why not gold:** nothing is deleted yet — the ~2× readout-side lever is a projection from attribution, and the M1's 29/15 µs claim (the premise named wrong) was never re-measured. The gold-maker: implement the dossier's own cheapest deletion (cache the per-tube phase inversion so `rebind` stops solving the old tube twice) and show the measured median drop at identical digests.
