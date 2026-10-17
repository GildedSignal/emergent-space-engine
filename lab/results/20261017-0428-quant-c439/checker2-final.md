Working...
Check complete. **Grade: gold** — written to `lab/results/20261017-0428-quant-c439/check2.md`.

**Reproduction** (from `work/patch.diff` at `df0386db`, my own builds and runs):
- Every deterministic count bit-identical: scan candidates **148,996** at both N, player 2,127, state_of 14,164, coast 33,875/184/10,828/20,048 exact; digests `d1822b88`/`c53c2de6`/`23b2e497` reproduce; plain=prof digest identity (P6) holds. Totals drift only in the stated root_state_raw jitter band (~±60).

**Adversarial arms** (all outside the author's range):
- **N=1e6**: 70.2 reads/scan — O(1) holds a third decade, and total events are O(1) too (16,212/16,215/16,215 across 1e4/1e5/1e6), which kills 8792's per-body extrapolation even harder than the dossier argues.
- **Seeds 2/3**: 88.4 (burn) / 144.1 (coast coast) reads/scan — near set realisation-dependent but bounded, as the author caveated.
- **Wave at 1e5**: 4.70 reads/event, 68.1 reads/scan; wave events grow only ~2.4×/decade (sub-linear).

**Premise killed**: the promotion page's standing "burn-10⁹ memory = the read stream's question, ~6 cores of hit-path ε" (8792) — no N-linear observer read stream exists on shipped main; what grows rides the kicks.

**Corrections to the author's wiki page** (in place): the event-riding projection is now bounded ~4×10³/s–10⁷/s (≤ ~1 core) — the dossier's 1.7×10⁻⁵ kicks/body/gs constant is unexplained and mismatches its own arms, though every extrapolation still lands at ≤ a few cores; near-set range extended with my seeds and N=1e6.

Predictions: mtime order can't prove pre-registration (single write), but the pre-registered *decisive* P2 failed against the author's own expectation with its kill criterion honoured — the signature of genuine pre-registration. Scratch example removed; the tree carries only the author's patch (restored by the runner's flow).
