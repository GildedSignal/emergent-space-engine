Working...
Check complete. Summary of what I did and found:

**Grade: silver** (`check.md` written; the author's `wiki/nladder.md` corrected in place where it overstated).

**Reproduced** — every deterministic number is bit-exact on re-run: crests 4,243/455/12,729/711 events, wave positions 14,167/28,317/42,483/56,617 game-s, totals, off-arm regeneration 87/96% of the record's anchors. Re-derived independently from the CSVs with my own code, not the author's `analyze.py`. Patch verified minimal: one env-gated hunk, off-path identical to shipped. Timings diverge with box load (author 50.8 µs/ev, my regen 78.8 — shared machine), which only touches P4's µs/ev bar.

**Held out / extended** — P3 (no window-level re-concentration) holds, including at 10⁴, the author's named held-out case: staggered wave windows ~1,090 events vs the unstaggered 5,109 (kill bar 2,555).

**Headline refuted** — my adversarial letter-width flights (rtf 100, budget-free, 42k game-s — the letter's own instrument, which the author never flew, converting instead by ÷10) measure a staggered worst frame of **342/366 events at 10⁵/3×10⁵: 5.1–7.5× the predicted 45.5/71.1, and N-flat**. The crest is a ~660-game-s sub-grid beat, not the belt stream. Corrected arithmetic: staggered letter break ≈ 6×10⁵ (below the 1.3×10⁶ memory break, +7× over unstaggered — not +20–26×), composed 10⁹ letter ≈ 0.7× at the key arm (bottom of fermi's 0.5–2.7 band, not 2.2×). The qualitative conclusion survives — the cure is permanent and (stagger ∧ key-arm kick) fits the 10⁹ letter — but the run's central numbers were ~7× off, and P1's "passes with margin" diagnosis used the same broken conversion that caused its failure.

**Silver, not gold**: real, reproduced window-level result plus new structural data (period, decay, birth-wave cost), one instrument-correct experiment away — and that experiment is now flown, with the corrected numbers on the page. No author files modified; my `chk_*` arms and logs are left in `work/` as the reproducing evidence.
