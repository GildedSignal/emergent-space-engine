Working...
Check complete. `check.md` written with **Grade: silver**.

**What was verified (reproduction + 15 adversarial samples):**
- `regen.sh` exits 0 (72 needles, 0 failures) — before and after my one in-place correction.
- Independent grade extraction over all 28 `origin/claude/lab-*` branches matches every `## Runs` line — including two stale assignment labels (`a4ed`, `54d9` are gold on branch; the author rightly followed the branches over the assignment). `cee8`'s branch holds the literal 429 error in its checker-final; "(missing)" is exact.
- 15 runs deep-sampled in context: every figure faithful and in the right direction, including unneedled numbers and the checkers' own corrections (ad35's e₀=0.3 domain, 1db4's rate-bar-only caveat, 9abe→67be supersession, cd52→f2e3 split). Routing of the 3 runs to kick-jet/belt holds — no cadence-rule claims among them.
- Predictions predate the finalised page (mtime order); failures reported honestly.

**Why silver, not gold:**
1. **Completeness** — the brief told the compiler to `for-each-ref` for missing runs; the author skipped it. My 8-second sweep found ≥3 graded silvers with *primary* cadence claims absent: 83f9 (level-triggered killed), 524e (impulse-quantum trigger positively verified — 3.4× fewer kicks, **no error walk**), 5cbd (quiet interior k=16–32). 524e directly contradicts the page's unconditional headline "anything fed back from state walks" (54d9) and is unlisted — a live contradiction the compiler lens was empowered to referee.
2. **One overstatement, corrected in place**: the 51bf sentence ("graded lead only because 7d0d…", plus an unqualified deletion claim its own checker called "false where most bodies live"). Regen stays green after the fix.
3. Minor: dossier/author-final grade tally is 7/13/4; page and branches hold 7/14/3.

The one experiment for gold: run the sweep, fold the missing runs in, list 524e-vs-54d9 under Contradictions — git reads only, no simulation.
