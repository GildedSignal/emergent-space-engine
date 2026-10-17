Grade: silver

**Abstract.** Second-author protocol re-run (≥ 3 seeds × ≥ 2 replicates) on shipped main + 01e7's finpol example, regen.sh exit 0. Reproduced here: single-call batch hits the shipped assert `alloc.rs:1451` in about half the draws (6/12 regen + 3/4 fresh; s11 8/8, s21 0/4 — seed-skewed), on- and off-grid alike, always at scene start 32→48; chunks 2/3 same-per-seed; frames 4/9; E = 2^rb on 52/52 survivors (≤ 2^160); min_region 32 (rb exactly 0) and window 32 hold even under batch (w32 now 14/14). Not reproduced: every late quiet-phase crash — 0/33 draws of the author's crashing arms in this window; the late phase stays single-window. Cost to adopt: none (measurement); driver/scene dodges retire, the engine-side publish/rollback fix stays the door.

## Reasons

**1. Reproduction (clean tree, patch applied, `regen.sh` exit 0, 63 draws).** Panic site, message, thread `alloc-N`, exit 101 verified against shipped `alloc.rs:1451` and the `.err` files. Numbers that differ from the dossier (all in the racy arms, none reversing a conclusion):

| arm | dossier (author window) | this checker's window |
|---|---|---|
| frames vmax 2 r600 | 3/9 | **4/9** (32→48 ×3, 80→96) |
| chunks 128 | 2/3, same values per seed | 2/3, same values per seed ✓ |
| batch 1792 on-grid | 3/6 | **4/6** |
| batch 1800 off-grid | 4/6 | **2/6** (+3/4 fresh s15 draws) |
| batch per seed | s11 4/4, s15 3/4, s21 0/4 | s11 4/4, s15 2/4 (then 3/4 fresh), s21 0/4 |
| vmax-16 late | 3/6 | **0/6** |
| vmax-8 late | 2/6 | **0/6** (+0/4 fresh) |
| crossing late | 1/4 | **0/4** (+0/4 fresh) |
| vmax-8 n480 late | 1/3 | **0/3** |
| n480 vmax 2 | 1/6 crash, rb 123–180 | **0/6**, rb 143–160 (inside band) |
| E = 2^rb | 37/37, ≤ 2^180 | **52/52**, ≤ 2^160 ✓ |
| batch survivors | 0.4 s, present/s 3900–6700 | 0.3–0.4 s, 4207–6737 ✓ |
| mr32 / w32 / wave / r300 | 0/3, 0/3, 0/5, 0/3 | same, rb bands match ✓ |

