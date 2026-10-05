Working...
Check complete. `check.md` written to `lab/results/20261005-0543-library-bb03/` — grade: **lead**.

**What held:**
- Full reproduction: `kickprobe.py` rerun gives **0 diffs** against the author's `results.json` (all truths, all schedule rows, both tail stats — deterministic, same container).
- Predictions predate the decisive sweep (mtimes 05:50:23 → 05:52:13 → 05:54:35); failures P2/P4 reported honestly; `patch.diff` empty, tree clean.

**What broke it:**
1. **The headline ranking is an artifact of the probe's first-order left-endpoint kick convention.** Under the engine's own symmetric split (law.md l.30, Wisdom–Holman), the re-anchored phase step *beats* uniform time where the engine lives: e=0.6 at 16 kicks/orbit dpre −2.0×10⁻² vs −1.8×10⁻¹ (9×); at e=0.8 uniform time **escapes** (e>1, solver dies) at n=8–32 while the phase step runs (−1.8×10⁻³ at n=32). The dossier's "unstable at e=0.6 / run died" verdict on the engine's live scheme is the convention, not the cadence — the author's own pre-registered P2 clause ("testbed suspect") fired and wasn't honored, and the "convention-robust" dismissal is provably unsound (left-endpoint bias cancels on uniform grids only).
2. **The S1′ evidence is not regenerable**: `results.json`'s `S1r_reanchored` block (the dossier's quoted numbers) is produced by no shipped code; my reimplementation lands within 5% (+1.19×10⁻² vs their +1.24×10⁻²), so the numbers are real but unshipped.
3. **What survives is already known**: S2a/S2b dead and concentration harmful restate the r4 v2 kill of arc-integrated kicks and H0190's averaging; "the lever is error-per-kick and correctors" is the board's standing focus list verbatim.

Net for the integrator: do *not* adopt "uniform-time over phase-step" from this run — under the engine's convention the existing phase-step cadence is the robust one at high e and coarse budgets; the schedule question needs a rerun with a symmetric (ultimately integer) kick convention before any conclusion.
