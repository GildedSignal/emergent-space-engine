Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place (add-only annotation) and the tree restored to pristine main.

**What I did:**

1. **Diagnosed the runner's regen failure (exit 101).** `work/patch.diff` is doubled — every file's diff appears twice — so `git apply` fails atomically; regen.sh's idempotence guard misreads "does not apply" as "already applied", skips, and the build dies on the missing `pass_bench` bin. One de-duplicated copy applies cleanly.

2. **Reproduced bit-exactly.** All 18 A/B flights re-flown on the clean, patched tree: digests byte-identical between arms at all 8 configs **and equal to the author's recorded rows**. My own pristine build reproduces the author's pristine digests (`3c02e035…`, `6338ec25…`), equal to my OFF arm — the pristine≡OFF≡ON triangle holds independently. Cuts: 6.4–7.8 µs/B median 6.74 (author 6.05–7.43); rails 43–46→36–39. Suite with the patch: 77/0.

3. **Attacked beyond the domain, three ways, all confirming:** held-out seeds 11 and 3 (digest-equal, cuts 5.5–7.6); N=6×10⁵, 2× the author's max (digest-equal, cut 8.3 µs/B = 24%, RSS 1.37 GB — no cache cliff); and the dossier's own admitted gap — **post-flight identity**, via main's own `ladder_digest`: all 13 scripted flights (burns, key mashing, first-kick wave, belt crossings) digest-identical across arms at canonical cuts.

4. **Verified the purity argument in code:** `readout` reads only binding fields; between the three `plan_clock` reads only `rec.ext` is written, so the shared value is provably each OFF read's value.

**Why silver, not gold:** everything held, inside and outside the flown domain — but the letter wants 10×, a deleted component, or a killed premise, and this is a ~1.2× rail cut. The named gold step: compose one-read ∧ d31c's shared planets ∧ the Hill block into the default birth path against the 404b rail. **What the author missed:** the doubled patch (their fix pass ran on an already-patched tree and never caught it), and that the post-flight certificate was one already-shipped `ladder_digest` invocation away.
