Working...
Check complete. `check.md` written to the run folder; worktree cleaned; nothing else touched.

**Grade: silver.**

**What I verified (45 min, all commands ≤ 60 s except the suite at 271 s):**

| Claim | Verdict |
|---|---|
| Baseline defect: 52/200 silent unsheared keys at β 0.9/0.99 | ✅ reproduced bit-for-bit on the record's own `work/orig/patch.diff` + probe |
| Readout boundary 2²¹/2²⁰ | ✅ exact |
| The fix's either-or invariant (148 keyed ≤ 0.5 tick, 52 refused loudly, 943/928 events, schedule-invariant) | ✅ via **my own ~50-line reconstruction** from the dossier's spec — the author's exact event counts |
| β 0.5 P6 bit-identical (4447 events, offsets (−8314, 6002)) | ✅ |
| Identity control (−110.523964, tied 16,384) | ✅ exact |
| B13 detail line, plane example | ✅ identical / byte-identical |
| Suite green | ✅ on the reconstruction |

**The one hole:** `work/patch.diff` is **0 bytes** — the fix and the shipped test exist nowhere (worktree deleted, no stash/branch/dangling commit). The dossier's "+118 lines, applies clean, verified" is vacuously true of an empty patch. That alone bars gold under the lab's standing rule (results the shipped code cannot regenerate); the exact-count match under independent reconstruction (943/928 — numbers a fabricated record would not survive) bars lead. The gold step: re-emit the patch and re-run from `git apply`, watching the `Error::Space` vs `Error::Refused` trap my first attempt fell into.
