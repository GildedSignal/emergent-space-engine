Working...
**Grade: gold** — written to `check2.md` (first line exact, abstract ≤120 words, reasons, what the author missed).

**What I verified independently, not by trusting the runner:**

- **Provenance:** `work/patch.diff` is byte-identical to 23a6's committed patch; all 15 predecessor artifacts md5-match their own git branches.
- **Reproduction:** applied the patch myself, rebuilt, re-flew F1 — digest `8eecf1fa…` byte-identical, 41 belt-wide answers, RSS 1.39 GB; `analyze.py` regenerates regen.log exactly.
- **Every B-number recomputed with my own parser:** gaps 165.27/330.54 gs, δ_eff 0.053–0.399 (40/40 <0.5, 28/40 in a2c0's band), c_check mean 27.43 ns, 7.5× growth at fixed cadence, mixture closure 97.55% exact.
- **D-series:** ALL counts exact on all legs; c2's real duration 56,035 gs kills the N^0.74 reading on the artifacts' own lines; ledger arithmetic exact (830–1,030× budget).
- **Adversarial flights (mine):** seed 2 reproduces the drift and letter (6.5× growth); a 45k-gs cut — outside the author's window — hits a tests≈0 stretch then a re-approach with δ_eff → 2.215, killing constant-δ kick-Poisson outright while confirming the slack mechanism; coast gives no belt answers; ES_BOUND_VERIFY at 1e5 shows zero false skips with the digest unchanged.

**Named blemishes in check2.md:** predictions.md's surviving mtime (20:24:43) contradicts the dossier's claimed 20:15:55 (coincident with the harness `base` write — unverifiable); the δ<0.5 letter and 0.40 max-ratio are window facts, not scene facts; the 6–7% answers share is window-optimistic in re-approach phases. The wiki page needed no further correction — checker 1's in-place scoping and the 1,648–3,998 s fix both check out against my own flights. Tree restored clean; nothing committed or pushed.
