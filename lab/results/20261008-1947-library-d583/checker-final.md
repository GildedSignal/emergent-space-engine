Grade: silvCheck complete. `check.md` written to the run folder; nothing else there modified; no commits.

**Grade: silver.**

**What held up (verified, not just re-run):**
- **Bit-identical reproduction** of `probe_conjunctions.py` (53 s) and `lookahead.py` — both output JSONs byte-equal to stored; `patch.diff` empty; every dossier number matches.
- **Timeline clean**: `predictions.md` (19:51) precedes the probe (19:56) and results (19:57+); the pre-registered kill criterion (index error > 2) triggered at median 5.5.
- **Kill robust under attack**: independent 8-seed replication median 19; oracle-frequency fit on all 150 conjunctions still leaves 13–27% amplitude residual (excludes the aliasing confound I found — two author pairs have period ≥ train length); two-frequency, linear-chirp, recency-10/30 refits all fail ≫ 2; cold belt e≤0.05 fails; eccentric sampling and differential precession each break the certificate independently; truth is grid-converged (fuzz only at 4/684 near-tangential crossings).

**Why not gold:** the claimed deletion target was already built. `crates/encounters` (merged 1 Oct, `107137c`) implements the pay-once CF as an **exact integer circle rotation on tick offsets of frozen integer-period orbits** — 0 missed/0 false over 15 belts — a different, stronger representation than the fitted fixed-frequency conjunction-index model this probe kills. The board's r8 v2 *sentence* dies; the merged design doesn't. The dossier cites neither the crate nor r8 v3/v4. Also flagged: the pre-registered "if this fails, VOID" trigger on the positive control was reinterpreted as a discovery (I supplied the missing instrument control myself — synthetic fixed-frequency recovered exactly — so the reinterpretation stands), and the "two-frequency fallback pre-declared in predictions.md" is not in that file.

**Gold experiment named:** precess the crate's belts (g₁≠g₂, Rayleigh e) and measure whether `first_hit` mispredicts after payment — my mechanism-separation result (precession alone: index error median 18.5) predicts it bites.
