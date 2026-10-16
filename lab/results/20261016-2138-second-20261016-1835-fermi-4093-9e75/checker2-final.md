Working...
Second check complete. **Grade: gold** — written to `check2.md`, with one page correction in the run's `wiki/kick-cadence.md`.

**Reproduction.** Applied `work/patch.diff` myself (example-only instrumentation, verified no law touched) and flew five arms of my own beyond the runner's regen: F2 law ratio 1.008 (spell 1,257 frames / 20.9 s / E = 298,496), deficit identity exact on my flight (70,200 − 28,342.5 = 41,857), integer anchors deterministic to 0.03% across four independent flights. The dossier's stated ranges sit ~5–8% narrower than the committed regen (spell 21.9–22.1 vs 20.9/23.5 s; Ĉ 50.5–52.7 vs 49.9/54.7 µs) — recorded as a blemish; the page's widened ranges cover everything.

**Adversarial arms (all outside the author's tested ranges).**
- **rtf 100, the player's own pace, 3×10⁵, two flights through the crest's full drain: no freeze at all** — deficit 1 game-s, max frame 11.99 of 12 ms, ~240 ev/frame riding the budget edge. The freeze is gated jointly by (N, rtf): onset between 100 and 450 at 3×10⁵; 4093's "at any rtf" holds at 10⁹ (density ∝ N), and the 10⁶/10⁹ arithmetic survives. This corrects the page's "at the player's rtf 100 the crest is the only freeze."
- **Burn at 5×10⁴** (author flew only 3×10⁵): inversion confirmed N-linear — spell/deficit N-independent (36 frames/0.6 s), worst 414 ms ≈ 2,581×50/300 carrying 8,462 events at 49 µs.
- **`--features prof` at 5×10⁴** fits the 2-GB cap and closes the dossier's admitted gap: the wave's wall is the ordinary kick mix (clock 43.3 µs/call, WH 39.6, boundaries 11.8) — no exotic item kind; the fix belongs to the per-item stop's structure.

**Why gold:** premise-wrong met twice (the burn risk inverted with the mechanism verified at `universe.rs` ~1006 and N-linear at two Ns; the saturated lag replaced by an exact-identity metric), a9d7's gold sentence gains its crest qualifier (verified at memory-h-live L314), the spell/deficit measurement is genuinely new (published page: 0 hits), P2/P3/P4 held at 1.01–1.02 everywhere, and adoption is page corrections only — the f2e3 pattern. Misses (P1 half, P5 35× off, reported as the finding) carry the internal evidence of genuine pre-registration; the author's own flights.log was overwritten by the runner's regen, so log-order proof was unavailable — noted in the verdict.

Tree left as found (patch reverted, zero tracked modifications); nothing committed or pushed.
