All three oEverything is in place and verified. Final state of the run folder:

- `predictions.md` — written before the decisive runs; all held (535/419/116/0, exactly 7 stale tokens, byte-identical controls)
- `check_gold.py` — honest paragraph-sweep verifier + grade audit: **PASS** (535 tokens: 419 in-page, 116 behind a cited run, 0 LOST; 0 tokens understating a branch grade)
- `apply_demo.py` — adoption through the real `lab/wiki.py`: **PASS** (A: HEAD's own apply reproduces main's 135-line/28-dup landing byte-for-byte — the negative control; B/C: patched apply lands 107 lines, 57 runs, 0 dupes, byte-identical, clean index row)
- `wiki/kick-jet.md` — the corrected page (107 lines; 7 grade tokens refreshed from branches + provenance)
- `work/patch.diff` — the `fold_runs` id-aware Runs union in `lab/wiki.py` (16+/2−, no engine edits); tree otherwise pristine, nothing committed
- `regen.sh` — regenerates every number in ~1 s, tested from a pristine tree with the patch guard
- `dossier.md` + `author-final.md` — complete

**The claim:** the checker's three named gold-gaps on the kick-jet compile are all closed on the shipped record — the number sweep is honest with paragraphs as units (535 tokens: 419 in-page, 116 behind a cited run, 0 lost), the 7 stale grade tokens are refreshed from the run branches (0 understating), and adoption is real through `lab/wiki.py` itself: HEAD's `apply()` reproduces byte-for-byte the 135-line/28-duplicate landing now on main, while the patched id-aware `fold_runs` union lands the compile's actual 107-line, 57-run, 0-duplicate page — both forward on main's current page with this run's corrected proposal and for every future publish.
