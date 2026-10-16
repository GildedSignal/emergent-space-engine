Working...
Check complete — `Grade: gold`, written to `lab/results/20261016-1207-taleb-f094/check.md`.

**What I did:**
- **Reproduction**: applied `work/patch.diff` myself (verified print-only — one example file, no engine line; prof timers are shipped). All headline numbers match clean-tree: 43/43 leavers at f62 (11.6 ms, lag 1.448 game-s) at N = 0/1e4/1e5; 357/357 at fleet 400; b5 arm 6.2 ms worst, 82 drain frames; prof split 69.9% bind + 27.5% replan, 672 µs/leaver.
- **Predictions**: pre-registered, 4/5 held (N-flatness exactly), one magnitude miss honestly reported — evidence of genuine pre-registration, not a fitted retelling.
- **Adversarial (4, one beyond domain)**: belt N = 5e5 (half-decade past the author's max, 1.15 GB) — identical 43/f62/1.448; frames 0–1500 — only a 5-member trickle after f400 (bounded; page corrected in place); seed 99 — 345/345; rtf 1000 — lag 15.256 under the 16.667 one-frame cap, which I confirmed is structural in `frame_to` (`target` follows presented time).
- **Novelty**: no HISTORY entry; ed3a only *observed* the exodus, 3cfc only measured the 1,600-member break — the attribution is new and composes (0.86 s inside 3cfc's 0.6–1.5 s).
- **Page**: faithful fold-in; two corrections added (the f1500 trickle sharpens "0 leavers after f100" and the second-wave residue).
- **One instrument finding**: regen.sh's grid runs on the prof build — every µs carries ~12% timer overhead (610 plain vs 690 prof); conservative direction, counts unaffected.

Tree restored clean; nothing outside `check.md` and the two page corrections touched.
