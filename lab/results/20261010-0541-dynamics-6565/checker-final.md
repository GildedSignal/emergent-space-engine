Working...
Check complete. `lab/results/20261010-0541-dynamics-6565/check.md` written: **Grade: silver**.

**Reproduced bit-for-bit:** all rerun summaries identical (t002_s21, t20n_s21, t01_s21, t01_hot_s21), `e_elastic.events.bin` byte-identical, `post_table.txt` regenerates from shipped code. Physics verified correct (exact WT epicyclic solution, restitution impulse, element reconstruction).

**Two headline defects found by attack:**

1. **Branching is an estimator artifact.** `post.py`'s `base` assumes full 30-tu post-event windows; steady windows are 20.9–91.2 tu, so windows truncate at `t_end`. The author's own code, fed my synthetic inhomogeneous Poisson, returns branch = −268 (ratio 0.347 = exactly the mean truncated-window fraction); a genuine Hawkes cascade returns −553. Corrected (per-event windows + time-and-degree-preserving permutation null), all 8 runs sit at 1.01–1.11 × baseline: no quenching, no ignition — the claimed "restitution cools participants, 16–69% below baseline" is arithmetic, not physics.

2. **The "τ=2" rows are τ=0.25** (the binary's own summary prints `tau 0.251462`). The actual τ=2 runs hit the 400k cap at T=18.3 and were dropped unnamed — violating the author's own pre-registered kill rule. Pre-registered P2 was never tested as registered; highest steady τ measured is 0.5.

**What survives:** no *large-burst* avalanche at τ ≤ 0.5 (7/8 Fano inside/below drifting null; corrected branching ≈ 0), drift-as-the-tail, the P4 attractor, and the elastic runaway — bit-for-bit reproduced, the engine-relevant "gate we lack". But my Hawkes cascade also *passes* their drift-null test, so "no cascade" is proven only against large bursts, not near-critical short-lag branching. Gold path: true steady τ=2 with the corrected estimator and archived Poisson+Hawkes canary pair.
