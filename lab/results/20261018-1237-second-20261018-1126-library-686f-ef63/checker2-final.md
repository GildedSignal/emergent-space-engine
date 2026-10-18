Working...
Check complete — `check2.md` written. **Grade: gold.**

**What I verified:**

- **Reproduction:** `./regen.sh` exit 0 twice, bit-identical to each other, the author's captured log, and the runner's output. patch.diff empty, tree at base. Every corrected number recomputed by hand from raw constants (0.548/0.097 s/s at 10⁹, T\*-law fits ≤0.05%, identity 212.6≈213, 10⁸ wave 1.8–3.1×, crossover [3.2–5.5]×10⁷, walls 15.75/28.43 GB) — all match.
- **Predictions:** mtimes prove `predictions.md` (12:42:05) preceded the corrected script (12:43:02) and the run (12:47); all six held, including the checker's named pair and P5 cell-identity (verified programmatically against the original run's branch — the original's line 70 does divide by rtf with full N and a stale T\*).
- **Provenance:** ladder.txt:143, e29c's bars.py (`REKICK_COST = 0.6` is a cost ratio — the retraction is right), e29c's dossier bars/k\*/0.28% identity, and all inherited constants trace verbatim.
- **Attack:** N=10¹⁰ (outside the range) extends coherently; the "third term" claim is rtf-invariant (re-kick = 0.90× spared stream at any rtf); the fence/horizon behavior is consistent with e29c's "never fires ≤10⁶".
- **Page:** every new line on the proposed wiki page matches the evidence; no corrections needed.

**Blemishes named (none load-bearing, none on the page):** the "9.8×10⁻⁵ on shipped rows" misquote of the original's actual 9.8×10⁻⁹…10⁻⁶; "most pessimistic 0.2%" at 10⁷ where the flat-bar reading is 0.76%; the 46% band edge; and the T\*-law being effectively anchored with one independent bar (10⁶, −0.05%).

Gold rationale: the premise "<10⁻⁴ s/s at every N" is dead by 3–4 orders on every reading, the "wrong by 4 orders" dismissal of gold-record e29c's 0.28% identity is retracted, the skipped 10⁸ decade re-fails the wave, and the record now regenerates — the exact failure that kept the 5 October silvers from gold. Adoption cost: none.
