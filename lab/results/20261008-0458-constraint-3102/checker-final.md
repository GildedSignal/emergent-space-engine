Working...
Check complete. `lab/results/20261008-0458-constraint-3102/check.md` written; tree restored (patch reversed, working tree clean apart from untracked `lab/results/`).

**Grade: silver.**

What I did:
- **Reproduced** every dossier command in a clean tree, including applying `work/patch.diff` myself: the split config's digest is **bit-identical** (`aadaa1c8…`); gather share 67.7% vs author's 69.8%, bodies loop 97% of gather, reads/alive 1.065 (author 1.06), 12.3 µs/live body; all five `overflow_frames` counts (1/47/1/55/197) match the table. Absolute ms run ~4× faster here — the author ran under load 2.3–2.5; shares are the structural claim and they hold.
- **Predictions audit:** predictions.md (05:03) predates the decisive benches (05:10); P2's falsification is genuine — I verified the `--members` clamp to 400 in `xtask/src/universe/mod.rs:32`.
- **Three adversarial cases:** seed 7 (memo floor holds, 1.057), rtf 1 paced with 400 in-fleet members (members nearly free — but gather only 32% of the frame, json dominates: the "62–98% of every frame" headline overstates), unpaced default (0.514 ms ≈ author's 0.46).
- **Novelty:** H0210 already recorded "the view gather is 83% of a light frame" and H0213 already pulled the cache lever to 1.2 readouts/emitter — the dossier cites neither. The real increments (cache now at floor, bodies/members split, next constraint named) are sound but the headline premise was known.
- **Not gold:** nothing measured moved 10×, nothing deleted; the run is a diagnosis answering the queued `b-readout-cost` entry. One experiment to gold: implement one lever (selection or a cheaper shared readout) and show ≥10× fewer per-frame readouts with view behaviour intact and overflow_frames back to 0.
