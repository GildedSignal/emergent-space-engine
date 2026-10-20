Working...
**Grade: silver** — `check.md` written; the author's page corrected in place (three lines) and still passing its own regen at 14/14 within budgets.

**Reproduced (independently, not just via the author's script):**
- The false positive is real and in shipped code: `lab/wiki.py:86` flags on the substring `<<<<<<<`, and `lab/wiki/wiki-memory.md` has zero line-start markers but quotes the syntax once in prose — stuck since 10-17 00:05 (~4 days) while `q-resolve-wiki-memory 60` sat first in `lab/queue.txt`; this run executes that directed job.
- regen.sh 14/14; page 88→39 lines, current best 23→5, both index flags clear with exactly one row changing; de18 silver / 87d0 gold from branch subjects; 35-assertion coverage fair against both proposals (read in full); predictions.md (22:04) predates the decisive instrument (22:08); all five predictions held, P1's count exact (6 Runs lines). The author's `fake_git` is faithful — worktree page == `HEAD:` page and the raw `merge-file` is clean; the duplication is the exact-text union.

**Why not gold:**
1. **Novelty gap:** 87d0's checker had already measured this exact false flag (its check.md, adversarial A4: "false-flags an inline `<<<<<<<` mention (the real wiki-memory row)") and its patch anchors the flag at line start. Uncited by the author; I added the credit to the page.
2. **Adoption alternative measured wrong (my adversarial case, outside the author's range):** I recovered 87d0's actual patch from its branch and published this page through the truly patched `apply()` — clean, 0 markers, flags clear, but still **6 Runs lines (de18×3, 87d0×2)**. The skip doesn't dedupe other runs' stale variants; only a hand-fold or the unimplemented id-keyed union lands one-line-per-run. Also: the +92/−9 patch **no longer applies at HEAD** (index hunk vs the 20 Oct budgets commit) — one hunk to hand-merge.
3. **Dossier letter-error:** "byte-identical to 87d0's proposal" is false in the Runs section (the body is identical; the Runs diff is itself the union artifact) — a claim outside regen.sh's net.

**My census extends the finding:** the Runs-union artifact is near-universal — 30 of 41 pages carry duplicated run ids (encounters 52 ids worst ×4, nladder worst ×7), far beyond the author's encounters-only P4; wiki-memory is the only substring-vs-linestart misflag today.

**The one experiment to gold:** land it — re-merge the patch at HEAD, key the union on run id, publish through the real publisher, measure one-line-per-run + 0 markers + flags clear + idempotent.
