Working...
**Grade: silver** — written to `lab/results/20261021-0106-q-compile-kick-jet-53a2/check.md`, with one in-place correction to the author's page.

**What reproduced:** every dossier number (regen.sh, 0.1 s: 444/248 → 107/9, 81→57 runs, PASS); the counting rule is a verbatim match of `lab/wiki.py`; the shipped `wiki.py index` on the compiled page reads no over-budget flag; predictions preceded the decisive run; tree clean, patch empty, `lab/wiki/` untouched.

**Three adversarial findings that cost it gold:**
1. **The verifier's sweep never touched old Current best.** `bullets()` only collects `- ` lines; the old Current best is eight `**` prose paragraphs → 0 bullets collected, so the "exhaustive sweep of both sections" (109 tokens) covered Refuted alone. My corrected sweep: 535 tokens — 419 in-page, 116 behind cited runs, **0 lost**. The conclusion survives; the evidence line is false, and the author's own "97% vs predicted 55–70%, miss in the safe direction" was the bug's fingerprint, uninvestigated.
2. **`wiki.py apply` undoes the run-line dedup.** Replicated its inner loop exactly: the Runs union is literal, not id-aware → the page lands at 135 lines with 28 duplicated ids. Unlike nladder (which landed over budget at 322), the flag still disappears here, so the goal holds — but "adoption cost: one `wiki.py apply`" is stated without this caveat, repeating the exact omission that held nladder at silver.
3. **P5 misreported:** "every prose short-id carried" — b30b was absent (restored in place; verifier still PASS). Plus 7 grade tokens understate branch truth (all inherited, none worsened).

Faithfulness at claim level rests on my manual audit (the instrument passes a deleted bullet and a corrupted number unchanged — probed), and that audit found the compiled page genuinely faithful: all eight paragraphs → nine bullets with checker corrections intact, all kills preserved, dedup kept latest/fuller variants correctly. Gold path: fix the sweep unit, refresh the 7 grade tokens, make the Runs union id-aware (or record the landed 135-line state).
