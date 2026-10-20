Working...
Check complete. **Grade: silver** — written to `lab/results/20261019-2339-fermi-f623/check.md`, with the author's wiki page corrected in place.

**What held (reproduced):**
- Applied `work/patch.diff` myself, rebuilt, reran; every per-kick constant recomputed independently from the raw logs matches the dossier (17.6/16.5/4.4 calls, 12.64/12.09 KB naive, family 8.71 calls/kick = 77% of ≤2 KiB bytes, 64% >2 KiB scratch, +53 MB live ratchet).
- `predictions.md` (23:43) predates all flight evidence (23:45+); failures honestly reported.
- Novel: the page had no allocator/bandwidth row; the 9edc-anatomy refutation ({88,240,304,352,384²,704,832} heap cuts, 192/208/288 absent) reproduces in **all five** arms.
- Drift recorded: kicks 96,108→94,541, bench 11.6→12.3 ns, 3e4 marginal 1.40→0.98 — immaterial.

**What broke under attack (3 arms; 10⁵ coast is outside the author's range):**
- **10⁵ coast**: naive constants in band, but OLS marginal reads **−1.08 KB/kick** and base churn is **53 KB/game-s** — the "N-flat flight base" (18→27→53) is wrong; page corrected.
- **Burn** (author's named miss): naive ×1.7 (21.5 KB/kick), 82% of bytes >2 KiB, ratchet ×6 — material; the closure survives only via the already-mandatory split8 (≈37% of 60 GB/s worst-case).
- **Seed 7**: marginal +5.34 — above the author's entire band. The marginal/base OLS spans −1.1…+5.3 and flips sign (already unstable in the author's own serial arms: 3.32/1.40 vs 3.32/0.98). Mechanism: the 12-ms frame budget cuts non-kick work when kicks spike — the regression is biased, not just noisy. So "23–48% marginal" is one draw, not a law.

**Why silver, not lead:** the decision claim ("no machine floor forces the mint deletion") survives every attribution reading, including naive burn, under the levers 3aec already made mandatory. **Not gold:** the headline row's precision exceeds the instrument. The one gold experiment: attribute bytes inside the fired kick item's own scope (unbudgeted control arms or direct mint-path instrumentation), not through budget-coupled windows.

Tree restored to clean (probe example removed; only `lab/results/` untracked, as found).
