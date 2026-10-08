Working...
Check complete. **Grade: gold** — written to `lab/results/20261008-1947-second-20261008-1859-scout-141c-3186/check.md`.

**Reproduction (bit-exact):**
- Clean build; both `kickdump` dumps md5-identical to the stored CSVs; `news_engine.py` stdout byte-identical, JSON regenerates deterministically. Note: the dossier's commands run in place, so reproducing overwrites `news_engine.json` — done, and disclosed in check.md.
- The load-bearing premise verified in the engine: ships are never sources (`add_doll`/`make_source` only), `massive_only` is a literal-faithful copy of `scenario::plane_with`, and the full-plane massive streams match the massive-only run bit-for-bit — the dossier's quoted md5s (`347771aa…`, `d0a611c4…`, `cac0bd29…`) reappear exactly. `AU_T` equals the engine's `AU` constant. Player registers confirm the Q anchor (step 2²², quantum 2⁻⁷⁴).
- All headline numbers regenerate: 1.957, saturation 5.62→5.62×10⁻¹⁰, ratios 358/1.4×10⁴/3.9×10⁶, r_b 4.8/8.2/35/970 AU, cancellation 0.52–0.74, correlation ≤1.09×.

**My attacks** (2 placement seeds; a ×1000-dv burst tail on 0.1% of kicks — the author's admitted blind spot): all survive; the burst moves the accumulator by +1.4% only.

**Defects found, none load-bearing:** the 10⁶-AU extrapolation quotes Q·10³'s accumulator (4×10⁻⁶) where Q_engine's is 1.5×10⁻⁴/frame; "24,525 kicks" vs the header's 24,520; the declared Q·10⁻⁴ negative control never ran; the −0.973 exponent is largely constructed (s ≡ s_loc/d³; seeds give 0.87–0.97); the −0.301 crossover slope is an octave-grid artifact; the addendum's 20:25Z timestamp contradicts its 20:00:03Z mtime (which does precede all output).

Gold because: the silver's named experiment is done in substance on the engine's real stream, the record regenerates from shipped code, the frozen-prediction failure was pre-declared and diagnosed honestly, both engine-physics falsifiers were measured, and it corrects the record's law (log R → O(1) saturation) with a one-step adoptable design consequence.