The stable structure regenerates; the incidence rows are window-flaky exactly as the dossier itself warns for the quiet classes — but the dossier presents the batch rows (3/6, 4/6) as settled, and they are not: pooled across all windows the single-call channel is 20/33, on-grid 7/12 vs off-grid 9/18 (author's own off-grid 4/6 vs my 2/6+3/4).

**2. Predictions.** `predictions.md` predates the run by file times (15 m old vs regen.sh 14 m, out/ 9 m, dossier 7 m in the delivered snapshot) and pre-registers thresholds with falsifiers. A2 held and **reproduced here**: panic values stable per seed (every batch crash 32→48), and the same-seed replicate split happened in my window too (s15@1800: r1–r3 crash, r4 survives). C1 held here (0/6 ≤ 2 crashes, rb 143–160). A1 partial (on-grid 3/6 author; off-grid 2/6 mine — each window fails one leg), A3 failed (s21 0/4), B1 failed (author 3/6; mine 0/12). All misses reported honestly in the dossier.

**3. Attack (26 fresh draws, 4 adversarial angles, 2 outside the author's range).**
- **vmax 32** (beyond the swept {2,8,16}): quiet 2/2 at the keeping-up rate (present/s 599, rb 0–1) — extends the dose-axis reading.
- **960 bodies** (arg 480, next N decade): **inconclusive — off the load band** (frontier stuck at 32, present/s 0.1, 2876/720 deadline misses). A stall, not a survivor; the page's own protocol note predicts this.
- **min_region 32 under single-call batch** (the strongest channel, s11/s15 which crash 8/8 pooled at m1): 0/2, rb exactly 0, completes 1792 in 0.2 s — the knob is channel-robust (11/11 pooled).
- **window 32 under single-call batch**: 0/2, rb 109–114, E = 2^114 exact — the coarser stride closes the batch channel too (14/14 pooled across windows and channels). The dossier's "no scene-design dodge exists; the engine-side fix is the only door" overstates against its own table: w32 is a policy dodge that has now survived everything, at a semantic price (publication stride) the page correctly keeps as "a lead, not a verdict".
- **Late-crash hunt** (vmax-16 s25–30, vmax-8 s17–20, crossing s15–18): **0/14**, rb 0–4. With regen's 19 draws of the same arms: **0/33 in this window against the author's 7 late crashes**. The late phase is consistent with a fat-tailed race but is single-window evidence; the page's "two crash phases exist" and the opening "every overlap class reaches it" rest on it.

**4. Novelty.** The pre-run page (01e7, silver) already held: frames and on-grid chunk crashes, single-call batch crashes (checker 4/4), min_region 32, window 32, rb-not-separator, E = 2^rb in the churn regime. New here: protocol-strength batch numbers with seed-skew and horizon-class irrelevance (a genuine strengthening of an established kill), the structural observation that crashing draws never print rb (verified: `row()` runs only after `run_frames` returns), the n480 rb band, and the late quiet-phase crashes — the only new mechanism-level content, and the part that does not reproduce outside its window. The "11/17 pooled" arithmetic checks (01e7 author 0/1 + checker 4/4 + bc0f 7/12). Not a repetition, but a consolidation; nothing moves 10×.

**5. Page.** Faithful folding overall; corrected in place: the one-window batch counts now carry this window (9/16; 20/33 pooled), the late-phase sentence now says no second window has reproduced it (0/33), open direction 4 carries 0/12, and window 32 gains the batch result (14/14). No three-gold closure: topic stays open.

**6. Goal fit.** Allocator-ratchet conflict, the board's smoothness limb. The certificate aborts rather than degrades — PRINCIPLES §13 "basically we don't want errors that can compound"; §25 "not making mistakes matters more than doing things efficiently… don't multiply by zero" — the zero now measured at protocol strength in the churn class. Measurement only; nothing to build; it selects 9b46's open direction 1.

## Why silver, not gold

Gold needs the held-out predictions to hold and the claim reproduced. The reproduced content (batch/channel/knob structure) was already standing on the page; the run's new claim — the late quiet-phase phase, "every overlap class reaches it", the first crossing crash — is single-window and stayed at 0/33 draws in an independent window, and A1/A3/B1 failed (reported, but failed). No 10× move, no deletion.

**The one experiment for gold:** make the late phase reproduce outside bc0f's window — either catch one late crash in a fresh window with per-draw load recorded (loadavg per draw; the author's own window hypothesis), or do the timing analysis the author's closing note names (predict when `fin_hi` crosses `s0` per reclash from publication cadence vs conflict discovery latency) and confirm a *predicted* crash. That converts "incidence is fat-tailed across windows" from a sampled story into a mechanism, and closes the last dodge.

## What the author missed

- "No scene-design dodge exists… the only door" contradicts the run's own window-32 row, now 14/14 with batch added; the honest split is scene dodge (dead) vs policy dodge (alive, priced, unproven).
- "(960 bodies)" on the n480 row is wrong: the arm is 480 bodies (2 × arg 240; the printed tag is `n240`; predictions.md says 480 correctly).
- Per-draw load unrecorded while the run's own discovery (window-fat-tailed incidence) makes load the leading confounder; two lines of loadavg per draw would have made the quiet-class rows interpretable.
- The n480 survivors ran at 433–488 present/s vs 598 at n240 — already near the load-band edge; the next N decade stalls (frontier 32), so "N grows, rb grows" has no on-band next rung at r600/6 s.
- `regen.sh` writes into the author's own `out/`, so the checker's regen destroyed the author's per-draw originals; write regen output to a separate directory if the window's raw record should survive checking.
