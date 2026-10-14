Working...
Check complete. `Grade: silver` written to `lab/results/20261014-1221-system-b8fc/check.md`, and the author's wiki page corrected in place with a checker bracket. The tree is back to pristine (only `lab/results/` touched).

**Verdict: silver — real census, correct physics conclusion, two record defects.**

**Reproduced** (patch applied to clean tree, two independent builds): every raw counter and digest bit-for-bit — 4,348/15,553 compiles, 76.9/92.3 knots/table, 224,233/825,221 readouts, 2.85 quads + 1.88 rate evals per readout, digest `b1feb4bf…` identical under unlimited and 3 ms budgets. I also verified "no bits moved" independently: the pristine tree prints the same three digests.

**Cost model adjudicated**: `quad()` evaluates 4 integrand points on every branch (code-verified), so the dossier's 31/69 read-dominant split recomputes correctly by hand — and under node()-class evals the read side dominates even harder (75/25).

**Attacks** (each outside the author's range): unique per-compile ids show honest cells-read/table is 6.2–6.3 (address identity *overstates* it — the dossier's bias reasoning is backwards, though the write-mostly conclusion strengthens); seed 7 → 6.4/86.0, digest identical under budget; 32 game-s → 6.5/59.2; 5,000 members → 6.0/117.5, read share 59%.

**Why not gold**: (1) the shipped regen's own summary line prints `build 73–75%`, contradicting the dossier's headline — `R_QUADS`/`AR_QUADS` are declared and consumed by the summary but never bumped by the hooks, and `fix-final.md`'s claim that regen reproduces the splits is false as shipped; (2) "read dominates everywhere" is falsified by the author's own quiet rtf-1 arm (build 62/38). The one experiment to gold: land the incomplete-Carlson readout for one channel digest-identically and fix the summary line.
