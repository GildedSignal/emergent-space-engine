# Five lessons for the scan pin's fix (20261018-1617-library-be73)

Board #1, the ladder's #1 term: the held-scan pin ("answer-or-expire", acf2).
Composition (compose_fix.py, page-cited constants): at 10⁶ the answer half costs
0.34% of the frame budget — the trigger is the wall, not the cost. All quotes
byte-identical (verify_quotes.py, 5/5). Details: dossier.md.

1. **Latch full-queue action = refuse-or-drop, never force.** "Limited work in
   progress improves efficiency by preventing overwhelming overhead." — Cal
   Newport, Tim Ferriss Show #722. A WIP bound pays by preventing starts, not
   bulk finishing; one forced answer = 190 ns·K = 19–44 ms = 158–364% of the
   12-ms frame at 10⁵–2.3×10⁵ (369× cheaper in the compare form). Test: latch
   at a byte budget, 10⁴ coast under load — forced answers → 0, game_s kept.
2. **Expire on supersede.** "Saying yes consumes time. Saying no creates time."
   — Farnam Street, The Focus to Say No. 91% of mints are the player's clock
   re-asking; the held yes is already superseded. Bound: ~1.9–2.0 entries/mint
   → 426–448 MB at 10⁶ (18× under 8 GB), load-independent. Test: expire at
   mint; alive flattens at ~2× distinct, VmHWM flat (acf2's pinstat).
3. **The count cap is extinct, not retuned.** "Rules that made sense when they
   were written may well be obsolete. Make them extinct, too" — Abrashoff via
   Farnam Street. Written when answers looked expensive; at 0.5 ns the count
   under-binds memory (35.7 entries = 8 GB at 10⁶) and makes the spike. One
   byte counter at capture replaces it; the byte edge regenerates acf2's band
   (1.740×10⁴ / 3.397×10⁴) with no new constant. Test: done (compose_fix.py).
4. **The pin's multiplier is the doll, not the universe.** "...every single
   piece has a principle of motion of its own" — Adam Smith via Farnam Street,
   The Chessboard Fallacy. The coast scene is one doll (0.7 game-s at 10⁹);
   d7d1's doll-local bail already walks −94.2% at identical digests. Under
   partition: 2·(D+38)·224 B and 2.71% of one core at D = 10⁷ — affordable iff
   D ≲ 1.8×10⁷. Test: d7d1's in-band probe with the mint counter on.
5. **The freeze gate is the loaded crossover.** "Anyone looks like a genius
   when they're in a good position" — Farnam Street, Leverage Time. Position is
   utilization (b8e2: µ/λ = 1.0 quiet vs 0.03–0.15 loaded; 470f's bimodality).
   Gate: the unflown 10³–10⁴ crossover, seeds × replicates, load swept, heat
   included; bar = memory flat AND game_s kept under load; falsifier = head-
   flips (9% of mints) stacking distinct questions above 2 entries in battle.

Blind spot honored: every lesson names its decision and its cheapest falsifier.
