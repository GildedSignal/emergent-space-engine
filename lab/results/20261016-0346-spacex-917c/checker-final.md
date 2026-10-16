Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-0346-spacex-917c/check.md`, with three overstatements corrected in place on the author's proposed `wiki/nladder.md` page.

**What I did:**
- **Reproduced** from a clean tree: applied `work/patch.diff`, rebuilt, verified every deterministic number from the runner's regen and my own runs — anchors bit-exact (487/1,328), attributable peaks 153/994/11/35, windows, the ×20.4 belt_first spread, and off-arm digest identity (both unset and explicit `=0`).
- **Four adversarial cases**, one beyond the author's domain:
  - **N=4×10⁵ staggered** (1.33× his largest; 1,835 MB, under the cap): attributable peak 48 vs linear prediction 47, pre-wave floor exactly 334, steady-stream rate 33.3 vs 33.2 ev/game-s predicted, wave completes, peak frame is the same locals' storm frame — every scaling claim extends.
  - **Direct attribution** (the check the dossier invited): at D's top frames the 10⁵ arm carries 338–345 events, the N=0 arm ~30 → the 369-event peak is ~90% ladder locals; belt adds ≤29. Locals-dominated, confirmed.
  - **Window-straddle attack**: rolling 250-s windows give 18.2×/23.9× flattening (fixed bins undercount the concentrated unstaggered wave most) — conclusion robust, slightly stronger.
  - **Armed legality probe**: ES_STAGGER=1 on `ladder_digest` is bit-identical to pristine, 13/13 — stronger than the dossier's own "digests change as any birth-draw change does".
- **Why silver, not gold**: P1 and P3 failed as written (disclosed in Evidence), but the dossier's Predictions recap reports P3 as "held … inside [1/12,1/4]" when 1/28 is outside it — the exact "reported as held" pattern that cost the 1 October red-team gold — and P2 is spun as "band's upper room" for 369 against a [90,350] band. Also corrected on the page: "334–452" storms (452 was a wave-contaminated post-wave frame) and the parity/letter-break conflation (3×10⁶ is belt/locals parity; the total frame's 12-ms M1 letter extrapolates to ≈6×10⁵, locals-driven, before the memory break — the "no wave-driven break" conclusion survives).
- **Gold experiment named**: fly the B13/B14-class behaviour gates armed; with the armed-digest identity that's the only step left to adopting ES_STAGGER as the birth default. Tree restored pristine; no commits made.
