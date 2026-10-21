Working...
Check complete. Verdict written to `check2.md`: **Grade: gold**.

**What I did**

- **Reproduced** from a pristine tree: applied `work/patch.diff` myself (`git apply` clean at HEAD 046d8d9c, `lab/wiki.py` untouched on main since 2b394f70), ran `regen.sh` — exit 0, 20/20 assertions + 12/12 verify checks in 1.4 s, identical numbers to the author's log. Independent census straight from `git show`: 29/40 diseased pages, 468 dups, promotion 32/14/18, nladder 143, encounters 89 — all match. P1's pristine-replay control plus glm-lab.yml:98 confirm the sandbox is the real publisher.
- **Predictions genuinely pre-registered** (02:21:16, sixteen minutes before the extension and replay). P6's two misses disclosed; kill criterion untriggered.
- **Four attacks**: synthetic 200-page scale with engineered edges (healed 0.15 s, idempotent; the same-token two-line collapse confirmed real but absent from the corpus); a fresh conflicting publish over marker-damaged Runs (path the author never ran — lands zero markers, fold correct); a textuality census (all 305 dup groups are grade-refresh rewordings; fold winners match the compiled proposals per id); post-heal publish on nladder (246→103→104 lines, 0 dups, no new flags).
- **Novelty**: e094's checker named this exact experiment for gold; this run also kills the premise that 6ccc's skip alone heals (P3) and corrects the standing wiki-memory page's false "landed end-to-end" claim.

**Two findings worth the integrator's eye at adoption** (in check2.md): kick-jet's non-byte-identity is not only order — 2/57 ids carry content-forked variants (7922: `(1−e)^(2/3)` vs `(1−e²)^(2/3)`), so `heal` and a same-window sweep can land different wordings; and `heal` inherits the shipped rewrite's drop of stray non-list lines inside a Runs section (unreachable on today's corpus — no page has both dups and stray lines).

**Page correction**: `wiki/wiki-memory.md` line 11 claimed 6ccc's fold "Landed end-to-end (this run)" — never landed on main; now says so (page stays in budget: 7 best lines, 42 total). Tree restored to pristine; scratch removed.
