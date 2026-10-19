Working...
Check complete. **Grade: lead** — written to `lab/results/20261019-1656-scout-e0c8/check.md`, with the author's wiki page corrected in place.

**Verdict in brief:** the run reproduces bit-identically (`python3 absorb.py`, clean tree, every dossier number matches; pre-registration order verified by file times; shipped constants checked at source — belt.rs `P_BITS=25`/`T_BITS=44`, scenario.rs μ=1/999, the e>0.4 redraw), but the headline number is an instrument artifact:

- `rice_bits` caps its width search at `range(0, 24)`; the t_p departures have E|q| = 2³³·⁰ (optimal width 32). The cap alone produces 1,040.74 — the dossier's number, reproduced exactly. At the optimal width: **35.21 bits**; under the shipped codec's own cost model (`codec.rs choose`, no width cap): **34.10**.
- Corrected totals: **72.9–84.1 bits/body**, not 1,057–1,090 — i.e., the first kick costs the *driven-worst* 126-bit scale from the start, so "in-place absorbability is dead" does not stand; the element-space fold is a ~1.5–1.9× lever, not 22–28×.
- Adversarial μ sweep (10⁴×, outside the author's range): corrected t_p moves only 34.1→35.4 — magnitude-robust with the opposite sign. The author's own tell was visible: the 22×-weaker arm "lost" 21 bits where a magnitude code must lose ≈4.5.
- What survives and is recorded: departure magnitudes (δt_p p50 3.5×10⁹ quanta ≈ 5.9 h on a ~6 ms grid), exact controls, predictor irrelevance, the resonance census, and the corrected first-kick price — consistent with 0820's known 126-bit floor, which should have ruled out a 10³-bit departure on its face.

The page corrections withdraw the artifact-based Refuted entry (now recording the withdrawal itself), fix the NEW block, both open-direction annotations, the mid-page bracket, Contradictions, and the Runs line; the author's verified 9fd1-closure sync (e828/73b5) was kept.
